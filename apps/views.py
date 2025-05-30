from django.db.models import Sum, Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, View, UpdateView, DeleteView

from apps.forms import DebtModelFormCreate, DebtModelFormUpdate
from apps.models import DebtBook


# ============================================Debt book===========================
class DebtListView(ListView):
    queryset = DebtBook.objects.all()
    template_name = 'project/debt.html'
    context_object_name = 'debts'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['total_debt'] = DebtBook.objects.aggregate(Sum('debt')).get('debt__sum', 0)
        data['paid_count'] = DebtBook.objects.filter(status='tolandi').aggregate(Count('status')).get('status__count',
                                                                                                      0)
        data['unpaid_count'] = DebtBook.objects.filter(status='tolanmagan').aggregate(Count('status')).get(
            'status__count', 0)
        data['total_debtors'] = DebtBook.objects.aggregate(Count('id')).get('id__count', 0)
        return data


class DebtCreatView(CreateView):
    queryset = DebtBook.objects.all()
    form_class = DebtModelFormCreate
    template_name = 'project/debt.html'
    success_url = reverse_lazy('debt')


class DebtUpdateView(UpdateView):
    form_class = DebtModelFormUpdate
    queryset = DebtBook.objects.all()
    template_name = 'project/debt.html'
    success_url = reverse_lazy('debt')

class DebtDeleteView(DeleteView):
    queryset = DebtBook.objects.all()
    template_name = 'project/debt.html'
    success_url = reverse_lazy('debt')
    pk_url_kwarg = 'pk'


class DebtFinish(View):
    def post(self, request, pk):
        DebtBook.objects.filter(pk=pk).update(status=DebtBook.StatusType.COMPLETED)
        return redirect('debt')

