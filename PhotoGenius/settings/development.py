from PhotoGenius.settings.base import *
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'photogenius',
        'USER': 'postgres',
        'PASSWORD': 'Abcdefgh.1',
        'HOST': 'db',
        'PORT': '5432',
    }
}
# Staticfiles_dirs yazdığımız app ler için statik dosyaların tamamanın bir nerede tutulduğunu gösterir, her uygulama için ayrı tutulmaz.
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# managepy collectstatics dediğimizde statik dosyaların toplanacağı adresi gösteriyor
STATIC_ROOT = os.path.join(BASE_DIR, 'static_cdn')
