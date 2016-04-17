from django.db import models

from rest_framework.serializers import ModelSerializer as OrigModelSerializer

from .fields import ThumbnailImageField


class ModelSerializer(OrigModelSerializer):
    def build_url_field(self, field_name, model_class):
        """
        Create a field representing the object's own URL.
        """
        field_class = self.serializer_url_field
        field_kwargs = {
            'view_name': '{model_name}s-detail'.format(model_name=model_class._meta.object_name.lower())
        }
        return field_class, field_kwargs


ModelSerializer.serializer_field_mapping[models.ImageField] = ThumbnailImageField
