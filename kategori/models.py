from django.db import models
from core.models import BaseModel

class Kategori(BaseModel):
    nama_kategori = models.CharField(max_length=100, verbose_name="Nama Kategori")
    kode_awal = models.CharField(max_length=10, unique=True, help_text="Contoh: ELEK untuk Elektronik", verbose_name="Kode Awal")
    induk = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='sub_kategori', verbose_name="Induk Kategori")
    deskripsi = models.TextField(blank=True, null=True, verbose_name="Deskripsi")

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Daftar Kategori"
        ordering = ['nama_kategori']

    def __str__(self):
        return self.nama_kategori