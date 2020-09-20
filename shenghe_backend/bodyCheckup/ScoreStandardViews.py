from django.http import HttpResponse
from .models import *
import json, datetime


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
            case when %s >= biss.lowScore and %s <= biss.highScore then
                'Y'
            when %s <= biss.lowScore and %s >= biss.highScore then
                'Y'
            else
                'N'
            end as inLevel,
            biss.highScore,
            biss.scoreDesc,
            biss.color,
            bim.type,
            bim.unit
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
                "level": [],
                "testDate": datetime.datetime.strftime(item.testDate, "%Y-%m-%d")
            }
            for row in ItemMaster.objects.raw(sql, [score, score, score, score, age, sex, itemId]):
                resultItem["name"] = row.item_name
                resultItem["standardValue"] = row.standardValue
                if row.inLevel == "Y":
                    resultItem["periodType"] = row.periodType
                    resultItem["periodName"] = typeMap[row.periodType]

                resultItem["level"].append({
                    "inLevel": row.inLevel,
                    "periodType": row.periodType,
                    "periodName": typeMap[row.periodType],
                    "lowScore": row.lowScore,
                    "highScore": row.highScore,
                    "scoreDesc": row.scoreDesc.replace("\n", "<br/>"),
                    "color": row.color
                })
                resultItem["type"] = row.type
                resultItem["unit"] = row.unit

            lowestLevel = list(filter(lambda level: level["periodType"] == ItemScoreStandard.typeChoices[0][0], resultItem["level"]))[0]
            highestLevel = list(filter(lambda level: level["periodType"] == ItemScoreStandard.typeChoices[-1][0], resultItem["level"]))[0]

            if lowestLevel["lowScore"] < lowestLevel["highScore"]:
                lowestScore = min(lowestLevel["lowScore"], lowestLevel["highScore"])
                highestScore = max(highestLevel["lowScore"], highestLevel["highScore"])
                if score < lowestScore:
                    lowestLevel["inLevel"] = "Y"
                    resultItem["periodType"] = ItemScoreStandard.typeChoices[0][0]
                    resultItem["periodName"] = typeMap[ItemScoreStandard.typeChoices[0][0]]
                    resultItem["displayScore"] = lowestScore
                if score > highestScore:
                    highestLevel["inLevel"] = "Y"
                    resultItem["periodType"] = ItemScoreStandard.typeChoices[-1][0]
                    resultItem["periodName"] = typeMap[ItemScoreStandard.typeChoices[-1][0]]
                    resultItem["displayScore"] = highestScore
            else:
                # 50米折返跑，数值低反而得分高
                lowestScore = max(lowestLevel["lowScore"], lowestLevel["highScore"])
                highestScore = min(highestLevel["lowScore"], highestLevel["highScore"])
                if score > lowestScore:
                    lowestLevel["inLevel"] = "Y"
                    resultItem["periodType"] = ItemScoreStandard.typeChoices[0][0]
                    resultItem["periodName"] = typeMap[ItemScoreStandard.typeChoices[0][0]]
                    resultItem["displayScore"] = lowestScore
                if score < highestScore:
                    highestLevel["inLevel"] = "Y"
                    resultItem["periodType"] = ItemScoreStandard.typeChoices[-1][0]
                    resultItem["periodName"] = typeMap[ItemScoreStandard.typeChoices[-1][0]]
                    resultItem["displayScore"] = highestScore

            result.append(resultItem)
    return result


def report(request):
    if request.method == "POST":
        data = json.loads(request.body)
        result = {
            "currentTest": [],
            "currentTestDate": "",
            "currentTestDesc": "",
            "latestTest": [],
            "latestTestDate": ""
        }
        if "memberId" in data and data["memberId"]:
            members = list(Member.objects.filter(memberId=data["memberId"]).filter(id__lte=data["id"]).order_by("-id")[:2])
            if len(members) > 0:
                result["currentTest"] = fetchData(members[0])
                result["currentTestDate"] = result["currentTest"][0]["testDate"] if result["currentTest"] else ''
            if len(members) > 1:
                result["latestTest"] = fetchData(members[1])
                result["latestTestDate"] = result["latestTest"][0]["testDate"] if result["latestTest"] else ''
        else:
            nonmember = NonMember.objects.get(pk=data["id"])
            if nonmember:
                result["currentTest"] = fetchData(nonmember)
                result["currentTestDate"] = result["currentTest"][0]["testDate"] if result["currentTest"] else ''
        if result["currentTest"]:
            result["currentTestDesc"] = getAvgScoreDesc(result["currentTest"])

        return HttpResponse(json.dumps(result, ensure_ascii=False))
    else:
        raise BaseException("不支持GET方法")


def getAvgScoreDesc(items):
    items = list(filter(lambda item: item["type"] == 2, items))
    scoreDesc = ItemScoreStandard.scoreLevelDesc
    for item in items:
        item["periodScore"] = scoreDesc[item["periodType"]]["score"]

    total_score = sum(list(map(lambda item: item["periodScore"] , items)))
    score = total_score / len(items)
    final_score = 1 if 1 <= score < 1.5 else 2 if 1.5 <= score < 2.5 else 3 if 2.5 <= score < 3.5 else 4 if 3.5 <= score else 0
    return list(filter(lambda s: s["score"] == final_score , scoreDesc.values()))[0]["desc"]

