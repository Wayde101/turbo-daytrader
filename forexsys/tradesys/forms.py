from django import forms
from  models import SUB_DIR,OBJ_DIR
from models import MarketDirect


class MarketDirectForm(forms.ModelForm):
    sub_dir = forms.CharField (max_length=3,widget=forms.Select(choices=SUB_DIR))
    obj_dir = forms.CharField (max_length=3,widget=forms.Select(choices=OBJ_DIR))

    class Meta:
        model  = MarketDirect
        fields = ('symbol_name','timeframe','obj_dir','sub_dir')

    
