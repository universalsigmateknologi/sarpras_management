from django.db import models
from core.models import BaseModel

class Lokasi(BaseModel):
    nama_ruangan = models.CharField(max_length=100, verbose_name="Nama Ruangan")
    gedung = models.CharField(max_length=50, blank=True, null=True, verbose_name="Gedung")
    lantai = models.IntegerField(blank=True, null=True, verbose_name="Lantai")
    keterangan = models.TextField(blank=True, null=True, verbose_name="Keterangan")

    class Meta:
        verbose_name = "Lokasi"
        verbose_name_plural = "Daftar Lokasi"
        ordering = ['gedung', 'lantai', 'nama_ruangan']

    def __str__(self):
        return f"{self.nama_ruangan} - {self.gedung}"