from django.contrib import admin
from models import CollectItem, CollectTag


class CollectItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(CollectItem, CollectItemAdmin)


class CollectTagAdmin(admin.ModelAdmin):
    pass
admin.site.register(CollectTag, CollectTagAdmin)
