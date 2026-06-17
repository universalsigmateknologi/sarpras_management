from django.db import models
from django.utils import timezone


class Jurusan(models.Model):
    """
    Data jurusan/program keahlian di SMK Nurul Jadid.
    """
    nama = models.CharField(max_length=100, unique=True, verbose_name="Nama Jurusan")
    kode = models.CharField(max_length=10, unique=True, verbose_name="Kode Jurusan")
    deskripsi = models.TextField(verbose_name="Deskripsi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Jurusan"
        verbose_name_plural = "Data Jurusan"
        ordering = ['nama']

    def __str__(self):
        return f"{self.kode} - {self.nama}"



class Kelas(models.Model):
    """
    Data kelas di SMK Nurul Jadid.
    Setiap kelas terhubung dengan satu jurusan.
    """
    TINGKAT_CHOICES = [
        ('10', 'X (Sepuluh)'),
        ('11', 'XI (Sebelas)'),
        ('12', 'XII (Dua Belas)'),
    ]

    # Hubungan dengan jurusan
    jurusan = models.ForeignKey(
        Jurusan,
        on_delete=models.CASCADE,
        related_name='kelas',
        verbose_name="Jurusan"
    )

    # Identitas kelas
    tingkat = models.CharField(
        max_length=2,
        choices=TINGKAT_CHOICES,
        verbose_name="Tingkat"
    )
    tahun_ajaran = models.CharField(
        max_length=9,
        verbose_name="Tahun Ajaran",
        help_text="Contoh: 2024/2025"
    )

    # Informasi tambahan
    ruangan = models.ForeignKey(
        'lokasi.Lokasi',
        on_delete=models.PROTECT,
        related_name='kelas',
        blank=True,
        null=True,
        verbose_name="Ruangan"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Kelas"
        verbose_name_plural = "Data Kelas"
        ordering = ['tahun_ajaran', 'tingkat', 'jurusan__nama']

    def __str__(self):
        return f"{self.get_tingkat_display()} {self.jurusan.nama} ({self.tahun_ajaran})"

    @property
    def nama_lengkap(self):
        """
        Menghasilkan nama lengkap kelas.
        Contoh: X RPL
        """
        return f"{self.get_tingkat_display()} {self.jurusan.nama}"

    @property
    def kode_kelas(self):
        """
        Menghasilkan kode kelas.
        Contoh: 10-RPL-2024
        """
        return f"{self.tingkat}-{self.jurusan.kode}-{self.tahun_ajaran[:4]}"
