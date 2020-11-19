from django.contrib import admin
from .models import Category, SpecialistModel
from django.contrib.admin import helpers, widgets
from .inlines import SpecialistInline
from .resources import SpecialistResource, CategoryResource
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from django.contrib import messages
from django.shortcuts import render
import random
from .models import calculate_age


def refreshAge():
    # pass
    qs = SpecialistModel.objects.all()
    for q in qs:
        q.spe_age = calculate_age(q.spe_birth)
        q.save()


# Register your models here.
@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    # inlines = [SpecialistInline]
    resource_class = CategoryResource
    list_display = ['ctg_code', 'ctg_name']
    list_filter = list_display
    search_fields = ['ctg_code', 'ctg_name']


@admin.register(SpecialistModel)
class SpecialistAdmin(ImportExportModelAdmin):
    # 分页器在分类菜单下存在bug，设置最大显示数量
    list_per_page = 2048
    resource_class = SpecialistResource
    list_display = ['spe_name', 'spe_gender', 'spe_birth', 'spe_cid', 'spe_company', 'spe_ctg1', 'spe_ctg2',
                    'spe_info']
    list_filter = ['spe_code', 'spe_name', 'spe_gender', 'spe_birth', 'spe_cid', 'spe_company', 'spe_tel', 'spe_title',
                   'spe_job',
                   'spe_station', 'spe_edu', 'spe_major', 'spe_ctg1__ctg_name', 'spe_ctg2__ctg_name']
    autocomplete_fields = ['spe_ctg1', 'spe_ctg2']
    actions = ['generate_random_code']

    def changelist_view(self, request, extra_context=None):
        if 'action' in request.POST and request.POST['action'] == 'generate_random_code':
            if not request.POST.getlist(helpers.ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                type = request.get_full_path().split("/")[-1][1:]
                type = type.split("=")[-1]
                qs = SpecialistModel.objects.filter(spe_ctg1__id=type)
                for u in qs:
                    post.update({helpers.ACTION_CHECKBOX_NAME: str(u.id)})
                request._set_post(post)
        return super(SpecialistAdmin, self).changelist_view(request, extra_context)

    def generate_random_code(self, request, queryset):
        type = request.get_full_path().split("/")[-1][1:]
        type = type.split("=")[-1]
        qs = SpecialistModel.objects.filter(spe_ctg1__id=type)
        length = len(qs)
        L1 = random.sample(range(1, length + 1), length)
        for i in range(0, length):
            q = qs[i]
            q.spe_code = L1[i]
            q.save()
        messages.add_message(request, messages.SUCCESS, '操作成功')

    def get_queryset(self, request):
        # refreshAge()
        return SpecialistModel.objects.all()

    generate_random_code.short_description = '生成随机序号'
    generate_random_code.confirm = "是否要对选定的专家生成序号"


admin.site.site_header = '考官抽取系统'
admin.site.site_title = "考官抽取系统"
