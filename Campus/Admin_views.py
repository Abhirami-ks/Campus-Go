from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import *
from django.contrib import messages
from django.dispatch import receiver
from django.db.models import Q
from django.db.models.signals import post_save
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import get_object_or_404



@login_required(login_url='/')
def HOME(request):
    faculty_count = CustomUser.objects.all().count()
    student_count = CustomUser.objects.all().count()
    driver_count = CustomUser.objects.all().count()
    bus_count = Bus.objects.all().count()

    context = {
        'student_count': faculty_count,
        'staff_count': student_count,
        'course_count': driver_count,
        'subject_count': bus_count,
    }
    return render(request, 'Admin/home.html', context)


# Owner Modules
def VIEW_REGISTERED_FACULTY(request):
    faculty = CustomUser.objects.filter(user_type=2,status='Added')

    context = {
        'faculty': faculty,
    }
    return render(request, 'Admin/view_regd_faculty.html', context)

def APPROVE_FACULTY(request, admin):
    
    faculty = CustomUser.objects.get(id=admin)
    faculty.status = 'Approved'
    faculty.save()
    messages.success(request, 'Approved Successfully !')

    return redirect('view_approved_faculty')


def VIEW_APPROVED_FACULTY(request):
    faculty = CustomUser.objects.filter(Q(status='Approved') & (Q(user_type=2) | Q(user_type=2.1)))
   
    context = {
        'faculty': faculty,
        
    }
    return render(request, 'Admin/view_approved_faculty.html', context)


def REJECT_FACULTY(request, admin):
    faculty = CustomUser.objects.get(id=admin)
    faculty.status = 'Reject'
    faculty.save()
    messages.warning(request, 'Access Rejected !')

    return redirect('view_regd_faculty')




def REMOVE_INCHARGE(request, admin):
    faculty = CustomUser.objects.get(id=admin)
    faculty.user_type = '2'
    faculty.save()
    messages.warning(request, 'Incharge Access Removed !')

    return redirect('view_approved_faculty')


def DELETE_FACULTY(request, admin):
    faculty = CustomUser.objects.get(id=admin)
    faculty.delete()
    messages.warning(request, 'Successfully Removed !')

    return redirect('view_approved_faculty')


# Driver Modules
def VIEW_REGISTERED_DRIVER(request):
    driver = CustomUser.objects.filter(status='Added')

    context = {
        'driver': driver,
    }
    return render(request, 'Admin/view_regd_driver.html', context)



def APPROVE_DRIVER(request, admin):
    driver = CustomUser.objects.get(id=admin)
    driver.status = 'Approved'
    driver.save()
    messages.success(request, 'Approved Successfully !')

    return redirect('view_approved_driver')


def ASSIGN_ROUTE(request):
    if request.method == "POST":
        driver_id = request.POST.get('driver_id')
        route_id = request.POST.get("route")

        driver = CustomUser.objects.get(id=driver_id)
        route = Route.objects.get(id=route_id)

        driver.route = route
        driver.save()

        messages.success(request, 'Route Assigned Successfully !')
        return redirect('view_approved_driver')


def REJECT_DRIVER(request, admin):
    driver = CustomUser.objects.get(id=admin)
    driver.status = 'Reject'
    driver.save()
    messages.warning(request, 'Access Rejected !')

    return redirect('view_regd_driver')


def DELETE_DRIVER(request, admin):
    driver = CustomUser.objects.get(id=admin)
    driver.delete()
    messages.warning(request, 'Successfully Removed !')

    return redirect('view_regd_driver')


def ADD_DESTINATION(request):
    destination = Destination.objects.all()

    context = {
        'destination': destination,
    }

    if request.method == "POST":
        path = request.POST.get('path')

        destination = Destination(
            path=path,
        )

        destination.save()
        messages.success(request, "Destinations are successfully added !")
        return redirect('add_destination')
    return render(request, 'Admin/view_destination.html', context)


# Room Modules
def ADD_ROUTE(request):
    route = Route.objects.all()
    destination = Destination.objects.all()

    context = {
        'route': route,
        'destination':destination,
    }

    if request.method == "POST":
        destination = request.POST.get('destination')
        start = request.POST.get('start')
        end = request.POST.get('end')
        fees = request.POST.get('fees')
        
        destination_id = Destination.objects.get(id=destination)

        route = Route(
            path=destination_id,
            start=start,
            end=end,
            fees=fees,
        )

        route.save()
        messages.success(request, "Routs are successfully added !")
        return redirect('add_route')
    return render(request, 'Admin/view_route.html', context)


def EDIT_ROUTE(request, id):
    route = Route.objects.filter(id=id)

    context = {
        'route': route
    }
    return render(request, 'Admin/edit_route.html', context)


def UPDATE_ROUTE(request):
    if request.method == "POST":
        route_id = request.POST.get('route_id')
        destination = request.POST.get('destination')
        fees = request.POST.get('fees')

        route = Route.objects.get(id=route_id)
        route.destination = destination
        route.fees = fees
        route.save()

        messages.success(request, "records are succesfully updated !")
        return redirect('add_route')

    return render(request, 'Admin/edit_route.html')


# Bus Modules
def ADD_BUS(request):
    destination =Destination.objects.all()
    bus = Bus.objects.all()
    for i in bus:
        destination_id=i.destination
    driver = CustomUser.objects.filter(status='Approved',user_type=4)
    faculty = CustomUser.objects.filter(status='Approved',user_type=2, destination = destination_id)

    context = {
        'bus': bus,
        'destination':destination,
        'driver':driver,
        'faculty':faculty
    }

    if request.method == "POST":
        driver_id = request.POST.get('driver')
        destination_id = request.POST.get('destination')
        number = request.POST.get('number')
        reg_no = request.POST.get('regno')

        driver = CustomUser.objects.get(id=driver_id)
        destination = Destination.objects.get(id=destination_id)
        if Bus.objects.filter(users=driver).exists():
            messages.warning(request, 'driver is already taken')
            return redirect('add_bus')
        
        if Bus.objects.filter(number=number).exists():
            messages.warning(request, 'number is already taken')
            return redirect('add_bus')

        bus = Bus(
            users=driver,
            destination=destination,
            number=number,
            reg_no=reg_no,
        
        )
        bus.save()
        
        messages.success(request, "Bus info are successfully added !")
        return redirect('add_bus')
    return render(request, 'Admin/view_bus.html', context)

def FACULTY_INCHARGE(request):
    if request.method == "POST":
        bus_id = request.POST.get('bus_id')
        faculty_id = request.POST.get('faculty_id')

        fac_id = get_object_or_404(CustomUser, id=faculty_id)
        bus = get_object_or_404(Bus, id=bus_id)

        bus.inch = fac_id
        bus.save()

        faculty = get_object_or_404(CustomUser, id=faculty_id)
        faculty.user_type = '2.1'
        faculty.save()

        messages.warning(request, 'Incharge Access Granted !')

    return redirect('add_bus')



def VIEW_APPROVED_DRIVER(request):
    driver = CustomUser.objects.filter(status='Approved', user_type=4)
    route = Route.objects.all()
    bus = Bus.objects.all()

    context = {
        'driver': driver,
        'route': route,
        'bus': bus,
    }
    return render(request, 'Admin/view_approved_driver.html', context)


def VIEW_ADD_BUS(request):
    bus = Bus.objects.all()
   

    context = {
        'bus': bus,
    
    }
    return render(request, 'Admin/viewbus.html', context)

def DELETE_BUS(request,id):
    bus=Bus.objects.get(id=id)
    bus.delete()
    messages.warning(request, 'Successfully Removed !')
    return redirect('view_add_bus')


def EDIT_BUS(request, id):
    bus = Route.objects.filter(id=id)

    context = {
        'bus': bus
    }
    return render(request, 'Admin/edit_route.html', context)


def UPDATE_BUS(request):
    if request.method == "POST":
        bus_id = request.POST.get('bus_id')
        route = request.POST.get('route')
        driver = request.POST.get('driver')

        bus = Bus.objects.get(id=bus_id)
        bus.route = route
        bus.driver = driver
        bus.save()

        messages.success(request, "records are succesfully updated !")
        return redirect('add_bus')

    return render(request, 'Admin/edit_bus.html')


# Feedback Modules
def FEEDBACK_VIEW(request):
    feedback = Feedback.objects.all()

    context = {
        'feedback': feedback,
    }

    return render(request, 'Admin/view_feedback.html', context)


def FEEDBACK_REPLY(request):
    if request.method == "POST":
        feedback_id = request.POST.get('feedback_id')
        reply = request.POST.get('reply')

        feedback = Feedback.objects.get(id=feedback_id)
        feedback.Reply = reply
        feedback.save()
        messages.success(request, "Feedback reply Send !")
        return redirect('admin_feedback_view')

    return render(request, 'Admin/view_feedback.html')


def VIEW_PAYMENT(request):
    payment = Payment.objects.all()

    context = {
        'payment': payment,

    }
    return render(request, 'Admin/view_payments.html', context)

# Notification Modules
def ADD_NOTIFICATION(request):
    notification = Notification.objects.all()

    context = {
        'notification': notification,
    }

    if request.method == "POST":
        content = request.POST.get('content')

        notification = Notification(
            content=content,
        )

        notification.save()
        messages.success(request, "Successfully added !")
        return redirect('add_notification')
    return render(request, 'Admin/view_notification.html', context)


def DELETE_NOTIFICATION(request, id):
    notification = Notification.objects.get(id=id)
    notification.delete()
    messages.warning(request, 'Successfully Removed !')

    return redirect('add_notification')

def VIEW_APPROVED_STUDENTS(request):

    students = CustomUser.objects.filter(status='Approved',user_type=3) 
    bus = Bus.objects.all()

    context = {
        'students': students,
        'bus': bus
    }
    return render(request, 'Admin/view_students.html', context)


