from django.contrib import admin

from .models import Family, Kid, Parent


class FamilyAdmin(admin.ModelAdmin):
    pass


class ParentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('family', 'user', 'first_name', 'last_name',)
        }),
    )


class KidAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('family', 'user', 'name', 'avatar',)
        }),
    )


admin.site.register(Family, FamilyAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(Kid, KidAdmin)
