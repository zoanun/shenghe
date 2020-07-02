from django.http import HttpResponse
from .models import *
import json

def find(request):
    """
    查询项目
    :param request:
    :return:
    """
    if request.method == 'GET':
        datatype = request.GET['type']
        nonmemberUseyn = request.GET['nonmemberUseYn']
        memberUseyn = request.GET['memberUseYn']
        useyn = request.GET['useYn']
        name = request.GET['name']
        result = ItemMaster.objects.all()
        if not (not datatype or datatype == 'A'):
            result = result.filter(type=datatype)
        if not (not nonmemberUseyn or nonmemberUseyn == 'A'):
            result = result.filter(nonmemberUseYn=nonmemberUseyn)
        if not (not memberUseyn or memberUseyn == 'A'):
            result = result.filter(memberUseYn=memberUseyn)
        if not (not useyn or useyn == 'A'):
            result = result.filter(useYn=useyn)
        if name:
            result = result.filter(name__contains=name)
        result = result.order_by('id')
        result = result.values('id', 'type', 'name', 'nonmemberUseYn', 'memberUseYn', 'useYn')
        return HttpResponse(json.dumps(list(result), ensure_ascii=False))
    else:
        raise BaseException('不支持POST方法')


def insert(request):
    """插入国标体测项目"""
    if request.method == 'POST':
        item = ItemMaster()
        data = json.loads(request.body)
        item.type = data['type']
        item.name = data['name']
        item.nonmemberUseYn = data['nonmemberUseYn']
        item.memberUseYn = data['memberUseYn']
        item.useYn = data['useYn']
        item.save()
        return HttpResponse(item.toJSON())
    else:
        raise BaseException('不支持GET方法')


def update(request):
    """插入国标体测项目"""
    if request.method == 'POST':
        data = json.loads(request.body)
        item = ItemMaster.objects.get(pk=data['id'])
        item.type = data['type']
        item.name = data['name']
        item.nonmemberUseYn = data['nonmemberUseYn']
        item.memberUseYn = data['memberUseYn']
        item.useYn = data['useYn']
        item.save()
        return HttpResponse(item.toJSON())
    else:
        raise BaseException('不支持GET方法')

def findSingleMaster(request):
    if request.method == 'GET':
        id = request.GET['id']
        item = ItemMaster.objects.get(pk=id)
        return HttpResponse(json.dumps(item.toJSON(), ensure_ascii=False))
    else:
        raise BaseException('不支持POST方法')