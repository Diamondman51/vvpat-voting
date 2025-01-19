from django import forms
from django.forms import modelformset_factory

from vvpat.models import Director, President, Voter

class CustomTextWidget(forms.TextInput):
    pass

class CustomTextWidgetForm(forms.Form):
    phone = forms.CharField(
        widget=CustomTextWidget(attrs={
            "class": "input-control search radius-0", 
            'placeholder': "Type Phone", 'style': 
            'padding: 20px; margin-top: 20px',
            # 'id': "search-member",
        }),
        label=''
    )


DirectorFormSet = modelformset_factory(
    model=Director,
    fields=['id'],  # Only allow selection of directors
    extra=0  # No extra forms
)


class PresidentVoteForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = ['president_vote']
        
    president_vote = forms.ModelChoiceField(
        queryset=President.objects.all(),  # Get all presidents
        required=True,
        label="Select President"
)