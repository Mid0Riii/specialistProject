#!/usr/bin/env python3

"""生成虚拟专家数据"""
import random
import sys
import os
import django
sys.path.append('../../')
os.environ['DJANGO_SETTINGS_MODULE'] = 'specialistProject.settings'
django.setup()

from specialistApp.models import Category as SpecialistCategory
from specialistApp.models import SpecialistModel as Specialist

NAMES = []

def init():
    """初始化"""
    f = open('name.txt', 'r',encoding='utf-8')
    names = f.read()
    ret = names.split('   ')
    for i in ret:
        NAMES.append(i)
    f.close()

    Specialist.objects.all().delete()

def make_name():
    """生成随机姓名"""
    max_num = len(NAMES) - 1
    return NAMES[random.randint(0, max_num)]

def make_sex():
    """生成随机性别"""
    sex = ('男', '女')
    return sex[random.randint(0, 1)]

def make_birth():
    """"生成随机日期"""
    year = random.randint(1970, 1999)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return '' + str(year) + '-' + str(month) + '-' + str(day)

def make_category():
    """"生成随机分类"""
    objs = SpecialistCategory.objects.all()
    max_num = len(objs) - 1
    while True:
        obj = objs[random.randint(0, max_num)]
        if len(obj.ctg_code) == 3:
            continue
        break
    return obj

def make_phone():
    """生成随机手机号"""
    return '13333345544'


def make_email():
    """生成随机邮箱"""
    return 'specialist@email.com'


import random
import time


def regiun():
    '''生成身份证前六位'''
    #列表里面的都是一些地区的前六位号码
    first_list = ['362402','362421','362422','362423','362424','362425','362426','362427','362428','362429','362430','362432','110100','110101','110102','110103','110104','110105','110106','110107','110108','110109','110111']
    first = random.choice(first_list)
    return first

def year():
    '''生成年份'''
    now = time.strftime('%Y')
    #1948为第一代身份证执行年份,now-18直接过滤掉小于18岁出生的年份
    second = random.randint(1948,int(now)-18)
    age = int(now) - second
    return second


def month():
    '''生成月份'''
    three = random.randint(1,12)
    #月份小于10以下，前面加上0填充
    if three < 10:
        three = '0' + str(three)
        return three
    else:
        return three


def day():
    '''生成日期'''
    four = random.randint(1,28)
    #日期小于10以下，前面加上0填充
    if four < 10:
        four = '0' + str(four)
        return four
    else:
        return four


def randoms():
    '''生成身份证后四位'''
    #后面序号低于相应位数，前面加上0填充
    five = random.randint(1,9999)
    if five < 10:
        five = '000' + str(five)
        return five
    elif 10 < five < 100:
        five = '00' + str(five)
        return five
    elif 100 < five < 1000:
        five = '0' + str(five)
        return five
    else:
        return five



def make_cid():
    """生成随机身份证"""
    first = regiun()
    second = year()
    three = month()
    four = day()
    last = randoms()
    print(str(first) + str(second) + str(three) + str(four) + str(last))
    return str(first) + str(second) + str(three) + str(four) + str(last)


def make_data():
    """创建一个伪造数据"""
    obj = Specialist()
    obj.spe_name = make_name()
    obj.spe_gender = make_sex()
    obj.spe_birth = make_birth()
    obj.spe_major = make_category()
    obj.spe_ctg1 = make_category()
    obj.spe_ctg2 = make_category()
    obj.spe_tel = make_phone()
    obj.spe_cid=make_cid()
    obj.save()

def make_data_set(num):
    """创建 num 个伪造数据"""
    while num:
        make_data()
        num = num - 1

def main():
    """main"""
    init()
    num = input('请输入要生成的数据条数：')
    make_data_set(int(num))

if __name__ == "__main__":
    main()
