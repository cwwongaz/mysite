import json
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from datetime import datetime, date, time
from django.core.exceptions import ObjectDoesNotExist
from .models import User, client, comment, item, rating

# Constant for pages
ITEM_PER_INDEX = 12
MORE_ITEM_PER_INDEX = 30

# my new data type to handle shopping cart
'''class cart(object):
    def __init__(self, item_id, item_number):
        self.item_id = item_id
        self.item_number = item_number

    def toJSON(self):
        return json.dumps(self, default=lambda o:o.__dict__)
'''

# Create your views here.

def index(request, page_number):
    # shopping cart management
    # create session
    request.session["cart"] = createSession(request)
    items = Paginator(item.objects.all(), ITEM_PER_INDEX)
    
    return render(request, "webstore/index.html", {
        "items": items.page(page_number).object_list,
        "page_number": page_number,
        "total_page": items.num_pages,
        "num_in_cart": len(request.session["cart"]),
    })

def item_page(request, item_id):
    # shopping cart management
    # create session
    request.session["cart"] = createSession(request)
    item_data = item.objects.get(id=item_id)

    return render(request, "webstore/item_page.html", {
        "item_data": item_data,
        "num_in_cart": len(request.session["cart"]),
    })

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("webstore:index", kwargs={'page_number':1}))
        else:
            return render(request, "webstore/login.html", {
                "message": "Invalid username / password."
            })
    else:
        return render(request, "webstore/login.html")

@login_required
def rate_item(request, item_id, rate_score):
    item_repr = item.objects.get(id=item_id)
    user_rated = True
    try: 
        user_rating = item_repr.rating.get(rater = request.user)
    except ObjectDoesNotExist:
        user_rating = None
        user_rated = False

    # check if the rate_score is valid
    valid_rate = False
    if rate_score >= 0 and rate_score <= 5:
        valid_rate = True

    if user_rated == False and valid_rate == True:
        item_repr.rating_average = item_repr.rating_average * item_repr.number_of_rating + rate_score
        item_repr.number_of_rating = item_repr.number_of_rating + 1
        item_repr.rating_average = item_repr.rating_average / item_repr.number_of_rating
        item_repr.save()

        user_new_rating = rating(rater=request.user, rating=rate_score)
        user_new_rating.save()
        item_repr.rating.add(user_new_rating)
    return HttpResponseRedirect(reverse("webstore:item_page", kwargs={'item_id': item_id}))

@login_required
def new_item(request):
    # form data
    class itemForm(forms.Form):
        # item basic information
        item_name = forms.CharField(label="item name", max_length=100)
        item_price = forms.FloatField(min_value=0)
        item_footnote = forms.CharField(label="item footnote", widget=forms.Textarea(attrs={'rows': 4}), max_length=100)
        item_Description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), max_length=1000)
        number_in_store = forms.IntegerField(min_value=0)
        picture = forms.ImageField()

        item_name.widget.attrs.update({'class':'form-control register_and_login', 'required':'required', 'style': 'height: 32.5px; font-size: 14px; border: 1px solid #9B9791'})
        item_price.widget.attrs.update({'class':'form-control register_and_login', 'required':'required', 'style': 'height: 32.5px; font-size: 14px; border: 1px solid #9B9791'})
        item_footnote.widget.attrs.update({'class':'form-control register_and_login', 'style': 'height: 32.5px; font-size: 14px; border: 1px solid #9B9791'})
        item_Description.widget.attrs.update({'class':'form-control register_and_login', 'style': 'height: 32.5px; font-size: 14px; border: 1px solid #9B9791'})
        number_in_store.widget.attrs.update({'class':'form-control register_and_login', 'required':'required', 'style': 'height: 32.5px; font-size: 14px; border: 1px solid #9B9791'})
        picture.widget.attrs.update({'class':'photo_upload form-control register_and_login', 'required': 'False', 'style': 'height: 32.5px; font-size: 14px; border: 1px solid #9B9791; padding: 2.5px'})

    # filter out non-logged-in users
    if request.user.is_authenticated:
        # filter out non-admin users
        if request.user.is_admin:
            if request.method == "POST": 
                # need to add request.FILES if there were images.
                form = itemForm(request.POST, request.FILES)
                # check whether it's valid
                if form.is_valid():

                    name = form.cleaned_data["item_name"]
                    price = form.cleaned_data["item_price"]
                    footnote = form.cleaned_data["item_footnote"]
                    description = form.cleaned_data["item_Description"]
                    number_in_store = form.cleaned_data["number_in_store"]
                    picture = form.cleaned_data["picture"]


                    New_item = item.objects.create(
                        item_name = name,
                        item_price = price,
                        item_footnote = footnote,
                        item_Description = description,
                        number_in_store = number_in_store,
                        picture = picture,
                    )
                    New_item.save()
                    return HttpResponseRedirect(reverse("webstore:index", kwargs = {'page_number':1}))
            else:
                form = itemForm()

        else:
            # filter out non-admin users, return them back to index page
            return HttpResponseRedirect(reverse("webstore:index", kwargs = {'page_number':1}))    
    else:
        # filter out non-logged-in users, return them back to index page
        return HttpResponseRedirect(reverse("webstore:index", kwargs = {'page_number':1}))
    return render(request, "webstore/new_item.html", {
                "form": form,
                "num_in_cart": len(request.session["cart"]),
            })

@login_required
def item_delete(request, item_id):
    # only admin can delete item
    if request.user.is_admin:
        item_repr = item.objects.get(id=item_id)
        item_repr.delete()

    return HttpResponseRedirect(reverse("webstore:index", kwargs = {'page_number':1}))

# cart handling
def cart_add(request, item_id):
    # shopping cart management
    # create session
    # Django session list cannot append class objects
    request.session["cart"] = createSession(request)

    # handling add to cart
    request.session["cart"].append(item_id)

    return HttpResponseRedirect(reverse("webstore:item_page", kwargs = {'item_id':item_id}))


def item_clear(request, item_id):
    # shopping cart management
    # create session
    request.session["cart"] = createSession(request)
    while item_id in request.session["cart"]:
        request.session["cart"].remove(item_id)
    return HttpResponseRedirect(reverse("webstore:cart_detail", kwargs = {'page_number':1}))


def item_increment(request, item_id):
    # shopping cart management
    # create session
    request.session["cart"] = createSession(request)
    request.session["cart"].append(item_id)
    return HttpResponseRedirect(reverse("webstore:cart_detail", kwargs = {'page_number':1}))


def item_decrement(request, item_id):
    # shopping cart management
    # create session
    request.session["cart"] = createSession(request)
    request.session["cart"].remove(item_id)
    return HttpResponseRedirect(reverse("webstore:cart_detail", kwargs = {'page_number':1}))


def cart_clear(request):
    # shopping cart management
    # create session
    request.session["cart"] = createSession(request)
    request.session["cart"] = []
    return HttpResponseRedirect(reverse("webstore:index", kwargs={'page_number':1}))
    

def cart_detail(request, page_number):
    # shopping cart management
    # create session
    request.session["cart"] = createSession(request)
    items = Paginator(item.objects.filter(id__in=request.session["cart"]), ITEM_PER_INDEX)

    return render(request, "webstore/cart.html", {
        "cart": request.session["cart"],
        "items": items.page(page_number).object_list,
        "page_number": page_number,
        "total_page": items.num_pages,
        "num_in_cart": len(request.session["cart"]),
    })

@login_required
def save_user_profile(request):
    if request.method == "POST":
        user = request.user

        em = request.POST["email"]
        bday = request.POST["birthday"]
        add = request.POST["address"]

        client_info = client.objects.get(user=request.user)
        client_info.delivery_address = add
        client_info.birthday = bday
        client_info.save()

        user.email = em
        user.save()
    return HttpResponseRedirect(reverse("webstore:profile"))

@login_required
def profile(request):
    # shopping cart management
    # create session
    request.session["cart"] = createSession(request)

    # return the user's profile
    # consider making bought history
    if request.user.is_authenticated:
        user_information = client.objects.get(user=request.user)
        user_email = request.user.email
        username = request.user.username
        user_delivery_address = user_information.delivery_address
        user_birthday = user_information.birthday.strftime('%Y-%m-%d')

        return render(request, "webstore/profile.html", {
            "user_name":username,
            "user_email":user_email,
            "user_delivery_address":user_delivery_address,
            "user_birthday":user_birthday,
            "num_in_cart": len(request.session["cart"]),
        })
    else:
        return HttpResponseRedirect(reverse("webstore:index", kwargs={"page_number":1}))

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("webstore:index", kwargs = {'page_number':1}))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        birthday = request.POST["birthday"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "webstore/register.html", {
                "message": "Passwords does not match."
            })

        # set client's profile
            # set date and check if the date is valid
        birthday_max = datetime.combine(date.today(), time.max).date()
        birthday_min = datetime.strptime("1990-01-01", "%Y-%m-%d").date()
        birthday = datetime.strptime(birthday, "%Y-%m-%d").date()

        # check if birthday is valid
        if birthday >= birthday_min and birthday <= birthday_max:
            try:
                # Attempt to create new user
                user = User.objects.create_user(username, email, password)
                client_create = client(user = user, birthday = birthday)
                
                # user is created in User.objects.create_user(username, email, password), not here
                user.save()
                # will not run the next sentence (this line) if error occurs
                client_create.save()

            except IntegrityError:
                return render(request, "webstore/register.html", {
                    "message": "Username already taken."
                })

        else:
            return render(request, "webstore/register.html", {
                    "message": "Birthday is not valid."
            })

        # log the user in after account is created.
        login(request, user)

        return HttpResponseRedirect(reverse("webstore:index", kwargs = {'page_number':1}))
    else:
        return render(request, "webstore/register.html")

### ### ### function prototypes ### ### ###
def createSession(request):
    if "cart" not in request.session:
        request.session["cart"] = []

    return request.session["cart"]
