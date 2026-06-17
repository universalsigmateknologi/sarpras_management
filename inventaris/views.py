from django.contrib import messages
from django.core.paginator import EmptyPage, Paginator
from django.db.models import Exists, OuterRef, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from inventaris.forms import BarangForm
from inventaris.models import Barang
from perawatan.models import JadwalPerawatan
from transaksi.models import RiwayatBarang


STATUS_FILTERS = {
    'semua': 'Semua',
    'tersedia': 'Tersedia',
    'dipinjam': 'Dipinjam',
    'perbaikan': 'Perbaikan',
}

SORT_FIELDS = {
    'kode': ('kode_aset', 'Kode'),
    'nama': ('nama_barang', 'Nama Barang'),
    'kategori': ('kategori__nama_kategori', 'Kategori'),
    'lokasi': ('lokasi__nama_ruangan', 'Lokasi'),
    'kondisi': ('kondisi', 'Kondisi'),
    'status': ('kode_aset', 'Status'),
}

ACTIVE_MAINTENANCE = ['PENGAJUAN', 'PROSES']


def with_status_annotations(queryset):
    maintenance_qs = JadwalPerawatan.objects.filter(
        barang_id=OuterRef('pk'),
        status_perbaikan__in=ACTIVE_MAINTENANCE,
    )
    borrowed_qs = RiwayatBarang.objects.filter(
        barang_id=OuterRef('pk'),
        jenis_transaksi='KELUAR',
        status='BERLANGSUNG',
    )
    return queryset.annotate(
        is_perbaikan=Exists(maintenance_qs),
        is_dipinjam=Exists(borrowed_qs),
    )


def get_filtered_queryset(request):
    queryset = with_status_annotations(
        Barang.objects.select_related('kategori', 'lokasi').all()
    )

    status_filter = request.GET.get('status', 'semua')
    if status_filter not in STATUS_FILTERS:
        status_filter = 'semua'

    if status_filter == 'tersedia':
        queryset = queryset.filter(is_perbaikan=False, is_dipinjam=False)
    elif status_filter == 'dipinjam':
        queryset = queryset.filter(is_dipinjam=True)
    elif status_filter == 'perbaikan':
        queryset = queryset.filter(is_perbaikan=True)

    query = request.GET.get('q', '').strip()
    if query:
        queryset = queryset.filter(
            Q(kode_aset__icontains=query)
            | Q(nama_barang__icontains=query)
            | Q(kategori__nama_kategori__icontains=query)
            | Q(lokasi__nama_ruangan__icontains=query)
            | Q(kondisi__icontains=query)
            | Q(merek__icontains=query)
            | Q(nomor_seri__icontains=query)
        ).distinct()

    sort_key = request.GET.get('sort', 'kode')
    if sort_key not in SORT_FIELDS:
        sort_key = 'kode'

    direction = request.GET.get('dir', 'asc')
    if direction not in ['asc', 'desc']:
        direction = 'asc'

    order_field = SORT_FIELDS[sort_key][0]
    if direction == 'desc':
        order_field = f'-{order_field}'

    queryset = queryset.order_by(order_field, 'kode_aset')

    return queryset, {
        'status_filter': status_filter,
        'query': query,
        'sort_key': sort_key,
        'direction': direction,
    }


def build_filter_options(request, active_status):
    options = []
    for status, label in STATUS_FILTERS.items():
        params = request.GET.copy()
        params['status'] = status
        params.pop('page', None)
        params.pop('detail', None)
        params.pop('edit', None)
        options.append({
            'status': status,
            'label': label,
            'query': params.urlencode(),
            'active': status == active_status,
        })
    return options


def build_sort_options(sort_key, direction):
    options = []
    for key, (_, label) in SORT_FIELDS.items():
        active = sort_key == key
        next_direction = 'desc' if active and direction == 'asc' else 'asc'
        icon = 'fa-sort'
        if active:
            icon = 'fa-sort-up' if direction == 'asc' else 'fa-sort-down'
        options.append({
            'key': key,
            'label': label,
            'active': active,
            'next_direction': next_direction,
            'icon': icon,
        })
    return options


def get_base_query(request):
    params = request.GET.copy()
    params.pop('page', None)
    params.pop('detail', None)
    params.pop('edit', None)
    return params.urlencode()


def build_context(request):
    queryset, filters = get_filtered_queryset(request)
    paginator = Paginator(queryset, 8)
    page_obj = paginator.get_page(request.GET.get('page'))

    total_queryset = with_status_annotations(Barang.objects.all())
    search_queryset = total_queryset
    query = filters['query']
    if query:
        search_queryset = search_queryset.filter(
            Q(kode_aset__icontains=query)
            | Q(nama_barang__icontains=query)
            | Q(kategori__nama_kategori__icontains=query)
            | Q(lokasi__nama_ruangan__icontains=query)
            | Q(kondisi__icontains=qubase_queryery)
            | Q(merek__icontains=query)
            | Q(nomor_seri__icontains=query)
        ).distinct()

    detail_barang = None
    edit_barang = None
    form = None

    if request.GET.get('detail'):
        detail_barang = get_object_or_404(Barang, pk=request.GET.get('detail'))

    if request.GET.get('edit'):
        edit_barang = get_object_or_404(Barang, pk=request.GET.get('edit'))
        form = BarangForm(instance=edit_barang)

    return {
        'active_page': 'inventaris',
        'items': page_obj,
        'page_obj': page_obj,
        'total_count': search_queryset.count(),
        'available_count': search_queryset.filter(is_perbaikan=False, is_dipinjam=False).count(),
        'borrowed_count': search_queryset.filter(is_dipinjam=True).count(),
        'maintenance_count': search_queryset.filter(is_perbaikan=True).count(),
        'visible_count': page_obj.paginator.count,
        'query': filters['query'],
        'status_filter': filters['status_filter'],
        'sort_key': filters['sort_key'],
        'direction': filters['direction'],
        'base_query': get_base_query(request),
        'status_options': build_filter_options(request, filters['status_filter']),
        'sort_options': build_sort_options(filters['sort_key'], filters['direction']),
        'detail_barang': detail_barang,
        'edit_barang': edit_barang,
        'form': form,
        'open_modal': bool(detail_barang or edit_barang),
    }


def handle_post(request):
    action = request.POST.get('action')

    if action == 'edit':
        barang = get_object_or_404(Barang, pk=request.POST.get('barang_id'))
        form = BarangForm(request.POST, request.FILES, instance=barang)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data aset berhasil diperbarui.')
        else:
            messages.error(request, 'Periksa kembali data yang dimasukkan.')
            context = build_context(request)
            context.update({
                'edit_barang': barang,
                'form': form,
                'open_modal': True,
            })
            return render(request, 'inventaris/index.html', context, status=400)
        return redirect(reverse('inventaris:index'))

    barang_ids = request.POST.getlist('barang_ids')
    if not barang_ids:
        messages.warning(request, 'Pilih minimal satu aset untuk aksi massal.')
        return redirect(reverse('inventaris:index'))

    queryset = Barang.objects.filter(pk__in=barang_ids)
    count = queryset.count()

    if action == 'pinjamkan':
        now = timezone.now()
        for barang in queryset:
            barang.tersedia = False
            barang.save(update_fields=['tersedia'])
            RiwayatBarang.objects.create(
                barang=barang,
                jenis_transaksi='KELUAR',
                nama_peminjam='Admin Pusat',
                tujuan='Aksi massal inventaris',
                tanggal_keluar=now,
                status='BERLANGSUNG',
                keterangan='Ditandai dipinjamkan dari halaman inventaris.',
            )
        messages.success(request, f'{count} aset berhasil ditandai dipinjamkan.')

    elif action == 'tersedia':
        for barang in queryset:
            barang.tersedia = True
            barang.save(update_fields=['tersedia'])
        messages.success(request, f'{count} aset berhasil ditandai tersedia.')

    elif action == 'label':
        label = f'Label inventaris diperbarui pada {timezone.localtime().strftime("%d/%m/%Y %H:%M")}'
        for barang in queryset:
            catatan = barang.catatan or ''
            barang.catatan = f'{catatan}\n{label}' if catatan else label
            barang.save(update_fields=['catatan'])
        messages.success(request, f'Label diterapkan ke {count} aset.')

    else:
        messages.warning(request, 'Aksi massal tidak dikenali.')

    return redirect(reverse('inventaris:index'))

@login_required
def inventaris_index(request):
    if request.method == 'POST':
        return handle_post(request)
    return render(request, 'inventaris/index.html', build_context(request))
