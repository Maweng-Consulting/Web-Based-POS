from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("pos/", include("apps.pos.urls")),
    path("inventory/", include("apps.inventory.urls")),
    path("users/", include("apps.users.urls")),
    path("suppliers/", include("apps.suppliers.urls")),
    path("payments/", include("apps.payments.urls")),
    path("reports/", include("apps.reports.urls")),
    path("apis/", include("apis.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
