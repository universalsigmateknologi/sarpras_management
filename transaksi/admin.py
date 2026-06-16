from django.contrib import admin
from .models import RiwayatBarang

@admin.register(RiwayatBarang)
class RiwayatBarangAdmin(admin.ModelAdmin):
    list_display = ('barang', 'jenis_transaksi', 'nama_peminjam', 'tanggal_keluar', 'tanggal_kembali', 'status')
    list_filter = ('jenis_transaksi', 'status', 'tanggal_keluar')
    search_fields = ('barang__nama_barang', 'barang__kode_aset', 'nama_peminjam')
    date_hierarchy = 'tanggal_keluar'
    
    # Agar admin lebih mudah input, kita buat raw_id_fields untuk dropdown barang yang banyak
    raw_id_fields = ('barang',)