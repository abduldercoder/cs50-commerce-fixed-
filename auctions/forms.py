from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Title"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "Description"}),
            "starting_bid": forms.NumberInput(attrs={"min": 0}),
            "image_url": forms.URLInput(attrs={"placeholder": "Image URL (optional)"}),
            "category": forms.Select()  # Select already styled in __init__
        }

    def clean_starting_bid(self):
        bid = self.cleaned_data["starting_bid"]
        if bid <= 0:
            raise forms.ValidationError("Starting bid must be greater than zero.")
        return bid
