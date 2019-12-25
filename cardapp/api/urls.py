from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^$', BloodPressureAPIView.as_view()),#cardapp/



    
]