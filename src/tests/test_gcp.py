import os

import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from google.auth.exceptions import DefaultCredentialsError
from google.cloud import storage
from google.oauth2 import service_account

from sponsors.models import Sponsor

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

@pytest.mark.django_db
@override_settings(
    DEFAULT_FILE_STORAGE='storages.backends.gcloud.GoogleCloudStorage',
    GS_BUCKET_NAME="pycontw-static",
    GS_CREDENTIALS=service_account.Credentials.from_service_account_file(
        os.path.join(PROJECT_ROOT, "google-cloud-storage.json")
    )
)
def test_gcs_credentials_loaded():
    """驗證 GCS 憑證是否正確載入"""
    try:
        credentials_path = os.path.join(PROJECT_ROOT, "google-cloud-storage.json")
        if not os.path.exists(credentials_path):
            pytest.fail(f"憑證檔案不存在於 {credentials_path}")

        client = storage.Client(credentials=settings.GS_CREDENTIALS)

        bucket = client.get_bucket(settings.GS_BUCKET_NAME)
        assert bucket.exists(), "bucket 不存在或無存取權限"

        test_blob = bucket.blob("integration-test-file.txt")
        test_blob.upload_from_string("test-content")
        test_blob.delete()

    except DefaultCredentialsError as e:
        pytest.fail(f"憑證載入失敗: {str(e)}")
    except Exception as e:
        pytest.fail(f"操作異常: {str(e)}")

@pytest.mark.django_db
@override_settings(
    DEFAULT_FILE_STORAGE='storages.backends.gcloud.GoogleCloudStorage',
    GS_BUCKET_NAME="pycontw-static",
    GS_CREDENTIALS=service_account.Credentials.from_service_account_file(
        os.path.join(PROJECT_ROOT, "google-cloud-storage.json")
    )
)
def test_real_gcs_upload_and_download(client):
    """完整檔案上傳/下載測試"""
    try:
        sponsor = Sponsor.objects.create(
            name="GCS Integration Test",
            level=Sponsor.Level.GOLD,
            intro="Test Sponsor"
        )

        test_content = b"<svg><text>TEST</text></svg>"
        svg_file = SimpleUploadedFile(
            "test.svg",
            test_content,
            content_type="image/svg+xml"
        )
        sponsor.logo_svg.save("gcs-test.svg", svg_file)

        assert "storage.googleapis.com" in sponsor.logo_svg.url
        assert "gcs-test.svg" in sponsor.logo_svg.url

        response = client.get(sponsor.logo_svg.url)
        assert response.status_code == 200
        assert test_content in response.content

    finally:
        if sponsor.logo_svg:
            sponsor.logo_svg.delete()
        sponsor.delete()
