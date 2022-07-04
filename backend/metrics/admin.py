from django.contrib import admin

from .models import Metrics, Notifications

class MetricsAdmin(admin.ModelAdmin):
    list_filter = ('device_id', 'metric', 'report')
    list_display = ('pk', 'device_id', 'metric', 'report')
admin.site.register(Metrics, MetricsAdmin)

class NotificationsAdmin(admin.ModelAdmin):
    list_filter = ('created',)
    list_display = ('pk', 'message')
admin.site.register(Notifications, NotificationsAdmin)