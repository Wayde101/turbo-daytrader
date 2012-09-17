from django.conf.urls import patterns, url
from tradesys.views import TradePlan


urlpatterns = patterns('tradesys.views',
                       url(r'^MyTradePlan/$', TradePlan.tp_sum_view),
                       url(r'^MyTradePlan/market_over_view/$', TradePlan.market_over_view),
                       url(r'^MyTradePlan/market_diff_view/$', TradePlan.market_diff_view)
                       )
