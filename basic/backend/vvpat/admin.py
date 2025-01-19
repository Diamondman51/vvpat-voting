import random
from django.contrib import admin
from vvpat.models import Director, President, User, Voter

# Register your models here.

class DirectorAdmin(admin.ModelAdmin):
    list_display = ('id', "first_name", 'last_name', 'membership_num')
    search_fields = ('first_name', "last_name")


class UserAdmin(admin.ModelAdmin):
    search_fields = ("first_name", "last_name", 'membership_num', 'phone')
    list_display = ('uuid', 'first_name', 'last_name', 'username', 'phone', 'email')
    mem_nums = [[str(random.randint(0, 9)) for _ in range(10)] for _ in range(100000)]
    def get_changeform_initial_data(self, request):
        mem_num = random.choice(self.mem_nums)
        random_num = ''.join(mem_num)
        user = User.objects.filter(membership_num=f"A/C {random_num}")
        user = user.exists()
        if not user:
            UserAdmin.mem_nums.remove(mem_num)
            return {
                'membership_num': f"A/C {random_num}",
            }
    
    def save_model(self, request, obj: User, form, change):
        obj._request = request
        if not obj.membership_num:
            mem_num = random.choice(self.mem_nums)
            random_num = ''.join(mem_num)
            obj.membership_num = f'A/C {random_num}'
        if not obj.is_director and not obj.is_president and not obj.is_employee:
            obj.is_employee = True
        return super().save_model(request, obj, form, change)


class PresidentAdmin(admin.ModelAdmin):
    list_display = ('id', "first_name", "last_name", 'membership_num')



class VoterAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'uuid', 'membership_num')
    
    def membership_num(self, obj):
        return obj.user_id.membership_num
    
    def uuid(self, obj):
        return obj.user_id.uuid
    
    def save_model(self, request, obj: Voter, form, change):
        if not obj.directors_vote:
            obj.directors_vote = []
        return super().save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)
admin.site.register(Voter, VoterAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(President, PresidentAdmin)
