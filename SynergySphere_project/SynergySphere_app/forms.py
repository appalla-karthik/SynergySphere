from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"}),
            "priority": forms.RadioSelect(),
            "tags": forms.TextInput(attrs={"placeholder": "Comma separated tags"}),
        }
