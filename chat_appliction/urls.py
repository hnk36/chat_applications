from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path('', include('chat.urls')),  # Include your app's URLs
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]