from django.db import models

class BaseModel(models.Model):
    """
    Model abstrak dasar yang akan di-extends oleh model lain.
    Menyimpan timestamp pembuatan dan update terakhir.
    """
    dibuat_pada = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat Pada")
    diperbarui_pada = models.DateTimeField(auto_now=True, verbose_name="Diperbarui Pada")

    class Meta:
        abstract = True  # Penting: ini membuat model tidak membuat tabel di database