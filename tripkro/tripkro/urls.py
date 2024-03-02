from django.contrib import admin
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/account/", include("account.urls")),
]

if settings.DEBUG:

    import debug_toolbar

    urlpatterns += [
        # django debug tollbar view
        path("__debug__/", include(debug_toolbar.urls)),
    ]
