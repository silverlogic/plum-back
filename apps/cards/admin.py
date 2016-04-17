from django.contrib import admin


class CreditCardAdmin(admin.ModelAdmin):
    fieldset = (
        (None, {
            'fields': ('owner_id', 'owner_type', 'name_on_card', 'number',
                       'expiration_date', 'type', 'subtype',)
        }),
    )
