# Create your views here.
# from tradesys.models import Symbol
from django import forms
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required

from django.views.generic.edit import CreateView,UpdateView
from django.views.generic import ListView,DetailView

from tradesys.forms import MarketOverViewForm,PlanResultForm
from tradesys.forms import FirstSelectFormset

from tradesys.models import MarketDetailInfo,TradePlanModel,TradePlanAction
from tradesys.models import MarketOverView

from tradesys.forms import MarketStrengthSelected,MovDetailInlineFormset
from tradesys.forms import TradePlanInitForm,MarketOverViewForm,MdvDetailInlineFormset
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

def market_overview_init(tradetype,tradeframe):
    now    = timezone.now()
    mov = MarketOverView(market_result = "", pub_date = now)
    mov.save()
    
    for tf in trade_frame_map(tradeframe):
        mdi = MarketDetailInfo(symbol_name = tradetype,
                               timeframe   = tf ,
                               obj_dir     = 'N',
                               sub_dir     = 'N',
                               market_overview = mov)

        mdi.save()
    return mov


def diff_overview_init(tradetype,tradeframe,diff_flag):
    now    = timezone.now()
    mov = MarketOverView(market_result = "", pub_date = now)
    mov.save()

    symbols = ['EURUSD','GBPUSD','CHFUSD','AUDUSD','CADUSD','JPYUSD']
    tf = trade_frame_map(tradeframe)
    
    for symbol in symbols:
        if diff_flag == 'b':
            tfm = tf[1]
        if diff_flag == 's':
            tfm = tf[0]
            
        mdi = MarketDetailInfo(symbol_name = symbol,
                               timeframe   = tfm ,
                               obj_dir     = 'N' ,
                               sub_dir     = 'N' ,
                               market_overview = mov)

        mdi.save()
    return mov

def selected_overview_init(tradetype,tradeframe,diff_s_overview):

    try:
        selected = MarketDetailInfo.objects.filter(market_overview = diff_s_overview,
                                        exclude_reason = 'N')
    except MarketDetailInfo.DoesNotExist:
        return False

    tfm = trade_frame_map(tradeframe)
    
    for mdi in selected:
        for tf in tfm:
            if mdi.timeframe == tf:
                continue
            mdi_new=MarketDetailInfo(symbol_name = mdi.symbol_name,
                             timeframe = tf,
                             market_overview = diff_s_overview,
                             obj_dir = 'N',
                             sub_dir = 'N')
            mdi_new.save()
            
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
            self.object.market_overview = market_overview_init(tt,tf)
            self.object.save()
        else:
            self.object = ltp[0]

        self.request.session['TradePlanModel_id'] = self.object.id
        return redirect(self.success_url)

        
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


def market_over_view(request,tp_id=None):

    if tp_id == None:
        tp_id = request.session['TradePlanModel_id']

    tp_obj = TradePlanModel.objects.get(pk = tp_id)
    
    if request.method == "POST":
        md_formset = MovDetailInlineFormset(request.POST,
                                            request.FILES,
                                            instance = tp_obj.market_overview)
        mov_form   = MarketOverViewForm(request.POST,instance = tp_obj.market_overview)
        plan_res_form  = PlanResultForm(request.POST,instance = tp_obj)
        if md_formset.is_valid():
            md_formset.save()
            mov_form.save()
            plan_res_form.save()
            if tp_obj.diff_b_overview is None:
                tp_obj.diff_b_overview = diff_overview_init(tp_obj.tradetype,
                                                            tp_obj.tradeframe,
                                                            'b')
            if tp_obj.diff_s_overview is None:            
                tp_obj.diff_s_overview = diff_overview_init(tp_obj.tradetype,
                                                            tp_obj.tradeframe,
                                                            's')
            tp_obj.save()
            return redirect('/tradesys/MyTradePlan/market_diff_view')
    else:
        md_formset = MovDetailInlineFormset(instance = tp_obj.market_overview)
        mov_form   = MarketOverViewForm(instance = tp_obj.market_overview)
        plan_res_form  = PlanResultForm(instance = tp_obj)
        
    return render_to_response("tradesys/MarketOverView.html", {
            "tradetype" : tp_obj.tradetype,
            "md_formset" : md_formset.as_ul(),
            "mov_form" : mov_form.as_ul(),
            "plan_res_result" : plan_res_form.as_ul()
            },context_instance=RequestContext(request))


def market_diff_view(request,tp_id = None):
    
    if tp_id == None:
        tp_id = request.session['TradePlanModel_id']
    
    tp_obj = TradePlanModel.objects.get(pk = tp_id)
    if request.method == "POST":
        b_diffview  = MdvDetailInlineFormset(request.POST,
                                             prefix = 'b',
                                             instance = tp_obj.diff_b_overview)
        mov_b_form  = MarketOverViewForm(request.POST,
                                         prefix = 'b',
                                         instance = tp_obj.diff_b_overview)
        
        s_diffview = MdvDetailInlineFormset(request.POST,
                                            prefix = 's',
                                            instance = tp_obj.diff_s_overview)
        mov_s_form  = MarketOverViewForm(request.POST,
                                         prefix = 's',
                                         instance = tp_obj.diff_s_overview)

        if b_diffview.is_valid():
            print '.' * 80
            b_diffview.save()

        if mov_b_form.is_valid():
            print '.' * 80
            mov_b_form.save()

        if s_diffview.is_valid():
            print '.' * 80
            s_diffview.save()

        if mov_s_form.is_valid():
            print '.' * 80
            mov_s_form.save()

        return redirect('/tradesys/MyTradePlan/first_select_view')
    
    else:
        b_diffview =  MdvDetailInlineFormset(prefix='b',instance = tp_obj.diff_b_overview)
        mov_b_form =  MarketOverViewForm(prefix = 'b',instance = tp_obj.diff_b_overview)
        s_diffview =  MdvDetailInlineFormset(prefix = 's',instance = tp_obj.diff_s_overview)
        mov_s_form =  MarketOverViewForm(prefix = 's',instance = tp_obj.diff_s_overview)


    return render_to_response("tradesys/MarketDiffView.html", {
            "tradetype"  : tp_obj.tradetype,
            "b_diffview" : b_diffview.as_ul(),
            "mov_b_form" : mov_b_form.as_ul(),
            "s_diffview" : s_diffview.as_ul(),
            "mov_s_form" : mov_s_form.as_ul(),
            },context_instance=RequestContext(request))


def first_select_view(request,tp_id = None):

    if tp_id == None:
        tp_id = request.session['TradePlanModel_id']


    tp_obj = TradePlanModel.objects.get(pk = tp_id)

    mdi_query_set =  MarketDetailInfo.objects.filter(market_overview = tp_obj.diff_s_overview,
                                                     timeframe = tp_obj.tradeframe)
    if request.method == "POST":
        first_select_view = FirstSelectFormset( request.POST,
                                                queryset = mdi_query_set )

        if first_select_view.is_valid():
            first_select_view.save()
            
        selected_overview_init(tp_obj.tradetype,
                               tp_obj.tradeframe,
                               tp_obj.diff_s_overview)

        return redirect('/tradesys/MyTradePlan/first_select_view')
    else:
        first_select_view = FirstSelectFormset( queryset = mdi_query_set )

    
    return render_to_response("tradesys/FirstSelectView.html", {
            "tradetype" :  tp_obj.tradetype,
            "first_select_view" : first_select_view.as_ul()
            },context_instance=RequestContext(request))


def analysis_selected_view(request, tp_id = None):
    
    if tp_id == None:
        tp_id = request.session['TradePlanModel_id']

    

tp_sum_view       = login_required(MyTradePlanView.as_view())
# market_over_view  = login_required(MarketOview.as_view())
# market_diff_view  = login_required(MarketDview.as_view())
# first_select_view = login_required(FirstSelectedView.as_view())
# select_view       = login_required(SelectedView.as_view())
