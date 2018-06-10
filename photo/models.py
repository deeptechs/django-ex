from django.db import models
from django.urls import reverse


# Create your models here.
class Album(models.Model):
    name = models.CharField(max_length=150)
    user = models.ForeignKey('accounts.MyUser', verbose_name='Album Owner', on_delete=models.CASCADE)

    @staticmethod
    def set_default_album(usr):
        if not Album.objects.filter(user=usr, name='All'):
            album = Album(name='All' + '_' + usr.email, user=usr)
            album.save()

    @staticmethod
    def get_default_album(usr):
        return Album.objects.get(name='All' + '_' + usr.email, user=usr)

    def __str__(self):
        return str(self.name)


class Face(models.Model):
    x1 = models.IntegerField()
    y1 = models.IntegerField()
    x2 = models.IntegerField()
    y2 = models.IntegerField()
    identity_name = models.CharField(max_length=150)
    feature = models.CharField(max_length=1024)

    def __str__(self):
        return str(self.id)


# Fotoğraflar S3 te tutulacak, ilgili field lar upload ardından doldurulacak
class Photo(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)
    path = models.TextField(blank=True, null=True)
    size = models.BigIntegerField(default=0)
    file_type = models.CharField(max_length=120, null=True, blank=True)
    upload_date = models.DateTimeField(verbose_name='Save Date', auto_now_add=True)
    uploaded = models.BooleanField(default=False)

    # Kullanıcıya ait her fotoğraf kullanıcıya ait n farklı albümde olabilir,
    # Kullanıcıya ait her albümde, kullanıcıya ait n farklı fotoğraf olabilir,
    album = models.ManyToManyField(Album)

    faces = models.ForeignKey('Face', on_delete=models.CASCADE, null=True)


    # Admin Panelde isim alanında görünecek alan
    def __str__(self):
        return str(self.name)

    def get_default_index_url(self):
        return reverse('photo:photo_index_default')

    def get_delete_url(self):
        # photo uygulamasındaki delete url i ni id parametresini vererek çağırdığımızı belirtiyoruz.
        return reverse('photo:delete', kwargs={'id': self.id})

    @property
    def title(self):
        return str(self.name)
