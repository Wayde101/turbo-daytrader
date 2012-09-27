import operator
from django import forms
from models import SUB_DIR,OBJ_DIR,NORMATIVE
from models import MarketDetailInfo
from models import TRADEFRAME,TRADETYPE,STRENGTHSCORE,PLANRESULT
from models import EXREASON

class MarketDetailInfoForm(forms.ModelForm):
    class Meta:
        model  = MarketDetailInfo
        fields = ('obj_dir','sub_dir')

class TradeInfoForm(forms.Form):
    tradetype  = forms.CharField(max_length=10,widget=forms.Select(choices = TRADETYPE))
    tradeframe = forms.CharField(max_length=10,widget=forms.Select(choices = TRADEFRAME))

class MarketOverViewForm(forms.Form):
    def __init__(self,symbol,trademap,*args,**kwargs):
        super(MarketOverViewForm, self).__init__(*args,**kwargs)
        
        choose = lambda x: SUB_DIR if x == 'sub_dir' else OBJ_DIR
        
        for zk in ['obj_dir','sub_dir']:
            for tm in trademap:
                n = '%s_%s_%s' % (symbol,zk,tm)
                self.fields[n] = forms.CharField(max_length=10,
                                                 widget=forms.Select(choices=choose(zk)),initial = 'U')
    
    market_result = forms.CharField(max_length = 200,widget = forms.Textarea())
    plan_result   = forms.CharField(max_length = 5,widget = forms.Select(choices = PLANRESULT))

    
class MarketDiffViewForm(forms.Form):
    def __init__(self,symbols,trademap,*args,**kwargs):
        super(MarketDiffViewForm, self).__init__(*args,**kwargs)
        choose = lambda x: SUB_DIR if x == 'sub_dir' else OBJ_DIR
                                                 
        for symbol in symbols:
            for zk in ['obj_dir', 'sub_dir', 'normative','strength']:
                for tm in [trademap[0],trademap[1]]:
                    
                    n = '%s_%s_%s' % (symbol,zk,tm)
                    
                    if zk == 'normative':
                        self.fields[n] = forms.CharField(max_length = 20,
                                                         widget = forms.Select(choices = NORMATIVE),
                                                         initial = 'NoCC')
                        continue

                    if zk == 'strength' and tm == trademap[0]:
                        self.fields[n] = forms.FloatField(widget = forms.Select(choices = STRENGTHSCORE),
                                                          initial = 0)
                        continue
                    
                    self.fields[n] = forms.CharField(max_length=10,
                                                     widget=forms.Select(choices=choose(zk)),initial = 'U')
                    
    diff_b_result =  forms.CharField(max_length=200,widget = forms.Textarea())
    diff_s_result =  forms.CharField(max_length=200,widget = forms.Textarea())


class MarketStrengthSelected(forms.Form):
    def __init__(self,symbol_strength,tf,*args,**kwargs):
        super(MarketStrengthSelected, self).__init__(*args,**kwargs)
        ss = sorted(symbol_strength.iteritems(),
                         key=operator.itemgetter(1))
        print ss
        for symbol in ss:
            n = '%s_strength_%s' % (symbol[0],tf)
            self.fields[n] = forms.FloatField(widget=forms.Select(choices=STRENGTHSCORE),
                                                      initial =  symbol[1])

class MarketExcludeSelected(forms.Form):
    def __init__(self,symbol_exclude,tf,*args,**kwargs):
        super(MarketExcludeSelected,self).__init__(*args,**kwargs)

        for symbol in symbol_exclude.keys():
            n = '%s_excluded_%s' % (symbol,tf)
            self.fields[n] = forms.CharField(max_length=100,
                                                  widget=forms.Select(choices = EXREASON),
                                                  initial = symbol_exclude[symbol])
            
