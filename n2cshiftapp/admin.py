# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *

admin.site.register(Records)
admin.site.register(Salary)
admin.site.register(StaffSalary)
admin.site.register(UserInfo)

