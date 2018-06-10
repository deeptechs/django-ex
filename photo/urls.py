from django.urls import path
from photo.views import photo_upload, photo_index, photo_delete
from photo.viewsAWS import photo_index_default_album2, PhotoPolicyAPI, FileUploadCompleteHandler
from django.views.generic.base import TemplateView

app_name = 'photo'

urlpatterns = (
    path('', photo_index_default_album2, name="photo_index_default"),
    path('upload2/', photo_upload, name="upload"),
    # index ile beraber album id gelmeli
    path('index/<int:alb_id>', photo_index, name="index"),
    path('delete/<int:id>', photo_delete, name="delete"),

    path('upload/', TemplateView.as_view(template_name='photo/upload.html'), name='upload-home'),
    path('api/files/policy/', PhotoPolicyAPI.as_view(), name='upload-policy'),
    path('api/files/complete/', FileUploadCompleteHandler.as_view(), name='upload-complete'),

)
