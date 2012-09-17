from django import forms
from models import SUB_DIR,OBJ_DIR,NORMATIVE
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
        
        choose = lambda x: SUB_DIR if x == 'sub_dir' else OBJ_DIR
        
        for zk in ['obj_dir','sub_dir','normative']:
            for tm in trademap:
                n = '%s_%s_%s' % (symbol,zk,tm)

                if zk == 'normative':
                    self.fields[n] = forms.CharField(max_length=20,
                                                     widget=forms.Select(choices=NORMATIVE),initial = 'NoCC')
                    continue

                self.fields[n] = forms.CharField(max_length=10,
                                                 widget=forms.Select(choices=choose(zk)),initial = 'U')
    
    market_result = forms.CharField(max_length=200,widget = forms.Textarea())
    plan_result   = forms.CharField(max_length=200,widget = forms.Textarea())
    
    
class MarketDiffViewForm(forms.Form):
    def __init__(self,symbols,trademap,*args,**kwargs):
        super(MarketDiffViewForm, self).__init__(*args,**kwargs)
        choose = lambda x: SUB_DIR if x == 'sub_dir' else OBJ_DIR
                                                 
        for symbol in symbols:
            for zk in ['obj_dir', 'sub_dir']:
                n = '%s_%s_%s' % (symbol,zk,trademap[0])
                self.fields[n] = forms.CharField(max_length=10,
                                                 widget=forms.Select(choices=choose(zk)),initial = 'U')
                n = '%s_%s_%s' % (symbol,zk,trademap[1])
                self.fields[n] = forms.CharField(max_length=10,
                                                 widget=forms.Select(choices=choose(zk)),initial = 'U')
    diff_result =  forms.CharField(max_length=200,widget = forms.Textarea())
        

        
        
        
        
