from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('students.urls')),
    path('teachers/', include('teachers.urls')),
    # path('blog/', include('blog.urls'))
]
