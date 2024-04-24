from django import forms
from counter.models import Log

class LogMessageForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = ("log_timestamp",)   # NOTE: the trailing comma is required