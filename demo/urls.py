from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from azbankgateways.urls import az_bank_gateways_urls
from core.views import go_to_gateway_view ,callback_gateway_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('allauth.urls')),
    path('account/', include('account.urls')),

    path('', include('core.urls', namespace='core')),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/rest-auth/', include('dj_rest_auth.urls')),
    path('api/rest-auth/', include('rest_auth.urls')),
    path('api/rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api-token-auth/', obtain_auth_token),
    path('comment/', include('comment.urls')),
    path('api/', include('comment.api.urls')),
    path('ratings/', include('star_ratings.urls',
                             namespace='ratings')),
    path('bankgateways/', az_bank_gateways_urls()),
    path('go_to_gateway/',go_to_gateway_view.as_view(),name='go_to_gateway'),
    path('callback-gateway/',callback_gateway_view.as_view(),name='callback-gateway'),




]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
