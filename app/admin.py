from django.contrib import admin

# Register your models here.
from app.models import UserProfile,TempUser,Studies,UploadedDocument,Universitie,Course

admin.site.register(UserProfile)
admin.site.register(TempUser)
admin.site.register(Studies)
admin.site.register(UploadedDocument)
admin.site.register(Universitie)
admin.site.register(Course)
