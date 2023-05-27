from re import template
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import *
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta
from io import BytesIO
from django.template import Context
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
from django.http import HttpResponse
from io import BytesIO
import xhtml2pdf.pisa as pisa
from xhtml2pdf import pisa
from django.template.loader import render_to_string

@login_required(login_url='/')
# Bus Modules
def VIEW_BUS(request):
    
    student = CustomUser.objects.get(id=request.user.id)
    destination_id = student.destination
    bus = Bus.objects.get(destination=destination_id)
    driverid=Location.objects.get(driver=bus.users)
    context = {
        'bus': bus,
        'student':student,
        'driverid':driverid
    }

    return render(request, 'Students/view_bus.html', context)


# Payment
def ADD_PAYMENT(request):
    if request.method == "POST":
        student = CustomUser.objects.get(id=request.user.id)
        route_id = student.route

        paym = {
            'student': student,
            'route': route_id,
            'status': 'Paid',
        }

        payment = Payment(
            payee=student,
            route=route_id,
            status='Paid',
        )

        template = get_template('Students/reciept.html')
        html = template.render(paym)

        # Generate PDF using xhtml2pdf
        pdf = BytesIO()
        pisa.CreatePDF(BytesIO(html.encode("UTF-8")), pdf)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="my_pdf.pdf"'
        response.write(pdf.getvalue())

        payment.save()
        messages.success(request, "Payment was successful!")
        return response

    return render(request, 'Students/view_bus.html')

def VIEW_PAYMENT(request):
    student = CustomUser.objects.get(id=request.user.id)
    payment = Payment.objects.filter(student=student)
    current_date = datetime.now()
    one_month_later = current_date + timedelta(days=30)

    context = {
        'payment': payment,
        'current_date': current_date,
        'one_month_later':one_month_later

    }

    return render(request, 'Students/view_payments.html', context)

def STU_PAYMENT(request):
    student = CustomUser.objects.get(id=request.user.id)
    payment = Payment.objects.filter(payee=student).first()
    current_date = datetime.now()
    one_month_later = current_date + timedelta(days=30)
    destination_id = student.destination
    bus = Bus.objects.get(destination=destination_id)


    context = {
        'payment': payment,
        'current_date': current_date,
        'one_month_later':one_month_later,
        'bus':bus,
        'student':student
    }
    
    return render(request, 'Students/stu_payment.html', context)


# Notification Modules
def VIEW_NOTIFICATION(request):
    notification = Notification.objects.all()

    context = {
        'notification': notification,
    }

    return render(request, 'Students/view_notification.html', context)

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
        return redirect('view_feedback')
    return render(request, 'Students/add_feedback.html')


def VIEW_FEEDBACK(request):
    
    users = CustomUser.objects.filter(id=request.user.id)
    for i in users:
        user_id = i.id
        feedback = Feedback.objects.filter(feed=user_id)
        context = {
            'feedback': feedback
        }

    return render(request, 'Students/view_feedback.html', context)

def STU_DASHBOARD(request):
    return render(request, 'Students/stu_dash.html')

