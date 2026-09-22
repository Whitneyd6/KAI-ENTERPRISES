from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Department, Equipment


class StoreTestCase(TestCase):
    """Shared sample data, rebuilt fresh for the tests in this class."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='tester', password='testpass123'
        )
        cls.medicine = Department.objects.create(
            name='School of Medicine', slug='medicine'
        )
        cls.law = Department.objects.create(
            name='School of Law', slug='law'
        )
        cls.cs = Department.objects.create(
            name='School of Computer Science', slug='computer-science'
        )
        cls.stethoscope = Equipment.objects.create(
            department=cls.medicine,
            name='Stethoscope',
            price='45.00',
            quantity_in_stock=30,
        )
        cls.briefcase = Equipment.objects.create(
            department=cls.law,
            name='Leather Briefcase',
            price='85.00',
            quantity_in_stock=20,
        )


class ModelTests(StoreTestCase):
    def test_department_str_is_its_name(self):
        self.assertEqual(str(self.medicine), 'School of Medicine')

    def test_equipment_str_includes_department(self):
        self.assertEqual(
            str(self.stethoscope), 'Stethoscope (School of Medicine)'
        )


class LoginTests(StoreTestCase):
    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_valid_login_goes_to_dashboard(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'tester', 'password': 'testpass123'},
        )
        self.assertRedirects(response, reverse('dashboard'))

    def test_wrong_password_shows_error(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'tester', 'password': 'wrong-password'},
        )
        self.assertContains(response, 'Incorrect username or password')


class DashboardTests(StoreTestCase):
    def test_anonymous_user_is_sent_to_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/login/?next=/')

    def test_logged_in_user_sees_all_three_departments(self):
        self.client.login(username='tester', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, 'School of Medicine')
        self.assertContains(response, 'School of Law')
        self.assertContains(response, 'School of Computer Science')

    def test_dashboard_counts_are_correct(self):
        self.client.login(username='tester', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        medicine = response.context['departments'].get(slug='medicine')
        self.assertEqual(medicine.item_count, 1)
        self.assertEqual(medicine.total_stock, 30)


class DepartmentPageTests(StoreTestCase):
    def test_anonymous_user_is_sent_to_login(self):
        response = self.client.get(
            reverse('department_detail', args=['medicine'])
        )
        self.assertRedirects(response, '/login/?next=/departments/medicine/')

    def test_page_shows_only_that_departments_equipment(self):
        self.client.login(username='tester', password='testpass123')
        response = self.client.get(
            reverse('department_detail', args=['medicine'])
        )
        self.assertContains(response, 'Stethoscope')
        self.assertNotContains(response, 'Leather Briefcase')

    def test_unknown_department_gives_404(self):
        self.client.login(username='tester', password='testpass123')
        response = self.client.get(
            reverse('department_detail', args=['does-not-exist'])
        )
        self.assertEqual(response.status_code, 404)

    def test_out_of_stock_badge_appears(self):
        Equipment.objects.create(
            department=self.medicine,
            name='Scalpel Set',
            price='20.00',
            quantity_in_stock=0,
        )
        self.client.login(username='tester', password='testpass123')
        response = self.client.get(
            reverse('department_detail', args=['medicine'])
        )
        self.assertContains(response, 'Out of stock')