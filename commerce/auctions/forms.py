from django import forms
from .models import CATEGORY_CHOICES

#  title = models.CharField(max_length=64)
#     description = models.CharField(max_length=144)
#     startingBid = models.CharField(max_length=64)
#     category = models.CharField(max_length=32, choices=CATEGORY_CHOICES)
#     imgUrl = models.CharField(max_length=64)
#     owner = models.CharField(max_length=64)


class ListingForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Title", "class": "form-control"})
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "Description", "class": "form-control"})
    )
    category = forms.CharField(
        widget=forms.Select(attrs={
            "class": "form-control"}, choices=CATEGORY_CHOICES)
    )
    startingBid = forms.DecimalField(decimal_places=2, max_digits=4)

    imgUrl = forms.CharField(
        widget=forms.URLInput(
            attrs={"placeholder": "imgUrl", "class": "form-control"})
    )
