from django.contrib import admin
from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "price")
    list_filter = ("category",)
    search_fields = ("description",)
