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

class TradePlanSumView(ListView):
    # form_class    = TradeFrameForm
    model         = TradePlanAction
    template_name = "tradesys/TradePlanSumView.html"

class TradePlanTest(ListView):


class TimeFrameMetrics(CreateView):
    form_class = MarketDirectForm
    model      = MarketDirect
    template_name = "tradesys/market_overview.html"
    success_url = "/"
    

create_view = login_required(TimeFrameMetrics.as_view())
tp_sum_view = login_required(TradePlanSumView.as_view())

