# cart/forms.py
from django import forms
import re

class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    address1 = forms.CharField(max_length=255, required=True)
    address2 = forms.CharField(max_length=255, required=False)
    state = forms.CharField(max_length=100, required=True)
    city = forms.CharField(max_length=100, required=True)
    pincode = forms.CharField(max_length=6, required=True)
    mobile = forms.CharField(max_length=15, required=True)

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        if not re.match(r'^\d{6}$', pincode):
            raise forms.ValidationError("Invalid pincode. It must be 6 digits.")
        return pincode

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not re.match(r'^\+?\d{10,15}$', mobile):
            raise forms.ValidationError("Invalid mobile number. It must be 10 to 15 digits.")
        return mobile

    def clean_state(self):
        state = self.cleaned_data.get('state')
        # Add more validation if necessary
        return state

    def clean_city(self):
        city = self.cleaned_data.get('city')
        # Add more validation if necessary
        return city
