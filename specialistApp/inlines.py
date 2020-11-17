from django.contrib import admin
from .models import SpecialistModel


class SpecialistInline(admin.StackedInline):
    model = SpecialistModel
    extra = 0
    # 显示跳转超链接
    show_change_link = True
