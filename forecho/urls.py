from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from . import view
import re

urlpatterns = [
    path('',view.index),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('account/', include('account.urls')),
    path('article/', include('article.urls')),
    path('image/', include('image.urls')),
    path('search/',include('haystack.urls')),
    path('home/', TemplateView.as_view(template_name="home.html"), name='home'),  # 新增
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
