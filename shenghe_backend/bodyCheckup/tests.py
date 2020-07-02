from django.test import TestCase

# Create your tests here.
typeChoices = (
    ('SUPERLOWER', '超低'),
    ('LOWER', '偏低'),
    ('NORMAL', '正常'),
    ('HIGH', '偏高'),
    ('SUPERHIGH', '超高'),
)
print(len(list(filter(lambda x: x[0] == 'SUPERLOWER', typeChoices))))