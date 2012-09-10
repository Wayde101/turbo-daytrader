# Create your views here.
# from tradesys.models import Symbol
from django import forms
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.views.generic import ListView

from tradesys.forms import MarketDirectForm

from tradesys.models import MarketDirect
from tradesys.models import TradePlanModel,TradePlanAction
from tradesys.models import TRADEFRAME
from tradesys.models import TradeFrame

from tradesys.forms import TradeFrameForm
from django.contrib.auth.models import User

class MyTradePlanView(ListView):
    # form_class    = TradeFrameForm
    model         = TradePlanAction
    template_name = "tradesys/TradePlanSumView.html"


    def get_context_data(self, **kwargs):
        context = super(MyTradePlanView, self).get_context_data(**kwargs)
        context['tradeframe'] = TradeFrameForm().as_ul()
        return context


# class TradePlanTest(ListView):

    
class TimeFrameMetrics(CreateView):
    form_class = MarketDirectForm
    model      = MarketDirect
    template_name = "tradesys/market_overview.html"
    success_url = "/"


# @login_required
# def tp_sum_view(request, *args, **kwargs):
    # latest_tp_list = TradePlanAction.objects.all().order_by('-tradeplan__begin_time')[:10]
    # return render_to_response('tradesys/TradePlanSumView.html', {
            # 'latest_tp_list': latest_tp_list})

create_view = login_required(TimeFrameMetrics.as_view())
tp_sum_view = login_required(MyTradePlanView.as_view())

