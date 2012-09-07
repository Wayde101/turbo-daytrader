# Create your views here.
from django.shortcuts import render_to_response

# from tradesys.models import Symbol
from tradesys.forms import MarketDirectForm
from django import forms
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.views.generic import ListView

from tradesys.models import MarketDirect
from tradesys.models import TradePlanModel,TradePlanAction
from tradesys.models import TRADEFRAME
from tradesys.models import TradeFrame

from tradesys.forms import TradeFrameForm

class TradePlanSumView(ListView):
    form_class    = TradeFrameForm
    model         = TradePlanAction
    template_name = "tradesys/TradePlanSumView.html"
    sucess_url = "/"



class TimeFrameMetrics(CreateView):
    form_class = MarketDirectForm
    model      = MarketDirect
    template_name = "tradesys/market_overview.html"
    success_url = "/"
    

create_view = TimeFrameMetrics.as_view()
tp_sum_view = TradePlanSumView.as_view()

