from django.urls import path

from . import views

app_name = "webstore"

urlpatterns = [
    path("page/<int:page_number>", views.index, name="index"),
    path("profile", views.profile, name="profile"),
    path("save_user_profile", views.save_user_profile, name="save_user_profile"),
    # make new item for the owner
    path("new_item", views.new_item, name="new_item"),
    path("item_delete/<int:item_id>", views.item_delete, name="item_delete"),
    path("rate_item/<int:item_id>/<int:rate_score>", views.rate_item, name="rate_item"),
    path("item_page/<int:item_id>", views.item_page, name="item_page"),
    # handling shopping cart:
    path("cart/add/<int:item_id>", views.cart_add, name="cart_add"),
    path("cart/item_clear/<int:item_id>", views.item_clear, name="item_clear"),
    path("cart/item_increment/<int:item_id>", views.item_increment, name="item_increment"),
    path("cart/item_decrement/<int:item_id>", views.item_decrement, name="item_decrement"),
    path("cart/cart_clear", views.cart_clear, name="cart_clear"),
    path("cart/cart_detail/<int:page_number>", views.cart_detail, name="cart_detail"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
