# Create your views here.
# from tradesys.models import Symbol
from django import forms
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from django.views.generic.edit import CreateView,UpdateView
from django.views.generic import ListView,DetailView

from tradesys.forms import MarketDirectForm,MarketOverViewForm,MarketDiffViewForm
# from tradesys.forms import MarketDirectForm

from tradesys.models import MarketDirect,TradePlanModel,TradePlanAction
from tradesys.models import Symbol,TradeFrame,TimeFrame

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


def tradeplan_lag_time(tradeframe):
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
        self.request.session['tradetype']  = self.request.POST.get('tradetype')
        self.request.session['tradeframe'] = self.request.POST.get('tradeframe')
        
        latest_tradeplan = TradePlanModel.objects.filter(tradeframe = self.request.session['tradeframe'],tradetype = self.request.session['tradetype'],created_by = self.request.user).order_by('-begin_time')[:1]

        if len(latest_tradeplan) == 0 or  (timezone.now() - latest_tradeplan[0].begin_time).total_seconds() > tradeplan_lag_time(self.request.session['tradeframe']):
            p = TradePlanModel(begin_time = timezone.now(),
                               completion = 1,
                               created_by = self.request.user,
                               tradeframe = self.request.session['tradeframe'],
                               tradetype  = self.request.session['tradetype'])
            p.save()
            self.request.session['TradePlanModel_id'] = p.id
        else:
            market_info_list = ['%s_%s_%s' % (x,y,z) for x in [self.request.session['tradetype']] for y in ['obj_dir','sub_dir'] for z in trade_frame_map(self.request.session['tradeframe'])]
            
            self.request.session['TradePlanModel_id'] = latest_tradeplan[0].id
            
            if latest_tradeplan[0].market_overview is None:
                for market_info in market_info_list:
                    self.request.session[market_info] = 'N/A'
            else:
                for zk in ['obj_dir','sub_dir']:
                    for tm in trade_frame_map(context['tradeframe']):
                        market_info = '%s_%s_%s' % (self.request.session['tradetype'],zk,tm)
                        if zk == 'obj_dir':
                            self.request.session[market_info] = p.market_overview.obj_dir
                        if zk == 'sub_dir':
                            self.request.session[market_info] = p.market_overview.sub_dir
            
        return initial
        
    def get_context_data(self, **kwargs):
        context = super(MarketOverView, self).get_context_data(**kwargs)
        # print self.request.session.keys()
        context['tradeframe'] = self.request.POST.get('tradeframe')
        context['tradetype']  = self.request.POST.get('tradetype')
        context['market_over_view']   = MarketOverViewForm(self.request.session['tradetype'],
                                                           trade_frame_map(context['tradeframe'])).as_ul()
        return context

class MarketDiffView(CreateView):
    model = TradePlanModel
    template_name = "tradesys/MarketDiffView.html"

    def get_initial(self):
        initial = super(MarketDiffView, self).get_initial()
        initial = initial.copy()

        market_overview_symbol = Symbol(symbol_name=self.request.session['tradetype'])
        # MarketDirect(symbol_name = models)

        tradeplan = TradePlanModel(id = self.request.session['TradePlanModel_id'])
        marketoverview = 


        tp = TradePlanModel.objects.get(created_by = self.request.user,
                                        id = self.request.session['TradePlanModel_id'])

        tp
            

        return initial

    def get_context_data(self, **kwargs):
        context = super(MarketDiffView, self).get_context_data(**kwargs)
        context['tradeframe'] = self.request.session['tradeframe']
        symbols = ['EURUSD','GBPUSD','CHFUSD','AUDUSD','CADUSD','JPYUSD']
        context['market_diff_view'] = MarketDiffViewForm(symbols,trade_frame_map(context['tradeframe'])).as_ul()
        return context

    
tp_sum_view      = login_required(MyTradePlanView.as_view())
market_over_view = login_required(MarketOverView.as_view())
market_diff_view = login_required(MarketDiffView.as_view())


