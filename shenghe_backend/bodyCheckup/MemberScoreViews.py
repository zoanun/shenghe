from django.http import HttpResponse
from .models import *
import json


def findMaster(request):
    '''
    找到右边需要填写的项目
    :param request:
    :return:
    '''
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
    '''
    找到左边的已经测试过的人员名单
    :param request:
    :return:
    '''
    if request.method == 'GET':
        memberId = request.GET['memberId']
        age = request.GET['age']
        sex = request.GET['sex']
        name = request.GET['name']
        result = Member.objects.all()
        if memberId:
            result = result.filter(memberId=memberId)
        if age:
            result = result.filter(age=age)
        if not (not sex or sex == 'A'):
            result = result.filter(sex=sex)
        if name:
            result = result.filter(name__contains=name)
        result = result.order_by('-id')
        result = result.values('id', 'memberId', 'age', 'sex', 'name')
        return HttpResponse(json.dumps(list(result), ensure_ascii=False))
    else:
        raise BaseException('不支持POST方法')


def score(request):
    if request.method == 'GET':
        id = request.GET['id']
        sex = request.GET['sex']
        age = request.GET['age']
        searchDict = {
            'member_id': id,
            'item__itemdetail__age': age,
            'item__itemdetail__sex': sex
        }
        result = MemberItemScore.objects.filter(**searchDict)
        result = result.values('id', 'item__id', 'item__name', 'item__itemdetail__value', 'score')
        result = list(map(lambda r: {'id': r['id'], 'itemId': r['item__id'], 'name': r['item__name'], 'value': r['item__itemdetail__value'], 'score': r['score']}, result))
        return HttpResponse(json.dumps(result, ensure_ascii=False))
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
        member.name = data['name'] if 'name' in data else ''
        member.save()

        for item in items:
            if 'score' in item:
                score = MemberItemScore()
                score.item = ItemMaster.objects.get(pk=item['id'])
                score.member = member
                score.score = item['score']
                score.save()

        return HttpResponse("SUCCESS")
    else:
        raise BaseException('不支持GET方法')


def update(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        items = data['items']
        if len(items) == 0:
            return HttpResponse("FAIL")

        member = Member.objects.get(pk=data['id'])
        member.age = data['age']
        member.sex = data['sex']
        member.name = data['name']
        member.save()

        for item in items:
            score = MemberItemScore.objects.get(pk=item['id'])
            if item['score']:
                score.score = item['score']
                score.save()
            else:
                score.delete()

        return HttpResponse("SUCCESS")
    else:
        raise BaseException('不支持GET方法')


def delete(request):
    if request.method == 'POST':
        id = json.loads(request.body)['id']
        item = Member.objects.get(pk=id)
        item.delete()
        score = MemberItemScore.objects.filter(member__id=id)
        score.delete()
        return HttpResponse("SUCCESS")
    else:
        raise BaseException('不支持GET方法')