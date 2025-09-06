from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from .models import Project, Task   # ✅ database models import
from django.http import JsonResponse

# ------------------- MAIN PAGES -------------------

def home(request):
    """Welcome page"""
    return render(request, "welcome.html")


@login_required
def dashboard(request):
    """Project dashboard → show only logged-in user’s projects"""
    projects = Project.objects.filter(manager=request.user).order_by("-created_at")
    return render(request, "project_view.html", {
        "projects": projects,
        "user": request.user
    })


def project_detail(request, pk):
    """Single project detail view"""
    project = get_object_or_404(Project, pk=pk)
    return render(request, "project_detail.html", {"project": project})


def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    # TODO: add a form for editing
    return render(request, "edit_project.html", {"project": project})


def add_people(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            project.members.add(user)
            return JsonResponse({"success": True, "username": user.username})
        except User.DoesNotExist:
            return JsonResponse({"success": False, "error": "User not found"}, status=404)
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

def search_users(request):
    query = request.GET.get("q", "")
    users = User.objects.filter(
        Q(username__icontains=query) | Q(email__icontains=query)
    ).values("username", "email")[:20]  # limit to 20 results

    return JsonResponse(list(users), safe=False)


def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect("dashboard")


def taskview(request):
    """My Tasks Page (all tasks)"""
    tasks = Task.objects.all().order_by("-created_at")
    return render(request, "mytaskview.html", {"tasks": tasks})


def task_inside_view(request, project_id=None):
    """Inside Project → Task list"""
    project = get_object_or_404(Project, pk=project_id)
    tasks = project.tasks.all().order_by("-created_at")
    return render(request, "taskinsideview.html", {
        "project": project,
        "tasks": tasks
    })


# ------------------- PROJECT CREATE -------------------

def new_project(request):
    """Render form to create new project"""
    return render(request, "projectcreate.html")


def save_project(request):
    """Create & save new project"""
    if request.method == "POST":
        name = request.POST.get("name")
        tags = ",".join(request.POST.getlist("tags"))  # store as CSV
        manager = request.POST.get("manager")
        deadline = request.POST.get("deadline")
        priority = request.POST.get("priority")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        if not name:
            messages.error(request, "❌ Project name is required!")
            return redirect("new_project")

        Project.objects.create(
            name=name,
            tags=tags,
            manager=manager,
            deadline=parse_date(deadline) if deadline else None,
            priority=priority,
            description=description,
            image=image,
        )

        messages.success(request, f"✅ Project '{name}' created successfully!")
        return redirect("dashboard")

    messages.error(request, "❌ Invalid request")
    return redirect("new_project")


# ------------------- TASK CREATE -------------------

def new_task(request, project_id=None):
    """Render task creation form for a project"""
    project = get_object_or_404(Project, pk=project_id)

    # Dummy users & tags (later connect with User model / DB)
    users = ["krutagya kaneria", "mihirpanara11", "rajveer", "alex"]
    tags = ["Bug", "Feature", "Testing", "Design"]

    return render(request, "newtask.html", {
        "project": project,
        "users": users,
        "tags": tags,
    })


def save_task(request, project_id=None):
    """Save new task in a project"""
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        name = request.POST.get("name")
        assignee = request.POST.get("assignee")
        tags = ",".join(request.POST.getlist("tags"))
        deadline = request.POST.get("deadline")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        if not name:
            messages.error(request, "❌ Task name is required!")
            return redirect("new_task", project_id=project_id)

        Task.objects.create(
            project=project,
            name=name,
            assignee=assignee,
            tags=tags,
            deadline=parse_date(deadline) if deadline else None,
            description=description,
            image=image,
        )

        messages.success(request, f"✅ Task '{name}' created in project '{project.name}'")
        return redirect("task_inside_view", project_id=project.id)

    messages.error(request, "❌ Invalid request")
    return redirect("task_inside_view", project_id=project.id)


# ------------------- USER PROFILE -------------------

@login_required
def profile_view(request):
    """Profile Page → Edit details + Reset password"""
    user = request.user

    if request.method == "POST":
        # ✅ Save Profile
        if "save_profile" in request.POST:
            name = request.POST.get("name")
            email = request.POST.get("email")
            bio = request.POST.get("bio", "")

            user.first_name = name
            user.email = email

            # Agar tumne Profile model banaya hai toh:
            if hasattr(user, "profile"):
                user.profile.bio = bio
                user.profile.save()

            user.save()
            messages.success(request, "✅ Profile updated successfully!")
            return redirect("profile")

        # ✅ Reset Password
        if "reset_password" in request.POST:
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")

            if new_password and confirm_password and new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # logout na ho
                messages.success(request, "🔑 Password changed successfully!")
                return redirect("profile")
            else:
                messages.error(request, "❌ Passwords do not match!")

    return render(request, "profile.html", {"user": user})

@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        if "save_profile" in request.POST:
            user.username = request.POST.get("username")
            user.email = request.POST.get("email")
            bio = request.POST.get("bio")

            # ✅ Profile bio update
            user.profile.bio = bio

            # ✅ Profile image update
            if "profile_pic" in request.FILES:
                user.profile.image = request.FILES["profile_pic"]

            user.save()
            user.profile.save()

            messages.success(request, "✅ Profile updated successfully!")
            return redirect("profile")

        if "reset_password" in request.POST:
            new_pass = request.POST.get("new_password")
            confirm_pass = request.POST.get("confirm_password")
            if new_pass and new_pass == confirm_pass:
                user.set_password(new_pass)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "🔑 Password changed successfully!")
                return redirect("profile")
            else:
                messages.error(request, "❌ Passwords do not match!")

    return render(request, "profile.html", {"user": user})


# app_name/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def split(value, delimiter=","):
    """Split string into list by delimiter."""
    if value:
        return [item.strip() for item in value.split(delimiter) if item.strip()]
    return []
