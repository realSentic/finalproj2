from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),

    path('category/list/', views.category_list, name='category_list'),
    path('category/add/', views.add_category, name='add_category'),
    path('category/update/<int:categoryId>/', views.update_category, name='update_category'),
    path('category/delete/<int:categoryId>/', views.delete_category, name='delete_category'),

    path('inventory/list/', views.inventory_list, name='inventory_list'),
    path('inventory/add/', views.add_inventory, name='add_inventory'),
    path('inventory/update/<int:inventoryId>/', views.update_inventory, name='update_inventory'),
    path('inventory/delete/<int:inventoryId>/', views.delete_inventory, name='delete_inventory'),

    path('inventory/export/', views.export_inventory_csv, name='export_inventory_csv'),
    path('inventory/import/', views.import_inventory_csv, name='import_inventory_csv'),

    path('supplier/list/', views.supplier_list, name='supplier_list'),
    path('supplier/add/', views.add_supplier, name='add_supplier'),
    path('supplier/update/<int:supplierId>/', views.update_supplier, name='update_supplier'),
    path('supplier/delete/<int:supplierId>/', views.delete_supplier, name='delete_supplier'),

    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    
    path('audit/', views.audit_log, name='audit_log'),

    path('settings/', views.admin_settings, name='admin_settings'),
    path('settings/update-profile/', views.update_profile, name='update_profile'),
    path('settings/remove-picture/', views.remove_profile_picture, name='remove_profile_picture'),
    path('settings/change-email/', views.request_email_change, name='request_email_change'),
    path('settings/change-password/', views.request_password_change, name='request_password_change'),
    path('settings/verify/<str:token>/', views.verify_change, name='verify_change'),
]