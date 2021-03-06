from django import forms

from .models import HelpDeskModel


class HelpDeskForm(forms.ModelForm):
    subject = forms.CharField(label='Subject of your issue', max_length=100, required=True,
                              widget=forms.Textarea(
                                  attrs={'style': 'resize:none;', 'rows': 1, 'class': 'form-control'}))
    issue = forms.CharField(label='Please describe the issue you are facing in detail', max_length=1000, required=True,
                            widget=forms.Textarea(
                                attrs={'style': 'resize:none;', 'rows': 12, 'class': 'form-control'}))

    class Meta:
        model = HelpDeskModel
        exclude = ['name_Request', 'issue_date', 'completed_date']
