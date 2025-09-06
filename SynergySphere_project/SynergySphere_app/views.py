from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.dateparse import parse_date

# Temporary storage
PROJECTS = []
PROJECT_COUNTER = 1
TASK_COUNTER = 1


# Home / Welcome Page
def home(request):
    return render(request, "welcome.html")


# Project Dashboard Page (list of projects)
def dashboard(request):
    # 👇 yaha sahi template lagana tha
    return render(request, "project_view.html", {"projects": PROJECTS})


# Project Detail Page
def project_detail(request, pk):
    project = next((p for p in PROJECTS if p["id"] == pk), None)
    if not project:
        messages.error(request, "❌ Project not found")
        return redirect("dashboard")
    return render(request, "project_detail.html", {"project": project})


# My Tasks Page
def taskview(request):
     return render(request, "mytaskview.html", {"projects": PROJECTS})


# Inside Project -> Task List View
def task_inside_view(request, project_id=None):
    project = next((p for p in PROJECTS if p["id"] == project_id), None)
    if not project:
        messages.error(request, "❌ Project not found")
        return redirect("dashboard")
    return render(request, "taskinsideview.html", {"project": project})


# ------------------- PROJECT CREATE -------------------

def new_project(request):
    return render(request, "projectcreate.html")


def save_project(request):
    global PROJECT_COUNTER

    if request.method == "POST":
        name = request.POST.get("name")
        tags = request.POST.getlist("tags")
        manager = request.POST.get("manager")
        deadline = request.POST.get("deadline")
        priority = request.POST.get("priority")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        if not name:
            messages.error(request, "❌ Project name is required!")
            return redirect("new_project")

        deadline_date = parse_date(deadline) if deadline else None

        new_project = {
            "id": PROJECT_COUNTER,
            "name": name,
            "tags": tags,
            "manager": manager,
            "deadline": deadline_date,
            "priority": priority,
            "description": description,
            "image": image,
            "status": "active",
            "progress": 0,
            "team_size": 1,
            "tasks": []
        }
        PROJECTS.append(new_project)
        PROJECT_COUNTER += 1

        messages.success(request, f"✅ Project '{name}' created successfully!")
        return redirect("dashboard")

    messages.error(request, "❌ Invalid request")
    return redirect("new_project")


# ------------------- TASK CREATE -------------------

# ------------------- TASK CREATE -------------------

def new_task(request, project_id=None):
    project = next((p for p in PROJECTS if p["id"] == project_id), None)
    if not project:
        messages.error(request, "❌ Project not found")
        return redirect("task_view")  # ✅ redirect to mytaskview

    users = ["krutagya kaneria", "mihirpanara11", "rajveer", "alex"]
    tags = ["Bug", "Feature", "Testing", "Design"]

    return render(request, "newtask.html", {
        "project": project,
        "users": users,
        "tags": tags,
    })


def save_task(request, project_id=None):
    global TASK_COUNTER

    project = next((p for p in PROJECTS if p["id"] == project_id), None)
    if not project:
        messages.error(request, "❌ Project not found")
        return redirect("taskview")  # ✅ fixed

    if request.method == "POST":
        name = request.POST.get("name")
        assignee = request.POST.get("assignee")
        tags = request.POST.getlist("tags")
        deadline = request.POST.get("deadline")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        if not name:
            messages.error(request, "❌ Task name is required!")
            return redirect("new_task", project_id=project_id)

        deadline_date = parse_date(deadline) if deadline else None

        new_task = {
            "id": TASK_COUNTER,
            "name": name,
            "assignee": assignee,
            "tags": tags,
            "deadline": deadline_date,
            "description": description,
            "image": image,
            "status": "open",
        }
        project["tasks"].append(new_task)
        TASK_COUNTER += 1

        messages.success(request, f"✅ Task '{name}' created in project '{project['name']}'")
        return redirect("taskview")  # ✅ after saving, go to mytaskview

    messages.error(request, "❌ Invalid request")
    return redirect("taskview")  # ✅ fallback
