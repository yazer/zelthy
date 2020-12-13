from datetime import datetime
import calendar

from django.shortcuts import render
from django.views import generic
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from . models import PurchaseStatusModel, PurchaseModel


class Dashboard(generic.TemplateView):
    model = PurchaseModel
    template_name = 'purchase/dashboard.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        queryset = self.model.objects.all()
        queryset_ids = get_filtered_list(queryset)
        queryset = PurchaseStatusModel.objects.filter(id__in=queryset_ids)
        context['object_list'] = queryset.annotate(month=TruncMonth('created_at') 
                                ).values('month').annotate(cnt=Count('id')).values('month', 'cnt')
        month_count = [0 for i in range(0, 12)]
        for i in context['object_list']:
            month_count[i['month'].month - 1] = i['cnt']
        context['month_data'] = month_count
        return context


def get_filtered_list(queryset, year=None):
    if not year:
        year = datetime.now().year
    temp_list = []
    for each in queryset:
        if each.purchaseModel.latest('id').status == 'dispatched' and \
            each.purchaseModel.latest('id').created_at.year == year:
            temp_list.append(each.purchaseModel.latest('id').id)
        elif each.purchaseModel.latest('id').status == 'delivered' and \
            each.purchaseModel.filter(status='dispatched').exists() and \
            each.purchaseModel.filter(status='dispatched')[0].created_at.year == year:
            temp_list.append(each.purchaseModel.filter(status='dispatched')[0].id)
        elif each.purchaseModel.latest('id').status == 'delivered' and \
            not each.purchaseModel.filter(status='dispatched').exists() and \
            each.purchaseModel.filter(status='delivered')[0].created_at.year == year:
            temp_list.append(each.purchaseModel.filter(status='delivered')[0].id)
    return temp_list


@method_decorator(csrf_exempt, name='dispatch')
class UpdatePurchaseChart(generic.View):
    """ Update FE Bar chart using year filter"""

    model = PurchaseModel

    def post(self, *args, **kwargs):
        filter_year = self.request.POST.get('year')
        if filter_year:filter_year=int(filter_year)
        queryset = self.model.objects.all()
        queryset_ids = get_filtered_list(queryset, filter_year)
        queryset = PurchaseStatusModel.objects.filter(id__in=queryset_ids)
        queryset = queryset.annotate(month=TruncMonth('created_at') 
                                ).values('month').annotate(cnt=Count('id')).values('month', 'cnt')
        month_count = [0 for i in range(0, 12)]
        for i in queryset:
            month_count[i['month'].month - 1] = i['cnt']
        month_data = month_count
        return_dict = {"code": 1, "msg": "", "response": {"month_data": month_data}}
        return JsonResponse(return_dict)