from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import *
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse,JsonResponse
import json


@login_required(login_url='/')
# Bus Modules
def VIEW_BUS(request):
    driver = CustomUser.objects.get(id=request.user.id,user_type=4)
    driver_id = driver.id
    route_id = driver.route
    bus = Bus.objects.get(users=driver_id)
    destination = bus.destination
    users=CustomUser.objects.filter(Q(destination=destination) & (Q(user_type=2) | Q(user_type=3)))
    context = {
        'users':users,
        'driver': driver,
        'bus' : bus
    }

    return render(request, 'Drivers/view_bus.html', context)



# Feedback Modules
def FEEDBACK_VIEW(request):
    feedback = Feedback.objects.all()

    context = {
        'feedback': feedback,
    }

    return render(request, 'Drivers/view_feedback.html', context)




# Notification Modules
def VIEW_NOTIFICATION(request):
    notification = Notification.objects.all()

    context = {
        'notification': notification,
    }

    return render(request, 'Drivers/view_notification.html', context)


def ON_LIVE_TRACKING_PAGE(request):
    return render(request, 'Drivers/tracking_page.html')

def TRACKING_UPDATE(request):
    driver = CustomUser.objects.get(id=request.user.id)
    if request.method=="POST":
        print('Tracking on')
        data = json.loads(request.body)
        lat=data.get('latitude')
        lon=data.get('longitude')
        if(Location.objects.filter(driver=driver.username)).exists():
            Location.objects.filter(driver=driver.username).update(latitude=lat,longitude=lon)
        else:
            ob=Location()
            ob.driver=driver.username
            ob.latitude=lat
            ob.longitude=lon
            ob.save()
        return redirect('driver_track_bus')
        