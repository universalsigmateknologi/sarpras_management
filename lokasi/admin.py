from django.contrib import admin
from .models import Lokasi

@admin.register(Lokasi)
class LokasiAdmin(admin.ModelAdmin):
    list_display = ('nama_ruangan', 'gedung', 'lantai', 'dibuat_pada')
    list_filter = ('gedung', 'lantai')
    search_fields = ('nama_ruangan', 'gedung')