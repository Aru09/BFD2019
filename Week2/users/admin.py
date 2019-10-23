from django.contrib import admin
from users.models import MainUser, Profile
from api.models import MemberProject, Task, Project, Block, TaskComment, TaskDocument
from django.contrib.auth.admin import UserAdmin


class InlineProfile(admin.StackedInline):
    model = Profile
    verbose_name = 'Profile'
    verbose_name_plural = 'Profiles'
    can_delete = False


@admin.register(MainUser)
class MainUserAdmin(UserAdmin):
    inlines = [InlineProfile,]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'bio', 'address', 'user',)

admin.site.register(MemberProject)
admin.site.register(Block)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(TaskComment)
admin.site.register(TaskDocument)