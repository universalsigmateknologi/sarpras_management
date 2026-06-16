from django.db import models
from core.models import BaseModel
from inventaris.models import Barang

# Pilihan Enum
JENIS_TRANSAKSI_CHOICES = [
    ('KELUAR', 'Peminjaman (Keluar)'),
    ('KEMBALI', 'Pengembalian (Masuk)'),
    ('MUTASI', 'Mutasi (Pindah Lokasi)'),
    ('PERBAIKAN', 'Perbaikan'),
]

STATUS_TRANSAKSI_CHOICES = [
    ('BERLANGSUNG', 'Sedang Berlangsung'),
    ('SELESAI', 'Selesai'),
    ('BATAL', 'Dibatalkan'),
    ('TERLAMBAT', 'Terlambat Kembali'),
]

class RiwayatBarang(BaseModel):
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE, verbose_name="Barang")
    jenis_transaksi = models.CharField(max_length=20, choices=JENIS_TRANSAKSI_CHOICES, verbose_name="Jenis Transaksi")
    
    # Jika hanya ada 1 user, nama peminjam diinput manual
    nama_peminjam = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nama Peminjam/Penerima")
    tujuan = models.CharField(max_length=255, blank=True, null=True, verbose_name="Tujuan/Keperluan")
    
    tanggal_keluar = models.DateTimeField(verbose_name="Tanggal Keluar/Pinjam")
    tanggal_kembali = models.DateTimeField(blank=True, null=True, verbose_name="Tanggal Kembali (Actual)")
    
    status = models.CharField(max_length=20, choices=STATUS_TRANSAKSI_CHOICES, default='BERLANGSUNG', verbose_name="Status")
    keterangan = models.TextField(blank=True, null=True, verbose_name="Keterangan Tambahan")

    class Meta:
        verbose_name = "Riwayat Transaksi"
        verbose_name_plural = "Riwayat Transaksi"
        ordering = ['-tanggal_keluar']

    def __str__(self):
        return f"{self.barang.nama_barang} - {self.jenis_transaksi} ({self.tanggal_keluar})"