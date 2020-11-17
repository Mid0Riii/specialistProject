from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse, FileResponse
from django.views import View
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Category, SpecialistModel
from django.db.models import Q
import random
from .resources import SpecialistResource
from datetime import datetime
import xlrd

# Create your views here.


class RandomSelectView(View):
    def get(self, requests):
        cq = Category.objects.all()
        categories = []
        for c in cq:
            categories.append(c.ctg_code + " " + c.ctg_name)

        dic = json.dumps({"categories": categories})
        return render(requests, "admin/randomselect.html", {"dic": dic})

    def post(self, requests):
        data = json.loads(requests.body)
        realSize = data['size'] * 3
        category = data['selectedValue'].split(" ")[0]
        company = data['company']
        # 两个查询结果做并集
        queryset = SpecialistModel.objects.filter(
            Q(spe_ctg1__ctg_code=category) | Q(spe_ctg2__ctg_code=category)
        ).exclude(spe_company=company)
        qs = queryset.distinct()
        data = eval(serializers.serialize("json", qs, use_natural_foreign_keys=True))
        if realSize < len(data):
            slice = random.sample(data, realSize)
        else:
            slice = data
        return JsonResponse(slice, safe=False)


class PrintView(View):
    CONTENT_TYPE = 'application/octet-stream'

    def get_export_filename(self):
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = "%s-%s.%s" % ("list",
                                 date_str,
                                 'xls')
        return filename

    def post(self, requests):
        data = json.loads(requests.body)
        pks = data['pks']
        # __in 修饰符表包含关系
        qs = SpecialistModel.objects.filter(id__in=pks)
        dataset = SpecialistResource().export(queryset=qs)
        res = HttpResponse(
            dataset.xls, content_type="application/vnd.ms-excel"
        )
        res['Content-Disposition'] = 'attachment; filename="test.xls"'
        return res


class UploadView(View):

    @method_decorator(csrf_exempt)  # CSRF Token相关装饰器在CBV只能加到dispatch方法上
    def dispatch(self, request, *args, **kwargs):
        return super(UploadView, self).dispatch(request, *args, **kwargs)

    def get(self, requests):
        cq = Category.objects.all()
        categories = []
        for c in cq:
            categories.append(c.ctg_code + " " + c.ctg_name)

        dic = json.dumps({"categories": categories})
        return render(requests, "admin/importfromxls.html", {"dic": dic})

    def post(self, requests):
        file = requests.FILES.get("file",None)
        category = requests.POST.get("selectedValue").split(" ")[1]
        company = requests.POST.get("company")
        queryset = SpecialistModel.objects.filter(
            Q(spe_ctg1__ctg_name=category) | Q(spe_ctg2__ctg_name=category)
        ).exclude(spe_company=company)
        xlsdata = xlrd.open_workbook(file_contents=file.read())
        table = xlsdata.sheet_by_index(0)
        temp = table.col_slice(colx=1,start_rowx=1)
        randomList=[]
        for row in temp:
            randomList.append(int(row.value))
        size = len(randomList)
        qs = queryset.filter(spe_code__in=randomList)
        qs.distinct()
        realSize = len(qs)
        if realSize<size:
            benchqs = queryset.exclude(spe_code__in=randomList)[0:size-realSize]
            qs = qs | benchqs
        data = eval(serializers.serialize("json", qs, use_natural_foreign_keys=True))
        return JsonResponse(data, safe=False)
