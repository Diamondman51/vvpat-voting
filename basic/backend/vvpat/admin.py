from django.contrib import admin

from vvpat.models import Director, Position, President, Voter

# Register your models here.

admin.site.register(Voter)
admin.site.register(Director)
admin.site.register(President)
admin.site.register(Position)