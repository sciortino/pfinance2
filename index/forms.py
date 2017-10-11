
from django import forms

class IntakeForm(forms.Form):
	amt = forms.FloatField(widget=forms.TextInput(attrs={
		'class':'form-box',
		'placeholder': 'too damn high'
		}))
	r = forms.FloatField(widget=forms.TextInput(attrs={
		'class':'form-box',
		'placeholder': 'not interesting'
		}))
	pmt = forms.FloatField(widget=forms.TextInput(attrs={
		'class':'form-box',
		'placeholder': 'arm + leg'
		}))


class ReportForm(forms.Form):
	amt = forms.FloatField(widget=forms.TextInput(attrs={
		'class':'form-box'
		}))
	r = forms.FloatField(widget=forms.TextInput(attrs={
		'class':'form-box'
		}))
	pmt = forms.FloatField(widget=forms.TextInput(attrs={
		'class':'form-box'
		}))
	per = forms.FloatField(widget=forms.TextInput(attrs={
		'class':'form-box'
		}))
	calc_type = forms.ChoiceField(choices=(
		('per', "months 'til paid off"),
		('pmt', 'monthly payment')
		),
		widget=forms.Select(attrs={
			'class':'form-choice'
		})
	)