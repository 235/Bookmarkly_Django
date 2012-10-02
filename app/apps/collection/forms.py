from django import forms


class CollectItemForm(forms.Form):
    url = forms.CharField(max_length=450)
    title = forms.CharField(max_length=255)
    description = forms.CharField(max_length=255)
    tags = forms.MultipleChoiceField()
