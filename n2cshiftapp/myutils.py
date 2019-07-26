from django.contrib.auth.models import User
from .models import Salary, StaffSalary, Threshold
from datetime import timedelta
from decimal import Decimal


def list_user_to_tuple():
    users = ()
    for user in User.objects.filter(is_active=True):
        if not user.is_staff:
            users = ((user.username, user.username),) + users
    users = (('all', 'all'),) + users
    return users


def list_user_to_list():
    users = []
    for user in User.objects.filter(is_active=True):
        if not user.is_staff:
            users.append(user.username)
    return users


def queryset_user_active():
    return User.objects.filter(is_active=True)


def bonus_threshold(weekday, shift, rate):
    my_threshold = Threshold.objects.get(is_active=True)
    threshold = {
        'Morning': {
            'weekdays': [my_threshold.wks_m_10, my_threshold.wks_m_20, my_threshold.wks_m_50],
            'weekends': [my_threshold.wkd_m_10, my_threshold.wkd_m_20, my_threshold.wkd_m_50],
            'hours': 7,
            'rate': rate,
        },
        'Dusk': {
            'weekdays': [my_threshold.wks_d_10, my_threshold.wks_d_20, my_threshold.wks_d_50],
            'weekends': [my_threshold.wkd_d_10, my_threshold.wkd_d_20, my_threshold.wkd_d_50],
            'hours': 7,
            'rate': rate,
        },
        'Night': {
            'weekdays': [my_threshold.wks_n_10, my_threshold.wks_n_20, my_threshold.wks_n_50],
            'weekends': [my_threshold.wkd_n_10, my_threshold.wkd_n_20, my_threshold.wkd_n_50],
            'hours': 10,
            'rate': rate + 1,
        },
    }
    if weekday == 5 or weekday == 6:
        wd = 'weekends'
    else:
        wd = 'weekdays'
    th = threshold[shift][wd]
    h = threshold[shift]['hours']
    r = threshold[shift]['rate']
    sl = [Decimal(10), Decimal(20), Decimal(50)]
    return th, h, r, sl


def save_salary_records(display, startdate, user):
    start_date = startdate
    created_date = start_date + timedelta(days=11)
    basic_salary = Decimal(0)
    bonus_salary = Decimal(0)
    for item in display:
        basic_salary += item['basic_salary']
        bonus_salary += item['bonus_salary']
    total_salary = basic_salary + bonus_salary
    mSalary = Salary()
    mSalary.created_user = user
    mSalary.created_time = created_date
    mSalary.start_date = start_date
    mSalary.basic_salary = basic_salary
    mSalary.bonus_salary = bonus_salary
    mSalary.total_salary = total_salary
    mSalary.actual_salary = total_salary
    mSalary.comments="No comments this week."
    mSalary.save()
    return basic_salary, bonus_salary, total_salary


def save_staff_salary_records(display, startdate):
    for item in display:
        mStaffSalary = StaffSalary()
        mStaffSalary.username = User.objects.get(username=item['staff'])
        mStaffSalary.belongs_to = Salary.objects.get(start_date=startdate)
        mStaffSalary.basic_salary = item['basic_salary']
        mStaffSalary.bonus_salary = item['bonus_salary']
        mStaffSalary.total_salary = item['total_salary']
        mStaffSalary.save()