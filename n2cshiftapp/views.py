# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta, date
from decimal import *

from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib import messages
from n2cshiftapp import myutils
from .forms import *
from .models import *

import sys


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'GET':
            form = ShiftForm()
            return render(request, 'index.html', {
                'user': request.user,
                'form': form,
                'is_staff': request.user.is_staff
            }, )
        else:
            form = ShiftForm(request.POST)
            if form.is_valid():
                mRecords = Records()
                mRecords.created_user = request.user
                mRecords.created_time = form.cleaned_data['date']
                mRecords.shift = form.cleaned_data['shift']
                mRecords.machine = form.cleaned_data['machine']
                mRecords.cash = form.cleaned_data['cash']
                mRecords.cards = form.cleaned_data['cards']
                mRecords.receipts = form.cleaned_data['receipts']
                mRecords.IOUs = form.cleaned_data['IOUs']
                mRecords.cards_dtl = form.cleaned_data['cards_dtl']
                mRecords.receipts_dtl = form.cleaned_data['receipts_dtl']
                mRecords.IOUs_dtl = form.cleaned_data['IOUs_dtl']
                mRecords.save()
                return render(request, 'index.html', {'info': True})
            else:
                return render(request, 'index.html', {'form': form, 'info': False})


def login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})

    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                # will logout after 1200 seconds
                request.session.set_expiry(1200)
                return redirect('index')
            else:
                return render(request, 'registration/login.html', {
                    'form': form,
                    'password_is_wrong': True,
                })
        else:
            return render(request, 'registration/login.html', {'form': form})


def logout(request):
    auth.logout(request)
    return redirect('login')


def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'GET':
            form = ChangePWForm()
            form2 = StaffQueryForm()
            return render(request, 'registration/profile.html', {
                'form': form,
                'form2': form2,
                'user': request.user,
            })


def changepw(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            form = ChangePWForm(request.POST)
            form2 = StaffQueryForm()
            if form.is_valid():
                old_password = form.cleaned_data['old_password']
                new_password = form.cleaned_data['new_password']
                new_password_2 = form.cleaned_data['new_password_2']
                user = auth.authenticate(username=request.user.username, password=old_password)
                if user is not None and new_password == new_password_2:
                    user.set_password(new_password)
                    user.save()
                    messages.info(request, "Your password has been changed!")
                    return redirect('login')
                else:
                    return render(request, 'registration/profile.html', {
                        'form': form,
                        'form2': form2,
                        'change_unsuccessful': True,
                        'user': request.user.username
                    })
            else:
                return render(request, 'registration/profile.html', {
                    'form': form,
                    'form2': form2,
                    'user': request.user.username
                })


def salary_staff_query(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            display = []
            form = ChangePWForm()
            form2 = StaffQueryForm(request.POST)
            if form2.is_valid():
                start_date = form2.cleaned_data['start_date']
                end_date = form2.cleaned_data['end_date']
                if end_date is None:
                    end_date = date.today()
                if start_date is None:
                    results = StaffSalary.objects.filter(
                        username=request.user,
                        belongs_to__start_date__lte=end_date,
                    )
                else:
                    results = StaffSalary.objects.filter(
                        username=request.user,
                        belongs_to__start_date__gte=start_date,
                        belongs_to__start_date__lte=end_date,
                    )
                for result in results.order_by('belongs_to__created_time'):
                    from_date = result.belongs_to.start_date
                    to_date = from_date + timedelta(days=6)
                    release_date = result.belongs_to.created_time
                    display_dict = {
                        'from_date': from_date,
                        'to_date': to_date,
                        'release_date': release_date,
                        'basic_salary': result.basic_salary,
                        'bonus_salary': result.bonus_salary,
                        'total_salary': result.total_salary,
                    }
                    display.append(display_dict)
                return render(request, 'registration/profile.html', {
                    'form': form,
                    'form2': form2,
                    'user': request.user.username,
                    'display': display,
                    'query_sucessful': True,
                })
            else:
                return render(request, 'registration/profile.html', {
                    'form': form,
                    'form2': form2,
                    'change_unsuccessful': False,
                    'user': request.user.username,
                    'query_staff_salary_unsuccessful': True,
                })


def query(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if not request.user.is_staff:
            return redirect('profile')
        else:
            if request.method == 'GET':
                form = QueryForm()
                return render(request, 'query.html', {
                    'not_authenticated': False,
                    'form': form,
                })
            else:
                form = QueryForm(request.POST)
                if form.is_valid():
                    staff = form.cleaned_data['staff']
                    start_date = form.cleaned_data['start_date']
                    end_date = form.cleaned_data['end_date']
                    if end_date is None:
                        if staff == 'all':
                            result = Records.objects.filter(created_time=start_date)
                        else:
                            result = Records.objects.filter(created_user__username__contains=staff)
                    else:
                        if staff == 'all':
                            result = Records.objects.filter(
                                created_time__gte=start_date,
                                created_time__lte=end_date,
                            )
                        else:
                            result = Records.objects.filter(
                                created_time__gte=start_date,
                                created_time__lte=end_date,
                                created_user__username__contains=staff,
                            )
                    result = result.order_by('created_time')
                    display = []

                    for item in result:
                        item_dict = {}
                        item_dict['staff'] = item.created_user
                        item_dict['date'] = item.created_time
                        item_dict['shift'] = item.shift
                        item_dict['machine'] = item.machine
                        item_dict['cash'] = item.cash
                        item_dict['card'] = item.cards
                        item_dict['receipts'] = item.receipts
                        item_dict['IOU'] = item.IOUs
                        item_dict['total'] = item.cash + item.cards + item.receipts + item.IOUs
                        item_dict['comments'] = \
                            '刷卡:' + item.cards_dtl \
                            + '\n' + '支出:' + item.receipts_dtl \
                            + '\n' + '欠条:' + item.IOUs_dtl
                        display.append(item_dict)
                    return render(request, 'query.html', {
                        'form': form,
                        'result': display,
                        'query_successful': True,
                    })
                else:
                    return render(request, 'query.html', {'form': form})


def salary(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_staff:
        return redirect('profile')
    if request.method == 'GET':
        form = SearchSalaryForm()
        return render(request, 'salary.html', {'form': form})
    else:
        form = SearchSalaryForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            change_total_to = form.cleaned_data['change_total_to']
            comments = form.cleaned_data['comments']
            type = form.cleaned_data['type']
            display = []
            actual_total = Decimal(0)
            display_comments = ""

            # IF Not Select write into database
            if not type:
                print("Load records from database")
                mySalary = Salary.objects.get(start_date=start_date)
                created_by = mySalary.created_user.username
                created_time = mySalary.created_time
                total_bscs = mySalary.basic_salary
                total_bnss = mySalary.bonus_salary
                total_ttls = mySalary.total_salary
                actual_total = mySalary.actual_salary
                display_comments = mySalary.comments
                for user in myutils.list_user_to_list():
                    myStaffSalary = StaffSalary.objects.get(
                        username__username=user,
                        belongs_to=mySalary
                    )
                    display_dict = {
                        'staff': myStaffSalary.username.username,
                        'basic_salary': myStaffSalary.basic_salary,
                        'bonus_salary': myStaffSalary.bonus_salary,
                        'total_salary': myStaffSalary.total_salary,
                    }
                    display.append(display_dict)

            else:
                # IF This week has NOT been recorded
                if not Salary.objects.filter(start_date=start_date):
                    # Each User Salary
                    for user in myutils.list_user_to_list():
                        user_basic_salary = Decimal(0)
                        user_bonus_salary = Decimal(0)
                        user_shifts = ""
                        records = Records.objects.filter(
                            created_time__gte=start_date,
                            created_time__lte=end_date,
                            created_user__username__contains=user,
                        )

                        # Each Shift Salary
                        for record in records:
                            turnover = record.machine
                            weekday = record.created_time.isoweekday()
                            shift = record.shift
                            salary_rate = UserInfo.objects.get(user__username=user).salary_rate
                            threshold, hours, rate, salary_limit = myutils.bonus_threshold(weekday, shift, salary_rate)
                            basic_salary = hours * rate
                            sys.stderr.write('msg')
                            if turnover < threshold[0]:
                                bonus_salary = Decimal(0)
                            elif threshold[0] <= turnover < threshold[1]:
                                bonus_salary = salary_limit[0]
                            elif threshold[1] <= turnover < threshold[2]:
                                bonus_salary = salary_limit[1]
                            else:
                                bonus_salary = salary_limit[2]
                            user_basic_salary += basic_salary
                            user_bonus_salary += bonus_salary
                            user_shifts = user_shifts + '; ' + shift

                        user_total_salary = user_basic_salary + user_bonus_salary
                        display_dict = {
                            'staff': user,
                            'basic_salary': user_basic_salary,
                            'bonus_salary': user_bonus_salary,
                            'total_salary': user_total_salary,
                        }
                        display.append(display_dict)
                    created_by = request.user.username
                    created_time = start_date + timedelta(days=11)

                    # Save the results to database
                    # get the total data for this week
                    total_bscs, total_bnss, total_ttls = myutils.save_salary_records(display, start_date, request.user)
                    myutils.save_staff_salary_records(display, start_date)
                    actual_total = total_ttls

                # IF This week has been recorded already
                else:
                    mySalary = Salary.objects.get(start_date=start_date)
                    created_by = mySalary.created_user.username
                    created_time = mySalary.created_time
                    total_bscs = mySalary.basic_salary
                    total_bnss = mySalary.bonus_salary
                    total_ttls = mySalary.total_salary
                    display_comments = mySalary.comments
                    for user in myutils.list_user_to_list():
                        myStaffSalary = StaffSalary.objects.get(
                            username__username=user,
                            belongs_to=mySalary
                        )
                        display_dict = {
                            'staff': myStaffSalary.username.username,
                            'basic_salary': myStaffSalary.basic_salary,
                            'bonus_salary': myStaffSalary.bonus_salary,
                            'total_salary': myStaffSalary.total_salary,
                        }
                        display.append(display_dict)

                    if change_total_to is not None and comments is not None:
                        mySalary = Salary.objects.get(start_date=start_date)
                        mySalary.comments = comments
                        mySalary.actual_salary = change_total_to
                        mySalary.save()
                        actual_total = change_total_to
                        display_comments = comments
                    else:
                        actual_total = total_ttls

            # Return render to show salary page
            return render(request, 'salary.html', {
                'form': form,
                'display': display,
                'search_successful': True,
                'created_by': created_by,
                'created_time': created_time,
                'total_bscs': total_bscs,
                'total_bnss': total_bnss,
                'total_tlls': total_ttls,
                'change_tll_to': actual_total,
                'comments': display_comments,
            })
        else:
            return render(request, 'salary.html', {'form': form})


def manage(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_staff:
        return redirect('profile')
    if request.method == 'GET':
        return render(request, 'manage.html', {
            'user': request.user.username,
        })
