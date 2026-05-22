from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import F, Sum, ExpressionWrapper, DecimalField
import csv
import io

from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password, make_password
from .forms import RegisterForm, LoginForm
from .models import Categories, InventoryItems, Suppliers, AuditLogs, Admins, PendingVerification

import secrets
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings


# Helper
def get_admin(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        try:
            return Admins.objects.get(admin_id=admin_id)
        except Admins.DoesNotExist:
            return None
    return None


# Dashboard
def dashboard(request):
    if not request.session.get('admin_id'):
        return redirect('register')

    try:
        from django.utils import timezone

        admin = get_admin(request)
        categories = Categories.objects.all()
        inventories = InventoryItems.objects.select_related('category').all()

        total_items = inventories.count()
        low_stock_count = inventories.filter(current_stock__lte=F('reorder_level'), current_stock__gt=0).count()
        out_of_stock_count = inventories.filter(current_stock=0).count()
        category_count = categories.count()

        total_value = inventories.aggregate(
            total=Sum(
                ExpressionWrapper(F('current_stock') * F('unit_cost'), output_field=DecimalField())
            )
        )['total'] or 0

        category_stock = []
        for cat in categories:
            items = inventories.filter(category=cat)
            total_qty = sum(i.current_stock for i in items)
            max_qty = sum(i.reorder_level * 2 for i in items) or 1
            percent = min(int((total_qty / max_qty) * 100), 100)
            category_stock.append({
                'name': cat.category_name,
                'qty_display': f'{total_qty} units',
                'percent': percent,
            })

        low_stock_items = inventories.filter(current_stock__lte=F('reorder_level')).order_by('current_stock')[:10]

        context = {
            'today': timezone.now(),
            'total_items': total_items,
            'low_stock_count': low_stock_count,
            'out_of_stock_count': out_of_stock_count,
            'category_count': category_count,
            'total_value': total_value,
            'category_stock': category_stock,
            'low_stock_items': low_stock_items,
            'recent_activity': AuditLogs.objects.all().order_by('-performed_at')[:10],
            'admin': admin,
        }
        return render(request, 'dashboard/Dashboard.html', context)
    except Exception as e:
        return HttpResponse(f"Error: {e}")


def sidebar(request):
    if not request.session.get('admin_id'):
        return redirect('register')

    context = {'admin': get_admin(request)}
    return render(request, 'include/SideBar.html', context)


# Categories
def category_list(request):
    if not request.session.get('admin_id'):
        return redirect('register')

    try:
        categories = Categories.objects.all()
        return render(request, 'categories/categoryList.html', {
            'categories': categories,
            'admin': get_admin(request),
        })
    except Exception as e:
        return HttpResponse(f"Error: {e}")


def add_category(request):
    if not request.session.get('admin_id'):
        return redirect('register')

    try:
        if request.method == 'POST':
            category = request.POST.get('category_name')
            next_url = request.POST.get('next', 'add_category')

            if not category:
                messages.error(request, "Category name is required.")
                return redirect(next_url)

            Categories.objects.create(category_name=category)

            AuditLogs.objects.create(
                action='create',
                model_name='Categories',
                description=f'Added category: {category}',
                performed_by_id=request.session.get('admin_id'),
            )

            messages.success(request, "Category added successfully!")
            return redirect(next_url)
        else:
            return render(request, 'categories/categoryAdd.html', {
                'admin': get_admin(request),
            })
    except Exception as e:
        return HttpResponse(f"Error: {e}")


def update_category(request, categoryId):
    if not request.session.get('admin_id'):
        return redirect('register')

    try:
        if request.method == "POST":
            categoryObj = Categories.objects.get(category_id=categoryId)
            categoryObj.category_name = request.POST.get('category_name')
            categoryObj.save()

            AuditLogs.objects.create(
                action='update',
                model_name='Categories',
                description=f'Updated category: {categoryObj.category_name}',
                performed_by_id=request.session.get('admin_id'),
            )

            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
        else:
            return redirect('category_list')
    except Exception as e:
        return HttpResponse(f"Error: {e}")


def delete_category(request, categoryId):
    if not request.session.get('admin_id'):
        return redirect('register')

    try:
        category = Categories.objects.get(category_id=categoryId)

        if request.method == 'POST':
            category_name = category.category_name
            category.delete()

            AuditLogs.objects.create(
                action='delete',
                model_name='Categories',
                description=f'Deleted category: {category_name}',
                performed_by_id=request.session.get('admin_id'),
            )

            messages.success(request, "Category successfully deleted!")
            return redirect('category_list')
        else:
            return redirect('category_list')
    except Exception as e:
        return HttpResponse(f"Error: {e}")


# Inventory
def inventory_list(request):
    if not request.session.get('admin_id'):
        return redirect('register')

    try:
        categories = Categories.objects.all()
        inventories = InventoryItems.objects.all()
        low_stock = inventories.filter(current_stock__lte=F('reorder_level'), current_stock__gt=0)
        out_of_stock = inventories.filter(current_stock=0)

        return render(request, 'inventory/inventoryList.html', {
            'categories': categories,
            'inventories': inventories,
            'low_stock': low_stock,
            'out_of_stock': out_of_stock,
            'admin': get_admin(request),
        })
    except Exception as e:
        return HttpResponse(f"Error: {e}")


def add_inventory(request):
    if not request.session.get('admin_id'):
        return redirect('register')

    try:
        if request.method == 'POST':
            category_id = request.POST.get('category')
            item_name = request.POST.get('item_name')
            unit = request.POST.get('unit')
            current_stock = request.POST.get('current_stock')
            reorder_level = request.POST.get('reorder_level')
            unit_cost = request.POST.get('unit_cost')

            if not item_name:
                messages.error(request, 'Item name is required.')
                return redirect('add_inventory')

            if not category_id:
                messages.error(request, 'Category is required.')
                return redirect('add_inventory')

            category = Categories.objects.get(pk=category_id)

            InventoryItems.objects.create(
                category=category,
                item_name=item_name,
                unit=unit,
                current_stock=current_stock,
                reorder_level=reorder_level,
                unit_cost=unit_cost
            )

            AuditLogs.objects.create(
                action='create',
                model_name='InventoryItems',
                description=f'Added new item: {item_name}',
                performed_by_id=request.session.get('admin_id'),
            )

            messages.success(request, 'Item added successfully!')
            return redirect('inventory_list')

        categories = Categories.objects.all()
        return render(request, 'inventory/inventoryAdd.html', {
            'categories': categories,
            'admin': get_admin(request),
        })
    except Exception as e:
        return HttpResponse(f"Error: {e}")


def update_inventory(request, inventoryId):
    if not request.session.get('admin_id'):
        return redirect('register')

    try:
        if request.method == 'POST':
            inventoryObj = InventoryItems.objects.get(item_id=inventoryId)

            inventoryObj.item_name = request.POST.get('item_name')
            inventoryObj.unit = request.POST.get('unit')
            inventoryObj.current_stock = request.POST.get('current_stock')
            inventoryObj.reorder_level = request.POST.get('reorder_level')
            inventoryObj.unit_cost = request.POST.get('unit_cost')
            inventoryObj.save()

            AuditLogs.objects.create(
                action='update',
                model_name='InventoryItems',
                description=f'Updated item: {inventoryObj.item_name}',
                performed_by_id=request.session.get('admin_id'),
            )

            messages.success(request, 'Item updated successfully!')
            return redirect('inventory_list')
        else:
            return redirect('inventory_list')
    except Exception as e:
        return HttpResponse(f"Error: {e}")


def delete_inventory(request, inventoryId):
    if not request.session.get('admin_id'):
        return redirect('register')

    try:
        inventory = InventoryItems.objects.get(item_id=inventoryId)

        if request.method == 'POST':
            item_name = inventory.item_name
            inventory.delete()

            AuditLogs.objects.create(
                action='delete',
                model_name='InventoryItems',
                description=f'Deleted item: {item_name}',
                performed_by_id=request.session.get('admin_id'),
            )

            messages.success(request, "Item successfully deleted!")
            return redirect('inventory_list')
        else:
            return redirect('inventory_list')
    except InventoryItems.DoesNotExist:
        messages.error(request, "Item not found.")
        return redirect('inventory_list')
    except Exception as e:
        return HttpResponse(f"Error: {e}")


# Suppliers
def supplier_list(request):
    if not request.session.get('admin_id'):
        return redirect('register')

    try:
        suppliers = Suppliers.objects.all()
        return render(request, 'suppliers/supplierList.html', {
            'suppliers': suppliers,
            'admin': get_admin(request),
        })
    except Exception as e:
        return HttpResponse(f"Error: {e}")


def add_supplier(request):
    if not request.session.get('admin_id'):
        return redirect('register')

    try:
        if request.method == 'POST':
            supplier_name = request.POST.get('supplier_name', '').strip()
            contact_person = request.POST.get('contact_person', '').strip()
            email = request.POST.get('email', '').strip()
            phone_number = request.POST.get('phone_number', '').strip()
            address = request.POST.get('address', '').strip()

            if not supplier_name:
                messages.error(request, 'Supplier name is required.')
                return redirect('add_supplier')

            Suppliers.objects.create(
                supplier_name=supplier_name,
                contact_person=contact_person,
                email=email,
                phone_number=phone_number,
                address=address,
            )

            AuditLogs.objects.create(
                action='create',
                model_name='Suppliers',
                description=f'Added supplier: {supplier_name}',
                performed_by_id=request.session.get('admin_id'),
            )

            messages.success(request, 'Supplier added successfully!')
            return redirect('supplier_list')

        return render(request, 'suppliers/supplierAdd.html', {
            'admin': get_admin(request),
        })
    except Exception as e:
        return HttpResponse(f"Error: {e}")


def update_supplier(request, supplierId):
    if not request.session.get('admin_id'):
        return redirect('register')

    try:
        supplier = Suppliers.objects.get(supplier_id=supplierId)

        if request.method == 'POST':
            supplier.supplier_name = request.POST.get('supplier_name', '').strip()
            supplier.contact_person = request.POST.get('contact_person', '').strip()
            supplier.email = request.POST.get('email', '').strip()
            supplier.phone_number = request.POST.get('phone_number', '').strip()
            supplier.address = request.POST.get('address', '').strip()

            if not supplier.supplier_name:
                messages.error(request, 'Supplier name is required.')
                return redirect('update_supplier', supplierId=supplierId)

            supplier.save()

            AuditLogs.objects.create(
                action='update',
                model_name='Suppliers',
                description=f'Updated supplier: {supplier.supplier_name}',
                performed_by_id=request.session.get('admin_id'),
            )

            messages.success(request, 'Supplier updated successfully!')
            return redirect('supplier_list')

        return redirect('supplier_list')
    except Suppliers.DoesNotExist:
        messages.error(request, 'Supplier not found.')
        return redirect('supplier_list')
    except Exception as e:
        return HttpResponse(f"Error: {e}")


def delete_supplier(request, supplierId):
    if not request.session.get('admin_id'):
        return redirect('register')

    try:
        supplier = Suppliers.objects.get(supplier_id=supplierId)

        if request.method == 'POST':
            supplier_name = supplier.supplier_name
            supplier.delete()

            AuditLogs.objects.create(
                action='delete',
                model_name='Suppliers',
                description=f'Deleted supplier: {supplier_name}',
                performed_by_id=request.session.get('admin_id'),
            )

            messages.success(request, 'Supplier deleted successfully!')
            return redirect('supplier_list')

        return redirect('supplier_list')
    except Suppliers.DoesNotExist:
        messages.error(request, 'Supplier not found.')
        return redirect('supplier_list')
    except Exception as e:
        return HttpResponse(f"Error: {e}")


# CSV
def export_inventory_csv(request):
    if not request.session.get('admin_id'):
        return redirect('register')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory.csv"'

    writer = csv.writer(response)
    writer.writerow(['category', 'item_name', 'unit', 'current_stock', 'reorder_level', 'unit_cost'])

    items = InventoryItems.objects.select_related('category').all()
    for item in items:
        writer.writerow([
            item.category.category_name,
            item.item_name,
            item.unit,
            item.current_stock,
            item.reorder_level,
            item.unit_cost,
        ])

    return response


def import_inventory_csv(request):
    if not request.session.get('admin_id'):
        return redirect('register')

    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')

        if not csv_file or not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a valid .csv file.')
            return redirect('inventory_list')

        try:
            decoded = csv_file.read().decode('utf-8-sig')  # utf-8-sig handles BOM from Windows
            reader = csv.DictReader(io.StringIO(decoded))

            created, skipped = 0, 0
            for row in reader:
                category_name = row.get('category', '').strip()
                item_name = row.get('item_name', '').strip()

                if not category_name or not item_name:
                    skipped += 1
                    continue

                category, _ = Categories.objects.get_or_create(category_name=category_name)

                InventoryItems.objects.update_or_create(
                    item_name=item_name,
                    category=category,
                    defaults={
                        'unit': row.get('unit', '').strip(),
                        'current_stock': row.get('current_stock', 0),
                        'reorder_level': row.get('reorder_level', 0),
                        'unit_cost': row.get('unit_cost', 0),
                    }
                )
                created += 1

            AuditLogs.objects.create(
                action='create',
                model_name='InventoryItems',
                description=f'Imported CSV: {created} items processed, {skipped} skipped.',
                performed_by_id=request.session.get('admin_id'),
            )

            messages.success(request, f'Import complete: {created} items processed, {skipped} skipped.')

        except Exception as e:
            messages.error(request, f'Import failed: {e}')

        return redirect('inventory_list')

    return redirect('inventory_list')


# Authentication
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('signin')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, error)
                    else:
                        messages.error(request, f'{error}')
    else:
        form = RegisterForm()

    return render(request, 'authentication/RegisterPage.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                admin = Admins.objects.get(username=username)
                if check_password(password, admin.password):
                    request.session['admin_id'] = admin.admin_id
                    request.session['admin_username'] = admin.username
                    messages.success(request, f'Welcome back, {admin.first_name}!')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Invalid username or password.')
            except Admins.DoesNotExist:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'authentication/SignInPage.html', {'form': form})


def signout(request):
    request.session.flush()
    messages.success(request, 'You have been signed out.')
    return redirect('signin')
    

# Admin Settings
def admin_settings(request):
    if not request.session.get('admin_id'):
        return redirect('signin')

    admin = get_admin(request)
    return render(request, 'settings/settings.html', {'admin': admin})


def update_profile(request):
    if not request.session.get('admin_id'):
        return redirect('signin')

    if request.method == 'POST':
        admin = get_admin(request)

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()

        if not first_name or not last_name or not username:
            messages.error(request, 'Name and username are required.')
            return redirect('admin_settings')

        if Admins.objects.filter(username=username).exclude(admin_id=admin.admin_id).exists():
            messages.error(request, 'That username is already taken.')
            return redirect('admin_settings')

        admin.first_name = first_name
        admin.last_name = last_name
        admin.username = username

        if 'profile_picture' in request.FILES:
            admin.profile_picture = request.FILES['profile_picture']

        admin.save()

        request.session['admin_username'] = admin.username

        AuditLogs.objects.create(
            action='update',
            model_name='Admins',
            description=f'Updated profile for: {admin.username}',
            performed_by_id=admin.admin_id,
        )

        messages.success(request, 'Profile updated successfully!')

    return redirect('admin_settings')


def remove_profile_picture(request):
    if not request.session.get('admin_id'):
        return redirect('signin')

    if request.method == 'POST':
        admin = get_admin(request)
        if admin.profile_picture:
            admin.profile_picture.delete(save=False) 
            admin.profile_picture = None
            admin.save()
            messages.success(request, 'Profile picture removed.')
        else:
            messages.error(request, 'No profile picture to remove.')

    return redirect('admin_settings')


def request_email_change(request):
    if not request.session.get('admin_id'):
        return redirect('signin')

    if request.method == 'POST':
        admin = get_admin(request)
        new_email = request.POST.get('new_email', '').strip()
        current_password = request.POST.get('current_password', '').strip()

        if not new_email or not current_password:
            messages.error(request, 'All fields are required.')
            return redirect('admin_settings')

        if not check_password(current_password, admin.password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('admin_settings')

        if Admins.objects.filter(email=new_email).exclude(admin_id=admin.admin_id).exists():
            messages.error(request, 'That email is already in use.')
            return redirect('admin_settings')

        token = secrets.token_hex(32)
        PendingVerification.objects.filter(admin=admin, change_type='email').delete()
        PendingVerification.objects.create(
            admin=admin,
            token=token,
            change_type='email',
            new_value=new_email,
            expires_at=timezone.now() + timedelta(hours=1),
        )

        verify_url = f"{settings.SITE_URL}/settings/verify/{token}/" 
        send_mail(
            subject='Confirm your new email address',
            message=f'Hi {admin.first_name},\n\nClick the link below to confirm your new email address. This link expires in 1 hour.\n\n{verify_url}\n\nIf you did not request this, ignore this email.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[new_email],
            fail_silently=False,
        )

        messages.success(request, f'A verification link has been sent to {new_email}. Check your inbox.')

    return redirect('admin_settings')


def request_password_change(request):
    if not request.session.get('admin_id'):
        return redirect('signin')

    if request.method == 'POST':
        admin = get_admin(request)
        current_password = request.POST.get('current_password', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if not current_password or not new_password or not confirm_password:
            messages.error(request, 'All fields are required.')
            return redirect('admin_settings')

        if not check_password(current_password, admin.password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('admin_settings')

        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('admin_settings')

        if len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return redirect('admin_settings')

        hashed = make_password(new_password)
        token = secrets.token_hex(32)
        PendingVerification.objects.filter(admin=admin, change_type='password').delete()
        PendingVerification.objects.create(
            admin=admin,
            token=token,
            change_type='password',
            new_value=hashed,
            expires_at=timezone.now() + timedelta(hours=1),
        )

        verify_url = f"{settings.SITE_URL}/settings/verify/{token}/"
        send_mail(
            subject='Confirm your password change',
            message=f'Hi {admin.first_name},\n\nClick the link below to confirm your password change. This link expires in 1 hour.\n\n{verify_url}\n\nIf you did not request this, please change your password immediately.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin.email],
            fail_silently=False,
        )

        messages.success(request, 'A verification link has been sent to your current email. Check your inbox.')

    return redirect('admin_settings')

def verify_change(request, token):
    try:
        pending = PendingVerification.objects.get(token=token)
    except PendingVerification.DoesNotExist:
        messages.error(request, 'Invalid or already used verification link.')
        return redirect('admin_settings')

    if pending.is_expired():
        pending.delete()
        messages.error(request, 'This verification link has expired. Please try again.')
        return redirect('admin_settings')

    admin = pending.admin

    if pending.change_type == 'email':
        admin.email = pending.new_value
        admin.save()
        AuditLogs.objects.create(
            action='update',
            model_name='Admins',
            description=f'Email changed for: {admin.username}',
            performed_by_id=admin.admin_id,
        )
        messages.success(request, 'Email address updated successfully!')

    elif pending.change_type == 'password':
        admin.password = pending.new_value 
        admin.save()
        AuditLogs.objects.create(
            action='update',
            model_name='Admins',
            description=f'Password changed for: {admin.username}',
            performed_by_id=admin.admin_id,
        )
        messages.success(request, 'Password updated successfully!')

    pending.delete() 
    return redirect('admin_settings')


# Pagination
def audit_log(request):
    log_list = AuditLogs.objects.all().order_by('-performed_at')

    paginator = Paginator(log_list, 10)
    page_number = request.GET.get('page')
    logs = paginator.get_page(page_number)

    return render(request, 'audit/auditLog.html', {
        'logs': logs,
        'admin': get_admin(request),
    })