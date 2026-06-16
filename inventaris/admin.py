from django.contrib import admin
from .models import Barang

@admin.register(Barang)
class BarangAdmin(admin.ModelAdmin):
    list_display = ('kode_aset', 'nama_barang', 'kategori', 'lokasi', 'kondisi', 'tersedia')
    list_filter = ('kondisi', 'tersedia', 'kategori', 'lokasi')
    search_fields = ('kode_aset', 'nama_barang', 'merek', 'nomor_seri')
    readonly_fields = ('dibuat_pada', 'diperbarui_pada')
    
    # Agar tampilan input di admin lebih rapi (Fieldset)
    fieldsets = (
        ('Informasi Utama', {
            'fields': ('kode_aset', 'nama_barang', 'kategori', 'lokasi')
        }),
        ('Detail Spesifikasi', {
            'fields': ('merek', 'nomor_seri', 'kondisi', 'foto')
        }),
        ('Informasi Pembelian', {
            'fields': ('tanggal_pembelian', 'harga_beli')
        }),
        ('Status & Keterangan', {
            'fields': ('tersedia', 'catatan')
        }),
        ('Timestamp', {
            'fields': ('dibuat_pada', 'diperbarui_pada'),
            'classes': ('collapse',)
        }),
    )