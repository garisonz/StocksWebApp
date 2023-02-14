from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages
import requests
import json

def home(request):

	if request.method == 'POST':
		ticker = request.POST['ticker']
		r = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_287bfd9266734b11a47966f878cf25df")
	
		try:
			api = json.loads(r.content)
		except Exception as e:
			api = "Error"
		return render(request, 'home.html', {'api': api})

	else:
		return render(request, 'home.html', {'ticker': "Enter a ticker symbol."})


def about(request):

	return render(request, 'about.html', {})

def add_stock(request):

	if request.method == 'POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ("Stock Has Been Added"))
			return redirect('add_stock')
	else:
		ticker = Stock.objects.all()
		temp = []
		for ticker_item in ticker:
			r = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_287bfd9266734b11a47966f878cf25df")
			try:
				api = json.loads(r.content)
				temp.append(api)
			except Exception as e:
				api = "Error"

		return render(request, 'add_stock.html', {'ticker': ticker, 'temp': temp})

def delete(request, stock_id):

	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock Has Been Deleted"))
	return redirect(add_stock)