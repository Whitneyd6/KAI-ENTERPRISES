from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, render

from .models import Department


@login_required
def dashboard(request):
    departments = Department.objects.annotate(
        item_count=Count('equipment'),
        total_stock=Sum('equipment__quantity_in_stock'),
    )
    return render(request, 'store/dashboard.html', {'departments': departments})


@login_required
def department_detail(request, slug):
    department = get_object_or_404(Department, slug=slug)
    equipment = department.equipment.all()
    return render(
        request,
        'store/department_detail.html',
        {'department': department, 'equipment': equipment},
    )