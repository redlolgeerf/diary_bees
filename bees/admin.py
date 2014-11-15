from django.contrib import admin
from bees.models import DUser, History, AuthorisationRequest


class HistoryInline(admin.TabularInline):
    model = History
    extra = 3


class DUserAdmin(admin.ModelAdmin):
    inlines = [HistoryInline]

admin.site.register(DUser, DUserAdmin)
admin.site.register(History)
admin.site.register(AuthorisationRequest)
