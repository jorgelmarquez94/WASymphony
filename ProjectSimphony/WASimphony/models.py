from django.db import models
from django.forms import ModelForm
from .validators import validate_file_extension


# def user_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     return 'user_{0}/{1}'.format(instance.user.id, filename)
#
# class SymphonyFileUpload(models.Model):
#     document = models.FileField(upload_to=user_directory_path, validators=[validate_file_extension])

class FileDb(models.Model):
    source = models.FileField(upload_to="source")