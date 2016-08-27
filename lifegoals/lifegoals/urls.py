from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from api import views

urlpatterns = [
    url(r'^$', views.SuccessfulResponse.as_view(), name='success'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include('api.urls'))
]

urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
