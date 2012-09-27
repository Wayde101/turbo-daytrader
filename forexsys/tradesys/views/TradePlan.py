# Create your views here.
# from tradesys.models import Symbol
from django import forms
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required

from django.views.generic.edit import CreateView,UpdateView
from django.views.generic import ListView,DetailView

from tradesys.forms import MarketDetailInfoForm,MarketOverViewForm,MarketDiffViewForm
# from tradesys.forms import MarketDetailInfoForm

from tradesys.models import MarketDetailInfo,TradePlanModel,TradePlanAction
from tradesys.models import MarketOverView

from tradesys.forms import MarketStrengthSelected
from tradesys.forms import TradePlanInitForm
from tradesys.forms import MarketExcludeSelected

from django.contrib.auth.models import User
from django.utils import timezone
import re

def trade_frame_map(tradeframe):
    if tradeframe == '5M':
        return ['5M','15M','1H','4H','1D']
    if tradeframe == '1H':
        return ['1H','4H','1D','1W','1Mon']

def tradeplan_lag_time(tradeframe):
    if tradeframe == '1H':
        return 60 * 60 * 4 * 4
    if tradeframe == '5M':
        return 60 * 5  * 3 * 4

    
class MyTradePlanView(CreateView):
    form_class    = TradePlanInitForm
    model         = TradePlanModel
    template_name = "tradesys/MyTradePlanView.html"
    success_url   = "/tradesys/MyTradePlan/market_over_view"

    def get_context_data(self, **kwargs):
        context = super(MyTradePlanView, self).get_context_data(**kwargs)
        context['tradeinfo'] = TradePlanInitForm().as_ul()
        return context

    def form_valid(self,form):
        if not form.is_valid():
            print "invalid from info"

        tt     =  form.cleaned_data['tradetype']
        tf     =  form.cleaned_data['tradeframe']
        user   =  self.request.user
        tp_obj =  self.model.objects
        now    = timezone.now()

        ltp = tp_obj.filter(tradeframe = tf,
                            tradetype =  tt,
                            created_by = user).order_by('-begin_time')[:1]

        lag_time = tradeplan_lag_time(tf)

        if len(ltp) == 0 or (now - ltp[0].begin_time).total_seconds() > lag_time:
            self.object = form.save(commit=False)
            self.object.begin_time = now
            self.object.completion = 1
            self.object.created_by = user
            self.object.save()
        else:
            self.object = ltp[0]

        self.request.session['TradePlanModel_id'] = self.object.id
        return redirect(self.success_url)

        
class MarketOview(CreateView):
    # form_class = MarketDetailInfoForm
    model = MarketDetailInfo
    template_name = "tradesys/MarketOverView.html"

    def get_initial(self):
        initial = super(MarketOview, self).get_initial()
        initial = initial.copy()

        # tp_obj = TradePlanModel
        
        # s_d_t_list = ['%s_%s_%s' % (s,d,t)
                      # for s in [self.request.session['tradetype']]
                      # for d in ['obj_dir','sub_dir']
                      # for t in trade_frame_map(self.request.session['tradeframe'])]

        

        
        return initial
        
    def get_context_data(self, **kwargs):
        context = super(MarketOview, self).get_context_data(**kwargs)
        # print self.request.session.keys()
        # context['tradeframe'] = self.request.POST.get('tradeframe')
        # context['tradetype']  = self.request.POST.get('tradetype')
        # context['market_over_view']   = MarketOverViewForm(self.request.session['tradetype'],
        # trade_frame_map(context['tradeframe'])).as_ul()
        context['market_over_view'] = MarketDetailInfoForm().as_ul
        return context


def save_market_overview(request):
    dir_list = filter(lambda x: re.search('_dir_',x), request.POST.keys())
    tp = TradePlanModel.objects.get(id = request.session['TradePlanModel_id'])
    tp.completion = 2
    if tp.market_overview  is None:
        mov_obj = MarketOverView(market_result = request.POST['market_result'],
                                 pub_date      = timezone.now())
        mov_obj.save()
        tp.market_overview = mov_obj
        tp.save()

    else:
        setattr(tp.market_overview,'market_result',request.POST['market_result'])
        tp.market_overview.save()
        setattr(tp,'plan_result',request.POST['plan_result'])
        tp.save()
        
    for each_tf in dir_list:
        tf_item = each_tf.split('_')
        symbol_name = tf_item[0]
        timeframe  = tf_item[3]

        try:
            md = MarketDetailInfo.objects.get(symbol_name = symbol_name,
                                              timeframe = timeframe,
                                              market_overview = tp.market_overview)
            
        except MarketDetailInfo.DoesNotExist:
            md = MarketDetailInfo()
            setattr(md,'symbol_name',symbol_name)
            setattr(md,'timeframe', timeframe)
            setattr(md,'%s_dir' % tf_item[1], request.POST[each_tf])
            setattr(md,'market_overview', tp.market_overview)
            md.save()
            continue

        setattr(md,'%s_dir' % tf_item[1] , request.POST[each_tf])
        md.save()


def save_market_diffview(request):
    dir_list = filter(lambda x: re.search('_dir_',x), request.POST.keys())
    tp = TradePlanModel.objects.get(id = request.session['TradePlanModel_id'])

    for x in ['b', 's']:
        result = 'diff_%s_result' % x
        diff_x_overview = 'diff_%s_overview' % x
        t = 1 if x == 'b' else 0
        
        timeframe = trade_frame_map(request.session['tradeframe'])[t]

        
        if getattr(tp,diff_x_overview) is None:
            mdv_obj = MarketOverView(market_result = request.POST[result],
                                     pub_date = timezone.now())        
            mdv_obj.save()
            setattr(tp,diff_x_overview,mdv_obj)
            tp.save()

        else:
            diff_x_overview_obj = getattr(tp,diff_x_overview)
            setattr(diff_x_overview_obj,'market_result',request.POST[result])
            

    for each_dir in dir_list:
        symbol,zk,x,timeframe = each_dir.split('_')
        
        if timeframe == trade_frame_map(request.session['tradeframe'])[1]:
            x = 'b'
            
        if timeframe == trade_frame_map(request.session['tradeframe'])[0]:
            x = 's'

        diff_x_overview_obj = getattr(tp,'diff_%s_overview' % x)
            
        try:
            md = MarketDetailInfo.objects.get(symbol_name = symbol,
                                              timeframe = timeframe,
                                              market_overview = diff_x_overview_obj)
        except MarketDetailInfo.DoesNotExist:
            md = MarketDetailInfo()
            setattr(md,'symbol_name',symbol)
            setattr(md,'timeframe',timeframe)
            setattr(md,'market_overview',diff_x_overview_obj)
            md.save()


        setattr(md,'%s_dir' % zk, request.POST[each_dir])
        setattr(md,'normative', request.POST['%s_normative_%s' % (symbol,timeframe)])

        if x == 's':
            setattr(md,'strength',request.POST['%s_strength_%s' % (symbol,timeframe)])
        md.save()


class MarketDview(CreateView):
    model = TradePlanModel
    template_name = "tradesys/MarketDiffView.html"

    def get_initial(self):
        initial = super(MarketDview, self).get_initial()
        initial = initial.copy()

        save_market_overview(self.request)
        return initial

    def get_context_data(self, **kwargs):
        context = super(MarketDview, self).get_context_data(**kwargs)
        context['tradeframe'] = self.request.session['tradeframe']
        # should be defind in models
        symbols = ['EURUSD','GBPUSD','CHFUSD','AUDUSD','CADUSD','JPYUSD']
        context['market_diff_view'] = MarketDiffViewForm(symbols,trade_frame_map(context['tradeframe'])).as_ul()
        return context

class FirstSelectedView(CreateView):
    model  = MarketDetailInfo
    template_name = 'tradesys/FirstSelectView.html'

    def get_initial(self):
        initial = super(FirstSelectedView, self).get_initial()
        initial = initial.copy()
        
        save_market_diffview(self.request)
        return initial

    def get_context_data(self, **kwargs):
        context = super(FirstSelectedView, self).get_context_data(**kwargs)

        tp_obj  = TradePlanModel.objects.get(id = self.request.session['TradePlanModel_id'])
        mdi_obj = MarketDetailInfo.objects.filter(market_overview = tp_obj.diff_s_overview.id)

        ss = dict([ (k.symbol_name,k.strength) for k in mdi_obj ])
        se = dict([ (k.symbol_name,k.exclude_reason) for k in mdi_obj ])
        tf = self.request.session['tradeframe']
        
        context['tradeframe'] = tf
        context['symbol_strength'] = MarketStrengthSelected(ss,tf).as_ul()
        context['symbol_excluded'] = MarketExcludeSelected(se,tf).as_ul()

        return context


tp_sum_view       = login_required(MyTradePlanView.as_view())
market_over_view  = login_required(MarketOview.as_view())
market_diff_view  = login_required(MarketDview.as_view())
first_select_view = login_required(FirstSelectedView.as_view())
# select_view       = login_required(SelectedView.as_view())
