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
from django.utils import timezone

def trade_frame_map(tradeframe):
    if tradeframe == '5M':
        return ['5M','15M','1H','4H','1D']
    if tradeframe == '1H':
        return ['1H','4H','1D','1W','1Mon']

class MyTradePlanView(ListView):
    model         = TradePlanAction
    template_name = "tradesys/MyTradePlanView.html"

    def get_context_data(self, **kwargs):
        context = super(MyTradePlanView, self).get_context_data(**kwargs)
        context['tradeinfo'] = TradeInfoForm().as_ul()
        return context


def lag_time(tradeframe):
    if tradeframe == '1H':
        return 60 * 60 * 4 * 4
    if tradeframe == '5M':
        return 60 * 5  * 3 * 4
    
class MarketOverView(CreateView):
    # form_class = MarketDirectForm
    model = TradePlanModel
    template_name = "tradesys/MarketOverView.html"

    def get_initial(self):
        initial = super(MarketOverView, self).get_initial()
        initial = initial.copy()
        initial['trader']     = self.request.user
        initial['tradetype']  = self.request.POST.get('tradetype')
        initial['tradeframe'] = self.request.POST.get('tradeframe')
        
        latest_tradeplan = TradePlanModel.objects.filter(tradeframe=initial['tradeframe'],tradetype=initial['tradetype']).order_by('-begin_time')[:1]

        lag = (timezone.now() - latest_tradeplan[0].begin_time).total_seconds()
        if len(latest_tradeplan) == 0 or  lag > lag_time(initial['tradeframe']):
            p = TradePlanModel(begin_time = timezone.now(),
                               completion = 1,
                               created_by = initial['trader'],
                               tradeframe = initial['tradeframe'],
                               tradetype  = initial['tradetype'])
            p.save()

        
        return initial
        
    def get_context_data(self, **kwargs):
        context = super(MarketOverView, self).get_context_data(**kwargs)
        print self.initial
        context['tradeframe'] = self.request.POST.get('tradeframe')
        context['tradetype']  = self.request.POST.get('tradetype')
        context['market_over_view']   = MarketOverViewForm('USDX',trade_frame_map(context['tradeframe'])).as_ul()
        return context

market_over_view = login_required(MarketOverView.as_view())
tp_sum_view = login_required(MyTradePlanView.as_view())

