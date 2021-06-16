from django.contrib import admin


from .models import Book, OrderBook, Order, UserProfile, Category, SlidShow, Payment, Coupon, Refund, Address,IPAddress


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'shipping_address',
                    'billing_address',
                    'payment',
                    'coupon',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted'
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        'billing_address',
        'payment',
        'coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'address_type',
        'zip_code',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip_code']


admin.site.register(Book)
admin.site.register(OrderBook)
admin.site.register(Order, OrderAdmin)
admin.site.register(SlidShow)
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(IPAddress)

admin.site.register(Address, AddressAdmin)
