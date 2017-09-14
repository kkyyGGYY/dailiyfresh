# coding=utf-8
from django.contrib import admin
from .models import *
# Register your models here.


class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'ttitle']


class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 15

    def isdelete(self, id):
        if self.isdelete:
            return '存在'
        else:
            return '已删除'

    isdelete.short_description = '是否删除'

    list_display = ['id', 'gtitle', 'gprice', 'gunit', 'gclick', 'gkucun', 'isdelete']


admin.site.register(TypeInfo, TypeInfoAdmin)
admin.site.register(GoodsInfo, GoodsInfoAdmin)
