from django.shortcuts import render
from .models import Blogpost
# from django.http import HttpResponse


# Create your views here.
def index(request):
    mypost = Blogpost.objects.all()
    print(mypost)
    return render(request, "blog/index.html", {'mypost': mypost})

def post(request, postid):
    posts = Blogpost.objects.filter(post_id=postid)[0]
    return render(request, "blog/post.html", {'post': posts})



"""def inde(request):
    allprods = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        allprods.append([prod, range(1, nslides), nslides])
    params = {'allProds': allprods}
    return render(request, 'store/index.html', params)"""