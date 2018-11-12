from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name,
                    password=None, is_active=True, is_staff=False, is_admin=False):
        '''
            creates & saves a User with the given email,
            password and other flags
        '''
        if not email:
            raise ValueError('Email can\'t be left blank.')
        if not password:
            raise ValueError('Password can\'t be left blank.')

        user_obj = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, first_name, last_name, password):
        '''
            creates & saves a staff_user with the given email,
            password and other flags
        '''
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user

class User(AbstractBaseUser):
    email       = models.EmailField(verbose_name='Email Address', max_length=255, unique=True)
    first_name  = models.CharField(max_length=50, blank=True, null=True)
    last_name   = models.CharField(max_length=50, blank=True, null=True)
    active      = models.BooleanField(default=True)
    staff       = models.BooleanField(default=False)
    admin       = models.BooleanField(default=False)
    timestamp   = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name'
    ]

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_fullname(self):
        return f'{self.first_name} {self.last_name}'

    def get_shortname(self):
        return f'{self.first_name}'

    def has_perm(self, perm, obj=None):
        '''
        :param perm: Does the user have a specific permission?
        :param obj:
        :return: Simplest answer - Yes, always
        '''
        return True

    def has_module_perms(self, app_label):
        '''
        :param app_label: Does the user have permissions to view the app `app_label`?
        :return: Simplest possible answer: Yes, always
        '''
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

class Guest(models.Model):
    email       = models.EmailField(max_length=255, unique=True)
    active      = models.BooleanField(default=True)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
