from django.contrib import admin
from .models import User, UserAttribute, Tracking, TrackingDetail


class UserAttributeInline(admin.TabularInline):
    model = UserAttribute
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'sw_allow', 'creation_time')
    list_filter = ('sw_allow', 'creation_time')
    inlines = [UserAttributeInline]


@admin.register(UserAttribute)
class UserAttributeAdmin(admin.ModelAdmin):
    list_display = ('attribute_key', 'attribute_value', 'audit_time')
    list_filter = ('id_user_fK', 'attribute_key')


class TrackingDetailInline(admin.TabularInline):
    model = TrackingDetail
    extra = 0


@admin.register(Tracking)
class TrackingAdmin(admin.ModelAdmin):
    list_display = ('track_type', 'track_code', 'creation_time')
    list_filter = ('track_type', 'creation_time')
    inlines = [TrackingDetailInline]


@admin.register(TrackingDetail)
class TrackingDetailAdmin(admin.ModelAdmin):
    list_display = ('detail_head', 'detail_text', 'audit_time')
    list_filter = ('id_tracking_fk', 'detail_head')
