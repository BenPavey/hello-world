# storage_backends/gcloud.py

from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import setting
from urllib.parse import urljoin

class GoogleCloudStaticFileStorage(GoogleCloudStorage):
    """
    Google file storage class for handling static files (e.g., CSS, JS).
    """
    bucket_name = setting('GS_STATIC_BUCKET_NAME')

    def url(self, name):
        """
        Returns the correct static URL instead of Google's default URL.
        """
        return urljoin(settings.STATIC_URL, name)