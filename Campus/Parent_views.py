from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import *
from django.contrib import messages
from datetime import datetime, timedelta

@login_required(login_url='/')
# Bus Modules
def VIEW_BUS(request):
    parent = CustomUser.objects.get(id=request.user.id )
    destination_id = parent.destination
    bus = Bus.objects.get(destination=destination_id)
    driverid=Location.objects.get(driver=bus.users)

    context = {
        'bus': bus,
        'parent': parent,
        'driverid':driverid
    }

    return render(request, 'Parent/view_bus.html', context)

def VIEW_NOTIFICATION(request):
    notification = Notification.objects.all()

    context = {
        'notification': notification,
    }

    return render(request, 'Parent/view_notification.html', context)

def ADD_FEEDBACK(request):
    if request.method == "POST":
        user_id = CustomUser.objects.get(id=request.user.id)
        content = request.POST.get('content')

        feedback = Feedback(
            feed=user_id,
            content=content,
        )
        feedback.save()

        messages.success(request, " Details are successfully added !")
        return redirect('parent_view_feedback')
    return render(request, 'Parent/add_feedback.html')


def VIEW_FEEDBACK(request):
    users = CustomUser.objects.filter(id=request.user.id)
    for i in users:
        user_id = i.id
        feedback = Feedback.objects.filter(feed=user_id)
        context = {
            'feedback': feedback
        }


    return render(request, 'Parent/view_feedback.html', context)


