from django import forms
from .models import Company
from django.contrib import messages

class CompanyForm(forms.ModelForm):
	class Meta:
		model = Company
		fields = ['ticker', 'nbr_shares', 'avg_price']
	
	def clean_ticker(self):
		import requests 
		import json

		ticker_ = self.cleaned_data.get('ticker')																			
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker_ + "/batch?types=quote&token=pk_0bf2e93e71414e3881861ea221c32703")

		try:
			response = json.loads(api_request.content)
		except :
			raise forms.ValidationError("Invalid Ticker, please try again")

		return ticker_.upper()


	def clean_nbr_shares(self):
		nbr_shares_ = self.cleaned_data.get('nbr_shares')

		if nbr_shares_ <= 0:
			raise forms.ValidationError("Invalid numbers of shares, please try again")

		return nbr_shares_


	def clean_avg_price(self):
		avg_price_ 	= self.cleaned_data.get('avg_price')

		if avg_price_ <= 0:
			raise forms.ValidationError("Invalid average price, please try again")

		return avg_price_


class UpdateForm(CompanyForm):
	class Meta:
		model =  Company
		fields = ['nbr_shares', 'avg_price']