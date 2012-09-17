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
from tradesys.models import Symbol,TradeFrame,TimeFrame,MarketOverView

from tradesys.forms import TradeInfoForm
from django.contrib.auth.models import User
from django.utils import timezone
import re

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
    
class MarketOview(CreateView):
    # form_class = MarketDirectForm
    model = TradePlanModel
    template_name = "tradesys/MarketOverView.html"

    def get_initial(self):
        initial = super(MarketOview, self).get_initial()
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
            market_info_list = ['%s_%s_%s' % (x,y,z) for x in [self.request.session['tradetype']] for y in ['obj_dir','sub_dir','normative'] for z in trade_frame_map(self.request.session['tradeframe'])]
            
            self.request.session['TradePlanModel_id'] = latest_tradeplan[0].id
            
            if latest_tradeplan[0].market_overview is None:
                for market_info in market_info_list:
                    self.request.session[market_info] = 'N/A'
            else:
                for zk in ['obj_dir','sub_dir','normative']:
                    for tm in trade_frame_map(self.request.session['tradeframe']):
                        market_info = '%s_%s_%s' % (self.request.session['tradetype'],zk,tm)
                        sym_obj     = Symbol.objects.get(symbol_name = self.request.session['tradetype'])
                        tf_obj      = TimeFrame.objects.get(timeframe = tm)
                        if zk == 'obj_dir':
                            try:
                                self.request.session[market_info] = MarketDirect.objects.get(symbol_name = sym_obj,
                                                                                             timeframe   = tf_obj,
                                                                                             market_overview = latest_tradeplan[0].market_overview).obj_dir
                            except MarketDirect.DoesNotExist:
                                self.request.session[market_info] = 'N/A'
                        if zk == 'sub_dir':
                            try:
                                self.request.session[market_info] = MarketDirect.objects.get(market_overview = latest_tradeplan[0].market_overview).sub_dir
                            except MarketDirect.DoesNotExist:
                                self.request.session[market_info] = 'N/A'
            
        return initial
        
    def get_context_data(self, **kwargs):
        context = super(MarketOview, self).get_context_data(**kwargs)
        # print self.request.session.keys()
        context['tradeframe'] = self.request.POST.get('tradeframe')
        context['tradetype']  = self.request.POST.get('tradetype')
        context['market_over_view']   = MarketOverViewForm(self.request.session['tradetype'],
                                                           trade_frame_map(context['tradeframe'])).as_ul()
        return context


def save_marketdirect(request):
    dir_list = filter(lambda x: re.search('_dir_',x), request.POST.keys())
    tp = TradePlanModel.objects.get(id = request.session['TradePlanModel_id'])
    if tp.market_overview  is None:
        mov_obj = MarketOverView(market_result = request.POST['market_result'],
                                 pub_date = timezone.now())

        mov_obj.save()
        tp.market_overview = mov_obj
        tp.save()
        
        
    for each_tf in dir_list:
        tf_item = each_tf.split('_')
        sym_object = Symbol.objects.get(symbol_name = tf_item[0])
        tf_object  = TimeFrame.objects.get(timeframe = tf_item[3])

        try:
            md = MarketDirect.objects.get(symbol_name = sym_object,timeframe = tf_object,market_overview = tp.market_overview)
        except MarketDirect.DoesNotExist:
            if tf_item[1]  == 'obj':
                md = MarketDirect(symbol_name = sym_object,
                                  timeframe   = tf_object,
                                  obj_dir     = request.POST[each_tf],
                                  normative   = request.POST['%s_normative_%s' % (tf_item[0],tf_item[3])],
                                  market_overview = tp.market_overview
                                  )
            if tf_item[1]  == 'sub':
                md = MarketDirect(symbol_name = sym_object,
                                  timeframe   = tf_object,
                                  sub_dir     = request.POST[each_tf],
                                  normative   = request.POST['%s_normative_%s' % (tf_item[0],tf_item[3])],
                                  market_overview = tp.market_overview
                                  )

                md.save()
                continue


        if tf_item[1]  == 'sub':
            md.sub_dir = request.POST[each_tf]
        if tf_item[1]  == 'obj':
            md.obj_dir = request.POST[each_tf]

        md.normative = request.POST['%s_normative_%s' % (tf_item[0],tf_item[3])]
        md.save()


class MarketDview(CreateView):
    model = TradePlanModel
    template_name = "tradesys/MarketDiffView.html"

    def get_initial(self):
        initial = super(MarketDview, self).get_initial()
        initial = initial.copy()

        save_marketdirect(self.request)
        # market_overview_symbol = 
        print 'x' * 80
        print Symbol(symbol_name=self.request.session['tradetype'])
        print self.request.POST.keys()
        print 'x' * 80
        return initial

    def get_context_data(self, **kwargs):
        context = super(MarketDview, self).get_context_data(**kwargs)
        context['tradeframe'] = self.request.session['tradeframe']
        symbols = ['EURUSD','GBPUSD','CHFUSD','AUDUSD','CADUSD','JPYUSD']
        context['market_diff_view'] = MarketDiffViewForm(symbols,trade_frame_map(context['tradeframe'])).as_ul()
        return context

    
tp_sum_view      = login_required(MyTradePlanView.as_view())
market_over_view = login_required(MarketOview.as_view())
market_diff_view = login_required(MarketDview.as_view())


