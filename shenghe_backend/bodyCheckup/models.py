from django.utils import timezone
from django.db import models

from .BaseModel import BaseModel

class ItemMaster(BaseModel):
    """
    国家标准项目管理
    """
    id = models.AutoField(primary_key=True)
    typeChoices = (
        (1, '体质类'),
        (2, '体能类')
    )
    type = models.IntegerField('项目类型', choices=typeChoices)

    name = models.CharField(verbose_name='项目名', max_length=100)
    nonmemberUseYn = models.CharField(verbose_name='非会员是否使用', choices=(('Y', '使用'), ('N', '不使用')), max_length=1)
    memberUseYn = models.CharField('会员是否使用', choices=(('Y', '使用'), ('N', '不使用')), max_length=1)
    useYn = models.CharField('该项目是否使用', choices=(('Y', '使用'), ('N', '不使用')), max_length=1)


class ItemDetail(BaseModel):
    """
    项目细节数据
    """
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, verbose_name="项目")
    staDate = models.DateField('适用开始日期', default=timezone.now)
    endDate = models.DateField('适用结束日期', default=timezone.now)
    age = models.IntegerField('年龄')
    sex = models.CharField(choices=(('M', '男'), ('F', '女')), max_length=1)
    value = models.FloatField('数值', default=0)


class ItemScoreStandard(BaseModel):
    """
    每个项目的打分标准
    """
    id = models.AutoField(primary_key=True)
    itemDetail = models.ForeignKey(ItemDetail, on_delete=models.CASCADE, verbose_name="项目")
    typeChoices = (
        ('FAILED', '不及格'),
        ('PASS', '及格'),
        ('GOOD', '良好'),
        ('EXCELLENT', '优秀'),
    )
    periodType = models.CharField(max_length=10, choices=typeChoices)
    lowScore = models.FloatField('范围开始值')
    highScore = models.FloatField('范围结束值')
    scoreDesc = models.TextField('评价')
    color = models.CharField(max_length=10, verbose_name='颜色')


class NonMember(BaseModel):
    """
    非会员
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='姓名', max_length=20)
    age = models.IntegerField('年龄')
    sex = models.CharField(choices=(('M', '男'), ('F', '女')), max_length=1)
    referee = models.CharField(verbose_name='推荐人', max_length=20)

    channelChoices = (
        ('EMPLOYEE', '员工获取'),
        ('STUDENT', '学员转介绍'),
        ('ACTIVE', '主动来访'),
        ('PUBLIC', '公众号'),
    )
    channel = models.CharField(choices=channelChoices, verbose_name='渠道', max_length=10)


class NonMemberItemScore(BaseModel):
    """
        每个项目的打分标准
        """
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, verbose_name="项目")
    score = models.FloatField('得分')
    member = models.ForeignKey(NonMember, on_delete=models.CASCADE, verbose_name="非会员")
    testDate = models.DateField('测试日期', default=timezone.now)


class Member(BaseModel):
    """
    会员
    """
    id = models.AutoField(primary_key=True)
    memberId = models.CharField(verbose_name='会员ID', max_length=30)
    name = models.CharField(verbose_name='姓名', max_length=20)
    age = models.IntegerField('年龄')
    sex = models.CharField(choices=(('M', '男'), ('F', '女')), max_length=1)
    testDate = models.DateField('测试日期', default=timezone.now)


class MemberItemScore(BaseModel):
    """
    项目的得分
    """
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, verbose_name="项目")
    score = models.FloatField('得分')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name="会员")
    testDate = models.DateField('测试日期', default=timezone.now)
