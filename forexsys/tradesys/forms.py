import operator
from django import forms
from django.forms.models import modelformset_factory
from django.forms.models import BaseModelFormSet
from django.forms.models import inlineformset_factory
from models import SUB_DIR,OBJ_DIR,NORMATIVE
from models import MarketDetailInfo,MarketOverView
from models import TradePlanModel
from models import TRADEFRAME,TRADETYPE,STRENGTHSCORE,PLANRESULT
from models import EXREASON


class TradePlanInitForm(forms.ModelForm):
    
    class Meta:
        model = TradePlanModel
        fields = ('tradeframe','tradetype')


class MarketOverViewForm(forms.ModelForm):
    class Meta:
        model = MarketOverView
        fields = ('market_result',)
                

class PlanResultForm(forms.ModelForm):
    class Meta:
        model  = TradePlanModel
        fields = ('plan_result',)


FirstSelectFormset  = modelformset_factory(MarketDetailInfo,
                                           extra = 0,
                                           fields = ('strength','exclude_reason'))

MovDetailInlineFormset=inlineformset_factory(MarketOverView,
                                             MarketDetailInfo,
                                             extra=0,
                                             can_delete = False,
                                             fields = ('timeframe','obj_dir','sub_dir')
                                             )


# form mixin needed maybe
# refer to http://stackoverflow.com/questions/1610892/passing-custom-form-parameter-to-formset
MdvDetailInlineFormset=inlineformset_factory(MarketOverView,
                                             MarketDetailInfo,
                                             extra=0,
                                             can_delete = False,
                                             fields = ('timeframe',
                                                       'obj_dir',
                                                       'sub_dir',
                                                       'strength',
                                                       'normative')
                                             )

# class BaseDetailFormSet(BaseModelFormSet):
    # def __init__(self, *args, **kwargs):
        # super(BaseAuthorFormSet, self).__init__(*args, **kwargs)
        # self.queryset = MarketDetailInfo.objects.filter(name__startswith='O')

# AuthorFormSet = modelformset_factory(MarketDetailInfo, formset=BaseDetailFormSet)

class MarketStrengthSelected(forms.Form):
    def __init__(self,symbol_strength,tf,*args,**kwargs):
        super(MarketStrengthSelected, self).__init__(*args,**kwargs)
        ss = sorted(symbol_strength.iteritems(),
                         key=operator.itemgetter(1))
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
            
