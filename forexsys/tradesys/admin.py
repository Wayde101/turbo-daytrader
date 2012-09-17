from tradesys.models import Symbol
from tradesys.models import TimeFrame,TradeFrame,TradePlanModel,TradePlanAction
from tradesys.models import MarketDirect,MarketOverView
from django.contrib import admin



class SymbolAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['symbol_name']}),
    ]

class TimeFrameAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['timeframe']}),
    ]

class TradeFrameAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['tradeframe']}),
    ]
    
class TradePlanModelAdmin(admin.ModelAdmin):
    pass

class TradePlanActionAdmin(admin.ModelAdmin):
    pass
    

class MarketDirectAdmin(admin.ModelAdmin):
    pass

class MarketOverViewAdmin(admin.ModelAdmin):
    pass


admin.site.register(Symbol,SymbolAdmin)
admin.site.register(TimeFrame,TimeFrameAdmin)
admin.site.register(TradeFrame,TradeFrameAdmin)
admin.site.register(TradePlanModel,TradePlanModelAdmin)
admin.site.register(TradePlanAction,TradePlanActionAdmin)
admin.site.register(MarketDirect,MarketDirectAdmin)
admin.site.register(MarketOverView,MarketOverViewAdmin)

