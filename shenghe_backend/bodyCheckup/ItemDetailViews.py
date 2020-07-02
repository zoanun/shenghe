from django.http import HttpResponse
from .models import *
import json, datetime
from django.db import connection


def findMaster(request):
    """
    查询项目
    :param request:
    :return:
    """
    if request.method == 'GET':
        sql = '''select 
                    bim.id, 
                    bim.type, 
                    bim.name, 
                    case 
                        when bid.id is null then 
                            0 
                        else 
                            count(*) 
                    end as cnt 
                from bodyCheckup_itemmaster bim 
                    left join bodyCheckup_itemdetail bid 
                        on bid.item_id=bim.id and bim.useYn='Y' 
                group by bim.id, bim.type, bim.name
                order by bim.id
        '''
        result = []
        for row in ItemMaster.objects.raw(sql):
            result.append({'id': row.id, 'type': row.type, 'name': row.name, 'cnt': row.cnt})
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    else:
        raise BaseException('不支持POST方法')


def find(request):
    """
    查询标准值
    :param request:
    :return:
    """
    if request.method == 'GET':
        age = request.GET['age']
        sex = request.GET['sex']
        itemId = request.GET['itemId']
        result = ItemDetail.objects.filter(item__id=itemId)
        if age != '':
            result = result.filter(age=age)
        if not (not sex or sex == 'A'):
            result = result.filter(sex=sex)
        result = [r.getDict() for r in result]
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    else:
        raise BaseException('不支持POST方法')


def insert(request):
    """插入标准值"""
    if request.method == 'POST':
        detail = ItemDetail()
        data = json.loads(request.body)
        detail.item = ItemMaster.objects.get(pk=data['itemId'])
        detail.age = data['age']
        detail.sex = data['sex']
        detail.staDate = datetime.datetime.strptime(data['staDate'], '%Y-%m-%d')
        detail.endDate = datetime.datetime.strptime(data['endDate'], '%Y-%m-%d')
        detail.value = data['value']
        detail.save()
        return HttpResponse(detail.toJSON())
    else:
        raise BaseException('不支持GET方法')


def delete(request):
    """刪除標準值"""
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data['id']
        itemDetail = ItemDetail.objects.get(pk=id)
        itemDetail.delete()
        return HttpResponse(itemDetail.toJSON())
    else:
        raise BaseException('不支持GET方法')

def update(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data['id']
        detail = ItemDetail.objects.get(pk=id)
        detail.age = data['age']
        detail.sex = data['sex']
        detail.staDate = datetime.datetime.strptime(data['staDate'], '%Y-%m-%d')
        detail.endDate = datetime.datetime.strptime(data['endDate'], '%Y-%m-%d')
        detail.value = data['value']
        detail.save()
        return HttpResponse(detail.toJSON())
    else:
        raise BaseException('不支持GET方法')