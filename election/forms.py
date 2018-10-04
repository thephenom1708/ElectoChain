from django import forms
from .models import Election, Candidate

class ElectionForm(forms.ModelForm):
    election_date = forms.DateField(widget=forms.DateInput)

    class Meta:
        model = Election
        fields = ['election_name', 'election_region', 'election_date', 'candidate_count', 'election_description', 'election_pic']