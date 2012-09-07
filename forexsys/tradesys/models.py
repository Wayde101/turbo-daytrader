# -*- coding: utf-8 -*-
# -*- mode: python -*-
from django.db import models
from django.forms import ModelForm
import datetime
from django.utils import timezone

# Create your models here.

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

SYMBOL_NAME = (
    (u'EURUSD', u'EURUSD'),
    (u'GBPUSD', u'GBPUSD'),
    (u'AUDUSD', u'AUDUSD'),
    (u'JPYUSD', u'JPYUSD'),
    (u'CADUSD', u'CADUSD'),
    (u'CHFUSD', u'CHFUSD'),
    (u'AUXUSD', u'AUXUSD'),
    (u'USDX', u'USDX'),
    )

TIMEFRAME = (
    (u'5M',  u'5M'),
    (u'15M', u'15M'),
    (u'1H',  u'1H'),
    (u'4H',  u'4H'),
    (u'1D',  u'1D'),
    (u'1W',  u'1W'),
    (u'1Mon',u'1Mon'),
    )

TRADEFRAME = (
    (u'5M', u'超短计划(以5分钟为最小交易级别)'),
    (u'15M',u'超短计划(以15分钟为最小交易级别)'),
    (u'1H', u'日计划(以1小时为最小交易级别)'),
    (u'4H', u'周计划(以4小时为最小交易级别)'),
    (u'1D', u'月计划(以日图为最小交易级别)'),
    )

OBJ_DIR = (
    (u'U', u'上'),
    (u'D', u'下'),
    (u'H', u'横'),
    (u'Z', u'转'),
    )
SUB_DIR = (
    (u'U', u'上'),
    (u'D', u'下'),
    (u'*', u'*'),
    )


TRADETYPE = (
    (u'U', u'美元直盘'),
    (u'J', u'日元叉盘'),
    (u'G', u'贵金属'),
    )

NORMATIVE = (
    (u'1stClass', u'一等中继模型'),
    (u'2thClass', u'二等通道模型'),
    (u'3thClass', u'三等反弹模型'),
    (u'MacdClass', u'MACD反弹模型'),
    (u'HaveRelay', u'已有中继或者次'),
    (u'HaveCC',  u'已有不规范的次'),
    (u'NoCC', u'暂时还没有中继或者次'),
    (u'LongNoCC','段时间不太可能形成次')   # 比如在一个横盘区间，不划分主次，突破之后有次要节奏调整才认定主次
    )

class Symbol(models.Model):
    symbol_name = models.CharField(max_length = 20,choices = SYMBOL_NAME)

    def __unicode__(self):
        return self.symbol_name

class TimeFrame(models.Model):
    timeframe = models.CharField(max_length = 10,choices = TIMEFRAME)

    def __unicode__(self):
        return self.timeframe

class TradeFrame(models.Model):
    tradeframe = models.CharField(max_length=10,choices=TRADEFRAME)

    def __unicode__(self):
        return '%s' % self.tradeframe

class MarketDirect(models.Model):
    symbol_name = models.ForeignKey(Symbol)
    timeframe   = models.ForeignKey(TimeFrame)
    obj_dir     = models.CharField(max_length=10,choices=OBJ_DIR)
    sub_dir     = models.CharField(max_length=10,choices=SUB_DIR)
    normative   = models.CharField(max_length=20,choices=NORMATIVE)
    pub_date    = models.DateTimeField()

    def __unicode__(self):
        return '%s %s %s %s' % (self.symbol_name,self.obj_dir,self.sub_dir,self.pub_date)

class MarketOverView(models.Model):
    market_direct = models.ForeignKey(MarketDirect)
    market_result = models.CharField(max_length=500,blank=True)
    # if trade_frame = 15M then 1st:15M 2th:1H 3th:4H 4th:1D 5th:1W
    # if trade_frame = 1H then 1st:1H 2th:4H 3th:1D 4th:1W 5th:1M


class TradePlanModel(models.Model):
    begin_time       = models.DateTimeField()
    end_time         = models.DateTimeField(blank=True)
    completion       = models.IntegerField()
    tradeframe       = models.CharField(max_length=10,choices=TRADEFRAME)
    tradetype        = models.CharField(max_length=10,choices=TRADETYPE)
    #tradeplan_action = models.ForeignKey(TradePlanAction) # 一个TradePlan 可能会对0个或多个 TradePlanAction , 当0 个的时候表示不交易，等待下一个交易计划周期
    market_overview  = models.ForeignKey(MarketOverView,related_name='market_overview',blank=True,null=True)    
    diff_b_overview  = models.ForeignKey(MarketOverView,related_name='diff_b_overview',blank=True,null=True)
    diff_s_overview  = models.ForeignKey(MarketOverView,related_name='diff_s_overview',blank=True,null=True)
    diff_result      = models.CharField(max_length=500,blank=True)
    plan_result      = models.CharField(max_length=500,blank=True)

class TradePlanAction(models.Model):
    symbol_name = models.ForeignKey(Symbol)
    tradeplan   = models.ForeignKey(TradePlanModel)
    action_type  = models.CharField(max_length=10)  # buy/sell/buy_limit/sell_limit/buy_stop/sell_stop/wait
    enter_price = models.FloatField()
    sl_price    = models.FloatField()
    tp_price    = models.FloatField()
    holding_log = models.CharField(max_length=5000)

    
class StrengthModel(models.Model):
    symbol_name = models.ForeignKey(Symbol)
    score       = models.FloatField()
    tradeplan   = models.ForeignKey(TradePlanModel)
    
    
