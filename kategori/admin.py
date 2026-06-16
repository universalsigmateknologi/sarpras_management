from django.contrib import admin
from .models import Kategori

@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ('nama_kategori', 'kode_awal', 'induk', 'dibuat_pada')
    search_fields = ('nama_kategori', 'kode_awal')
    list_filter = ('induk',)