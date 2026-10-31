from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit/', views.submit_complaint, name='submit_complaint'),
    path('register/', views.register, name='register'),
    path('login/', views.student_login, name='login'),
    path('logout/', views.student_logout, name='logout'),
    path('all-complaints/', views.all_complaints, name='all_complaints'),
    path('my-complaints/', views.my_complaints, name='my_complaints'),
    path('edit-complaint/<int:complaint_id>/',views.submit_complaint, name='edit_complaint'),
    path('delete-complaint/<int:complaint_id>/',views.delete_complaint, name='delete_complaint'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path(
    'admin-dashboard/complaint/<int:complaint_id>/status/',
    views.update_complaint_status,
    name='update_complaint_status',
),

]