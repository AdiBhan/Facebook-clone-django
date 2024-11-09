from datetime import datetime
from django import forms
from .models import Voter

class VoterFilterForm(forms.Form):
    party_affiliation = forms.ChoiceField(
        choices=[('', 'All')] + list(Voter.objects.values_list('party_affiliation', 'party_affiliation').distinct()),
        required=False,
    )
    min_date_of_birth = forms.ChoiceField(
        choices=[('', 'All')] + [(str(year), str(year)) for year in range(1900, datetime.now().year+1)],
        required=False,
    )
    max_date_of_birth = forms.ChoiceField(
        choices=[('', 'All')] + [(str(year), str(year)) for year in range(1900, datetime.now().year+1)],
        required=False,
    )
    voter_score = forms.ChoiceField(
        choices=[('', 'All')] + [(str(i), str(i)) for i in range(11)],
        required=False,
    )
    voted_in_v20state = forms.BooleanField(required=False)
    voted_in_v21town = forms.BooleanField(required=False)
    voted_in_v21primary = forms.BooleanField(required=False)
    voted_in_v22general = forms.BooleanField(required=False)
    voted_in_v23town = forms.BooleanField(required=False)