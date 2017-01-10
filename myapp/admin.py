from django.contrib import admin
from .models import challengeData
from .models import detail
from .models import detailResponse

# Register your models here.
#admin.site.register()
admin.site.register(challengeData)
admin.site.register(detail)
admin.site.register(detailResponse)