from django.shortcuts import render, redirect , get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.contrib import messages
from app.models import *
import base64

# Create your views here.

def login(request):
    return render(request, 'admin/login.html')

def addUser(request):
    if request.method == 'POST':
      nik = request.POST['nik']
      name = request.POST['name']
      divisi = request.POST['divisi']
      photo_data = request.POST.get('photo', '')

      if photo_data:
        try:
          # Decode base64 image from the photo data
          format, imgstr = photo_data.split(';base64,')
          ext = format.split('/')[-1]
          data = ContentFile(base64.b64decode(imgstr), name=f'{nik}.{ext}')

          # Create new data entry
          user = Users(
              nik=nik,
              name=name,
              divisi=divisi,
              photo=data,
          )
          user.save()

          messages.success(request, 'Data karyawan berhasil diupload.')
          return redirect('/admins/addUser')
        except Exception as e:
            messages.error(request, f'Gagal mengupload data karyawan: {e}')
      else:
        messages.error(request, 'Foto tidak tersedia atau tidak valid.')

      return redirect('/admins/addUser')
    return render(request, 'admin/addUser.html')
