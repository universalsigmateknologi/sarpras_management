from django import forms
from .models import Barang


class BarangForm(forms.ModelForm):
    class Meta:
        model = Barang
        fields = [
            'kode_aset',
            'nama_barang',
            'kategori',
            'lokasi',
            'merek',
            'nomor_seri',
            'tanggal_pembelian',
            'harga_beli',
            'kondisi',
            'foto',
            'tersedia',
            'catatan',
        ]
        widgets = {
            'kode_aset': forms.TextInput(attrs={'class': 'w-full text-sm bg-subtle border-0 rounded-lg p-3 focus:outline-none focus:ring-1 focus:ring-ink/20 font-body'}),
            'nama_barang': forms.TextInput(attrs={'class': 'w-full text-sm bg-subtle border-0 rounded-lg p-3 focus:outline-none focus:ring-1 focus:ring-ink/20 font-body'}),
            'kategori': forms.Select(attrs={'class': 'w-full text-sm bg-subtle border-0 rounded-lg p-3 focus:outline-none focus:ring-1 focus:ring-ink/20 font-body'}),
            'lokasi': forms.Select(attrs={'class': 'w-full text-sm bg-subtle border-0 rounded-lg p-3 focus:outline-none focus:ring-1 focus:ring-ink/20 font-body'}),
            'merek': forms.TextInput(attrs={'class': 'w-full text-sm bg-subtle border-0 rounded-lg p-3 focus:outline-none focus:ring-1 focus:ring-ink/20 font-body'}),
            'nomor_seri': forms.TextInput(attrs={'class': 'w-full text-sm bg-subtle border-0 rounded-lg p-3 focus:outline-none focus:ring-1 focus:ring-ink/20 font-body'}),
            'tanggal_pembelian': forms.DateInput(attrs={'type': 'date', 'class': 'w-full text-sm bg-subtle border-0 rounded-lg p-3 focus:outline-none focus:ring-1 focus:ring-ink/20 font-body'}),
            'harga_beli': forms.NumberInput(attrs={'class': 'w-full text-sm bg-subtle border-0 rounded-lg p-3 focus:outline-none focus:ring-1 focus:ring-ink/20 font-body'}),
            'kondisi': forms.Select(attrs={'class': 'w-full text-sm bg-subtle border-0 rounded-lg p-3 focus:outline-none focus:ring-1 focus:ring-ink/20 font-body'}),
            'foto': forms.FileInput(attrs={'class': 'w-full text-sm bg-subtle border-0 rounded-lg p-3 focus:outline-none focus:ring-1 focus:ring-ink/20 font-body'}),
            'catatan': forms.Textarea(attrs={'class': 'w-full text-sm bg-subtle border-0 rounded-lg p-3 focus:outline-none focus:ring-1 focus:ring-ink/20 font-body resize-none', 'rows': 4}),
        }
