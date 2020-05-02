import random

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
import names

from .models import User, Activities
from datetime import datetime, timedelta


TIME_ZONE_LIST = ['America/Los_Angeles', 'Asia/Kolkata']

#CONFIGURABLE NUMBERS
MINIMUM_COUNTS_OF_USERS_TO_GENERATE = 3
MAXIMUM_COUNTS_OF_USERS_TO_GENERATE = 10
MINIMUM_ACIVITY_PERIODS_COUNT = 1
MAXIMUM_ACIVITY_PERIODS_COUNT = 2
MAX_COUNT_OF_EMPLOYESS = 10


#Query the database , get data and parse in desired format
def get_user_activities():
    user_obj = User.objects.all()
    members = []
    final_dict = {}
    for each_user in user_obj:
        activity_periods = []

        user_id = each_user.user_id
        real_name = each_user.real_name
        tz = each_user.tz
        activities_obj = Activities.objects.filter(user_id=user_id)
        for each_activity in activities_obj:
            start_time = change_date_format(each_activity.start_time)
            end_time = change_date_format(each_activity.end_time)
            activity_periods.append({"start_time":start_time, "end_time":end_time})
        members.append({"id":user_id, "real_name":real_name, "tz":tz, "activity_periods":activity_periods})
    final_dict = {"ok":True, "members":members}
    return(final_dict)
        

#to generate the random user_ids
def get_user_id():
    return(''.join(random.choice('0123456789ABCDEFHIGKLMNOPQRSTUVWXYZ') for i in range(9)))

#to generate names of user 
def get_user_name():
    return(names.get_full_name())

#to get random count of activity
def get_random_number(range1, range2):
    return(random.randint(range1, range2))

#to change the datetime to mentioned format
def change_date_format(date_time_obj):
    required_data_obj = date_time_obj.strftime("%b %d %Y %-I:%M%p")
    return required_data_obj

#to generate random start time and end time
def get_timings(acivity_periods_count):
    list_of_timings = []
    for i in range(acivity_periods_count + 1):
        timings = []
        timings = [(datetime.now() - timedelta(days=1,hours=i,minutes=i+3)), (datetime.now() - timedelta(days=i,hours=i+2,minutes=i+8))]
        list_of_timings.append(timings)
    return(list_of_timings)
    
#auto generation of data
def generate_data(request):
    user_obj = User.objects.all()
    if user_obj.count()>MAX_COUNT_OF_EMPLOYESS:
        for each in user_obj:
            each.delete()
        return HttpResponse('Max count of {} reached. Data will be auto reset. Please refresh.'.format(MAX_COUNT_OF_EMPLOYESS + 1))
    user_id = get_user_id()
    real_name = get_user_name()
    tz = random.choice(TIME_ZONE_LIST) 
    acivity_periods_count = get_random_number(MINIMUM_ACIVITY_PERIODS_COUNT, MAXIMUM_ACIVITY_PERIODS_COUNT)
    start_time_end_time = get_timings(acivity_periods_count)
    validate_and_save(user_id, real_name, start_time_end_time,tz)
    
    final_dict = get_user_activities()
    return JsonResponse(final_dict)

#save activities per user 
def save_user_activities(user_id, start_time_end_time):
    for each in start_time_end_time:
        activity = Activities(user_id=user_id, start_time=each[0], end_time=each[1])
        activity.save()

#validate and save users to data base   
def validate_and_save(user_id, real_name, start_time_end_time,tz):
    user_obj = User.objects.filter(user_id=user_id)
    if user_obj:
        # here user already exists with that id , so just add activity timings
        save_user_activities(user_id, start_time_end_time)
    else:
        # new entry, maximum cases
        user = User(user_id=user_id, real_name=real_name, tz=tz)
        user.save()
        save_user_activities(user_id, start_time_end_time)
            
