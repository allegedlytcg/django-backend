from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import requests
import json
import django_filters
from datetime import datetime, timedelta


from django.http import HttpResponse
from customApp_bloodPressure.models import BloodPressure
from .serializers import BloodPressureSerializer


def is_json(json_data):
	try:
		real_json = json.loads(json_data)
		is_valid  = True
	except ValueError:
		is_valid = False
	return is_valid


class BloodPressureAPIView(mixins.CreateModelMixin,
 generics.ListAPIView):

# mixins.RetrieveModelMixin, 
 #mixins.DestroyModelMixin, 
 #mixins.UpdateModelMixin, 


	permission_classes= [permissions.IsAuthenticated]
	authentication_classes= [JSONWebTokenAuthentication]

	serializer_class 		= BloodPressureSerializer



	#provides particular records of patient blood pressure data dependent on the user with an optional passed date range
	def get_queryset(self):
		print("Current date: " + str(datetime.now().date()))
		request = self.request
		print("Data for user:" + str(request.user))
		json_data 			= {}
		body_				= request.body
		#get the json data of passed key's or they don't exist
		if is_json(body_):
			json_data 			= json.loads(request.body)
		passed_id 		  = json_data.get('bpId', None) 
		passed_start_date = json_data.get('start_date', None)
		passed_end_date   = json_data.get('end_date', None)
		print("Id passed is: " + str(passed_id))
		print("Start date passed  " + str(passed_start_date))
		print("End date passed  " + str(passed_end_date))
		if passed_id is not None:												 #return object of id
			qs = BloodPressure.objects.all().filter(user=request.user).filter(id = passed_id)
		elif passed_end_date is not None and passed_start_date is not None:#return objects of the date range
			qs = BloodPressure.objects.all().filter(user=request.user).filter(
		    timestamp__gte = passed_start_date,
		    timestamp__lt = passed_end_date,
			).distinct()
		else:															
			qs = BloodPressure.objects.all().filter(user=request.user)	 #return all

		return qs




	#First checks if data is valid before creating parent record, then creates both parent and child records
	def post(self, request, *args, **kwargs):
		request = self.request
		body_ = request.body
		if is_json(body_):
			json_data 			= json.loads(request.body)
		print("Type of value for variable 'json_data' is: " + str(type(json_data)))

		return self.create(request, *args, **kwargs)



			


	#NOTHING BELOW HAS BEEN TESTED
	#NOTHING BELOW HAS BEEN TESTED
	#NOTHING BELOW HAS BEEN TESTED
	#NOTHING BELOW HAS BEEN TESTED
	#NOTHING BELOW HAS BEEN TESTED
	#NOTHING BELOW HAS BEEN TESTED
	#NOTHING BELOW HAS BEEN TESTED
	#NOTHING BELOW HAS BEEN TESTED
	#NOTHING BELOW HAS BEEN TESTED
	#NOTHING BELOW HAS BEEN TESTED
	#NOTHING BELOW HAS BEEN TESTED
	#NOTHING BELOW HAS BEEN TESTED
	#NOTHING BELOW HAS BEEN TESTED
	#NOTHING BELOW HAS BEEN TESTED



	def perform_destroy(self, instance):
		print(str(instance))
		if instance is not None:
			return instance.delete()
		return None



	def put(self, request, *args, **kwargs):
		url_passed_id		= request.GET.get('id', None)
		json_data 			= {}
		body_				= request.body
		if is_json(body_):
			json_data 			= json.loads(request.body)
		new_passed_id 		= json_data.get('id', None)
		self.passed_id = url_passed_id or new_passed_id or None
		return self.update(request, *args, **kwargs)


	def patch(self, request, *args, **kwargs):
		url_passed_id		= request.GET.get('id', None)
		json_data 			= {}
		body_				= request.body
		if is_json(body_):
			json_data 			= json.loads(request.body)
		new_passed_id 		= json_data.get('id', None)
		self.passed_id = url_passed_id or new_passed_id or None
		return self.update(request, *args, **kwargs)


	def delete(self, request, *args, **kwargs):
		url_passed_id		= request.GET.get('id', None)
		json_data 			= {}
		body_				= request.body
		if is_json(body_):
			json_data 			= json.loads(request.body)
		new_passed_id 		= json_data.get('id', None)
		self.passed_id = url_passed_id or new_passed_id or None
		return self.destroy(request, *args, **kwargs)


	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
