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
from django.forms.models import model_to_dict
from .admin import refreshAge


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
        try:
            data = json.loads(requests.body)
            querysetAll = SpecialistModel.objects.only('id')
            querysetIdList = []
            for q in querysetAll:
                querysetIdList.append(q.id)
            forms = data['data']
            slice = []
            results = []
            for form in forms:
                queryset = SpecialistModel.objects.filter(id__in=querysetIdList)
                realSize = form['size'] * 3
                category = form['selectedValue'].split(" ")[0]
                company = form['company']
                current_query = queryset.filter(Q(spe_ctg1__ctg_code=category) | Q(spe_ctg2__ctg_code=category) | Q(
                    spe_major__ctg_code=category)).exclude(
                    spe_company=company)
                current_query = current_query.distinct()
                formResult = []
                deleteID = []
                if realSize < current_query.count():
                    randList = random.sample(range(current_query.count()), realSize)
                else:
                    randList = range(current_query.count())
                for i in randList:
                    deleteID.append(current_query[i].id)
                    dict = model_to_dict(current_query[i])
                    major = Category.objects.get(id=dict['spe_major'])
                    ctg1 = Category.objects.get(id=dict['spe_ctg1'])
                    ctg2 = Category.objects.get(id=dict['spe_ctg2'])
                    dict['spe_major'] = model_to_dict(major)
                    dict['spe_ctg1'] = model_to_dict(ctg1)
                    dict['spe_ctg2'] = model_to_dict(ctg2)
                    dict['spe_birth'] = dict['spe_birth'].strftime("%Y-%m-%d")
                    formResult.append(dict)
                    querysetIdList.remove(current_query[i].id)
                results.append(formResult)
                # print(results)
                return JsonResponse(results, safe=False)
        except Exception as e:
                return HttpResponse(e)



class PrintView(View):
    CONTENT_TYPE = 'application/octet-stream'
    def get_export_filename(self):
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = "%s-%s.%s" % ("list",
                                 date_str,
                                 'xls')
        return filename

    def post(self, requests):
        try:
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
        except Exception as e:
            return HttpResponse(e)


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
        try:
            file = requests.FILES.get("file", None)
            category = requests.POST.get("selectedValue").split(" ")[1]
            company = requests.POST.get("company")
            queryset = SpecialistModel.objects.filter(
                Q(spe_ctg1__ctg_name=category) | Q(spe_ctg2__ctg_name=category)
            ).exclude(spe_company=company)
            xlsdata = xlrd.open_workbook(file_contents=file.read())
            table = xlsdata.sheet_by_index(0)
            temp = table.col_slice(colx=1, start_rowx=1)
            randomList = []
            for row in temp:
                randomList.append(int(row.value))
            size = len(randomList)
            qs = queryset.filter(spe_code__in=randomList)
            qs.distinct()
            realSize = len(qs)
            if realSize < size:
                benchqs = queryset.exclude(spe_code__in=randomList)[0:size - realSize]
                qs = qs | benchqs
            data = eval(serializers.serialize("json", qs, use_natural_foreign_keys=True))
            return JsonResponse(data, safe=False)
        except Exception as e:
            return HttpResponse(e)


def statisticAgeSpan(queryset):
    ageSpan = {
        "<21": 0,
        "21-30": 0,
        "31-40": 0,
        "41-50": 0,
        "51-60": 0,
        ">60": 0,
    }
    result = []
    for q in queryset:
        age = int(q.spe_age)
        if age in range(1, 20):
            ageSpan["<21"] += 1
        elif age in range(21, 30):
            ageSpan["21-30"] += 1
        elif age in range(31, 40):
            ageSpan["31-40"] += 1
        elif age in range(41, 50):
            ageSpan["41-50"] += 1
        elif age in range(51, 60):
            ageSpan["51-60"] += 1
        elif age in range(61,100):
            ageSpan[">60"] += 1
    for key in ageSpan:
        result.append({
            "name": key,
            "value": ageSpan[key]
        })
    return result


class StatisticView(View):

    def get(self, requests):
        cq = Category.objects.all()
        categories = []
        for c in cq:
            categories.append(c.ctg_code + " " + c.ctg_name)
        ageSpan = statisticAgeSpan(SpecialistModel.objects.all())

        dic = json.dumps({"categories": categories, "ageSpan": ageSpan})
        return render(requests, "admin/statistic.html", {"dic": dic})


class StatisticCategoryView(View):
    def get(self, requests, category):
        try:
            categories = category.split('-')

            major = categories[0]
            ctg1 = categories[1]
            ctg2 = categories[2]
            if major:
                major = major.split(' ')[0]
            if ctg1:
                ctg1 = ctg1.split(' ')[0]
            if ctg2:
                ctg2 = ctg2.split(' ')[0]
            print(ctg1)
            qs = SpecialistModel.objects.filter(
                Q(spe_major__ctg_code=major) | Q(spe_ctg1__ctg_code=ctg1) | Q(spe_ctg2__ctg_code=ctg2))
            print(qs)
            return JsonResponse(json.dumps(statisticAgeSpan(qs)), safe=False)
        except Exception as e:
            return HttpResponse(e)


class CheckView(View):
    def get(self, requests):
        try:
            retired = []
            qs = SpecialistModel.objects.filter(spe_age__gte=60)
            for q in qs:
                retired.append({
                    "name": q.spe_name,
                    "id": q.id,
                })
            return JsonResponse(json.dumps(retired), safe=False)
        except Exception as e:
            return HttpResponse(e)

    def post(self, requests):
        try:
            data = json.loads(requests.body)
            pks = data['data']
            qs = SpecialistModel.objects.filter(id__in=pks).delete()
            return JsonResponse(json.dumps({"": ""}), safe=False)
        except Exception as e:
            return HttpResponse(e)


class refreshAgeView(View):
    def get(self, requests):
        try:
            refreshAge()
            return JsonResponse(json.dumps({"": ""}), safe=False)
        except Exception as e:
            return HttpResponse(e)
