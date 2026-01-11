from django import forms
from .models import VolunteerApplication

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = VolunteerApplication
        fields = ("motivation",)
        widgets = {
            "motivation": forms.Textarea(attrs={"rows": 4, "placeholder": "Почему вы хотите стать волонтёром?"}),
        }
