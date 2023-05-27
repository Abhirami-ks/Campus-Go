"""
URL configuration for CyberVillage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views, Admin_views, Faculty_views, Student_views, Driver_views, Parent_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE, name='base'),
    path('', views.LANDING, name='landing'),

    path('Faculty_Registration/', views.ADD_FACULTY, name='add_faculty'),
    path('Student_Registration/', views.ADD_STUDENT, name='add_student'),
    path('Driver_Registration/', views.ADD_DRIVER, name='add_driver'),
    # path('Parent_Registration/', views.ADD_PARENT, name='add_parent'),

    #login_Path
    path('login/', views.LOGIN, name='login'),
    path('doLogin', views.login_user, name='doLogin'),
    path('doLogout', views.doLogout, name='doLogout'),
    path('forgotPassword', views.forgotPassword, name='forgot_password'),

    #profile update
    path('profile', views.PROFILE, name='profile'),
    path('profile/update', views.PROFILE_UPDATE, name='profile_update'),

#Admin Panel
    path('Admin/Home', Admin_views.HOME, name='admin_home'),

# Admin-Students
    path('Admin/Student', Admin_views.VIEW_APPROVED_STUDENTS, name='view_students'),

# Admin -Faculty
    path('ADMIN/Faculty/Registered', Admin_views.VIEW_REGISTERED_FACULTY, name='view_regd_faculty'),
    path('ADMIN/Faculty/Approved', Admin_views.VIEW_APPROVED_FACULTY, name='view_approved_faculty'),
    path('ADMIN/Faculty/Approve/<str:admin>', Admin_views.APPROVE_FACULTY, name='approve_faculty'),
    path('ADMIN/Faculty/Reject/<str:admin>', Admin_views.REJECT_FACULTY, name='reject_faculty'),
    path('ADMIN/Faculty/Incharge', Admin_views.FACULTY_INCHARGE, name='faculty_incharge'),
    path('ADMIN/Faculty/Incharge/Remove/<str:admin>', Admin_views.REMOVE_INCHARGE, name='faculty_remove_incharge'),
    path('ADMIN/Faculty/Delete/<str:admin>', Admin_views.DELETE_FACULTY, name='delete_faculty'),

# Admin -Driver
    path('ADMIN/Driver/Registered', Admin_views.VIEW_REGISTERED_DRIVER, name='view_regd_driver'),
    path('ADMIN/Driver/Approved', Admin_views.VIEW_APPROVED_DRIVER, name='view_approved_driver'),
    path('ADMIN/Driver/Assign_Route', Admin_views.ASSIGN_ROUTE, name='assign_route'),
    path('ADMIN/Driver/Approve/<str:admin>', Admin_views.APPROVE_DRIVER, name='approve_driver'),
    path('ADMIN/Driver/Reject/<str:admin>', Admin_views.REJECT_DRIVER, name='reject_driver'),
    path('ADMIN/Driver/Delete/<str:admin>', Admin_views.DELETE_DRIVER, name='delete_driver'),

    path('ADMIN/Destination/Add', Admin_views.ADD_DESTINATION, name='add_destination'),
# Admin -Route
    path('ADMIN/Route/Add', Admin_views.ADD_ROUTE, name='add_route'),
    path('ADMIN/Route/Edit/<str:id>', Admin_views.EDIT_ROUTE, name='edit_route'),
    path('ADMIN/Route/Update', Admin_views.UPDATE_ROUTE, name='update_route'),

# Admin -Bus
    path('ADMIN/Bus/Add', Admin_views.ADD_BUS, name='add_bus'),
    path('ADMIN/Bus/Edit/<str:id>', Admin_views.EDIT_BUS, name='edit_bus'),
    path('ADMIN/Bus/Update', Admin_views.UPDATE_BUS, name='update_bus'),
    path('ADMIN/Bus/View', Admin_views.VIEW_ADD_BUS, name='view_add_bus'),
    path('ADMIN/Bus/Delete/<str:id>', Admin_views.DELETE_BUS, name='delete_bus'),


# Admin -Notification
    path('ADMIN/Notification/Add', Admin_views.ADD_NOTIFICATION, name='add_notification'),
    # path('ADMIN/Notification/sent', Admin_views.send_notification, name='sent_notification'),
    path('ADMIN/Notification/Delete/<str:id>', Admin_views.DELETE_NOTIFICATION, name='delete_notification'),

# Admin - Feedback
    path('AdminFeedback/View',Admin_views.FEEDBACK_VIEW, name='admin_feedback_view'),
    path('Admin/Feedback/Reply',Admin_views.FEEDBACK_REPLY, name='feedback_reply'),
    path('Admin/Payments/View', Admin_views.VIEW_PAYMENT, name='admin_view_payment'),


#----------FACULTY-------------------------------------
# Faculty -Students
    path('Faculty/Student/Registered', Faculty_views.VIEW_REGISTERED_STUDENTS, name='view_regd_students'),
    path('Faculty/Student/Approved', Faculty_views.VIEW_APPROVED_STUDENTS, name='view_approved_students'),
    path('Faculty/Student/Approve/<str:admin>', Faculty_views.APPROVE_STUDENTS, name='approve_students'),
    path('Faculty/Student/Reject/<str:admin>', Faculty_views.REJECT_STUDENTS, name='reject_students'),
    path('Faculty/Student/Delete/<str:admin>', Faculty_views.DELETE_STUDENTS, name='delete_students'),

# Faculty -Bus
    path('Faculty/Bus/View', Faculty_views.VIEW_BUS, name='faculty_view_bus'),
    path('Faculty/Bus/Inch_View', Faculty_views.INCH_ROUTE, name='inch_view_bus'),
    path('Faculty/Payments/Add', Faculty_views.ADD_PAYMENT, name='faculty_add_payment'),
    path('Faculty/Payments/View', Faculty_views.VIEW_PAYMENT, name='faculty_view_payment'),
    path('Faculty/Payments', Faculty_views.FAC_PAYMENT, name='fac_pay_payment'),

# Faculty -Notification
    path('Faculty/Notification/Add', Faculty_views.VIEW_NOTIFICATION, name='faculty_view_notification'),
    path('Faculty/Feedback/Add', Faculty_views.ADD_FEEDBACK, name='faculty_add_feedback'),
    path('Faculty/Feedback/View', Faculty_views.VIEW_FEEDBACK, name='faculty_view_feedback'),
    path('Faculty/dash', Faculty_views.INCH_DASHBOARD, name='dashboard'),
    path('Faculty/dashboard', Faculty_views.FAC_DASHBOARD, name='faculty_dashboard'),



# Student -Bus
    path('Student/Bus/View', Student_views.VIEW_BUS, name='student_view_bus'),
    path('Student/Payments/Add', Student_views.ADD_PAYMENT, name='student_add_payment'),
    path('Student/Payments/View', Student_views.VIEW_PAYMENT, name='student_view_payment'),
    path('Student/Payments', Student_views.STU_PAYMENT, name='stu_pay_payment'),
    path('Student/dash', Student_views.STU_DASHBOARD, name='stu_dashboard'),

# Student -Notification
    path('Student/Notification/View', Student_views.VIEW_NOTIFICATION, name='student_view_notification'),

    path('Student/Feedback/Add', Student_views.ADD_FEEDBACK, name='add_feedback'),
    path('Student/Feedback/View', Student_views.VIEW_FEEDBACK, name='view_feedback'),


# Driver -Bus
    path('Driver/Bus/View', Driver_views.VIEW_BUS, name='driver_view_bus'),
# driver tracking page
    path('Driver/Bus/track', Driver_views.ON_LIVE_TRACKING_PAGE, name='driver_track_bus'),
    path('Driver/Bus/trackupdate/', Driver_views.TRACKING_UPDATE, name='driver_update_track_bus'),

# Driver -Notification
    path('Driver/Notification/View', Driver_views.VIEW_NOTIFICATION, name='driver_view_notification'),
    
# parent
    path('Parent/Bus/View', Parent_views.VIEW_BUS, name='parent_view_bus'),
    path('Parent/Feedback/Add', Parent_views.ADD_FEEDBACK, name='parent_feedback'),
    path('Parent/Notification/View', Parent_views.VIEW_NOTIFICATION, name='parent_view_notification'),
    path('Parent/Feedback/View', Parent_views.VIEW_FEEDBACK, name='parent_view_feedback'),





] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
