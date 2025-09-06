from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random

User = get_user_model()


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Password match check
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")

        # Strong password check
        try:
            validate_password(password1)
        except ValidationError as e:
            messages.error(request, f"Weak Password: {' '.join(e.messages)}")
            return redirect("signup")

        # Check existing user
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("signup")

        # Generate OTP
        otp = str(random.randint(100000, 999999))

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            otp=otp,
            is_verified=False
        )
        user.save()

        # Send OTP via email with HTML template
        subject = "Your SynergySphere OTP Verification"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [email]

        html_content = render_to_string("emails/otp_email.html", {
            "username": username,
            "otp": otp,
        })
        text_content = strip_tags(html_content)

        email_message = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        email_message.attach_alternative(html_content, "text/html")
        email_message.send()

        request.session["email_for_verification"] = email
        messages.success(request, "Signup successful! Check your email for OTP verification.")
        return redirect("verify_otp")

    return render(request, "auth/signup.html")


def verify_otp_view(request):
    if request.method == "POST":
        email = request.session.get("email_for_verification")
        otp_entered = request.POST.get("otp")

        try:
            user = User.objects.get(email=email)
            if user.otp == otp_entered:
                user.is_verified = True
                user.otp = None
                user.save()
                messages.success(request, "OTP verified successfully! You can now login.")
                return redirect("login")
            else:
                messages.error(request, "Invalid OTP. Please try again.")
                return redirect("verify_otp")
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect("signup")

    return render(request, "auth/verify_otp.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect("login")

        user = authenticate(request, username=user.email, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")  # Change this if you want another redirect
        else:
            messages.error(request, "Invalid email or password")
            return redirect("login")

    return render(request, "auth/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")
