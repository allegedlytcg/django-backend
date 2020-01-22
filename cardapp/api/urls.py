from django.conf.urls import url
from .views import *


urlpatterns = [
    url('deck/', DeckAPIView.as_view()),#cardapp/
    url('cardTransactions/', CardTransactAPIView.as_view())



    
]