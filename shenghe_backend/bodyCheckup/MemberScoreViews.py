from django.http import HttpResponse
from .models import *
import json


def findMaster(request):
    if request.method == 'GET':
        age = request.GET['age']
        sex = request.GET['sex']
        sql = '''
        select bim.id, bim.name, bid.value
        from bodyCheckup_itemmaster bim, bodyCheckup_itemdetail bid
        where bim.id = bid.item_id
            and bim.useYn='Y'
            and bim.memberUseYn='Y'
            and date('now') between bid.staDate and bid.endDate
            and bid.age=%s and bid.sex=%s
        '''
        result = []
        for row in NonMember.objects.raw(sql, [age, sex]):
            result.append({'id': row.id, 'name': row.name, 'value': row.value})
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    else:
        raise BaseException('不支持POST方法')


def find(request):
    if request.method == 'GET':
        memeberId = request.GET['memeberId']
        age = request.GET['age']
        sex = request.GET['sex']
        name = request.GET['name']
        result = NonMember.objects.all()
        if memeberId:
            result = result.filter(memeberId=memeberId)
        if age:
            result = result.filter(age=age)
        if not (not sex or sex == 'A'):
            result = result.filter(sex=sex)
        if name:
            result = result.filter(name__contains=name)
        result = result.order_by('-id')
        result = result.values('id', 'referee', 'channel', 'age', 'sex', 'name')
        return HttpResponse(json.dumps(list(result), ensure_ascii=False))
    else:
        raise BaseException('不支持POST方法')


def insert(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        items = data['items']
        if len(items) == 0:
            return HttpResponse("FAIL")

        member = Member()
        member.memberId = data['memberId']
        member.age = data['age']
        member.sex = data['sex']
        member.save()

        for item in items:
            if data['score']:
                score = MemberItemScore()
                score.item = ItemMaster.objects.get(pk=item['id'])
                score.member = member
                score.score = data['score']
                score.save()

        return HttpResponse("SUCCESS")
    else:
        raise BaseException('不支持GET方法')


def score(request):
    if request.method == 'GET':
        id = request.GET['id']
        result = MemberItemScore.objects.filter(member__id=id)
        result = result.values('id', 'item__name', 'item__itemdetail__value', 'score')
        return HttpResponse(json.dumps(list(result), ensure_ascii=False))
    else:
        raise BaseException('不支持POST方法')


def update(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item = ItemMaster.objects.get(pk=data['id'])
        item.type = data['type']
        item.name = data['name']
        item.nonmemberUseYn = data['nonmemberUseYn']
        item.memberUseYn = data['memberUseYn']
        item.useYn = data['useYn']
        item.save()
        return HttpResponse("SUCCESS")
    else:
        raise BaseException('不支持GET方法')


def delete(request):
    if request.method == 'POST':
        id = json.loads(request.body)['id']
        item = NonMember.objects.get(pk=id)
        item.delete()
        score = NonMemberItemScore.objects.filter(member__id=id)
        score.delete()
        return HttpResponse("SUCCESS")
    else:
        raise BaseException('不支持GET方法')