from rest_framework import serializers
from .models import Task
from .validators import validate_due_date

class TaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={'blank': 'This field may not be blank.'}
    )
    due_date = serializers.DateField(validators=[validate_due_date])

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']
