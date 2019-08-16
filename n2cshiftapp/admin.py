# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *


class RecordsAdmin(admin.ModelAdmin):
    list_display = ('created_user', 'created_time', 'shift', 'machine')
    list_display_links = ('created_user', 'created_time')
    list_per_page = 21


class SalaryAdmin(admin.ModelAdmin):
    list_per_page = 5
    list_display = ('created_time', 'start_date', 'actual_salary')


class UserInfoAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = ('user', 'salary_rate')


class ThreshHoldAdmin(admin.ModelAdmin):
    list_display = ('threshold_name', 'is_active')
    list_per_page = 50


class StaffSalaryAdmin(admin.ModelAdmin):
    list_display = ('username', 'belongs_to', 'basic_salary', 'bonus_salary', 'total_salary')


admin.site.register(Records, RecordsAdmin)
admin.site.register(Salary, SalaryAdmin)
admin.site.register(StaffSalary, StaffSalaryAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Threshold, ThreshHoldAdmin)