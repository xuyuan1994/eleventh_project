from django.shortcuts import render, redirect
from .models import *
import bcrypt
item_regex=re.compile(r'\w{3,}')
def index(request):
    return render(request,'index.html')
def register(request):
    valid,response=User.objects.validate_registration(request.POST)
    if valid:
        request.session['message']="successfully registered an account!"
        User.objects.create(name=request.POST['name'],username=request.POST['username'],password= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
    else:
        request.session['message']="Failed to registered !"
        request.session['errors']=response
    return render(request,'result.html')
def login(request):
    valid,response=User.objects.validate_login(request.POST)
    if valid:
        request.session['logged_id']=User.objects.get(username=request.POST['username']).id
        context={
            "user":User.objects.get(username=request.POST['username']),
            "wishlists": Wishlist.objects.all()
        }
        return render(request,'home.html',context)
    else:
        request.session['message']="Failed to login !"
        request.session['errors']=response
        return render(request,'result.html')
def logout(request):
    del request.session['logged_id']
    return render(request,'index.html')
def create(request):
    return render(request,'create.html')
def process(request):
    errors=[]
    if not item_regex.match(request.POST['item']):
        error.append("item should be at lease 3 characters")
        context={
            "errors":errors
        }
        return render(request,'result2.html',context)
    else:
        if not Product.objects.filter(name=request.POST['item']).exists():
            Product.objects.create(name=request.POST['item'],added_by=User.objects.get(id=request.session['logged_id']).username)
        if Wishlist.objects.filter(name=User.objects.get(id=request.session['logged_id']).username).exists():
            wishlist1=Wishlist.objects.get(name=User.objects.get(id=request.session['logged_id']).username)
            Product1=Product.objects.get(name=request.POST['item'])
            wishlist1.product.add(Product1)
        else:
            Wishlist.objects.create(name=User.objects.get(id=request.session['logged_id']).username)
            wishlist1=Wishlist.objects.get(name=User.objects.get(id=request.session['logged_id']).username)
            Product1=Product.objects.get(name=request.POST['item'])
            wishlist1.product.add(Product1)
        context={
            "wishlists":Wishlist.objects.exclude(name=User.objects.get(id=request.session['logged_id']).username),
    
            "wishlist0":Wishlist.objects.get(name=User.objects.get(id=request.session['logged_id']).username).product.all(),
            "user":User.objects.get(id=request.session['logged_id'])
        }

        return render(request,'home.html',context)
def item(request,item_id):
    context={
        "product": Product.objects.get(id=item_id).name,
        "wishlists":Wishlist.objects.all()
        
    }
    return render(request,'item.html',context)
def delete(request,item_id):
    Product1=Product.objects.get(id=item_id)
    Product1.delete()
    Product1.save()
    context={
                "wishlists":Wishlist.objects.exclude(name=User.objects.get(id=request.session['logged_id']).username),
        
                "wishlist0":Wishlist.objects.get(name=User.objects.get(id=request.session['logged_id']).username).product.all(),
                "user":User.objects.get(id=request.session['logged_id'])
            }

    return render(request,'home.html',context)
def remove(request,item_id):
    wishlist1=Wishlist.objects.get(name=User.objects.get(id=request.session['logged_id']).username)
    Product1=Product.objects.get(id=item_id)
    wishlist1.product.remove(Product1)
    wishlist1.save()
    context={
                "wishlists":Wishlist.objects.exclude(name=User.objects.get(id=request.session['logged_id']).username),
        
                "wishlist0":Wishlist.objects.get(name=User.objects.get(id=request.session['logged_id']).username).product.all(),
                "user":User.objects.get(id=request.session['logged_id'])
            }

    return render(request,'home.html',context)
def add(request,item_id):

    wishlist1=Wishlist.objects.get(name=User.objects.get(id=request.session['logged_id']).username)
    Product1=Product.objects.get(id=item_id)
    wishlist1.product.add(Product1)

    context={
                "wishlists":Wishlist.objects.exclude(name=User.objects.get(id=request.session['logged_id']).username),
        
                "wishlist0":Wishlist.objects.get(name=User.objects.get(id=request.session['logged_id']).username).product.all(),
                "user":User.objects.get(id=request.session['logged_id'])
            }

    return render(request,'home.html',context)
def back_to_home(request):
    context={
                "wishlists":Wishlist.objects.exclude(name=User.objects.get(id=request.session['logged_id']).username),
        
                "wishlist0":Wishlist.objects.get(name=User.objects.get(id=request.session['logged_id']).username).product.all(),
                "user":User.objects.get(id=request.session['logged_id'])
            }

    return render(request,'home.html',context)

# Create your views here.

