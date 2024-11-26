from django import forms
from .models import Task
from .validators import validate_due_date

class TaskForm(forms.ModelForm):
    title = forms.CharField(required=True)
    due_date = forms.DateField(validators=[validate_due_date])  # Добавляем валидатор

    class Meta:
        model = Task
        fields = '__all__'
