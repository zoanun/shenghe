
items = [
'体重',
'立定跳远',
'体前屈',
'仰卧起坐',
'一分钟跳绳',
'身高'
]
for item in items:
    for age in range(4,13):
        for sex in ['男', '女']:
            print('{}\t{}\t{}'.format(item, age, sex))