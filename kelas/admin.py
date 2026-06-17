from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Jurusan, Kelas



@admin.register(Jurusan)
class JurusanAdmin(admin.ModelAdmin):
    list_display = [
        'kode',
        'nama',
        'created_at'
    ]

    search_fields = [
        'nama',
        'kode',
        'deskripsi'
    ]

    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Informasi Jurusan', {
            'fields': (
                'nama',
                'kode',
                'deskripsi'
            )
        }),
        ('Status', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )



@admin.register(Kelas)
class KelasAdmin(admin.ModelAdmin):
    list_display = [
        'nama_lengkap_display',
        'jurusan',
        'tingkat',
        'tahun_ajaran',
        'ruangan',
        'kode_kelas_display'
    ]

    list_filter = [
        'jurusan',
        'tingkat',
        'tahun_ajaran',
    ]

    search_fields = [
        'jurusan__nama',
        'jurusan__kode',
        'ruangan__nama_ruangan',
        'ruangan__gedung',
    ]

    readonly_fields = ['created_at', 'updated_at', 'kode_kelas_display']

    autocomplete_fields = ['jurusan']

    fieldsets = (
        ('Identitas Kelas', {
            'fields': (
                'jurusan',
                'tingkat',
                'tahun_ajaran',
            )
        }),
        ('Informasi Tambahan', {
            'fields': (
                'ruangan',
            )
        }),
        ('Status', {
            'fields': (
                'kode_kelas_display',
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )

    def nama_lengkap_display(self, obj):
        """
        Menampilkan nama lengkap kelas dengan link ke filter.
        """
        url = reverse('admin:app_kelas_changelist') + f'?q={obj.nama_lengkap}'
        return format_html(
            '<a href="{}" style="font-weight: bold;">{}</a>',
            url,
            obj.nama_lengkap
        )

    nama_lengkap_display.short_description = "Nama Kelas"

    def kode_kelas_display(self, obj):
        """
        Menampilkan kode kelas yang di-generate otomatis.
        """
        return format_html(
            '<code style="background: #f8f9fa; padding: 5px 10px; border-radius: 4px; font-size: 1.1em;">{}</code>',
            obj.kode_kelas
        )

    kode_kelas_display.short_description = "Kode Kelas"

    def save_model(self, request, obj, form, change):
        """
        Override save untuk validasi tambahan.
        """
        # Auto-set tahun ajaran jika kosong
        if not obj.tahun_ajaran:
            current_year = timezone.now().year
            obj.tahun_ajaran = f"{current_year}/{current_year + 1}"

        super().save_model(request, obj, form, change)

    def get_actions(self, request):
        """
        Menambahkan action untuk copy kelas ke tahun ajaran berikutnya.
        """
        actions = super().get_actions(request)
        actions['copy_to_next_year'] = (
            self.copy_to_next_year,
            'copy_to_next_year',
            'Copy kelas ke tahun ajaran berikutnya'
        )
        return actions

    def copy_to_next_year(self, request, queryset):
        """
        Action untuk mengcopy kelas ke tahun ajaran berikutnya.
        """
        count = 0
        for kelas in queryset:
            try:
                tahun_awal = int(kelas.tahun_ajaran.split('/')[0])
                tahun_berikutnya = f"{tahun_awal + 1}/{tahun_awal + 2}"

                existing = Kelas.objects.filter(
                    jurusan=kelas.jurusan,
                    tingkat=kelas.tingkat,
                    tahun_ajaran=tahun_berikutnya
                ).exists()

                if not existing:
                    Kelas.objects.create(
                        jurusan=kelas.jurusan,
                        tingkat=kelas.tingkat,
                        tahun_ajaran=tahun_berikutnya,
                        ruangan=kelas.ruangan,
                    )
                    count += 1
            except (ValueError, IndexError):
                pass

        self.message_user(
            request,
            f"Berhasil mengcopy {count} kelas ke tahun ajaran berikutnya."
        )

    copy_to_next_year.short_description = "Copy ke tahun ajaran berikutnya"
