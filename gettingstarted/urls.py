from django.urls import url, path, include

from django.contrib import admin


from rest_framework_jwt.views import obtain_jwt_token

admin.autodiscover()

import hello.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("db/", hello.views.db, name="db"),
    path("admin/", admin.site.urls),
    url(r'^api-token-auth/', obtain_jwt_token),
	url('cardapp/', include('cardapp.api.urls')),  
]

