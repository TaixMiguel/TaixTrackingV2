from django.contrib import admin
from .models import UserAttribute, Tracking, TrackingDetail, TrackingUser


@admin.register(UserAttribute)
class UserAttributeAdmin(admin.ModelAdmin):
    list_display = ('attribute_key', 'attribute_value', 'audit_time')
    list_filter = ('id_user_fK', 'attribute_key')


class TrackingDetailInline(admin.TabularInline):
    model = TrackingDetail
    extra = 0


class TrackingUserInline(admin.TabularInline):
    model = TrackingUser
    extra = 0


@admin.register(Tracking)
class TrackingAdmin(admin.ModelAdmin):
    list_display = ('track_type', 'track_code', 'creation_time')
    list_filter = ('track_type', 'creation_time')
    inlines = [TrackingDetailInline, TrackingUserInline]


@admin.register(TrackingDetail)
class TrackingDetailAdmin(admin.ModelAdmin):
    list_display = ('detail_head', 'detail_text', 'audit_time')
    list_filter = ('id_tracking_fk', 'detail_head')


@admin.register(TrackingUser)
class TrackingUserAdmin(admin.ModelAdmin):
    list_display = ('id_user_fK', 'id_tracking_fk')
    list_filter = ('id_user_fK', 'id_tracking_fk')
