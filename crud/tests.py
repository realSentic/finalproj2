from django.test import TestCase
from django.urls import reverse

from .models import Admins, AuditLogs, Suppliers


class SupplierViewsTests(TestCase):
    def setUp(self):
        self.admin = Admins.objects.create(
            first_name='Test',
            last_name='Admin',
            username='testadmin',
            email='test@example.com',
            password='hashedpassword',
        )

        session = self.client.session
        session['admin_id'] = self.admin.admin_id
        session['admin_username'] = self.admin.username
        session.save()

    def test_supplier_list_page_loads(self):
        response = self.client.get(reverse('supplier_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'suppliers/supplierList.html')

    def test_add_supplier_creates_record_and_audit_log(self):
        response = self.client.post(reverse('add_supplier'), {
            'supplier_name': 'Fresh Beans Co.',
            'contact_person': 'Mina',
            'email': 'mina@beans.com',
            'phone_number': '1234567',
            'address': 'Cafe Street',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Suppliers.objects.filter(supplier_name='Fresh Beans Co.').exists())
        self.assertTrue(AuditLogs.objects.filter(model_name='Suppliers', action='create').exists())

    def test_update_supplier_updates_record_and_audit_log(self):
        supplier = Suppliers.objects.create(supplier_name='Old Name')
        response = self.client.post(reverse('update_supplier', args=[supplier.supplier_id]), {
            'supplier_name': 'New Name',
            'contact_person': '',
            'email': '',
            'phone_number': '',
            'address': '',
        })
        self.assertEqual(response.status_code, 302)
        supplier.refresh_from_db()
        self.assertEqual(supplier.supplier_name, 'New Name')
        self.assertTrue(AuditLogs.objects.filter(model_name='Suppliers', action='update').exists())

    def test_delete_supplier_deletes_record_and_audit_log(self):
        supplier = Suppliers.objects.create(supplier_name='Delete Me')
        response = self.client.post(reverse('delete_supplier', args=[supplier.supplier_id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Suppliers.objects.filter(supplier_id=supplier.supplier_id).exists())
        self.assertTrue(AuditLogs.objects.filter(model_name='Suppliers', action='delete').exists())
