from django.conf.urls import patterns, url
from tradesys.views import TradePlan


urlpatterns = patterns('tradesys.views',
                       url(r'^MyTradePlan/$', TradePlan.tp_sum_view),
                       url(r'^MyTradePlan/create/$', TradePlan.create_view),
                       )
