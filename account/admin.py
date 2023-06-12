from django.contrib import admin

from account.models import Child, Guardian, Otp, PortalUser

admin.site.register(PortalUser)
admin.site.register(Child)
admin.site.register(Guardian)
admin.site.register(Otp)
