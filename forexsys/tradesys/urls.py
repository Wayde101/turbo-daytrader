from django.conf.urls import patterns, url
from tradesys.views import TradePlan


urlpatterns = patterns('tradesys.views',
                       url(r'^MyTradePlan/$', 'TradePlan.tp_sum_view'),
                       url(r'^MyTradePlan/market_over_view/$', 'TradePlan.market_over_view'),
                       url(r'^MyTradePlan/market_over_view/(?P<tp_id>\d+)/$', 'TradePlan.market_over_view'),
                       url(r'^MyTradePlan/market_diff_view/$', 'TradePlan.market_diff_view'),
                       url(r'^MyTradePlan/market_diff_view/(?P<tp_id>\d+)/$', 'TradePlan.market_diff_view'),
                       url(r'^MyTradePlan/first_select_view/$', 'TradePlan.first_select_view'),
                       url(r'^MyTradePlan/first_select_view/(?P<tp_id>\d+)/$', 'TradePlan.first_select_view'),
                       url(r'^MyTradePlan/analysis_selected_view/$', 'TradePlan.analysis_selected_view'),
                       url(r'^MyTradePlan/analysis_selected_view/(?P<tp_id>\d+)/$', 'TradePlan.analysis_selected_view')
                       )

