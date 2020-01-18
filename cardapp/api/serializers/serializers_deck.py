from rest_framework import serializers

from cardapp.models import Deck
# Turns models to json data using django REST framework(alternatively use pure django api, alt use pure python)
# Serializers -> Json IMPORTANT CONCEPT
# Serializers -> validate data IMPORTANT CONCEPT
# 
# 

class DeckSerializer(serializers.ModelSerializer):#checks these fields and/or returns these fields as json
	class Meta:
		model = Deck
		fields =[
			'user',
		
		]
		read_only_fields = ['user']




	def validate(self, data): #takes int he raw data we need using serializer for entire data
		print('Deck Serializer validates here')
		return data



