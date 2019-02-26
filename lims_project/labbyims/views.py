from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import F

from django.views import View
from .forms import AdvancedSearch, Product_UnitForm, Product_Form, Location_Form
from .models import Product_Unit, Product, Location, Room
from .tables import Product_UnitTable, LocationTable, Product_Unit_ExpTable, FP_Product_UnitTable
from django_tables2 import RequestConfig
from .filters import ProductFilter, LocationFilter
import datetime
from datetime import datetime, timedelta
from django.utils import timezone

def home(request):
    if request.method == 'POST':
        form = AdvancedSearch(request.POST)
        if form.is_valid():
            search_res = form.cleaned_data["search"]
            print(search_res)
        else:
            print(form.errors)

        return HttpResponseRedirect('/search/?description={}'.format(search_res))

    else:
        form = AdvancedSearch(initial=request.GET)

    current_date = timezone.now()
    exp_warning = current_date + timedelta(days=27)
    exp_filter = Product_Unit.objects.filter(is_inactive = False, exp_date__range = [current_date,exp_warning ])
    table_exp = FP_Product_UnitTable(exp_filter)
    RequestConfig(request).configure(table_exp)
    return render(request, 'labbyims/home_afterlogin.html' ,{'form':form, 'table_exp': table_exp},)
    

def no_login(request):
    return render(request, 'labbyims/no_login.html')

def add_product(request):
    if request.method == "POST":
        form = Product_Form(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('.')
        else:
            print(form.errors)
    else:
        form = Product_Form()

    context = {'form': form}
    return render(request, 'labbyims/add_product.html', context)


def add_item(request):
    if request.method == "POST":
        form = Product_UnitForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('.')
            #return render(request, 'labbyims/home_afterlogin.html')
        else:
            print(form.errors)
    else:
        form = Product_UnitForm()


    context = {'form': form}
    return render(request, 'labbyims/add_item.html', context)

def inventory(request):
    table = Product_UnitTable(Product_Unit.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'labbyims/inventory.html', {'table': table})


def add_location(request):
    if request.method == "POST":
        form = Location_Form(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('.')
            #return render(request, 'labbyims/home_afterlogin.html')
        else:
            print(form.errors)
    else:
        form = Location_Form()

    context = {'form': form}
    return render(request, 'labbyims/add_location.html', context,)


def locations(request):
    table_1 = LocationTable(Location.objects.all())
    RequestConfig(request).configure(table_1)
    return render(request, 'labbyims/locations.html', {'table_1': table_1})

def expiring(request):
    current_date = timezone.now()
    exp_warning = current_date + timedelta(days=27)
    exp_filter = Product_Unit.objects.filter(exp_date__range = [current_date,exp_warning ])
    table_exp = Product_Unit_ExpTable(exp_filter)
    RequestConfig(request).configure(table_exp)
    return render(request, 'labbyims/expiring_retesting.html', {'table_exp': table_exp})



def search(request):
    product_list = Product_Unit.objects.all()
    product_list_up = product_list.update(curr_amount=F('init_amount')-F('used_amount'))
    product_filter = ProductFilter(request.GET, queryset=product_list)
    return render(request, "labbyims/product_list.html", {'filter': product_filter})



def search_location(request):
    location_list = Location.objects.all()
    location_filter = LocationFilter(request.GET, queryset=location_list)
    return render(request, "labbyims/search_location.html", {'filter': location_filter})
