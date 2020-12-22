from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json

# Create your views here.

def index(request):
    allprods = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        allprods.append([prod, range(1, nslides), nslides])
    params = {'allProds': allprods}
    return render(request, 'store/index.html', params)


def about(request):
    return render(request, 'store/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        cont = Contact(name=name, email=email, phone=phone, desc=desc)
        cont.save()
    return render(request, 'store/contact.html')


def tracker(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=order_id, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=order_id)
                updates = []
                for item in update:
                  updates.append({'text': item.update_desc, 'time': item.timestamp})
                  response = json.dumps({"status": "success", "update": updates, "itamjson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status": "noitem"}')
        except Exception as e:
            return HttpResponse('{"status": "error"}')
    return render(request, 'store/tracker.html')


def search(request):
    query = request.GET.get('search')
    allprods = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchmatch(query, item)]
        n = len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allprods.append([prod, range(1, nslides), nslides])
    params = {'allProds': allprods, 'msg': ''}
    if len(allprods) == 0 or len(query) < 4:
        params = {'msg': 'Please make sure to enter relevent scarch'}
    return render(request, 'store/search.html', params)

def searchmatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def productview(request, myid):
    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    return render(request, 'store/productview.html', {'product': product[0]})


def checkout(request):

    if request.method == "POST":
        itemsjson = request.POST.get('itemjson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        add = request.POST.get('address', '')
        city = request.POST.get('city', '')
        zipc = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Order(items_json=itemsjson, name=name, email=email, address=add, city=city, zip_code=zipc, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        myid = order.order_id
        return render(request, 'store/checkout.html', {'thank': thank, 'id': myid})
    return render(request, 'store/checkout.html')