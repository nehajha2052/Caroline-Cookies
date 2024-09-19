from django.urls import path
from .views import  (isAuthenticated, LoginView, UserView, LogoutView,
                     AccountView, RegisterLoginIndexView, RegisterView, ProductLandingPageView,
                     CancelView, SuccessView, CreateCheckoutSessionView,
                     StripeIntentView, stripe_webhook, BuyCookiesView, CommunityView, QRCodeView, CartView, getFreeCookies, getPointsForCookies, cookies_view, 
                     )
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	path('', views.BuyCookiesView.as_view(), name='home'),
    path('user', UserView.as_view()),
	path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('isAuthenticated', isAuthenticated().as_view()),
    path('myaccount/', AccountView.as_view(), name='myaccount'),
    path('registerLogin', RegisterLoginIndexView.as_view()),
    path('register/', RegisterView.as_view(), name = 'registration'),
    path('community', CommunityView.as_view(), name= 'community'),
    path('QRcode', QRCodeView.as_view(), name= 'QRcode'),
    path('cart',  CartView.as_view(), name= 'cart'),
    path('cookies/', cookies_view, name='cookies'),

]

urlpatterns += [
    path('create-payment-intent/', StripeIntentView.as_view(), name='create-payment-intent'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('buy-cookies/', BuyCookiesView.as_view(), name='buy-cookies'),
    path('cookies', ProductLandingPageView.as_view(), name='cookies'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('getFreeCookies', getFreeCookies.as_view(), name='getFreeCookies'),
    path('getPointsForCookies', getPointsForCookies.as_view(), name='getPointsForCookies'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
