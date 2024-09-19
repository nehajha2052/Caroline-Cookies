from django.db import models
from django.conf import settings
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class CustomerUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('You have not provided a valid email')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=100)
    points = models.IntegerField(default=20)  # Default is twenty since we give users some points on signup

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomerUserManager()

    USERNAME_FIELD: str = 'email'
    EMAIL_FIELD: str = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'project_user'

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.last_name


# Purchases table
class Purchases(models.Model):
    purchase_id = models.IntegerField(primary_key=True)
    purchase_date = models.DateTimeField(default=timezone.now)
    purchase_amount = models.IntegerField(default=0)

    class Meta:
        db_table = 'purchases'


# Products table
class Products(models.Model):
    class Meta:
        db_table = 'products'
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to='CookiePhotos/')
    product_description = models.CharField(max_length=500)
    price = models.IntegerField(default=0)

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)


# Product Reviews table
class ProductReviews(models.Model):
    review_id = models.CharField(max_length=8, primary_key=True)
    product_id = models.IntegerField(default=0)
    review_text = models.CharField(max_length=500)
    review_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'product_reviews'


class Coupons(models.Model):
    coupon_id = models.CharField(primary_key=True, max_length=2)
    coupon_discount_price = models.IntegerField(default=0)
    class Meta:
        db_table = 'coupons'


class UserCoupons(models.Model):
    userCoupon_id = coupon_id = models.CharField(primary_key=True, max_length=8)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon_id = models.ForeignKey(Coupons, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_coupons'


class UserPayment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    amount = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'User Payment'
        verbose_name_plural = 'User Payments'
        db_table = 'userpayment'

    def __repr__(self) -> str:
        return super().__repr__()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Products, through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart_item'
