from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .widgets import DatePickerInput
from .models import Task


# Use date picker widget to replace default widget
class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['task', 'category', 'due_date']
        widgets = {
            'due_date': DatePickerInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Add Task'))
