from django.shortcuts import render, redirect
from .forms import CompanyForm, UpdateForm
from .models import Company
from django.contrib import messages	
from django.contrib.auth.decorators import login_required

@login_required(login_url='login/')
def main_view(request):

	import requests 
	import json

	companyList = []
	companies = request.user.company_set.all()
	for comp in companies:
		companyList.append(comp.ticker)

	
	if len(companyList) != 0:

		final = ','.join(companyList)

		api_request = requests.get("https://cloud.iexapis.com/stable/stock/market/batch?symbols=" + final + "&types=quote&token=pk_0bf2e93e71414e3881861ea221c32703")

		api = json.loads(api_request.content)

		market_total = 0
		book_total = 0
		stocks = {}

		for comp in companies:

			stocks[str(comp)] = {
				'companyName'	: api[str(comp)]['quote']['companyName'],
				'ticker'		: str(comp),
				'nbr_shares'	: comp.nbr_shares,
				'avg_cost'  	: comp.avg_price,
				'closePrice'	: api[str(comp)]['quote']['latestPrice'],
				'book_cost'		: comp.avg_price * comp.nbr_shares,
				'market_value'	: api[str(comp)]['quote']['previousClose'] * comp.nbr_shares,
				'total_gain'	: api[str(comp)]['quote']['previousClose'] * comp.nbr_shares - comp.avg_price * comp.nbr_shares,
				'total_gain_pc'	: (api[str(comp)]['quote']['previousClose'] - comp.avg_price) / comp.avg_price * 100,
				'id'			: comp.id
			}

			market_total += stocks[str(comp)]['market_value']
			book_total += stocks[str(comp)]['book_cost']		


			if stocks[str(comp)]['total_gain'] < 0 :
				stocks[str(comp)]['total_gain'] = '<span style="color:red">' + format(stocks[str(comp)]['total_gain'], ',.0f') + '$</span>'
				stocks[str(comp)]['total_gain_pc'] = '<span style="color:red">' + format(stocks[str(comp)]['total_gain_pc'], ',.0f') + '%</span>'
			else:
				stocks[str(comp)]['total_gain'] = '<span style="color:green">' + format(stocks[str(comp)]['total_gain'], ',.0f') + '$</span>'
				stocks[str(comp)]['total_gain_pc'] = '<span style="color:green">' + format(stocks[str(comp)]['total_gain_pc'], ',.0f') + '%</span>'


		profit = market_total - book_total
		profitPercent = profit / book_total * 100

		if profit > 0:
			profit = '<span style="color:green">' + format(profit, ',.0f') + '$</span>'
			profitPercent = '<span style="color:green">' + format(profitPercent, ',.1f') + '%</span>'
			market_total = '<span style="color:green">' + format(market_total, ',.0f') + '$</span>'
		else:
			profit = '<span style="color:red">' + format(profit, ',.0f') + '$</span>'
			profitPercent = '<span style="color:red">' + format(profitPercent, ',.1f') + '%</span>'
			market_total = '<span style="color:red">' + format(market_total, ',.0f') + '$</span>'

	else:
		stocks = ""
		book_total = 0
		market_total = '0$'
		profit = '0$'
		profitPercent = '0%'

	context = {
		'stocks' : stocks,
		'book_total' : book_total,
		'market_total' : market_total,
		'profit' : profit,
		'profitPercent' : profitPercent,
	}

	return render(request, "portfolio/main.html", context)


@login_required(login_url='login/')
def add_stock_view(request):

	company = request.POST.get('ticker')
	form = CompanyForm(request.POST or None)
	
	if form.is_valid():
		# Try if company already exist and update data
		try:
			exist = request.user.company_set.get(ticker = company.upper())
			instance = form.save(commit=False)
			instance.avg_price = (instance.avg_price *instance.nbr_shares + exist.nbr_shares * exist.avg_price) / (instance.nbr_shares + exist.nbr_shares)
			instance.nbr_shares += exist.nbr_shares
			instance.save()
			exist.delete()
			request.user.company_set.add(instance)

		# If company is not in portfolio then add it	
		except:
			instance = form.save(commit=False)
			instance.save()
			request.user.company_set.add(instance)

		messages.success(request, "Portfolio successfuly updated")
		return redirect('main')

	form = CompanyForm(request.POST or None)

	return render(request, "portfolio/add_stock.html", {'form' : form} )	


@login_required(login_url='login/')
def delete_stock_view(request, id):

	stock = request.user.company_set.get(pk = id)
	stock.delete()
	messages.success(request ,"Stock successfuly removed from portfolio")
	
	return redirect('main')


@login_required(login_url='login/')
def update_view(request, id):

	obj = Company.objects.get(pk = id)
	
	form = UpdateForm(request.POST or None, instance= obj)

	if form.is_valid():
		form.save()
		messages.success(request, "Stock successfuly updated!")
		return redirect('main')

	context = {
		'form' : form,
		'obj' : obj,
	}

	return render(request, 'portfolio/update_stock.html', context)