from django.http import HttpResponse
from .models import *
import json


def findMaster(request):
    if request.method == "GET":
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
        age = request.GET["age"]
        sex = request.GET["sex"]
        for row in ItemDetail.objects.raw(sql, [age, age, sex, sex, sex]):
            result.append(
                {"id": row.id, "type": row.type, "name": row.name, "value": row.value, "sex": row.sex, "age": row.age}
            )
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    else:
        raise BaseException("不支持POST方法")


def find(request):
    if request.method == "GET":
        itemDetailId = request.GET["itemDetailId"]
        result = ItemScoreStandard.objects.filter(itemDetail__id=itemDetailId)
        result = [r.getDict() for r in result]
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    else:
        raise BaseException("不支持POST方法")


def insert(request):
    if request.method == "POST":

        data = json.loads(request.body)
        itemDetailId = data["itemDetailId"]
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
            opss.lowScore = data["data"][type[0] + "_lowScore"]
            opss.highScore = data["data"][type[0] + "_highScore"]
            opss.scoreDesc = data["data"][type[0] + "_scoreDesc"]
            opss.color = data["data"][type[0] + "_color"]
            opss.save()
        return HttpResponse("SUCCESS")
    else:
        raise BaseException("不支持GET方法")


def update(request):
    return insert(request)


def fetchData(data):
    items = data.items.all()
    sql = '''
        select 
            bim.id,
            bim.name as item_name,
            bid.age,
            bid.sex,
            bid.value as standardValue,
            biss.periodType,
            biss.lowScore,
            case when %s > biss.lowScore and %s <= biss.highScore then
                'Y'
            else
                'N'
            end as inLevel,
            biss.highScore,
            biss.scoreDesc,
            biss.color
        from
            bodyCheckup_itemmaster bim,
            bodyCheckup_itemdetail bid,
            bodyCheckup_itemscorestandard biss
        where bid.id = biss.itemDetail_id
            and bim.id = bid.item_id
            and bid.age = %s 
            and bid.sex = %s
            and bid.item_id = %s
            and date('now') between bid.staDate and bid.endDate
    '''
    age = data.age
    sex = data.sex
    result = []
    typeMap = {k: v for k,v in ItemScoreStandard.typeChoices}
    for item in items:
        if item.score:
            score = item.score
            itemId = item.item.id
            resultItem = {
                "id": itemId,
                "score": score,
                "displayScore": score,
                "itemId": itemId,
                "age": age,
                "sex": sex,
                "level": []
            }
            for row in ItemMaster.objects.raw(sql, [score, score, age, sex, itemId]):
                resultItem["name"] = row.item_name
                resultItem["standardValue"] = row.standardValue
                if row.inLevel == "Y":
                    resultItem["periodType"] = row.periodType

                resultItem["level"].append({
                    "inLevel": row.inLevel,
                    "periodType": row.periodType,
                    "periodName": typeMap[row.periodType],
                    "lowScore": row.lowScore,
                    "highScore": row.highScore,
                    "scoreDesc": row.scoreDesc.replace("\n", "<br/>"),
                    "color": row.color
                })
            lowest = list(filter(lambda level: level["periodType"] == ItemScoreStandard.typeChoices[0][0], resultItem["level"]))[0]
            highest = list(filter(lambda level: level["periodType"] == ItemScoreStandard.typeChoices[-1][0], resultItem["level"]))[0]
            if score < lowest["lowScore"]:
                lowest["inLevel"] = "Y"
                resultItem["periodType"] = ItemScoreStandard.typeChoices[0][0]
                resultItem["displayScore"] = lowest["lowScore"]
            if score > highest["highScore"]:
                highest["inLevel"] = "Y"
                resultItem["periodType"] = ItemScoreStandard.typeChoices[-1][0]
                resultItem["displayScore"] = highest["highScore"]
            result.append(resultItem)
    return result


def report(request):
    if request.method == "POST":
        data = json.loads(request.body)
        result = {
            "current_test": [],
            "current_test_desc": "",
            "latest_test": []
        }
        if "memberId" in data:
            members = list(Member.objects.filter(memberId=data["memberId"]).filter(id_lte=data["id"]).order_by("-id")[:2])
            result["current_test"] = fetchData(members[0])
            result["latest_test"] = fetchData(members[1])
        else:
            nonmember = NonMember.objects.get(pk=data["id"])
            result["current_test"] = fetchData(nonmember)
        result["current_test_desc"] = getAvgScoreDesc(result["current_test"])

        return HttpResponse(json.dumps(result, ensure_ascii=False))
    else:
        raise BaseException("不支持GET方法")


def getAvgScoreDesc(items):
    scoreDesc = ItemScoreStandard.scoreDesc
    total_score = sum(list(map(lambda item: scoreDesc[item["periodType"]]["score"] if item["inLevel"] == "Y" else 0 , items)))
    score = total_score / len(items)
    return list(filter(lambda s: s["score"] == score , scoreDesc.values()))[0]["desc"]

