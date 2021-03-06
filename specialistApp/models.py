from django.db import models
from utils.modeltool import set_choices
from django.core.validators import MaxLengthValidator, MinLengthValidator
import datetime


def calculate_age(born):
    today = datetime.date.today()
    try:
        birthday = born.replace(year=today.year)
    except ValueError:  # raised when birth date is February 29 and the current year is not a leap year
        birthday = born.replace(year=today.year, month=born.month + 1, day=1)
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year


class Category(models.Model):
    ctg_name = models.CharField(verbose_name="分类名", max_length=128, unique=True)
    ctg_code = models.CharField(verbose_name="分类编号", max_length=128)

    class Meta:
        verbose_name = "分类信息"
        verbose_name_plural = verbose_name
        unique_together = (('ctg_name', 'ctg_code'),)

    def __str__(self):
        return str(self.ctg_code) + "-" + str(self.ctg_name)

    def natural_key(self):
        return self.ctg_code + " " + self.ctg_name


class SpecialistModel(models.Model):
    spe_name = models.CharField(verbose_name="姓名", max_length=128)
    spe_gender = models.CharField(verbose_name="性别", max_length=128, choices=set_choices(['女', '男']))
    spe_birth = models.DateField(verbose_name="出生年月", null=True, blank=True)
    spe_cid = models.CharField(verbose_name="身份证号", max_length=128, blank=True,
                               validators=[MaxLengthValidator(18), MinLengthValidator(18)], default='0')
    spe_age = models.IntegerField(verbose_name="年龄",  blank=True, default='0')
    spe_company = models.CharField(verbose_name="工作单位", max_length=128, default="空")
    spe_tel = models.CharField(verbose_name="联系电话", max_length=128, default="空")
    spe_title = models.CharField(verbose_name="职称", max_length=128, default="空")
    spe_job = models.CharField(verbose_name="职务", max_length=128, default="空")
    spe_station = models.CharField(verbose_name="受聘岗位", max_length=128,
                                   choices=set_choices(['专业技术', '管理', '工勤', '双肩挑']), default="专业技术")
    spe_edu = models.CharField(verbose_name="学历", max_length=128, default="空")
    spe_major = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='spe_major', verbose_name="所学专业", )
    spe_ctg1 = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="所从事专业一", related_name="spe_ctg1")
    spe_ctg2 = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="所从事专业二", related_name="spe_ctg2")
    spe_code = models.IntegerField(verbose_name="随机序号", default=0)
    spe_info = models.TextField(verbose_name="备注", blank=True)

    class Meta:
        verbose_name = "考官信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.spe_name)

    def save(self, **kwargs):
        birth = self.spe_cid[6:14]
        birthDate = datetime.date(int(birth[0:4]),int(birth[4:6]),int(birth[6:8]))
        self.spe_birth = birthDate
        self.spe_age = int(calculate_age(birthDate))
        super(SpecialistModel, self).save()
