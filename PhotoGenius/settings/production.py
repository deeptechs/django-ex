from PhotoGenius.settings.base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

from . import database

DATABASES = {
    'default': database.config()
}

# Staticfiles_dirs yazdığımız app ler için statik dosyaların tamamanın bir nerede tutulduğunu gösterir, her uygulama için ayrı tutulmaz.
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# managepy collectstatics dediğimizde statik dosyaların toplanacağı adresi gösteriyor
# productionda nginx gibi statik dosya sunucusu olarak görev yapacak araca bu adres elle verilecek, dikkat !
STATIC_ROOT = os.path.join(BASE_DIR, 'static_cdn')
