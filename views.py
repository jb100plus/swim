from django.shortcuts import render
from django.shortcuts import redirect
from counter.models import Log, Starter, LastLog, ListHash
from django.views.generic import ListView
from django.utils.timezone import datetime
from counter import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import xxhash
import random


# Create your views here.
class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LastLog
    ordering = ['log']

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context


home_list_view = HomeListView.as_view(
    context_object_name="log_list",
    template_name="counter/home.html",
    )


count_list_view = HomeListView.as_view(
    context_object_name="log_list",
    template_name="counter/count.html",
    )


class StarterLogListView(ListView):
    """Renders a page, with a list of all logs for a starter."""
    model = Log
    ordering = ['-logtimestamp']
    #context_object_name="log_list",
    template_name="counter/logdetail.html"

    def get_context_data(self, **kwargs):
        context = super(StarterLogListView, self).get_context_data(**kwargs)
        return context
    
    def get_queryset(self):
        pk = self.kwargs["starter_id"]
        return super().get_queryset().filter(starter=pk)

'''
logdetailview = StarterLogListView.as_view(
    context_object_name="log_list",
    template_name="counter/logdetail.html",
    )
'''


def about(request):
    result = models.getresult()
    context ={'result':result}
    print(result)
    return render(request, "counter/about.html", context=context)

def contact(request):
    return render(request, "counter/contact.html")



def add_log(request, starter_id):
    starter = Starter.objects.get(pk = starter_id)
    #log = Log.objects.create(starter=starter)
    log = Log(starter=starter)
    try:
        log.full_clean()
    except ValidationError:
        print('Scheisse')# Do something when validation is not passing
    else:
        # Validation is ok we will save the instance
        log.save()
    try:
        lastlog = LastLog.objects.get(starter=starter)
        lastlog.log = log
        lastlog.save()
    except LastLog.DoesNotExist:
        lastlog = LastLog(starter=starter, log=log)
        lastlog.save()
    response = redirect('home')
    return response

# Create your views here.
class StartListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = Starter
    ordering = ['startnumber']

    def get_context_data(self, **kwargs):
        context = super(StartListView, self).get_context_data(**kwargs)
        return context
    
    # show only starter with no logs (i.e. who are not yet in the race)
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(lastlog=None)


start_list_view = StartListView.as_view(
    context_object_name="starter_list",
    template_name="counter/start.html",
    )


def asyncview(request):
    log_list = LastLog.objects.order_by('log')
    newhash = xxhash.xxh64(str(log_list)).hexdigest()
    print(newhash)

    try:
        oldhash = ListHash.objects.get(pk=1)
    except ObjectDoesNotExist:
        lh = ListHash.objects.create(hash=newhash)
        lh.save()
    if oldhash.hash == newhash:
        r = random.random()
        print(r)
        if r > 1.0:
            log_list = None
    else:
        print('ungleich')
        oldhash.hash = newhash
        oldhash.save()

    return render(request, "counter/async.html", {'log_list': log_list})

