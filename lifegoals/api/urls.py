from django.conf.urls import url, include
from api import views

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^accounts/$', views.WalletDetail.as_view(), name='wallet'),
    url(r'^transfers/$', views.FundTransfer.as_view(), name='fund_transfer')
]
urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
