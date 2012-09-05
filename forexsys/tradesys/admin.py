from tradesys.models import Symbol
from tradesys.models import TimeFrame
from tradesys.models import MarketDirect
from django.contrib import admin



class SymbolAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['symbol_name']}),
    ]

class TimeFrameAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['timeframe']}),
    ]

class MarketDirectAdmin(admin.ModelAdmin):
    pass


admin.site.register(Symbol,SymbolAdmin)
admin.site.register(TimeFrame,TimeFrameAdmin)
admin.site.register(MarketDirect,MarketDirectAdmin)

