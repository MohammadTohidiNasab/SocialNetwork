from django.test import TestCase
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
# Create your tests here.



#forms test
class TestRegisterationForm(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='mohammad',email='mohammad@email.com', password='mohammad123')
        
    def test_valide_data(self):
        form = UserRegistrationForm(data= {'username': 'mohmad','email': 'mohamd@gmail.com', 
                                           'password1':'mohamad', 'password2': 'mohamad'})
        self.assertTrue(form.is_valid())

    def test_empty_data(self):
        form = UserRegistrationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors),4)
        
        
    def test_exist_email(self):
        form = UserRegistrationForm(data= {'username': 'mmd','email': 'mohammad@email.com', 
                                             'password1':'mmd', 'password2': 'mmd'})
        self.assertEqual(len(form.errors),1)
        self.assertTrue(form.has_error('email'))
        
    def test_unmatched_passwords(self):
            form = UserRegistrationForm(data= {'username': 'mmd','email': 'tohidi@email.com', 
                                                          'password1':'mmd', 'password2': 'mmd123'})
            self.assertEqual(len(form.errors),1)
            self.assertTrue(form.has_error)


