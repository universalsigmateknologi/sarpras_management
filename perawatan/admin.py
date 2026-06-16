from django.contrib import admin
from .models import JadwalPerawatan

@admin.register(JadwalPerawatan)
class JadwalPerawatanAdmin(admin.ModelAdmin):
    list_display = ('barang', 'kerusakan', 'tanggal_perbaikan', 'status_perbaikan', 'biaya')
    list_filter = ('status_perbaikan', 'tanggal_perbaikan')
    search_fields = ('barang__nama_barang', 'teknisi')
    raw_id_fields = ('barang',)