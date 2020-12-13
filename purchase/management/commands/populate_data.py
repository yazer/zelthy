
import random
from django.core.management.base import BaseCommand

from purchase.models import PurchaseStatusModel, PurchaseModel


class Command(BaseCommand):
    help = 'To populate models'

    def handle(self, *args, **kwargs):
        purchase_name_list = ['Micheal Jackson', 'Ricky Martin', 'Shakira', 'Bob Marley', \
                            'Adraine Grande', 'Adele', 'John Denver', 'Bruno Mars', \
                            'Pharrel Williams', 'Calvin Harris']
        for each in range(0, 5000):
            purchase_name_to_add = random.choice(purchase_name_list)
            status = True
            while True:
                quantity = randint(0, 11)
                if not PurchaseModel.objects.all().aggregate(Avg('quantity')) > 7:
                    for i in purchase_name_list:
                        if PurchaseModel.objects.filter(purchaser_name=purchase_name_list[i]).aggregate(Avg('quantity')) == \
                           PurchaseModel.objects.filter(purchaser_name=purchase_name_to_add).aggregate(Avg('quantity')):
                            status = False
                    if status:
                        break

            if PurchaseModel.objects.filter(purchaser_name=purchase_name_to_add).exists():
                pus_obj = PurchaseModel.objects.filter(purchaser_name=purchase_name_to_add)
                for each in pus_obj:
                    status_list = [st.status for st in each.purchaseModel.all()]
                    remaining_status = set(status_list) - set('open', 'verified', 'dispatched', \
                                        'delivered') 
                    if remaining_status:
                        status_to_add = remaining_status[0]
                    else:
                        status_to_add = 'open'
            purchase_ob = PurchaseModel.objects.create(purchaser_name=purchase_name_to_add, quantity=quantity)
            # Date creation TO DO
            PurchaseStatusModel.objects.create(purchase=purchase_ob, status=status_to_add)