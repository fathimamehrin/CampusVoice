
from django.shortcuts import render, redirect ,get_object_or_404
from .models import Complaint
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required


def home(request):
    return render(request, 'complaints/home.html')



@login_required

@login_required
def submit_complaint(request, complaint_id=None):
    if complaint_id is not None:
        complaint = get_object_or_404(
            Complaint,
            id=complaint_id,
            user=request.user
        )

        if complaint.status != 'Pending':
            messages.error(request, 'Only pending complaints can be edited.')
            return redirect('my_complaints')
    else:
        complaint = None

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        category = request.POST.get('category', '')
        description = request.POST.get('description', '').strip()

        valid_categories = dict(Complaint.CATEGORY_CHOICES)

        if title and category in valid_categories and description:
            if complaint:
                complaint.title = title
                complaint.category = category
                complaint.description = description
                complaint.save()
                messages.success(request, 'Complaint updated successfully!')
            else:
                Complaint.objects.create(
                    user=request.user,
                    name=request.user.username,
                    title=title,
                    category=category,
                    description=description
                )
                messages.success(request, 'Complaint submitted successfully!')

            return redirect('my_complaints')

    return render(request, 'complaints/submit_complaint.html', {
        'complaint': complaint
    })



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'complaints/register.html', {
        'form': form
    })



def student_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.is_superuser or user.is_staff:
                return redirect('admin_dashboard')

            return redirect('home')
    else:
        form = AuthenticationForm(request)

    return render(request, 'complaints/login.html', {'form': form})



def student_logout(request):
    if request.method == 'POST':
        logout(request)

    return redirect('home')


def all_complaints(request):
    complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, 'complaints/all_complaints.html', {
        'complaints': complaints
    })

def my_complaints(request):
    complaints = Complaint.objects.filter(
        user=request.user
    ).order_by('-created_at') if request.user.is_authenticated else []

    return render(request, 'complaints/my_complaints.html', {
        'complaints': complaints
    })



@login_required
def edit_complaint(request, complaint_id):
    complaint = get_object_or_404(
        Complaint,
        id=complaint_id,
        user=request.user
    )

    if complaint.status != 'Pending':
        messages.error(
            request,
            'Only pending complaints can be edited.'
        )
        return redirect('my_complaints')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        category = request.POST.get('category', '')
        description = request.POST.get('description', '').strip()

        valid_categories = dict(Complaint.CATEGORY_CHOICES)

        if title and category in valid_categories and description:
            complaint.title = title
            complaint.category = category
            complaint.description = description
            complaint.save()

            messages.success(request, 'Complaint updated successfully!')
            return redirect('my_complaints')

    return render(request, 'complaints/edit_complaint.html', {
        'complaint': complaint
    })


@login_required
def delete_complaint(request, complaint_id):
    complaint = get_object_or_404(
        Complaint,
        id=complaint_id,
        user=request.user
    )

    if request.method == 'POST' and complaint.status == 'Pending':
        complaint.delete()
        messages.success(request, 'Complaint deleted successfully!')
    elif complaint.status != 'Pending':
        messages.error(
            request,
            'Only pending complaints can be deleted.'
        )

    return redirect('my_complaints')


@staff_member_required
def admin_dashboard(request):
    total = Complaint.objects.count()
    pending = Complaint.objects.filter(status='Pending').count()
    in_progress = Complaint.objects.filter(status='In Progress').count()
    resolved = Complaint.objects.filter(status='Resolved').count()

    complaints = Complaint.objects.all().order_by('-created_at')

    return render(request, 'complaints/admin_dashboard.html', {
        'total': total,
        'pending': pending,
        'in_progress': in_progress,
        'resolved': resolved,
        'complaints': complaints,
    })

@staff_member_required
def update_complaint_status(request, complaint_id):
    from django.shortcuts import get_object_or_404
    from django.views.decorators.http import require_POST

    if request.method != 'POST':
        return redirect('admin_dashboard')

    complaint = get_object_or_404(Complaint, id=complaint_id)
    new_status = request.POST.get('status')

    valid_statuses = ['Pending', 'In Progress', 'Resolved']

    if new_status in valid_statuses:
        complaint.status = new_status
        complaint.save(update_fields=['status'])

    return redirect('admin_dashboard')



