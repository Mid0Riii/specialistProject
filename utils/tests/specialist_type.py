#!/usr/bin/env python3
"""自动化生成数据库中的专家分类表"""

import re

import sys
import os
import django
sys.path.append('../../')
os.environ['DJANGO_SETTINGS_MODULE'] = 'specialistProject.settings'
django.setup()

from specialistApp.models import Category


def main():
    """main"""
    with open("categories-simple.txt", "r",encoding='utf-8') as f:
        for line in f.readlines():
            print(line)
            key = line.split(" ")[0]
            val = line.split(" ")[1]
            obj = Category(ctg_code=key, ctg_name=val)
            obj.save()

if __name__ == "__main__":
    main()
