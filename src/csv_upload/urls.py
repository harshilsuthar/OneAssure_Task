from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()


router.register(r"csv_upload", views.CsvUploadView, basename="csv_upload")

urlpatterns = router.urls
