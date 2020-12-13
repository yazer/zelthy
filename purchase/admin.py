from django.contrib import admin

from . models import PurchaseModel, PurchaseStatusModel

admin.site.register(PurchaseModel)
admin.site.register(PurchaseStatusModel)