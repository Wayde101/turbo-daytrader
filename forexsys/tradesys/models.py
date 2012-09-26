# -*- coding: utf-8 -*-
# -*- mode: python -*-
from django.db import models
from django.forms import ModelForm
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
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
    (u'XAGUSD', u'XAGUSD'),
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
    (u'1H', u'日计划(以1小时为最小交易级别)'),
    )

OBJ_DIR = (
    (u'N', u'N/A'),
    (u'U', u'上'),
    (u'D', u'下'),
    (u'H', u'横'),
    (u'Z', u'转'),
    )

SUB_DIR = (
    (u'N', u'N/A'),
    (u'U', u'上'),
    (u'D', u'下'),
    (u'*', u'*'),
    )

TRADETYPE = (
    (u'USDX', u'美元直盘'),
    (u'AUXUSD', u'黄金'),
    (u'XAGUSD', u'白银'),
    )

TRADEACTIONTYPE = (
    (u'OP_BUY'      , u'市价买入'),
    (u'OP_SELL'     , u'市价卖出'),
    (u'OP_BUYLIMIT' , u'限价买入'),
    (u'OP_SELLLIMIT', u'限价卖出'),
    (u'OP_BUYSTOP'  , u'突破买入'),
    (u'OP_SELLSTOP' , u'突破卖出')
    )

TRADESTATUS = (
    (u'ST_PENDING'     , u'场外挂单中'),
    (u'ST_HOLDING'     , u'场内持仓中'),
    (u'ST_CANCEL'      , u'撤销挂单'),
    (u'ST_TPOUT'       , u'盈利出局'),
    (u'ST_SLOUT'       , u'亏损出局')
    )

STRENGTHSCORE = (
    ('4', '4'),
    ('3.75', '3.75'),
    ('3.5', '3.5'),
    ('3.25', '3.25'),
    ('3', '3'),
    ('2','2'),
    ('0','0')
    )

PLANRESULT = (
    (u'B', u'做多'),
    (u'S', u'做空'),
    (u'N', u'不做交易')
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

EXREASON = (
    (u'N'   , u'暂无'),
    (u'较弱' , u'相对较弱'),
    (u'太强' , u'相对较强'),
    (u'强(支撑/阻力)不顶着做'   , u'强(支撑/阻力)不做(多/空)'),
    (u'macd 动能充盈不逆向交易' , u'macd 动能充盈不逆向交易')
    )

class MarketOverView(models.Model):
    market_result = models.CharField(max_length=500,blank=True)
    pub_date      = models.DateTimeField()
    # if trade_frame = 5M then 1st:5M 2th:15M 3th:1H 4th:4H
    # if trade_frame = 1H then 1st:1H 2th:4H 3th:1D 4th:1W 5th:1M
    def __unicode__(self):
        return '%s' % self.pub_date

class MarketDetailInfo(models.Model):
    symbol_name = models.CharField(max_length = 20,choices = SYMBOL_NAME)
    timeframe   = models.CharField(max_length = 10,choices = TIMEFRAME)
    obj_dir     = models.CharField(max_length =10,choices  = OBJ_DIR)
    sub_dir     = models.CharField(max_length =10,choices  = SUB_DIR)
    strength    = models.FloatField(max_length=5,
                                    choices=STRENGTHSCORE,
                                    blank=True,
                                    null=True)
    normative   = models.CharField(max_length=20,
                                   choices=NORMATIVE,
                                   blank=True,
                                   null=True)
    exclude_reason = models.CharField(max_length = 100,
                                      choices = EXREASON,
                                      blank=True,
                                      null=True)

    market_overview = models.ForeignKey(MarketOverView)
    
    def __unicode__(self):
        return '%s %s %s' % (self.symbol_name,self.obj_dir,self.sub_dir)


class TradePlanModel(models.Model):
    begin_time       = models.DateTimeField()
    end_time         = models.DateTimeField(blank=True,null=True)
    completion       = models.IntegerField()
    created_by       = models.ForeignKey(User,blank=True,null=True)
    tradeframe       = models.CharField(max_length=10,choices=TRADEFRAME)
    tradetype        = models.CharField(max_length=10,choices=TRADETYPE)
    #tradeplan_action = models.ForeignKey(TradePlanAction)
    # 一个TradePlan 可能会对0个或多个 TradePlanAction , 当0 个的时候表示不交易，等待下一个交易计划周期
    
    market_overview  = models.ForeignKey(MarketOverView,
                                         related_name='market_overview',
                                         blank=True,
                                         null=True)    
    diff_b_overview  = models.ForeignKey(MarketOverView,
                                         related_name='diff_b_overview',
                                         blank=True,
                                         null=True)
    diff_s_overview  = models.ForeignKey(MarketOverView,
                                         related_name='diff_s_overview',
                                         blank=True,
                                         null=True)
    plan_result      = models.CharField(max_length=5,choices=PLANRESULT,blank=True,null=True)

    def isOwnedBy(self, user):
        return self.created_by == user
    
    def __unicode__(self):
        return 'ID:%s | @[%s]' % (self.id,self.begin_time)

class TradePlanAction(models.Model):
    symbol_name = models.CharField(max_length = 20,choices = SYMBOL_NAME)
    tradeplan   = models.ForeignKey(TradePlanModel)
    trade_type  = models.CharField(max_length=50,choices=TRADEACTIONTYPE)
    trade_status  = models.CharField(max_length=50,choices=TRADESTATUS)
    enter_price = models.FloatField()
    sl_price    = models.FloatField()
    tp_price    = models.FloatField()
    holding_log = models.CharField(max_length=5000)
    
    def __unicode__(self):
        return 'ID:%s | @[%s] | Action[%s]' % (self.id,self.symbol_name,self.trade_type)
    
