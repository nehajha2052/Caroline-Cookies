from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from .models import User, Purchases, Products, ProductReviews, UserPayment, Cart, CartItem




class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login', )}),
    )

    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )


# Register your models here.


admin.site.register(User)
admin.site.register(Purchases)
admin.site.register(Products)
admin.site.register(ProductReviews)
admin.site.register(UserPayment)
admin.site.register(CartItem)
admin.site.register(Cart)



