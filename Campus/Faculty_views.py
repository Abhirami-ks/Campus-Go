from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import *
from django.contrib import messages
from datetime import datetime, timedelta
from django.db.models import Q
from io import BytesIO
from django.http import HttpResponse
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
        faculty = CustomUser.objects.get(id=request.user.id)
        route_id = faculty.route
        current_date = datetime.now()

        paym = {
            'faculty': faculty,
            'route': route_id,
            'current_date': current_date,
            'status': 'Paid',
        }

        payment = Payment(
            payee=faculty,
            route=route_id,
            status='Paid',
        )

        template = get_template('Students/reciept.html')
        html = template.render(paym)

        # Generate PDF using xhtml2pdf
        pdf = BytesIO()
        pisa.CreatePDF(BytesIO(html.encode("UTF-8")), pdf)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="fees.pdf"'
        response.write(pdf.getvalue())

        payment.save()
        messages.success(request, "Payment was successful!")
        return response
    

    return render(request, 'Faculty/view_bus.html')

def VIEW_PAYMENT(request):
    faculty = CustomUser.objects.get(id=request.user.id)
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
        user_id = CustomUser.objects.get(id=request.user.id)
        content = request.POST.get('content')

        feedback = Feedback(
            feed=user_id,
            content=content,
        )
        feedback.save()

        messages.success(request, " Details are successfully added !")
        return redirect('faculty_view_feedback')
    return render(request, 'Faculty/add_feedback.html')


def VIEW_FEEDBACK(request):
    users = CustomUser.objects.filter(id=request.user.id)
    for i in users:
        user_id = i.id
        feedback = Feedback.objects.filter(feed=user_id)
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
    faculty=CustomUser.objects.get(id=request.user.id,user_type = 2.1)
    destination_id = faculty.destination
    driver=CustomUser.objects.filter(destination_id=destination_id)
    context={
        'driver':driver
    }
    
    return render(request, 'Faculty/fac_dash.html', context)

def FAC_DASHBOARD(request):
    return render(request, 'Faculty/faculty_dash.html')

def INCH_ROUTE(request):
    faculty=CustomUser.objects.get(id=request.user.id)
    destination_id = faculty.destination
    bus = Bus.objects.get(destination=destination_id)
    driverid=Location.objects.get(driver=bus.users)
    context ={
        'bus':bus,
        'faculty':faculty,
        'driverid':driverid
    }
    return render(request, 'Faculty/inch_route.html', context)

def INCH_PAYMENTVIEW(request):
    inch = CustomUser.objects.get(id=request.user.id, user_type=2.1)
    bus = Bus.objects.get(inch=inch)
    users = CustomUser.objects.filter(Q(destination=bus.destination) & (Q(user_type=2) | Q(user_type=3)))
    payment = Payment.objects.filter(payee__in=users)

    context = {
        'payment': payment,
    }
    return render(request, 'Faculty/inch_viewpayment.html', context)


def VIEW_PASSENGER(request):
    inch = CustomUser.objects.get(id=request.user.id,user_type=2.1)
    inch_id = inch.id
    bus = Bus.objects.get(inch=inch_id)
    destination = bus.destination
    users=CustomUser.objects.filter(Q(destination=destination) & (Q(user_type=2) | Q(user_type=3)))
    context = {
        'users':users,
        'bus' : bus,
    }
    return render (request,'Faculty/passenger.html',context)
