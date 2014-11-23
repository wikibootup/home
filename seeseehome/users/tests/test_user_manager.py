from django.test import TestCase
from users.models import User
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from seeseehome import testdata

class UserManagerTestCase(TestCase):
    def setUp(self):
        pass    

    def test_create_user(self):
        print (testdata.users_valid_password)
        self.assertIsNotNone(
            User.objects.create_user(
                username = testdata.users_valid_name,
                email = testdata.users_valid_email,
                password = testdata.users_valid_password,
            )
        )

    def test_get_user(self):
        user = User.objects.create_user(
                   username = testdata.users_valid_name,
                   email = testdata.users_valid_email,
                   password = testdata.users_valid_password,
               )
                                
        self.assertIsNotNone(
            User.objects.get_user(
                id = user.id
            )
        )

    def test_user_password_without_alphabet_char(self):
        self.assertRaises(
            ValidationError,
            User.objects.create_user,
            username = testdata.users_valid_name,
            email = testdata.users_valid_email,
            password = testdata.users_pwd_without_alphabet_char,
        )

    def test_user_password_without_special_char(self):
        self.assertRaises(
            ValidationError,
            User.objects.create_user,
            username = testdata.users_valid_name,
            email = testdata.users_valid_email,
            password = testdata.users_pwd_without_special_char,
        )


