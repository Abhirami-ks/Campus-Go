from django.shortcuts import render, redirect, HttpResponse
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, logout, login, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import *
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.db.models.signals import post_save


def BASE(request):
    return render(request, 'base.html')


def LANDING(request):
    return render(request, 'index.html')


def LOGIN(request):
    return render(request, 'login.html')


def forgotPassword(request):
    if request.method == "POST":
        password = request.POST.get('pass2')
        email = request.POST.get('mail2')
        user_model = get_user_model()
        user = user_model.objects.get(email=email)
        user.set_password(password)
        user.save()
        # Redirect to a success page or URL
        messages.error(request, 'Password Reset Successfull !')
        return redirect('login')
    return render(request, 'login.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']

        user = EmailBackEnd.authenticate(request,
                                         username=request.POST.get('email'),
                                         password=request.POST.get('password'),)

        if user is not None:
            if user.user_type == '1':
                login(request, user)
                return redirect('admin_home')  # Redirect to the admin home page
            elif user.status == 'Approved':
                if user.user_type == '2':
                    login(request, user)
                    return redirect('faculty_view_notification')  # Redirect to the donor home page
                if user.user_type == '2.1':
                    login(request, user)
                    return redirect('inch_view_bus') 
                elif user.user_type == '3':
                    login(request, user)
                    return redirect('student_view_bus')  # Redirect to the collector home page
                elif user.user_type == '4':
                    login(request, user)
                    return redirect('driver_view_notification')  # Redirect to the beneficiary home page
            else:
                messages.error(request, 'Your account is not approved.')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'login.html')


def doLogout(request):
    logout(request)
    return redirect('landing')


@login_required(login_url='/')
def PROFILE(request):
    user = CustomUser.objects.get(id=request.user.id)
    print(user)

    context = {
        "user": user,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(profile_pic, first_name, last_name, email, username, password)
        # print(profile_pic)
        try:
            customuser = CustomUser.objects.get(id=request.user.id)

            customuser.first_name = first_name
            customuser.last_name = last_name

            if password != None and password != "":
                customuser.set_password(password)
            if profile_pic != None and profile_pic != "":
                customuser.profile_pic = profile_pic

            customuser.save()
            messages.success(request, 'Your Profile Updated Successfully !')
            return redirect('profile')
        except:
            messages.error(request, 'failed to update your profile !')
    return render(request, 'profile.html')


def ADD_FACULTY(request):
    route = Route.objects.all()
    destination = Destination.objects.all()

    context = {
        'route': route,
        'destination': destination,
    }

    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        dept = request.POST.get('dept')
        route_id = request.POST.get('route')
        destination_id = request.POST.get('destination')

        route = Route.objects.get(id=route_id)
        destination = Destination.objects.get(id=destination_id)

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'email is already taken')
            return redirect('add_faculty')

        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username is already taken')
            return redirect('add_faculty')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                address=address,
                phone=phone,
                dept=dept,
                route=route,
                destination=destination,
                user_type=2,
                status='Added'
            )
            user.set_password(password)
            user.save()
            return redirect('login')

    return render(request, 'register_faculty.html', context)


def ADD_STUDENT(request):
    route = Route.objects.all()
    destination = Destination.objects.all()

    context = {
        'route': route,
        'destination': destination,
    }

    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        dept = request.POST.get('dept')
        route_id = request.POST.get('route')
        destination_id = request.POST.get('destination')

        route = Route.objects.get(id=route_id)
        destination = Destination.objects.get(id=destination_id)
        
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'email is already taken')
            return redirect('add_student')

        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username is already taken')
            return redirect('add_student')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=3,
                status='Added',
                address=address,
                phone=phone,
                dept=dept,
                route=route,
                destination=destination,
                
            )
            user.set_password(password)
            user.save()
            return redirect('login')

    return render(request, 'register_student.html', context)


def ADD_DRIVER(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        license = request.POST.get('license')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'email is already taken')
            return redirect('add_driver')

        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username is already taken')
            return redirect('add_driver')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=4,
                status='Added',
                address=address,
                phone=phone,
                license=license,
            )
            user.set_password(password)
            user.save()
            return redirect('login')

    return render(request, 'register_driver.html')


# def ADD_PARENT(request):
#     if request.method == "POST":
#         profile_pic = request.FILES.get('profile_pic')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         password = request.POST.get('password')
#         phone = request.POST.get('phone')
#         route_id = request.POST.get('route')
#         student_id=request.POST.get('student')
#         route = Route.objects.get(id=route_id)
#         student = Student.objects.get(id=student_id)
        
      
#         user = CustomUser(
#                 first_name=first_name,
#                 last_name=last_name,
#                 profile_pic=profile_pic,
#                 user_type=4
#             )
#         user.set_password(password)
#         user.save()

#         parent = Parent(
#                 admin=user,
#                 phone=phone,
#                 route=route,
#                 student=student
#             )
#         parent.save()
#         return redirect('login')

#     return render(request, 'register_parent.html')
