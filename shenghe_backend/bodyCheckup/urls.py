from django.urls import path

from . import ItemMasterViews, CommonViews, ItemDetailViews, ScoreStandardViews, NonmemberScoreViews, MemberScoreViews

urlpatterns = [
    # API
    path('api/itemtype', CommonViews.itemType, name='apiItemType'),
    path('api/periodtype', CommonViews.periodType, name='apiPeriodType'),
    path('api/channel', CommonViews.channel, name='channel'),

    # ItemMaster
    path('itemmaster', ItemMasterViews.find, name='itemMaster'),
    path('itemmaster/insert', ItemMasterViews.insert, name='insertItemMaster'),
    path('itemmaster/update', ItemMasterViews.update, name='updateItemMaster'),

    # ItemDetail
    path('itemdetail/master', ItemDetailViews.findMaster, name='itemMaster'),
    path('itemdetail', ItemDetailViews.find, name='index'),
    path('itemdetail/insert', ItemDetailViews.insert, name='insertItemDetail'),
    path('itemdetail/delete', ItemDetailViews.delete, name='deleteItemDetail'),
    path('itemdetail/update', ItemDetailViews.update, name='updateItemDetail'),

    # ScoreStandardViews
    path('scorestandard/master', ScoreStandardViews.findMaster, name='itemMaster'),
    path('scorestandard', ScoreStandardViews.find, name='index'),
    path('scorestandard/insert', ScoreStandardViews.insert, name='insertScoreStandard'),
    path('scorestandard/update', ScoreStandardViews.update, name='updateScoreStandard'),
    # report
    path('report', ScoreStandardViews.report, name='report'),

    # NonmemberScoreView
    path('nonmember/master', NonmemberScoreViews.findMaster, name='itemMaster'),
    path('nonmember', NonmemberScoreViews.find, name='index'),
    path('nonmember/insert', NonmemberScoreViews.insert, name='insertNonmember'),
    path('nonmember/update', NonmemberScoreViews.update, name='updateNonmember'),
    path('nonmember/score', NonmemberScoreViews.score, name='selectNonmemberScore'),
    path('nonmember/delete', NonmemberScoreViews.delete, name='deleteMember'),

    # memberScoreView
    path('member/master', MemberScoreViews.findMaster, name='itemMaster'),
    path('member', MemberScoreViews.find, name='index'),
    path('member/insert', MemberScoreViews.insert, name='insertMember'),
    path('member/update', MemberScoreViews.update, name='updateMember'),
    path('member/score', MemberScoreViews.score, name='selectMemberScore'),
    path('member/delete', MemberScoreViews.delete, name='deleteMember'),

]