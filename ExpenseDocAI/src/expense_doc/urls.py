from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from expense_doc.api.views import ExpenseDocumentViewSet, ExpenseEntryViewSet
from expense_doc.api.health import health_check

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'documents', ExpenseDocumentViewSet, basename='document')
router.register(r'entries', ExpenseEntryViewSet, basename='entry')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API URLs
    path('api/v1/', include([
        path('', include(router.urls)),
        path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ])),
    
    # Health check endpoint
    path('health/', health_check, name='health_check'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 