from django.contrib import admin
from django.http import HttpRequest
from .models import MenuLink, SiteSetup


class MenuLinkInline(admin.TabularInline):
    model = MenuLink
    extra = 1


@admin.register(SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):
    list_display = 'title', 'description'
    inlines = MenuLinkInline,

    def has_add_permission(self, request: HttpRequest) -> bool:
        # basically, if has some register in DB, the user is not allowed to add
        # another one (in SiteSetup)
        return not SiteSetup.objects.exists()
