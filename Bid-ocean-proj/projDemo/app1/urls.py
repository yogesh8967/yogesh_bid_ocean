from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_p, name = "login"),
    path('logout/', views.logouter, name = "logout"),
    path('register/', views.register, name = "register"),
    path('home/', views.home, name = "home"),
    path('products/', views.products, name = "products"),
    path('customer/', views.customer, name = "customer"),
    path('menu/<str:Category>/', views.Menu, name = "menu"),
    path('menu/<str:Category>/<str:usr>/<str:menu_cart>/', views.Menu_cart, name = "menu_cart"),
    path('home/<str:dishname>/', views.home_cart, name = "home_dish"),
    path('manager/', views.manager_control, name = "manager"),
    path('Dish_Adder/', views.Dish_Adder, name = "Dish_Adder"),
    path('update_dish/', views.Update_Dish, name = "Update_Dish"),
    path('Updater/<str:Dish_N>/', views.Updater, name = "Updater"),
    path('Deleter/<str:Dish_N>/', views.Deleter, name = "Deleter"),
    path('login/add_details/<str:usr>/', views.details_adder, name = "add_details"),
    path('profile_page/<str:usr>/', views.profile_page, name = "profile_page"),
    path('contact_updater/<str:usr>/', views.contact_Updater, name = "contact_Updater"),
    path('cart/<str:usr>/', views.cart, name = "cart"),
    path('Dishes/', views.Dishes, name = "Dishes"),
    path('Orders/', views.Orders, name = "Orders"),
    path('<str:cart>/<str:usr>/my-ajax-test/', views.myajaxtestview, name='ajax-test-view'),
    path('<str:ord>/my-ajax-test2/', views.myajaxtestview2, name='ajax-test-view2'),
]
