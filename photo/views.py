from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from .forms import PhotoForm, Album, AlbumForm
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Photo

# Create your views here.

# Kullanıcıya ait default albumdeki fotoğrafları döndürür
@login_required
def photo_index_default_album(request):
    album = Album.get_default_album(request.user)

    # Bu şekilde çağırınca, paginator.get_page(page) yanlış çalışıyor.
    # photo_list = Photo.objects.filter(album=album.id).order_by('id')
    photo_list = album.photo_set.all()

    paginator = Paginator(photo_list, 2)  # Show 2 post per page

    page = request.GET.get('sayfa')

    photos = paginator.get_page(page)

    context = {
        'title': album.name,
        'photo': photos,
    }

    return render(request, 'photo/index.html', context)


# Sadece default albüme fotoğraf ekler
@login_required
def photo_upload(request):

    form = PhotoForm(request.POST or None, request.FILES or None)
    album = Album.get_default_album(request.user)

    if form.is_valid():
        files = request.FILES.getlist('image')
        photo = Photo()
        for file in files:
            photo = Photo()
            photo.image = file
            photo.save()
            photo.album.add(album)

        messages.success(request, 'Image uploaded successfuly')
        # İlgili postun detay sayfasına yönlendirme yapıyoruz
        return HttpResponseRedirect(photo.get_default_index_url())
    context = {
        'form': form,
        'title': 'Upload Images',
    }

    return render(request, 'photo/form.html', context)


# Alb_id li albüme ait fotoğrafları döndürür
@login_required
def photo_index(request, alb_id):
    album = Album.objects.get(id=alb_id)

    photo_list = Photo.objects.filter(album=album)

    paginator = Paginator(photo_list, 2)  # Show 2 post per page

    page = request.GET.get('sayfa')
    photos = paginator.get_page(page)

    context = {
        'title': 'My Images',
        'photo': photos,
    }

    return render(request, 'photo/index.html', context)


@login_required
def photo_delete(request, id):

    photo = get_object_or_404(Photo, id=id)

    form = PhotoForm(instance=photo)
    if request.method == 'POST':
        photo.delete()
        return redirect('photo:index', alb_id=Album.get_default_album(request.user).id)
    context = {
        'form': form,
    }
    return render(request, 'photo/form.html', context)


@login_required
def album_index(request):
    album_list = Album.objects.all()

    context = {
        'title': 'My Albums',
        'albums': album_list,
    }

    return render(request, 'photo/albums.html', context)


@login_required
def album_delete(request, id):
    album = get_object_or_404(Album, id=id)

    form = AlbumForm(instance=album)
    if request.method == 'POST':
        album.delete()
        return redirect('album:index')
    context = {
        'form': form,
    }
    return render(request, 'photo/form.html', context)
