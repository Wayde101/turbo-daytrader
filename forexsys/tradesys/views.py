# Create your views here.
from django.shortcuts import render_to_response

# from tradesys.models import Symbol
from tradesys.forms import MarketDirectForm
from django import forms
from django.views.generic.edit import CreateView
from models import MarketDirect

def index(request):
    symbol_list = Symbol.objects.all()
    return render_to_response('tradesys/index.html', {'symbol_list': symbol_list})


class TimeFrameMetrics(CreateView):
    form_class = MarketDirectForm
    model      = MarketDirect
    template_name = "tradesys/market_overview.html"
    success_url = "/"

create_view = TimeFrameMetrics.as_view()
    
    



# from django.http import Http404

# def detail(request, poll_id):
    # try:
        # p = Poll.objects.get(pk=poll_id)
    # except Poll.DoesNotExist:
        # raise Http404
    # return render_to_response('polls/detail.html', {'poll': p})
