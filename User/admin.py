from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission

from User.forms import UserAdminCreationForm, UserAdminChangeForm
# Register your models here.


User = get_user_model()

admin.site.register(Permission)


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['full_Name',
                    'email', 'number_of_identification', 'mobile', 'gender', 'created_at', 'modified_at']
    list_filter = ['is_superuser', 'is_active', 'is_staff', 'is_admin']
    fieldsets = (
        ('Regesitration info', {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'middle_name',
                                      'number_of_identification', 'mobile', 'gender')}),
        ('Permissions', {'fields': ('is_superuser',
                                    'is_active', 'is_staff', 'is_admin')}),
        ('Group Permissions', {
            'classes': ('wide',),
            'fields': ('groups',)
        }),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        ('Regesitration info', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password')}
         ),
        (
            'Personal info', {'fields': ('first_name', 'last_name', 'middle_name',
                                         'number_of_identification', 'mobile', 'gender')}
        ),
        (
            'Permissions', {'fields': ('is_superuser',
                                       'is_active', 'is_staff', 'is_admin')}
        )
    )
    search_fields = ['username']
    ordering = ['created_at']
    filter_horizontal = ('groups',)


admin.site.register(User, UserAdmin)
