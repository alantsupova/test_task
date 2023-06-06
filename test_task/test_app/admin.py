from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User, Organization, Event
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['email',]
    list_filter = ['email',]
    list_display = ("email", "password")

class UserInline(admin.TabularInline):
    model = Organization.users.through
    verbose_name = "Пользователь"
    verbose_name_plural = "Пользователи"

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):

    list_display = "title", 'short_description', "address", "postcode"
    search_fields = ['title',]
    list_filter = ['title', "users"]
    exclude = ("users",)
    inlines = (
        UserInline,
    )


class OrganizationInline(admin.TabularInline):
    model = Event.organizations.through
    verbose_name = "Организация"
    verbose_name_plural = "Организации"

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = "title", "short_description", "get_image", "date"
    search_fields = ['title',]
    list_filter = ['title', "organizations", "date"]
    exclude = ("organizations",)
    inlines = (
        OrganizationInline,
    )

    def get_image(self, obj):
        return mark_safe('<img src="%s" style="width:150px;height:150px;"/>' % obj.image.url)

    get_image.short_description = "Изображение"
