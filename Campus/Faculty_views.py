from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import *
from django.contrib import messages
from datetime import datetime, timedelta
from django.db.models import Q
from io import BytesIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa



@login_required(login_url='/')



# Owner Modules
def VIEW_REGISTERED_STUDENTS(request):
    faculty = CustomUser.objects.get(id=request.user.id)
    destination_id = faculty.destination
    students = CustomUser.objects.filter(status='Added', destination = destination_id, user_type=3)

    context = {
        'students': students,
    }
    return render(request, 'Faculty/view_regd_students.html', context)


def VIEW_APPROVED_STUDENTS(request):
    faculty = CustomUser.objects.get(id=request.user.id)

    route=faculty.route
    students = CustomUser.objects.filter(status='Approved', route=route, user_type=3)

    context = {
        'students': students,
    }
    return render(request, 'Faculty/view_approved_students.html', context)


def APPROVE_STUDENTS(request, admin):
    students = CustomUser.objects.get(id=admin)
    students.status = 'Approved'
    students.save()
    messages.success(request, 'Approved Successfully !')

    return redirect('view_approved_students')


def REJECT_STUDENTS(request, admin):
    students = CustomUser.objects.get(id=admin)
    students.status = 'Reject'
    students.save()
    messages.warning(request, 'Access Rejected !')

    return redirect('view_regd_students')


def DELETE_STUDENTS(request, admin):
    students = CustomUser.objects.get(id=admin)
    students.delete()
    messages.warning(request, 'Successfully Removed !')

    return redirect('view_approved_students')


# Bus Modules
def VIEW_BUS(request):
    faculty = CustomUser.objects.get(id=request.user.id)
    destination_id = faculty.destination
    bus = Bus.objects.get(destination=destination_id)
    driverid=Location.objects.get(driver=bus.users)

    context = {
        'bus': bus,
        'faculty':faculty,
        'driverid':driverid
    }

    return render(request, 'Faculty/view_bus.html', context)

# Payment

def FAC_PAYMENT(request):
    faculty = CustomUser.objects.get(id=request.user.id)
    payment = Payment.objects.filter(payee=faculty).first()
    current_date = datetime.now()
    one_month_later = current_date + timedelta(days=30)
    destination_id = faculty.destination
    bus = Bus.objects.get(destination=destination_id)
    context = {
        'payment': payment,
        'current_date': current_date,
        'one_month_later':one_month_later,
        'bus':bus,
        'faculty':faculty
    }

    return render(request, 'Faculty/fac_payment.html',context)

def ADD_PAYMENT(request):
    if request.method == "POST":
        faculty = CustomUser.objects.get(admin=request.user.id)
        route_id = faculty.route
        destination_id = faculty.destination
        bus = Bus.objects.get(destination=destination_id)
        payment = Payment(
            faculty = faculty,
            route = route_id,
            status = 'Paid',
            bus=bus
        )
        paym={
            'faculty' : faculty,
            'route' : route_id,
            'status' : 'Paid',
            }
       
        template1 = get_template('Faculty/reciept.html')
        html = template1.render(paym)
        result = BytesIO()
        # , link_callback=fetch_resources)
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        pdf = result.getvalue()
        filename = 'payment_bill_.pdf'

        payment.save()
        return pdf
        messages.success(request, "Payment was Succesfull !")
        return redirect('faculty_view_payment')

    return render(request, 'Faculty/view_payments.html')

def VIEW_PAYMENT(request):
    faculty = CustomUser.objects.get(admin=request.user.id)
    payment = Payment.objects.filter(faculty=faculty)
    current_date = datetime.now()
    one_month_later = current_date + timedelta(days=30)

    context = {
        'payment': payment,
        'current_date': current_date,
        'one_month_later':one_month_later

    }

    return render(request, 'Faculty/view_payments.html', context)

# Feedback Modules
def ADD_FEEDBACK(request):
    if request.method == "POST":
        user_id = CustomUser.objects.get(admin=request.user.id)
        content = request.POST.get('content')

        feedback = Feedback(
            faculty=user_id,
            content=content,
        )
        feedback.save()

        messages.success(request, " Details are successfully added !")
        return redirect('faculty_view_feedback')
    return render(request, 'Faculty/add_feedback.html')


def VIEW_FEEDBACK(request):
    users = CustomUser.objects.filter(admin=request.user.id)
    for i in users:
        user_id = i.id
        feedback = Feedback.objects.filter(faculty=user_id)
        context = {
            'feedback': feedback
        }

    return render(request, 'Faculty/view_feedback.html', context)




# Notification Modules
def VIEW_NOTIFICATION(request):
    notification = Notification.objects.all()
    

    context = {
        'notification': notification,
       
    }

    return render(request, 'Faculty/view_notification.html', context)
# dashboard
def INCH_DASHBOARD(request):
    faculty=CustomUser.objects.get(admin=request.user.id)
    route=faculty.route
    driver=CustomUser.objects.get(route_id=route)
    context={
        'driver':driver
    }
    
    return render(request, 'Faculty/fac_dash.html', context)

def FAC_DASHBOARD(request):
    return render(request, 'Faculty/faculty_dash.html')

def INCH_ROUTE(request):
    faculty=CustomUser.objects.get(id=request.user.id)
    bus = Bus.objects.filter(inch = faculty)
    context ={
        'bus':bus
    }
    return render(request, 'Faculty/inch_route.html', context)


