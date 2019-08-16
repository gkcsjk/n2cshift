# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date
from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    salary_rate = models.DecimalField(default=9, max_digits=3, decimal_places=1)


class Records(models.Model):
    created_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateField()
    shift = models.CharField(max_length=20)
    machine = models.DecimalField(default=Decimal(0), max_digits=6, decimal_places=2)
    cash = models.DecimalField(default=Decimal(0), max_digits=6, decimal_places=2)
    cards = models.DecimalField(default=Decimal(0), max_digits=6, decimal_places=2)
    receipts = models.DecimalField(default=Decimal(0), max_digits=6, decimal_places=2)
    IOUs = models.DecimalField(default=Decimal(0), max_digits=6, decimal_places=2)
    cards_dtl = models.CharField(max_length=5000)
    receipts_dtl = models.CharField(max_length=5000)
    IOUs_dtl = models.CharField(max_length=5000)


class Salary(models.Model):
    created_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateField(default=date.today)
    start_date = models.DateField(primary_key=True)
    basic_salary = models.DecimalField(default=Decimal(0), max_digits=6, decimal_places=2)
    bonus_salary = models.DecimalField(default=Decimal(0), max_digits=6, decimal_places=2)
    total_salary = models.DecimalField(default=Decimal(0), max_digits=6, decimal_places=2)
    actual_salary = models.DecimalField(default=Decimal(0), max_digits=6, decimal_places=2)
    comments = models.CharField(max_length=500)


class StaffSalary(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    belongs_to = models.ForeignKey(Salary, on_delete=models.CASCADE)
    hours = models.IntegerField(default=0)
    basic_salary = models.DecimalField(max_digits=6, decimal_places=2)
    bonus_salary = models.DecimalField(max_digits=6, decimal_places=2)
    total_salary = models.DecimalField(max_digits=6, decimal_places=2)


class Threshold(models.Model):
    threshold_name = models.CharField(primary_key=True, max_length=20)
    create_time = models.DateField(default=date.today)
    is_active = models.BooleanField(default=False)
    wks_m_10 = models.DecimalField(max_digits=4, decimal_places=0)
    wks_m_20 = models.DecimalField(max_digits=4, decimal_places=0)
    wks_m_50 = models.DecimalField(max_digits=4, decimal_places=0)
    wks_d_10 = models.DecimalField(max_digits=4, decimal_places=0)
    wks_d_20 = models.DecimalField(max_digits=4, decimal_places=0)
    wks_d_50 = models.DecimalField(max_digits=4, decimal_places=0)
    wks_n_10 = models.DecimalField(max_digits=4, decimal_places=0)
    wks_n_20 = models.DecimalField(max_digits=4, decimal_places=0)
    wks_n_50 = models.DecimalField(max_digits=4, decimal_places=0)
    wkd_m_10 = models.DecimalField(max_digits=4, decimal_places=0)
    wkd_m_20 = models.DecimalField(max_digits=4, decimal_places=0)
    wkd_m_50 = models.DecimalField(max_digits=4, decimal_places=0)
    wkd_d_10 = models.DecimalField(max_digits=4, decimal_places=0)
    wkd_d_20 = models.DecimalField(max_digits=4, decimal_places=0)
    wkd_d_50 = models.DecimalField(max_digits=4, decimal_places=0)
    wkd_n_10 = models.DecimalField(max_digits=4, decimal_places=0)
    wkd_n_20 = models.DecimalField(max_digits=4, decimal_places=0)
    wkd_n_50 = models.DecimalField(max_digits=4, decimal_places=0)
