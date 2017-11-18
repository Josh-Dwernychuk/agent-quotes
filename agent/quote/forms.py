from django import forms


class PriceForm(forms.Form):
    """ Price form to take agent input for quote value """
    price_form = forms.DecimalField(label='Enter Quote Value ')
