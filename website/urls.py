from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.clientDashboard, name='dashboard'),
    path('login/', views.login_page, name='login'),
    path('signup/', views.signup, name='signup'),
    path('signup/medical', views.mediclainfos, name='medical'),
    path('logout/', views.loggout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('housedata/', views.storeHouseData, name='housedata'),
    path('cardata/', views.storeCarData, name='cardata'),
    path('data/', views.data, name='data'),
]
