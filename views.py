from django.shortcuts import render
from django.shortcuts import redirect
from counter.models import Log, Starter, LastLog, STATE
from django.views.generic import ListView
from django.utils.timezone import datetime
from counter import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from channels.layers import get_channel_layer
from apscheduler.schedulers.background import BackgroundScheduler
from asgiref.sync import async_to_sync


current_loglist = None

# executet on start or reload
scheduler = None
def check():
    layer = get_channel_layer()
    async_to_sync(layer.group_send)("countergroup", {'type': 'chat.message', 'message': 'dummy'})


# Function to run every 3 seconds
if scheduler is None:
    scheduler = BackgroundScheduler()
    scheduler.add_job(check, 'cron', second='*/3')
    scheduler.start()


def home_list_view(request):
    return render(request, "counter/home.html")


# Create your views here.
class CountListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LastLog
    ordering = ['log']

    def get_context_data(self, **kwargs):
        context = super(CountListView, self).get_context_data(**kwargs)
        return context


# outer html for the count view
def count_list_view(request):
    return render(request, "counter/wscount.html")


# inner html fot the count_list_view
def loglist(request):
    global current_loglist
    if current_loglist is None:
        current_loglist = LastLog.objects.filter(starter__state__in=[STATE.SWIM, STATE.IN]).order_by('log')
    # render every call because timers
    return render(request, "counter/loglist.html", {'log_list': current_loglist})


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


def about(request):
    result = models.getresult()
    context ={'result':result}
    return render(request, "counter/about.html", context=context)

def contact(request):
    return render(request, "counter/contact.html")


def add_log(request, starter_id):
    models.add_log(starter_id)
    global current_loglist
    current_loglist = None
    layer = get_channel_layer()
    async_to_sync(layer.group_send)("countergroup", {'type': 'chat.message', 'message': 'dummy'})
    return redirect('count')


class StartListView(ListView):
    """Renders the home page, with a list of all starters not in the race."""
    model = Starter
    ordering = ['startnumber']

    def get_context_data(self, **kwargs):
        context = super(StartListView, self).get_context_data(**kwargs)
        return context
    
    # show only starter with no logs (i.e. who are not yet in the race)
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        # return qs.filter(lastlog=None)
        return qs.filter(state=STATE.OUT)


start_list_view = StartListView.as_view(
    context_object_name="starter_list",
    template_name="counter/start.html",
    )


def take_a_break(request, starter_id):
    models.take_a_break(starter_id)
    global current_loglist
    current_loglist = None
    layer = get_channel_layer()
    async_to_sync(layer.group_send)("countergroup", {'type': 'chat.message', 'message': 'dummy'})
    return redirect('count')


def back_to_swim(request, starter_id, lane):
    models.back_to_swim(starter_id, lane)
    global current_loglist
    current_loglist = None
    layer = get_channel_layer()
    async_to_sync(layer.group_send)("countergroup", {'type': 'chat.message', 'message': 'dummy'})
    return redirect('start')