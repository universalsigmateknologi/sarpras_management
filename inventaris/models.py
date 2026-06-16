from django.db import models
from core.models import BaseModel
from lokasi.models import Lokasi
from kategori.models import Kategori

# Pilihan Enum untuk Kondisi
KONDISI_CHOICES = [
    ('Baru', 'Baru'),
    ('Baik', 'Baik'),
    ('Rusak Ringan', 'Rusak Ringan'),
    ('Rusak Berat', 'Rusak Berat'),
]

class Barang(BaseModel):
    kode_aset = models.CharField(max_length=50, unique=True, verbose_name="Kode Aset")
    nama_barang = models.CharField(max_length=255, verbose_name="Nama Barang")
    
    # Foreign Keys
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Kategori")
    lokasi = models.ForeignKey(Lokasi, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Lokasi Saat Ini")
    
    # Detail Barang
    merek = models.CharField(max_length=100, blank=True, null=True, verbose_name="Merek")
    nomor_seri = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nomor Seri")
    tanggal_pembelian = models.DateField(blank=True, null=True, verbose_name="Tanggal Pembelian")
    harga_beli = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="Harga Beli (Rp)")
    kondisi = models.CharField(max_length=20, choices=KONDISI_CHOICES, default='Baik', verbose_name="Kondisi")
    
    # Media & Status
    foto = models.ImageField(upload_to='foto_barang/', blank=True, null=True, verbose_name="Foto Barang")
    tersedia = models.BooleanField(default=True, verbose_name="Tersedia untuk Dipinjam")
    catatan = models.TextField(blank=True, null=True, verbose_name="Catatan")

    class Meta:
        verbose_name = "Barang"
        verbose_name_plural = "Data Inventaris Barang"
        ordering = ['-dibuat_pada']

    def __str__(self):
        return f"{self.kode_aset} - {self.nama_barang}"