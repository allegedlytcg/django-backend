from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^$', DeckAPIView.as_view()),#cardapp/
    # url('cardTransactions/', CardTransactAPIView.as_view())



    
]