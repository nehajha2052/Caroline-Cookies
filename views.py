from django.shortcuts import render, redirect
from .models import *
from django.views import generic
from .serializers import UserSerializer
import jwt, datetime
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from rest_framework.views import APIView
from django.views.generic.base import View
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.views import View
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.views import View
import json
import stripe
from datetime import date
from django.contrib.auth.password_validation import validate_password






class HomeView(generic.ListView):
	model = User
	template_name = 'buy_cookies.html'


class CartView(generic.ListView):

    def get(self, request):
        user = request.user
        context = {
            'user': user
            }

        return render(request, 'cart.html', context)

class AccountView(generic.ListView):
    # In your AccountView
    def get(self, request):
        user = request.user  # Get the logged-in user
        
        
                
       
        context = {
            'user': user,
        }
        return render(request, 'accountpage.html', context)



class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')
        print(request.COOKIES)

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'SECRET', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id = payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)
        # return Response(request.data)

class isAuthenticated(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')
        print(request.COOKIES)

        if not token:
            return JsonResponse({'isAuthenticated': False})

        try:
            payload = jwt.decode(token, 'SECRET', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            return JsonResponse({'isAuthenticated': False})

        return JsonResponse({'isAuthenticated': True})


class LoginView(APIView):


    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()


        


        if not password:
            messages.error(request, 'Make sure to enter your password')
            return redirect('login')
        
        if not email:
            messages.error(request, 'Make sure to enter your email')
            return redirect('login')
        
        if user is None:
            #raise AuthenticationFailed('User not found!')
            messages.error(request, 'User not found!')
            return redirect('login')

        if not user.check_password(password):
            #raise AuthenticationFailed('Incorrect Password!')
            messages.error(request, 'Incorrect Password!')
            return redirect('login')
        
        
        
        
        login(request, user) # This was needed to log the user in to display the information on the Account page.

        if user.is_authenticated:
           
            if date.today().month == user.date_of_birth.month and date.today().day == user.date_of_birth.day:

                messages.success(request, "Happy Birthday! Have 100 points!")
                user.points += 100
                user.save()

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() +  datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow() }
        token = jwt.encode(payload, 'SECRET', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'jwt':token}
        print(f"\\n\n\n\n{response.data}")
        return redirect('myaccount')



from django.contrib.auth import logout

class LogoutView(APIView):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been successfully logged out.")
        # Redirect to a logged-out page or wherever you prefer
        return redirect('home')



class RegisterView(View):
    template_name = 'register.html'

    def post(self, request):
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        date_of_birth = request.POST.get('date_of_birth', '')
        address = request.POST.get('address', '')

        # Check if the email is already in use
        if User.objects.filter(email=email).exists():
            messages.error(request, 'User already exists!')
            return redirect('registration')

        # Check if all required fields are filled
        if not email or not password or not first_name or not last_name or not date_of_birth or not address:
            messages.error(request, 'Make sure all fields are filled')
            return redirect('registration')

        
        try:
            validate_password(password)
            
        except:
            messages.error(request, "Please include at least one upper case character, one special character, and be at least 8 characters long")
            return redirect('registration')
        

        # Create a new user with a hashed password
        User.objects.create(
            email=email,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            address=address
        )

        messages.success(request, 'You have successfully registered.')
        messages.success(request, 'Congrats! You get 20 points on signup!')
        return redirect('login')


    def get(self, request):

        return render(request, 'register.html')


class RegisterLoginIndexView(generic.CreateView):
    def get(self, request):
        return render(request, 'registerLogin.html')


class ProductLandingPageView(TemplateView):
    template_name = "cookies.html"

    # def get_context_data(self, **kwargs):
    #     product = Products.objects.get(product_name="Test Product")
    #     products = Products.objects.all()
    #     total_price = 0
    #     product_ids = []
    #     order = {}

    #     for product in products:
    #         quantity = product.product_id + 1
    #         order[product.product_id] = {'name':product.product_name,
    #                                      'price':product.get_display_price(),
    #                                      'quantity':quantity}
    #         total_price += (float(product.get_display_price()) * quantity)
    #         product_ids.append(product.product_id)
    #     print(order)
    #     order_json = json.dumps(order)
    #     context = super(ProductLandingPageView, self).get_context_data(**kwargs)
    #     context.update({
    #         "products": products,
    #         "product_ids": product_ids,
    #         "single_product":product,
    #         "total_price": total_price,
    #         "order": order,
    #         "order_json":order_json,
    #         "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
    #     })
    #     return context

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)

        if user.is_authenticated:
            try:
                cart = Cart.objects.get(user=user)
                total_price = 0
                order = {}

              

                for cart_item in cart.cartitem_set.all():
                    quantity = cart_item.quantity
                    product = cart_item.product
                    order[product.product_id] = {'name':product.product_name,
                                                'price':product.get_display_price(),
                                                'quantity':quantity}
                    total_price += (float(product.get_display_price()) * int(quantity))
                order_json = json.dumps(order)
                

                

                context = super(ProductLandingPageView, self).get_context_data()
                context.update({
                    "total_price": total_price,
                    "order": order,
                    "order_json":order_json,
                    "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
                    "user": user
                    
                })
                # Render the template with the updated context
                # return self.render_to_response(context)


            except Cart.DoesNotExist:
                context.update({
                    "total_price": 0.00,
                    "order": {},
                    "order_json":json.dumps({})
                })
        else:
            context.update({
                    "total_price": 0.00,
                    "order": {},
                    "order_json":json.dumps({})
                })

        return context



    def post(self, request):
        
        
        data = request.POST
        total_price = 0
        order = {}
        user = request.user


        if user.is_authenticated:

            cart, created = Cart.objects.get_or_create(user=user)
            for name, quantity in data.items():
                if name == 'csrfmiddlewaretoken':
                    continue
                product = Products.objects.filter(product_name = name).first()
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                cart_item.quantity = int(quantity)
                cart_item.save()
                order[product.product_id] = {'name':product.product_name,
                                            'price':product.get_display_price(),
                                            'quantity':quantity}

                total_price += (float(product.get_display_price()) * int(quantity))
            order_json = json.dumps(order)

            context = super(ProductLandingPageView, self).get_context_data()
            context.update({
                "total_price": total_price,
                "order": order,
                "order_json":order_json,
                "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
            })
            # Render the template with the updated context
            return self.render_to_response(context)
        else:
            messages.error(request, "Please Sign In")
            return redirect('home')


stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"


class BuyCookiesView(TemplateView):
    template_name = "buy_cookies.html"


    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        


        
        # Retrieve the product data from the Product model
        products = Products.objects.all()  # You may want to filter the products as needed
        context = {}
        context['products'] = products

        if(self.request.user.is_authenticated):
            user = User.objects.filter(email=self.request.user.email)
            context['loggedInUser'] = user

          # Add the products and logged-in user's points to the context
        return context


class CreateCheckoutSessionView(View):

    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get('jwt')
        user = request.user
        print(f'\n\n\n{user.email}\n\n\n')
        req_json = json.loads(request.body)
        order = json.loads(req_json['order_json'])
        line_items = []
        for product_id, detail in order.items():
            product = Products.objects.get(product_id=product_id)
            item = {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': product.price,
                        'product_data': {
                            'name': product.product_name,
                            'description': product.product_description,
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': detail['quantity'],
                }
            line_items.append(item)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items= line_items,
            metadata={
                "product_id": product.product_id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )

        for product_id, detail in order.items():
            product = Products.objects.get(product_id=product_id)
            amount = float(product.get_display_price()) * int(detail['quantity'])
            user_payment = UserPayment.objects.create(user=user, product=product, amount=amount, date=timezone.now())

            # user_payment.user.add(user)
            #
        cart = Cart.objects.get(user=user)

        for item in cart.cartitem_set.all():
            product = item.product

            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.delete()


        return JsonResponse({
            'id': checkout_session.id
        })


def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    print(event)
    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_email = session["customer_details"]["email"]
        product_id = session["metadata"]["product_id"]

        product = Products.objects.get(id=product_id)

        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. Here is the product you ordered. The product description is {product.product_description}",
            recipient_list=[customer_email],
            from_email="ali.mokhtaary@gmail.com"
        )

        # TODO - decide whether you want to send the file or the URL

    elif event["type"] == "payment_intent.succeeded":
        intent = event['data']['object']

        stripe_customer_id = intent["customer"]
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)

        customer_email = stripe_customer['email']
        product_id = intent["metadata"]["product_id"]

        product = Products.objects.get(id=product_id)

        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. Here is the product you ordered. The product description is {product.product_description}",
            recipient_list=[customer_email],
            from_email="matt@test.com"
        )

    return HttpResponse(status=200)


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:

            print(200*'+')
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json['email'])
            product_ids = req_json['product_ids']
            print(product_ids)
            product_id = self.kwargs["pk"]
            product = Products.objects.get(product_id=product_id)
            intent = stripe.PaymentIntent.create(
                amount=product.price,
                currency='usd',
                customer=customer['id'],
                metadata={
                    "product_id": product.product_id
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret'],
                'success': True
            })
        except Exception as e:
            return JsonResponse({ 'error': str(e) })


class CommunityView(generic.ListView):

    def get(self, request):
        return render(request, 'community.html')
    

class QRCodeView(generic.ListView):

    def get(self, request):
        return render(request, 'QRCode.html')
    

class getFreeCookies(View):

    def post(self, request):
        user = request.user

        if user.points >= 100:
            
            user.points -= 100
            user.save()

        return render(request, "cookies.html")
    

class getPointsForCookies(View):

    def post(self, request):
        user = request.user
        req_json = json.loads(request.body)
        totalPriceForPoints = json.loads(req_json['totalPrice'])

        user.points += totalPriceForPoints * 10
        user.save()
    
        return redirect('home')


def cookies_view(request):
    products = stripe.Product.objects.all()
    return render(request, 'buy_cookies.html', {'products': products})


