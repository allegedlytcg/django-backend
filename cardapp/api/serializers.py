from rest_framework import serializers

from cardapp.models import BloodPressure
# Turns models to json data using django REST framework(alternatively use pure django api, alt use pure python)
# Serializers -> Json IMPORTANT CONCEPT
# Serializers -> validate data IMPORTANT CONCEPT
# 
# 





class BloodPressureSerializer(serializers.ModelSerializer):#checks these fields and/or returns these fields as json
	class Meta:
		model = BloodPressure
		fields =[
			'bpId',
			'dPressure',
			'sPressure',
			'heartRate',
			'user',
			'timestamp'

		]
		read_only_fields = ['user']




	def validate(self, data): #takes int he raw data we need using serializer for entire data
		print('BloodPressureSerializer validates here')
		print(str(type(data)))


		content = data.get("dPressure", None)
		if content == "":
			content = None
		if content is None:
			raise serializers.ValidationError("dPressure is required.")
		return data