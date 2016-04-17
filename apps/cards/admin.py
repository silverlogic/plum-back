from django.contrib import admin

from .models import Card, Rule, Transfer


class CardAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('owner_id', 'owner_type', 'name_on_card', 'number',
                       'expiration_date', 'type', 'subtype',)
        }),
    )


class RuleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('card', 'type', 'merchant_type',)
        }),
    )


class TransferAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('to_card', 'from_card', 'amount')
        }),
    )


admin.site.register(Card, CardAdmin)
admin.site.register(Rule, RuleAdmin)
admin.site.register(Transfer, TransferAdmin)
