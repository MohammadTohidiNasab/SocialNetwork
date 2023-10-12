from django.test import TestCase, Client
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from .forms import UserLoginForm
from django.urls import reverse

# Create your tests here.


# forms test
class TestRegisterationForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username="mohammad", email="mohammad@email.com", password="mohammad123"
        )

    def test_valide_data(self):
        form = UserRegistrationForm(
            data={
                "username": "mohmad",
                "email": "mohamd@gmail.com",
                "password1": "mohamad",
                "password2": "mohamad",
            }
        )
        self.assertTrue(form.is_valid())

    def test_empty_data(self):
        form = UserRegistrationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_exist_email(self):
        form = UserRegistrationForm(
            data={
                "username": "mmd",
                "email": "mohammad@email.com",
                "password1": "mmd",
                "password2": "mmd",
            }
        )
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error("email"))

    def test_unmatched_passwords(self):
        form = UserRegistrationForm(
            data={
                "username": "mmd",
                "email": "tohidi@email.com",
                "password1": "mmd",
                "password2": "mmd123",
            }
        )
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error)


# test registretion view
class TestUserRegisterView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_register_GET(self):
        response = self.client.get(reverse("account:user_register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/register.html")
        self.failUnless(response.context["form"], UserRegistrationForm)

    def test_user_register_POST_valid(self):
        response = self.client.post(
            reverse("account:user_register"),
            data={
                "username": "mohammad",
                "email": "mme@gmail.com",
                "password1": "mmd",
                "password2": "mmd",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home:home"))
        self.assertEqual(User.objects.count(), 1)

    def test_user_register_POST_invalid(self):
        response = self.client.post(
            reverse("account:user_register"),
            data={
                "username": "mohamad",
                "email": "invalid email",
                "password1": "mmd22",
                "password2": "mmd22",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context["form"].is_valid())
        self.assertFormError(
            form=response.context["form"],
            field="email",
            errors=["یک ایمیل آدرس معتبر وارد کنید."],
        )


# user log out view


class UserLogOutView(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(
            username="tohidi", email="tohidi@email.com", password="tohidi123"
        )
        self.client.login(
            username="tohidi", email="tohidi@email.com", password="tohidi123"
        )

    def test_user_loguou(self):
        response = self.client.get(reverse("account:user_logout"))
        self.assertEqual(response.status_code, 302)
