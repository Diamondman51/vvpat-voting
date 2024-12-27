from django import forms

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

