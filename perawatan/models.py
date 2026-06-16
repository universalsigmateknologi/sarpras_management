from django.db import models
from core.models import BaseModel
from inventaris.models import Barang

STATUS_PERBAIKAN_CHOICES = [
    ('PENGAJUAN', 'Pengajuan'),
    ('PROSES', 'Sedang Diperbaiki'),
    ('SELESAI', 'Selesai'),
]

class JadwalPerawatan(BaseModel):
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE, verbose_name="Barang")
    kerusakan = models.TextField(verbose_name="Deskripsi Kerusakan")
    tindakan = models.TextField(blank=True, null=True, verbose_name="Tindakan Perbaikan")
    biaya = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="Biaya Perbaikan")
    tanggal_perbaikan = models.DateField(blank=True, null=True, verbose_name="Tanggal Perbaikan")
    teknisi = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nama Teknisi/Vendor")
    status_perbaikan = models.CharField(max_length=20, choices=STATUS_PERBAIKAN_CHOICES, default='PENGAJUAN', verbose_name="Status")

    class Meta:
        verbose_name = "Perawatan Barang"
        verbose_name_plural = "Data Perawatan Barang"
        ordering = ['-dibuat_pada']

    def __str__(self):
        return f"Perawatan: {self.barang.nama_barang}"