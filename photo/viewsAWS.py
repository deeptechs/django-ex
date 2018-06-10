from django.contrib.auth.decorators import login_required
from .forms import Album
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Photo
import base64
import hashlib
import hmac
import os
import time
from rest_framework import permissions, status, authentication
from rest_framework.response import Response
from rest_framework.views import APIView
from PhotoGenius.config_aws import (
    AWS_UPLOAD_BUCKET,
    AWS_UPLOAD_REGION,
)
from PhotoGenius import config_aws
from Libs import pgS3Lib

aws = pgS3Lib.PgS3()


# Kullanıcıya ait default albumdeki fotoğrafları döndürür
@login_required
def photo_index_default_album2(request):
    album = Album.get_default_album(request.user)

    page = request.GET.get('sayfa')

    photo_list = album.photo_set.all()
    url_list = aws.get_user_photo_urls_by_bucket_name(AWS_UPLOAD_BUCKET, request.user.email)

    paginator = Paginator(photo_list, 2)  # Show 2 post per page
    paginator2 = Paginator(url_list, 2)  # Show 2 post per page

    photos = paginator.get_page(page)
    urls = paginator2.get_page(page)

    photos_urls = zip(photos, urls)

    # TODO: photos u gönderme. Template tarafta zip i bölemedim, bölünse photos a gerek yok.
    context = {
        'title': album.name,
        'photos_urls': photos_urls,
        'photos': photos,
    }

    return render(request, 'photo/index.html', context)


# Frontend tarafı upload u bitirdğinde, her upload da gerekli güncellemeleri yapmak için bu api yi çağırır.
# Yapacağı da, başarılı upload sonrası veri tabanında ilgili alanlara photo değerleri yazmaktır.
# Çağrıya da cevap olarak ilgili photo id yi ve true değerini döner. Yapamadı ise boş obje döner.
class FileUploadCompleteHandler(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]

    def post(self, request, *args, **kwargs):
        file_id = request.POST.get('file')
        size = request.POST.get('fileSize')
        data = {}
        type_ = request.POST.get('fileType')
        uploaded = True
        if file_id:
            obj = Photo.objects.get(id=int(file_id))
            obj.size = int(size)
            obj.uploaded = uploaded
            obj.file_type = type_
            obj.save()
            data['id'] = obj.id
            data['saved'] = True
        return Response(data, status=status.HTTP_200_OK)


# Bu api sayesinde frontend çağrısına cevap verilir. Cevapta Aws S3 upload yapılabilmesi için gerekli bilgiler frontende
# gönderilir. javascript ile de frontend bu bilgiler ile XMLHttpRequest yapar ve dosyayı s3 e atar. Eğer javascript
# tarafında hata olursa bu api backend de ilgili obje için kayıt oluşturmuş olur, dikkat ! ama uploaded alanı boş kalır.
class PhotoPolicyAPI(APIView):
    """
    This view is to get the AWS Upload Policy for our s3 bucket.
    What we do here is first create a Photo object instance in our
    Django backend. This is to include the Photo instance in the path
    we will use within our bucket as you'll see below.
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]

    def post(self, request, *args, **kwargs):
        """
        The initial post request includes the filename
        and auth credientails. In our case, we'll use
        Session Authentication but any auth should work.
        """
        filename_req = request.data.get('filename')
        if not filename_req:
            return Response({"message": "A filename is required"}, status=status.HTTP_400_BAD_REQUEST)
        policy_expires = int(time.time() + 5000)
        username_str = str(request.user.email)
        """
        Below we create the Django object. We'll use this
        in our upload path to AWS. 

        Example:
        To-be-uploaded file's name: Some Random File.mp4
        Eventual Path on S3: <bucket>/username/2312/2312.mp4
        """
        photo_obj = Photo.objects.create(name=filename_req)
        photo_obj.album.add(Album.get_default_album(request.user))
        photo_obj_id = photo_obj.id
        upload_start_path = "{username}/{photo_obj_id}/".format(
            username=username_str,
            photo_obj_id=photo_obj_id
        )
        _, file_extension = os.path.splitext(filename_req)
        filename_final = "{photo_obj_id}{file_extension}".format(
            photo_obj_id=photo_obj_id,
            file_extension=file_extension

        )
        """
        Eventual file_upload_path includes the renamed file to the 
        Django-stored Photo instance ID. Renaming the file is 
        done to prevent issues with user generated formatted names.
        """
        # final_upload_path --> /username/2312/2312.mp4
        final_upload_path = "{upload_start_path}{filename_final}".format(
            upload_start_path=upload_start_path,
            filename_final=filename_final,
        )
        if filename_req and file_extension:
            """
            Save the eventual path to the Django-stored Photo instance
            """
            photo_obj.path = final_upload_path
            photo_obj.save()

        policy_document_context = {
            "expire": policy_expires,
            "bucket_name": AWS_UPLOAD_BUCKET,
            "key_name": "",
            "acl_name": "private",
            "content_name": "",
            "content_length": 524288000,
            "upload_start_path": upload_start_path,

        }
        policy_document = """
        {"expiration": "2019-01-01T00:00:00Z",
          "conditions": [ 
            {"bucket": "%(bucket_name)s"}, 
            ["starts-with", "$key", "%(upload_start_path)s"],
            {"acl": "%(acl_name)s"},

            ["starts-with", "$Content-Type", "%(content_name)s"],
            ["starts-with", "$filename", ""],
            ["content-length-range", 0, %(content_length)d]
          ]
        }
        """ % policy_document_context
        aws_secret = str.encode(config_aws.AWS_UPLOAD_SECRET_KEY)
        policy_document_str_encoded = str.encode(policy_document.replace(" ", ""))
        url = 'https://{bucket}.s3-{region}.amazonaws.com/'.format(
            bucket=AWS_UPLOAD_BUCKET,
            region=AWS_UPLOAD_REGION
        )
        policy = base64.b64encode(policy_document_str_encoded)
        signature = base64.b64encode(hmac.new(aws_secret, policy, hashlib.sha1).digest())
        data = {
            "policy": policy,
            "signature": signature,
            "key": config_aws.AWS_UPLOAD_ACCESS_KEY_ID,
            "file_bucket_path": upload_start_path,
            "file_id": photo_obj_id,
            "filename": filename_final,
            "fileType": file_extension,
            "url": url,
            "username": username_str,
        }
        return Response(data, status=status.HTTP_200_OK)
