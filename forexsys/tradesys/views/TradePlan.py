# -*- coding: utf-8 -*-
# -*- mode: python -*-
# Create your views here.
# from tradesys.models import Symbol
from django import forms
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils import timezone

from django.views.generic.edit import CreateView

from tradesys.models import MarketDetailInfo,TradePlanModel,TradePlanAction
from tradesys.models import MarketOverView,TradePlanAction

from tradesys.forms import MarketOverViewForm,PlanResultForm
from tradesys.forms import FirstSelectFormset,SelectedFormset
from tradesys.forms import MovDetailInlineFormset,TradePlanActionFormset
from tradesys.forms import TradePlanInitForm,MarketOverViewForm,MdvDetailInlineFormset
import re

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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


def diff_overview_init(tp_model,diff_flag):
    now    = timezone.now()
    mov = MarketOverView(market_result = "", pub_date = now)
    mov.save()

    tf = trade_frame_map(tp_model.tradeframe)
    
    # 目前实现上主要是处理 6 个非美货币的交易
    symbols = ['EURUSD','GBPUSD','CHFUSD','AUDUSD','CADUSD','JPYUSD']

    for symbol in symbols:
        if diff_flag == 'b':
            tfm = tf[1]
            mov = tp_model.diff_s_overview
        if diff_flag == 's':
            tfm = tf[0]

        mdi = MarketDetailInfo(symbol_name = symbol,
                               timeframe   = tfm ,
                               obj_dir     = 'N' ,
                               sub_dir     = 'N' ,
                               market_overview = mov)
        mdi.save()
    return mov

def selected_overview_init(tp_obj):
    try:
        selected = MarketDetailInfo.objects.filter(market_overview = tp_obj.diff_s_overview,
                                                   timeframe = tp_obj.tradeframe,
                                                   exclude_reason = 'N')
    except MarketDetailInfo.DoesNotExist:
        return False

    tfm = trade_frame_map(tp_obj.tradeframe)

    for mdi in selected:
        for tf in tfm:
            try:
                mdi_new = MarketDetailInfo.objects.get(symbol_name = mdi.symbol_name,
                                                       market_overview = tp_obj.diff_s_overview,
                                                       timeframe = tf)

            except MarketDetailInfo.DoesNotExist:
                mdi_new=MarketDetailInfo(symbol_name = mdi.symbol_name,
                                         timeframe   = tf,
                                         market_overview = tp_obj.diff_s_overview,
                                         obj_dir = 'N',
                                         sub_dir = 'N')
                mdi_new.save()

def get_selected_symbols(tradeframe,selected_overview):
    mdi = MarketDetailInfo.objects.filter(timeframe = tradeframe,
                                          exclude_reason = 'N',
                                          market_overview = selected_overview)

    if len(mdi) == 0:
        return None

    return [ '%s' % x.symbol_name for x in mdi ]


def tradeplan_action_init(tp_obj):
    
    selected = MarketDetailInfo.objects.filter(market_overview = tp_obj.diff_s_overview,
                                               timeframe = tp_obj.tradeframe,
                                               exclude_reason = 'N')

    exist_action = TradePlanAction.objects.filter(tradeplan = tp_obj)

    if len(exist_action) > 0:
        s = set(['%s' % x.symbol_name for x in selected ])
        e = set(['%s' % x.symbol_name for x in exist_action ])
        for sym in  e - s:
            del_tp = TradePlanAction.objects.get(tradeplan = tp_obj, symbol_name = sym)
            del_tp.delete()
        
    if len(selected) == 0:
        return False

    for mdi in selected:
        try:
            TradePlanAction.objects.get(symbol_name = mdi.symbol_name,
                                        tradeplan   = tp_obj)
        except TradePlanAction.DoesNotExist:
            plan_action_new=TradePlanAction(symbol_name = mdi.symbol_name,
                                            tradeplan   = tp_obj,
                                            enter_price = 0.0,
                                            sl_price    = 0.0,
                                            tp_price    = 0.0,
                                            holding_log = 'Init:')
            plan_action_new.save()

        
        
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

# 可能需要 用 login_required 修饰一下，确保登录使用
def market_over_view(request,tp_id=None):

    if tp_id == None:
        tp_id = request.session['TradePlanModel_id']

    tp_obj = TradePlanModel.objects.get(pk = tp_id)
    
    if request.method == "POST":
        movd_formset = MovDetailInlineFormset(request.POST,
                                            request.FILES,
                                            instance = tp_obj.market_overview)
        mov_form   = MarketOverViewForm(request.POST,instance = tp_obj.market_overview)
        plan_res_form  = PlanResultForm(request.POST,instance = tp_obj)
        if movd_formset.is_valid():
            movd_formset.save()
            mov_form.save()
            plan_res_form.save()
            if tp_obj.diff_s_overview is None:            
                tp_obj.diff_s_overview = diff_overview_init(tp_obj,'s')
                tp_obj.save()
            if tp_obj.diff_b_overview is None:
                tp_obj.diff_b_overview = diff_overview_init(tp_obj,'b')
                tp_obj.save()

            return redirect('/tradesys/MyTradePlan/market_diff_view')
    else:
        movd_formset = MovDetailInlineFormset(instance = tp_obj.market_overview)
        mov_form   = MarketOverViewForm(instance = tp_obj.market_overview)
        plan_res_form  = PlanResultForm(instance = tp_obj)
        
    return render_to_response("tradesys/MarketOverView.html", {
            "tradetype" : tp_obj.tradetype,
            "movd_formset" : movd_formset,
            "mov_form" : mov_form,
            "plan_res_result" : plan_res_form
            },context_instance=RequestContext(request))

# 可能需要 用 login_required 修饰一下，确保登录使用
def market_diff_view(request,tp_id = None):
    
    if tp_id == None:
        tp_id = request.session['TradePlanModel_id']
    
    tp_obj = TradePlanModel.objects.get(pk = tp_id)
    if request.method == "POST":
        s_diffview = MdvDetailInlineFormset(request.POST,
                                            prefix = 's',
                                            instance = tp_obj.diff_s_overview)

        mov_b_form  = MarketOverViewForm(request.POST,
                                         prefix = 'b',
                                         instance = tp_obj.diff_b_overview)

        mov_s_form  = MarketOverViewForm(request.POST,
                                         prefix = 's',
                                         instance = tp_obj.diff_s_overview)


        if s_diffview.is_valid():
            s_diffview.save()

        if mov_b_form.is_valid():
            mov_b_form.save()

        if mov_s_form.is_valid():
            mov_s_form.save()

        return redirect('/tradesys/MyTradePlan/first_select_view')
    
    else:
        s_diffview =  MdvDetailInlineFormset(prefix = 's',instance = tp_obj.diff_s_overview)
        mov_b_form =  MarketOverViewForm(prefix = 'b',instance = tp_obj.diff_b_overview)
        mov_s_form =  MarketOverViewForm(prefix = 's',instance = tp_obj.diff_s_overview)


    return render_to_response("tradesys/MarketDiffView.html", {
            "tradetype"  : tp_obj.tradetype,
            "s_diffview" : s_diffview,
            "mov_b_form" : mov_b_form.as_ul(),
            "mov_s_form" : mov_s_form.as_ul(),
            },context_instance=RequestContext(request))

# 可能需要 用 login_required 修饰一下，确保登录使用
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
            
        selected_overview_init(tp_obj)

        return redirect('/tradesys/MyTradePlan/analysis_selected_view')
    else:
        first_select_view = FirstSelectFormset( queryset = mdi_query_set )
    
    return render_to_response("tradesys/FirstSelectView.html", {
            "tradetype" :  tp_obj.tradetype,
            "first_select_view" : first_select_view.as_ul()
            },context_instance=RequestContext(request))

# 可能需要 用 login_required 修饰一下，确保登录使用
def analysis_selected_view(request, tp_id = None):
    
    if tp_id == None:
        tp_id = request.session['TradePlanModel_id']

    tp_obj  = TradePlanModel.objects.get(pk = tp_id)
    selected = get_selected_symbols(tp_obj.tradeframe,tp_obj.diff_s_overview)
    
    if selected is None:
        return u'没有选出要交易的货币，之后需要一个逻辑来处理，比如场外等待多久继续做交易计划,因为不交易也是一种交易状态'
        # return redirect('/tradesys/MyTradePlan/no_selected_symbol')
    
    if request.method == "POST":
        selected_view = SelectedFormset( request.POST,
            queryset = MarketDetailInfo.objects.filter(
                Q(exclude_reason = 'N'  ,market_overview = tp_obj.diff_s_overview) |
                Q(exclude_reason__isnull = True,market_overview = tp_obj.diff_s_overview),
                symbol_name__in=selected))
        if selected_view.is_valid():
            selected_view.save()
            tradeplan_action_init(tp_obj)
            
        return redirect('/tradesys/MyTradePlan/tradeplan_action_view')
    else:
        selected_view = SelectedFormset(queryset = MarketDetailInfo.objects.filter(
                Q(exclude_reason = 'N'  ,market_overview = tp_obj.diff_s_overview) |
                Q(exclude_reason__isnull = True,market_overview = tp_obj.diff_s_overview),
                symbol_name__in=selected))
        
    return render_to_response("tradesys/AnalysisSelectedView.html", {
            "tradetype" :  tp_obj.tradetype,
            "selected_view" : selected_view.as_ul()
            },context_instance=RequestContext(request))

# 可能需要 用 login_required 修饰一下，确保登录使用
def tradeplan_action_view(request, tp_id = None):

    if tp_id == None:
        tp_id = request.session['TradePlanModel_id']

        
    tp_obj  = TradePlanModel.objects.get(pk = tp_id)

    tp_action_query = TradePlanAction.objects.filter(tradeplan = tp_obj)
    
    if request.method == "POST":
        tradeplan_action_view = TradePlanActionFormset( request.POST,
                                                        queryset = tp_action_query)
        if tradeplan_action_view.is_valid():
            tradeplan_action_view.save()
        return redirect('/tradesys/MyTradePlan/tradeplan_action_view')
    else:
        tradeplan_action_view = TradePlanActionFormset( queryset = tp_action_query )

    return render_to_response("tradesys/TradePlanActionView.html", {
            "tradetype" :  tp_obj.tradetype,
            "tradeplan_action_view" : tradeplan_action_view.as_ul()
            },context_instance=RequestContext(request))


tp_sum_view       = login_required(MyTradePlanView.as_view())
# market_over_view  = login_required(MarketOview.as_view())
# market_diff_view  = login_required(MarketDview.as_view())
# first_select_view = login_required(FirstSelectedView.as_view())
# select_view       = login_required(SelectedView.as_view())
