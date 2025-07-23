from django.urls import path
from .import views
urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.login_view,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.logout_view,name='logout'),
    path('Admin',views.admin_view,name='Admin'),
    path('add-expenses',views.add_expense,name="add_expense"),
    path('add-trip',views.add_trip,name="add_trip"),
    path('add-category',views.add_category,name="add_category"),
    path('trips-list',views.trip_list,name="trips_list"),
    path('expense-list/<int:pk>/',views.expense_list,name="expense_list"),
    path('end-trip/<int:pk>/',views.finsih_trip,name="end_trip")
]