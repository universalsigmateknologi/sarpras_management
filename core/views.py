from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def login_view(request):
    """Halaman login yang menerima username dan password.

    Catatan: Template login yang Anda pakai sudah menggunakan field `username`.
    """

    if request.user.is_authenticated:
        # Kalau user sudah login, tidak perlu login lagi
        return redirect('inventaris:index') if _has_inventaris_index() else redirect('/')

    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip()
        password = request.POST.get('password') or ''

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inventaris:index') if _has_inventaris_index() else redirect('/')

        messages.error(request, 'Username atau kata sandi salah.')
        # render ulang halaman login
        return render(request, 'core/auth/login.html')

    return render(request, 'core/auth/login.html')


@csrf_protect
def logout_view(request):
    """Melakukan logout user dan redirect ke halaman awal."""
    logout(request)
    messages.success(request, 'Anda telah berhasil logout.')
    return redirect('login')


def _has_inventaris_index() -> bool:
    """Menghindari hard-fail kalau nama route belum ada."""
    try:
        from django.urls import resolve

        resolve('/inventaris/')
        return True
    except Exception:
        return False

