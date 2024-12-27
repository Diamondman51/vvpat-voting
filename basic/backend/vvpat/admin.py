import random
from django.contrib import admin

from vvpat.models import Director, President, User, Voter

# Register your models here.

class DirectorAdmin(admin.ModelAdmin):
    list_display = ('id', "first_name", 'last_name',)
    list_editable = ("first_name", "last_name",)
    # list_filter = ('side', )


class UserAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'first_name', 'last_name', 'username', 'phone', 'email')

    def get_changeform_initial_data(self, request):
        random_num = [str(random.randint(0, 9)) for _ in range(10)]
        random_num = ''.join(random_num)
        user = User.objects.filter(membership_num=f"A/C {random_num}")
        user = user.exists()
        if not user:
            return {
                'membership_num': f"A/C {random_num}",
            }
        else:
            self.get_changeform_initial_data(request)
    

class PresidentAdmin(admin.ModelAdmin):
    list_display = ('id', "first_name", "last_name")


class VoterAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')


admin.site.register(User, UserAdmin)
admin.site.register(Voter, VoterAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(President, PresidentAdmin)
