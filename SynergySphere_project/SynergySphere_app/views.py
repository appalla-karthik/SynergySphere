from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from .models import Project, Task   # ✅ database models import


# ------------------- MAIN PAGES -------------------

def home(request):
    """Welcome page"""
    return render(request, "welcome.html")


def dashboard(request):
    """Project dashboard (all projects from DB)"""
    projects = Project.objects.all().order_by("-created_at")
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
 
 # ------------------- PROFILE PAGE -------------------

@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        bio = request.POST.get("bio")

        user.first_name = name
        user.email = email

        if hasattr(user, "profile"):
            user.profile.bio = bio
            user.profile.save()

        user.save()
        messages.success(request, "✅ Profile updated successfully!")
        return redirect("profile")

    return render(request, "profilepage.html", {"user": user})


@login_required
def settings_view(request):
    return render(request, "settings.html", {"user": request.user})


@login_required
def signout_view(request):
    logout(request)
    messages.success(request, "✅ Logged out successfully!")
    return redirect("home")

