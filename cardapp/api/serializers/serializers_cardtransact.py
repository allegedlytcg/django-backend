from rest_framework import serializers

from cardapp.models import CardTransact
# Turns models to json data using django REST framework(alternatively use pure django api, alt use pure python)
# Serializers -> Json IMPORTANT CONCEPT
# Serializers -> validate data IMPORTANT CONCEPT
# 
# added comment




class CardTransactSerializer(serializers.ModelSerializer):
	class Meta:
		model = CardTransact
		fields =[
		'cardTransactId',
			'deckId',
			'cardId',
		]




	def validate(self, data): 
		# deckId			= data.get("deckId", None)
		cardId 			= data.get("cardId", None)
		print('Card Transact validates here')
		# if deckId == "":#
		# 	deckId = None
		if cardId == "":#must be an integer  #toadd or isinstance(ekgId, int) != True
			cardId = None
		if cardId is None:
			raise serializers.ValidationError("One or more required fields weren't provided")
		return data