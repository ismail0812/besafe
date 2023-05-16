from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser,UserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CostumUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'),max_length=100, unique=True)
    
    phone = models.CharField(_('phone'),max_length=15,blank=True)
    gender = models.CharField(_('gender'),max_length=7,blank=True)
    birthday = models.DateField(_('birthday'),blank=True, null=True)
    housedevice_id = models.CharField(_('house device id'), max_length=255, blank=True)
    cardevice_id = models.CharField(_('car device id'), max_length=255, blank=True)
    bloodtype = models.CharField(_('blood type'),max_length=3, null=True)
    allergy = models.TextField(_('allergy'),max_length=255, blank=True, null=True)
    healthissues = models.TextField(_('health issues'),max_length=255, blank=True, null=True)
    surgery = models.CharField(_('surgery'),max_length=6, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    object = CustomUserManager()

class Housedata(models.Model):
    user = models.ForeignKey(CostumUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    gas = models.SmallIntegerField()
    fire = models.SmallIntegerField()
    earthquake = models.SmallIntegerField()

class Cardata(models.Model):
    user = models.ForeignKey(CostumUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    gas = models.SmallIntegerField()
    fire = models.SmallIntegerField()
    gps = models.CharField(_('gps'), max_length=255)

# class Client(models.Model):
#     user = models.ForeignKey(CostumUser, on_delete=models.CASCADE)
#     phone = models.CharField(_('phone'),max_length=15,blank=True)
#     gender = models.CharField(_('gender'),max_length=7,blank=True)
#     birthday = models.DateField(_('birthday'),blank=True, null=True)
#     housedevice_id = models.CharField(_('device id'), max_length=255, unique=True, blank=True)
#     cardevice_id = models.CharField(_('device id'), max_length=255, unique=True, blank=True)
#     bloodtype = models.CharField(_('blood type'),max_length=3,null=True)
#     allergy = models.TextField(_('allergy'),max_length=255,null=True)
#     healthissues = models.TextField(_('health issues'),max_length=255,null=True)
#     surgery = models.CharField(_('surgery'),max_length=6,null=True)


    



