from django.conf.urls import patterns, url
from tradesys.views import TradePlan


urlpatterns = patterns('tradesys.views',
                       url(r'^TradePlan/$', TradePlan.tp_sum_view),
                       url(r'^TradePlan/create/$', TradePlan.create_view),
                       # url(r'^TradePlan/update/(?P<pk>\d+)/$', TradePlan.tp_sum_view)
                       )
