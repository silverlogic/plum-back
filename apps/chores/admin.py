from django.contrib import admin

from .models import Chore


class ChoreAdmin(admin.ModelAdmin):
    fields = ('kid', 'name', 'points', 'status',)


admin.site.register(Chore, ChoreAdmin)
