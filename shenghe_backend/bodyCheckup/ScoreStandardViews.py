from django.http import HttpResponse
from .models import *
import json


def findMaster(request):
    if request.method == 'GET':
        sql = '''select 
                    bid.id,
                    bim.type,
                    bim.name,
                    bid.age,
                    bid.sex,
                    bid.value
                from bodyCheckup_itemmaster bim 
                    left join bodyCheckup_itemdetail bid 
                        on bid.item_id=bim.id and bim.useYn='Y'
                where bim.useYn='Y' and date('now') between bid.staDate and bid.endDate
                and (%s='' or bid.age = %s)  and (%s='' or %s='A' or bid.sex=%s)
                group by bim.id, bim.type, bim.name, bid.age, bid.sex
        '''
        result = []
        age = request.GET['age']
        sex = request.GET['sex']
        for row in ItemDetail.objects.raw(sql, [age, age, sex, sex, sex]):
            result.append(
                {'id': row.id, 'type': row.type, 'name': row.name, 'value': row.value, 'sex': row.sex, 'age': row.age}
            )
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    else:
        raise BaseException('不支持POST方法')


def find(request):
    if request.method == 'GET':
        itemDetailId = request.GET['itemDetailId']
        result = ItemScoreStandard.objects.filter(itemDetail__id=itemDetailId)
        result = [r.getDict() for r in result]
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    else:
        raise BaseException('不支持POST方法')


def insert(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        itemDetailId = data['itemDetailId']
        itemDetail = ItemDetail.objects.get(pk=itemDetailId)

        scoreStandardList = list(ItemScoreStandard.objects.filter(itemDetail_id=itemDetailId))
        for type in ItemScoreStandard.typeChoices:
            sslist = list(filter(lambda ss: ss.periodType == type[0], scoreStandardList))
            if len(sslist) > 0:
                opss = sslist[0]
            else:
                opss = ItemScoreStandard()
            opss.periodType = type[0]
            opss.itemDetail = itemDetail
            opss.lowScore = data['data'][type[0] + '_lowScore']
            opss.highScore = data['data'][type[0] + '_highScore']
            opss.scoreDesc = data['data'][type[0] + '_scoreDesc']
            opss.color = data['data'][type[0] + '_color']
            opss.save()
        return HttpResponse("SUCCESS")
    else:
        raise BaseException('不支持GET方法')


def update(request):
    return insert(request)

def report(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        items = data['items']
        if len(items) == 0:
            return HttpResponse("FAIL")

        sql = '''
            select 
                bim.name as item_name,
                bid.age,
                bid.sex,
                bid.value as standardValue,
                biss.periodType
                biss.lowScore,
                biss.highScore,
                biss.scoreDesc,
                biss.color
            from
                bodyCheckup_itemmaster bim,
                bodyCheckup_itemdetail bid,
                bodyCheckup_itemscorestandard biss
            where bid.id = biss.itemDetail_id
                and bim.id = bid.item_id
                and %s between biss.lowScore and biss.highScore
                and bid.age = %s 
                and bid.sex = %s
                and bid.item_id = %s
                and date('now') between bid.staDate and bid.endDate
        '''
        age = data['age']
        sex = data['sex']
        result = []
        for item in items:
            if item['score']:
                itemId = item['itemId']
                for row in ItemMaster.objects.raw(sql, [age, sex, itemId]):
                    result.append({
                        'name': row.name,
                        'age': row.age,
                        'sex': row.sex,
                        'standardValue': row.standardValue,
                        'periodType': row.periodType,
                        'lowScore': row.lowScore,
                        'highScore': row.highScore,
                        'scoreDesc': row.scoreDesc,
                        'color': row.color
                    })
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    else:
        raise BaseException('不支持GET方法')