from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .models import User

#
# class UserAdmin(BaseUserAdmin):
#     form = UserAdminChangeForm
#     add_form = UserAdminCreationForm
#
#     list_display = ('email', 'admin')
#     list_filter = ('admin',)
#
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal Info', {'fields': ()}),
#         ('Permissions', {'fields': ('admin',)}),
#     )
#
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide', ),
#             'fields': ('email', 'password1', 'password2')}
#          )
#     )
#     search_fields = ('email',)
#     ordering = ('email',)
#     filter_horizontal = ()


admin.site.register(User)
# admin.site.unregister(Group)
