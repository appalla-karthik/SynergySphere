from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'welcome.html')

def task_inside_view(request, project_id=None):
    # Abhi ke liye dummy data bhej rahe hain
    project = {
        "id": project_id,
        "name": "RD Sales",
        "tasks": [
            {"title": "Optimize Website Controllers", "due": "21/03/22", "tags": ["Feedback", "Priority"], "image": "images/sample1.png"},
            {"title": "Remove Sales App", "due": "21/03/22", "tags": ["Feedback", "Dev"], "image": "images/sample2.png"},
            {"title": "Stripe Integration", "due": "21/03/22", "tags": ["Bit Brains"], "image": "images/sample3.png"},
        ]
    }
    return render(request, "projects/taskinsideview.html", {"project": project})

def dashboard(request):
    return render(request, "dashboard.html")