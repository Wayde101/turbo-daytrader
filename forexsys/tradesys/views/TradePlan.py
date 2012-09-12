# Create your views here.
# from tradesys.models import Symbol
from django import forms
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.views.generic import ListView,DetailView

from tradesys.forms import MarketDirectForm,MarketOverViewForm
# from tradesys.forms import MarketDirectForm

from tradesys.models import MarketDirect
from tradesys.models import TradePlanModel,TradePlanAction

from tradesys.forms import TradeInfoForm
from django.contrib.auth.models import User

class MyTradePlanView(ListView):
    model         = TradePlanAction
    template_name = "tradesys/MyTradePlanView.html"

    def get_context_data(self, **kwargs):
        context = super(MyTradePlanView, self).get_context_data(**kwargs)
        context['tradeinfo'] = TradeInfoForm().as_ul()
        return context

    
class MarketOverView(CreateView):
    # form_class = MarketOverViewForm
    model = TradePlanModel
    template_name = "tradesys/MarketOverView.html"


    def get_initial(self):
        initial = super(MarketOverView, self).get_initial()
        initial['tradeframe']=self.request.POST.get('tradeframe')
        initial['tradetype'] =self.request.POST.get('tradetype')
        return initial
        
    def get_context_data(self, **kwargs):
        context = super(MarketOverView, self).get_context_data(**kwargs)
        context['tradeframe'] = self.initial['tradeframe']
        context['tradetype']  = self.initial['tradetype']
        context['market_over_view']   = MarketOverViewForm().as_ul()
        return context


# @login_required
# def tp_sum_view(request, *args, **kwargs):
    # latest_tp_list = TradePlanAction.objects.all().order_by('-tradeplan__begin_time')[:10]
    # return render_to_response('tradesys/TradePlanSumView.html', {
            # 'latest_tp_list': latest_tp_list})

create_view = login_required(MarketOverView.as_view())
tp_sum_view = login_required(MyTradePlanView.as_view())

