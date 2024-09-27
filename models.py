from django.db import models
from django.utils import timezone
from django.db.models import Count
from django.utils.translation import gettext
from django.core.exceptions import ValidationError
from datetime import timedelta


class STATE(models.IntegerChoices):
    SWIM = 10, 'swimming'
    IN = 20, 'in'
    OUT = 30, 'out'
    GONE = 40, 'gone'
    DONE = 50, 'done'


def getStateStr(state):
    return {10: 'swimming',20: 'in', 30: 'out', 40: 'gone', 50: 'done'}[state]

class Starter(models.Model):
    startnumber = models.CharField(max_length=6)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    startingclass = models.CharField(max_length=30, default='person ')  # no relation because of import
    teamname = models.CharField(max_length=30, default='n/a')  # no relation because of import
    lane = models.IntegerField(default=0)
    state = models.IntegerField(choices=STATE.choices, default='10')

    def __str__(self):
        return f"{self.startnumber} {self.lastname}, {self.firstname[0:5]}, {getStateStr(self.state)}"
    
    @property
    def statestr(self):
        return getStateStr(self.state)

'''
# not uses anymore, but can't be deleted it seems to resist in a migration
def validate_time(value):
    if ((value.logtimestamp - value.starter.lastlog.log.logtimestamp).total_seconds()) < 8:
        raise ValidationError("To Fast!!!!!", params={"value": value},)
        return False
    return True
'''

class Log(models.Model):
    #logtimestamp = models.DateTimeField("timestamp logged", auto_now_add=True, validators=[validate_time,])
    logtimestamp = models.DateTimeField("timestamp logged", auto_now_add=True)
    starter = models.ForeignKey(Starter, on_delete=models.CASCADE)
    kind = models.IntegerField(choices=STATE.choices, default='10', verbose_name='state')
    
    def __str__(self):
        """Returns a string representation of a log"""
        logtimestamp = timezone.localtime(self.logtimestamp)
        return f"{self.starter.startnumber} - {logtimestamp.strftime('%d.%m.%Y %H:%M:%S')} {getStateStr(self.kind)}"
    
    def gettimestr(self):
        dt = timezone.localtime(self.logtimestamp)
        return f"{dt:%Y.%m.%d %H:%M:%S}.{dt.microsecond // 100000:01d}"
    
    def since_sec(self):
        return int((timezone.now() - timezone.localtime(self.logtimestamp)).total_seconds())
    
    def since(self):
        return str(timedelta(seconds=self.since_sec()))
    
    def kindstr(self):
        return getStateStr(self.kind)


class LastLog(models.Model):
    log = models.ForeignKey(Log, on_delete=models.CASCADE)
    starter = models.OneToOneField(Starter, on_delete=models.CASCADE)
    
    def __str__(self):
        """Returns a string representation of a log."""
        return f"'{str(self.starter)}' logged on { str(self.log)}"

    def new_Log_possible(self):
        return self.log.since_sec() > 5


def getresult():    
    return Log.objects.values('starter__id', 'starter__firstname', 'starter__lastname', 'starter__startingclass', 'starter__state').\
        filter(kind=STATE.SWIM).annotate(count=Count('logtimestamp')).\
            order_by('-count')



def add_log_kind(starter, kind):
    try:
        lastlog = LastLog.objects.get(starter=starter)
        if lastlog.new_Log_possible():        
            log = Log.objects.create(starter=starter)
            log.kind = kind
            log.save()
            lastlog.log = log
            lastlog.save()
            print(lastlog)
    # first log for starter
    except Exception as ex:
        print(ex)
        log = Log.objects.create(starter=starter)
        log.save()
        lastlog = LastLog.objects.create(starter=starter, log=log)
        lastlog.save()
    starter.state=kind
    starter.save()


def add_log(starter_id):
    starter = Starter.objects.get(pk = starter_id)
    add_log_kind(starter=starter, kind=STATE.SWIM)


def take_a_break(starter_id):
    starter = Starter.objects.get(pk = starter_id)
    starter.state=STATE.OUT
    starter.save()
    add_log_kind(starter, STATE.OUT)
    

def back_to_swim(starter_id, lane):
    starter = Starter.objects.get(pk = starter_id)
    starter.state=STATE.SWIM
    starter.lane = lane
    starter.save()
    add_log_kind(starter, STATE.IN)

