from django.contrib import admin
from .models import Library
from .models import Livre


# Register your models here.

admin.site.register(Livre)
admin.site.register(Library)