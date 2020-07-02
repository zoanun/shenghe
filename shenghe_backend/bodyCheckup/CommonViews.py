from django.http import HttpResponse
from .models import *
import json


def itemType(request):
    choices = ItemMaster.typeChoices
    return HttpResponse(json.dumps(choices))


def periodType(request):
    choices = ItemScoreStandard.typeChoices
    return HttpResponse(json.dumps(choices))


def channel(request):
    choices = NonMember.channelChoices
    return HttpResponse(json.dumps(choices))