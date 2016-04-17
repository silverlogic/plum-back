from drf_extra_fields.fields import Base64ImageField


class ThumbnailImageField(Base64ImageField):
    def to_representation(self, value):
        if not value:
            return None

        if not getattr(value, 'url', None):
            # If the file has not been saved it may not have a URL.
            return None
        url = value.url
        request = self.context.get('request', None)
        if request is not None:
            url = request.build_absolute_uri(url)

        return {
            'full_size': url
        }
