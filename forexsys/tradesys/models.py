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
    timeframe  = models.ForeignKey(TimeFrame)

class MarketDirect(models.Model):
    symbol_name = models.ForeignKey(Symbol)
    timeframe   = models.ForeignKey(TimeFrame)
    obj_dir     = models.CharField(max_length=10,choices=OBJ_DIR)
    sub_dir     = models.CharField(max_length=10,choices=SUB_DIR)
    # pub_date  = models.DateTimeField('date published')
    pub_date   = models.DateTimeField(auto_now_add=True, blank=True)

    def __unicode__(self):
        return '%s %s %s %s' % (self.symbol_name,self.obj_dir,self.sub_dir,self.pub_date)


class TradePlanModel(models.Model):
    begin_time = models.DateTimeField()
    end_time   = models.DateTimeField()
    tradeframe = models.CharField(max_length=10,choices=TRADEFRAME)
