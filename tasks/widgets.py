from django import forms


# Date picker widget replaces default date input widget on the tasks form
class DatePickerInput(forms.DateInput):
    input_type = 'date'
