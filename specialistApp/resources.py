from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import SpecialistModel, Category
from django.db import models


class SpecialistResource(resources.ModelResource):
    # 控制外键关系的插件，column_name为导出后表头
    spe_ctg1 = fields.Field(
        column_name="所从事专业1",
        attribute="spe_ctg1",
        widget=ForeignKeyWidget(Category, 'ctg_name')
    )
    spe_ctg2 = fields.Field(
        column_name="所从事专业2",
        attribute="spe_ctg2",
        widget=ForeignKeyWidget(Category, 'ctg_name')
    )
    spe_major = fields.Field(
        column_name="所学专业",
        widget=ForeignKeyWidget(Category,'ctg_name')
    )

    class Meta:
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('id',)
        model = SpecialistModel
        export_order = (
            'id', 'spe_name', 'spe_gender', 'spe_birth', 'spe_company', 'spe_tel', 'spe_title', 'spe_job',
            'spe_station','spe_cid',
            'spe_edu', 'spe_major', 'spe_ctg1', 'spe_ctg2')

    # import—export中文列名的最终解决方案
    @classmethod
    def field_from_django_field(cls, field_name, django_field, readonly):
        FieldWidget = cls.widget_from_django_field(django_field)
        widget_kwargs = cls.widget_kwargs_for_field(field_name)
        field = cls.DEFAULT_RESOURCE_FIELD(
            attribute=field_name,
            # 重写column_name
            column_name=django_field.verbose_name,
            widget=FieldWidget(**widget_kwargs),
            readonly=readonly,
            default=django_field.default,
        )
        return field


class CategoryResource(resources.ModelResource):
    # 控制外键关系的插件，column_name为导出后表头
    class Meta:
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('id',)
        model = Category
    # import—export中文列名的最终解决方案
    @classmethod
    def field_from_django_field(cls, field_name, django_field, readonly):
        FieldWidget = cls.widget_from_django_field(django_field)
        widget_kwargs = cls.widget_kwargs_for_field(field_name)
        field = cls.DEFAULT_RESOURCE_FIELD(
            attribute=field_name,
            # 重写column_name
            column_name=django_field.verbose_name,
            widget=FieldWidget(**widget_kwargs),
            readonly=readonly,
            default=django_field.default,
        )
        return field