from django import forms
from models import SUB_DIR,OBJ_DIR
from models import MarketDirect
from models import TRADEFRAME,TRADETYPE

class MarketDirectForm(forms.ModelForm):
    class Meta:
        model  = MarketDirect
        fields = ('obj_dir','sub_dir')

class TradeInfoForm(forms.Form):
    tradetype  = forms.CharField(max_length=10,widget=forms.Select(choices = TRADETYPE))
    tradeframe = forms.CharField(max_length=10,widget=forms.Select(choices = TRADEFRAME))

class MarketOverViewForm(forms.Form):
    def __init__(self,symbol,trademap,*args,**kwargs):
        super(MarketOverViewForm, self).__init__(*args,**kwargs)
        
        for zk in ['obj_dir','sub_dir']:
            for tm in trademap:
                n = '%s_%s_%s' % (symbol,zk,tm)
                self.fields[n] = forms.CharField(max_length=10,
                                                 widget=forms.Select(choices=SUB_DIR),initial = 'U')
    
    market_result = forms.CharField(max_length=200,widget = forms.Textarea())
    plan_result   = forms.CharField(max_length=200,widget = forms.Textarea())
    
    
