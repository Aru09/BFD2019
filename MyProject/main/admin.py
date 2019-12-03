from django.contrib import admin
from main.models import City,AudCompany,ReviewedCompany,Review,Order,Auditor
from users.models import MainUser, Profile



admin.site.register(City)
admin.site.register(Auditor)
admin.site.register(AudCompany)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(ReviewedCompany)
# Register your models here.
