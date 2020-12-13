from django.db import models

STATUS = (  ('open', 'Open'),
            ('verified', 'Verified'),
            ('dispatched', 'Dispatched'),
            ('delivered', 'Delivered'),
        )

class PurchaseModel(models.Model):
    purchaser_name = models.CharField(max_length=30)
    quantity = models.IntegerField()


class PurchaseStatusModel(models.Model):
    purchase = models.ForeignKey(PurchaseModel, related_name="purchaseModel")
    status = models.CharField(max_length=25, choices=STATUS, default='open')
    created_at = models.DateTimeField(auto_now_add=True)