from django.urls import path
from app import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_view
from .forms import *



urlpatterns = [

    #-------------Auth-----------------------
    path('login/', auth_view.LoginView.as_view(template_name = 'app/login.html', authentication_form=CustomerLoginForm), name='login'),
    path('logout/', auth_view.LogoutView.as_view(next_page = '/'), name='logout'),

    path('password_change/', auth_view.PasswordChangeView.as_view(template_name='app/password_change.html', form_class = CustomerPasswordChangeForm), name='password_change'),
    path('password_change/done/', auth_view.PasswordChangeDoneView.as_view(template_name='app/password_change_done.html'), name='password_change_done'),

    path('password_reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html', form_class = CustomerPasswordResetForm), name='password_reset'),
    path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(template_name = 'app/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name = 'app/password_reset_confirm.html', form_class = CustomerPasswordResetConfirmForm), name='password_reset_confirm'),
    path('reset/done/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

    #------------Auth-End-------------------

    #------------Cart/Ajax--------------------

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='show-cart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),

    #------------Cart/Ajax End----------------


    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/', views.orders, name='orders'),

    
    path('', views.home.as_view(), name = 'home'),
    path('product-detail/<int:id>/', views.ProductDetail.as_view(), name='product-detail'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('mobile/', views.mobile, name='mobile'),
    path('registration/', views.customerregistration.as_view(), name='customerregistration'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

