from django.db import models, transaction
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager, UserManager, Group, Permission
)
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.dispatch import receiver
from HelperClasses.AbstractDateModels import AbstractDateModels
from HelperClasses.DjangoValidator import DjangoValidator
from RTA import settings
from EmploymentStatus.models import EmploymentStatus
from Jobs.models import Jobs

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin, AbstractDateModels):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    """
    CHOICES = (("M", "Male"), ("F", "Female"))

    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    username = models.CharField(unique=True, max_length=30)
    email = models.EmailField(max_length=128, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(
        db_column='middle_name', max_length=30)
    gender = models.CharField(
        max_length=1, choices=CHOICES)
    number_of_identification = models.CharField(
        db_column='number_of_identification', unique=True, max_length=14, validators=[DjangoValidator().validation_numberOfIdentintification])
    home_address = models.CharField(
        db_column='home_address', max_length=45,  null=True, blank=True)
    mobile = models.CharField(
        unique=True, max_length=14, validators=[DjangoValidator().validation_EgyptionMobileNumber])

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'middle_name',
                       'password', 'email', 'number_of_identification', 'mobile', 'gender']

    @property
    def full_Name(self):
        return self.first_name + ' ' + self.middle_name + ' ' + self.last_name

    @property
    def admin(self):
        return self.is_admin

    def __str__(self):
        return "{} | {}".format(self.full_Name, self.username)

    def __repr__(self):
        return "{} | {}".format(self.full_Name, self.username)

    @transaction.atomic
    def update_user_permissions(self):
        self.user_permissions.clear()
        groups = self.groups.all()
        for group in groups:
            permissions = group.permissions.all()
            for permission in permissions:
                self.user_permissions.add(permission)
        self.save()

    def save(self, *args, **kwargs):
        self.full_clean()
        super(User, self).save(*args, **kwargs)
        return self


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "please change this \n TempPassword={} \n to your new password".format(
        reset_password_token.key)

    email_from = settings.EMAIL_HOST_USER

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Ernst"),
        # message:
        email_plaintext_message,
        # from:
        email_from,
        # to:
        [reset_password_token.user.email],
        fail_silently=False

    )


class System(AbstractDateModels):
    system_id = models.AutoField(primary_key=True)
    system_ar = models.CharField(max_length=128, unique=True)
    system_en = models.CharField(max_length=128, unique=True)

    class Meta:
        managed = False
        db_table = 'System_Table'

    def __str__(self):
        return self.system_en

    def __repr__(self):
        return self.system_en


class SystemGroup(AbstractDateModels):
    system_group_id = models.AutoField(primary_key=True)
    group = models.OneToOneField(
        Group, models.CASCADE,  db_column='group_id')
    system = models.ForeignKey(System, models.CASCADE, db_column='system_id')

    class Meta:
        managed = False
        db_table = 'SystemGroup'
        unique_together = ('group', 'system')

    def __str__(self):
        return "{} | {}".format(self.group.name, self.system.system_en)

    def __repr__(self):
        return "{} | {}".format(self.group.name, self.system.system_en)


class UserEmploymentJobStatus(AbstractDateModels):
    user_employment_id = models.AutoField(
        primary_key=True, db_column='user_employment_id')
    user = models.OneToOneField(User, models.CASCADE,
                                related_name="employment_user",  db_column="user_id")
    employment = models.ForeignKey(
        EmploymentStatus, models.CASCADE, db_column="employment_id")
    job = models.ForeignKey(Jobs, models.CASCADE, db_column="job_id")
    action_user = models.ForeignKey(
        User, models.CASCADE, related_name="creator_user_emp", db_column="action_user")

    class Meta:
        managed = False
        db_table = 'UserEmploymentJobStatus'
        unique_together = ('user', 'employment', 'job')

    def __str__(self):
        return "{} | {} | {}".format(self.user.full_Name, self.employment.employment_title_En, self.job.job_title_En)

    def __repr__(self):
        return "{} | {} | {}".format(self.user.full_Name, self.employment.employment_title_En, self.job.job_title_En)
