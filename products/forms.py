from django import forms
from .models import ProductReview

class OrderAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].label = "Mugdar"


class ProductReviewForm(forms.ModelForm):
    # stars_given = forms.IntegerField(min_value=1, max_value=5)
    class Meta:
        model = ProductReview
        fields = ['comment']