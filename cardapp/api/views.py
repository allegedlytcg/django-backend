from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import requests
import json
import django_filters
from datetime import datetime, timedelta
import time
from http.client import responses

from django.http import HttpResponse, HttpResponseBadRequest
from customApp_ekg.models import Ekg, EkgVoltageReadings
from .serializers.serializers_deck import DeckSerializer
from .serializers.serializers_cardtransact import CardTransactSerializer


#########################EkgAPIView############################################################
# Class    : EkgAPIView
# Purpose  : Implements CRUD using a single endpoints 
# Workflow : Maps the incoming response (get, post, put, patch, delete) to a method
#            defined below. 
#
#            If a detail view is request and no parameters are given, the 
#            get_queryset() method will then be called. 
#
#####################################################################################
def is_json(json_data):
	try:
		real_json = json.loads(json_data)
		is_valid  = True
	except ValueError:
		is_valid = False
	return is_valid

def validate_child_records(passed_voltages, ekgtags, ptags, json_data):#batch validation for voltages for an 'all or none' effect
	try:
		dumbyEkgId 		 = {'ekgId': 1}#safe because no values are actually saved here
		json_data.update(dumbyEkgId)

		print('\n\n\n')
		for indice in range(0, len(passed_voltages)):
			voltage_value = passed_voltages[indice]
			ekgtag_value  = ekgtags[indice]
			ptag_value	  = ptags[indice]
			#kept for debugging purposes
			# print("Voltage value at indice:" + str(indice) + ": is of value: " + str(voltage_value))
			# print("ekgtag_value value at indice:" + str(indice) + ": is of value: "  + str(ekgtag_value))
			# print("ptag_value value at indice:" + str(indice) +": is of value: " + str(ptag_value))
			volt_pair   = {'voltage_reading': voltage_value}
			ekgtag_pair	= {'ekgtag': ekgtag_value}
			ptag_pair   = {'ptag': ptag_value}

			json_data.update(volt_pair)
			json_data.update(ekgtag_pair)
			json_data.update(ptag_pair)


			ekgVoltageSerializer = EkgVoltageSerializer(data=json_data)	
			if ekgVoltageSerializer.is_valid():

				json_data.pop('voltage_reading', None)#remove to make room for the next voltage reading
				json_data.pop('ekgtag', None)#remove to make room for the next ekgtag
				json_data.pop('ptag', None)#remove to make room for the next ptag
				
			else:
				return False
		json_data.pop('ekgId', None)
		return True
	except:
		return False
	


class EkgAPIView(mixins.CreateModelMixin,
 generics.ListAPIView):


	permission_classes= [permissions.IsAuthenticated]
	authentication_classes= [JSONWebTokenAuthentication]
	serializer_class 		= EkgSerializer




	# provides particular records of patient ekg data dependent on the user with an optional passed date range
	def get_queryset(self):
		print("Current date: " + str(datetime.now().date()))
		request = self.request
		print("Data for user:" + str(request.user))
		json_data 			= {}
		body_				= request.body
		#get the json data of passed key's or they don't exist
		if is_json(body_):
			json_data 			= json.loads(request.body)
		passed_id 		  = json_data.get('ekgId', None) 
		passed_start_date = json_data.get('start_date', None)
		passed_end_date   = json_data.get('end_date', None)
		print("Id passed is: " + str(passed_id))
		print("Start date passed  " + str(passed_start_date))
		print("End date passed  " + str(passed_end_date))
		if passed_id is not None:												 #return object of id
			qs = Ekg.objects.all().filter(user=request.user).filter(id = passed_id)
		elif passed_end_date is not None and passed_start_date is not None:#return objects of the date range
			qs = Ekg.objects.all().filter(user=request.user).filter(
		    timestamp__gte = passed_start_date,
		    timestamp__lt = passed_end_date,
			).distinct()
		else:															
			qs = Ekg.objects.all().filter(user=request.user)	 #return all ekg records
		return qs






	#First checks if data is valid before creating parent record, then creates both parent and child records
	def post(self, request, *args, **kwargs):
		request = self.request
		print("Post method initiates here")
		body_	= request.body
		if is_json(body_):
			# print("the original json data is: " + str(request.body) + " of type: " +str(type(request.body)))
			# print('\n\n\n')
			json_data 		= json.loads(request.body)
			passed_voltages  = json_data.get('voltages', None)
			passed_ekgtags   = json_data.get('ekgtags', None)
			passed_ptags     = json_data.get('ptags', None)
			# print("Voltages passed are: "+ str(passed_voltages))
			# print('\n\n\n')
			# print("Ekgtags passed are: "+ str(passed_ekgtags))
			# print('\n\n\n')
			# print("Ptags passed are: "+ str(passed_ptags))
			# print('\n\n\n')
			# print("User passed is: " + str(request.user))
			# print('\n\n\n')
			equalquantitiesFlag = False
			if (len(passed_voltages) == len(passed_ekgtags)) and (len(passed_ekgtags) == len(passed_ptags)):
				equalquantitiesFlag = True

			if equalquantitiesFlag and validate_child_records(passed_voltages, passed_ekgtags, passed_ptags, json_data):#all or none
				print("Voltages have been confirmed as valid data")
				returned_response 	 = self.create(request, *args, **kwargs) #creates the parent ekg record
				content_of_response  = returned_response.data
				new_ekgId 			 = content_of_response.get('ekgId')#gets the parent id value for the child table(EkgVoltageReadings)
				json_for_child 		 = {'ekgId': new_ekgId}#comment out for unit test to illustrate parent id validation for newly added record
				# print("ekg id from response is: "+ str(new_ekgId) +" and of type: "+ str(type(new_ekgId)) )
				json_data.update(json_for_child)
				for indice in range(0, len(passed_voltages)):

					voltage_value = passed_voltages[indice]
					ekgtag_value  = passed_ekgtags[indice]
					ptag_value	  = passed_ptags[indice]

					volt_pair   = {'voltage_reading': voltage_value}
					ekgtag_pair	= {'ekgtag': ekgtag_value}
					ptag_pair   = {'ptag': ptag_value}

					json_data.update(volt_pair)
					json_data.update(ekgtag_pair)
					json_data.update(ptag_pair)
					ekgVoltageSerializer = EkgVoltageSerializer(data=json_data)	
					ekgVoltageSerializer.is_valid()#must be called before save, regardless that we've already validated prior to this
					ekgVoltageSerializer.save()
					json_data.pop('voltage_reading', None)#remove to make room for the next voltage reading
					json_data.pop('ekgtag', None)
					json_data.pop('ptag', None)
			else:
				print("Invalid data was sent")
				return HttpResponseBadRequest("One or more passed values are invalid")

			#verify voltages were stored
			qs = EkgVoltageReadings.objects.all().filter(ekgId= new_ekgId)
			for e in qs:#.filter(ekgId = new_ekgId):
				print ("Ekg record id: " + str(e.ekgId_id))#_id is concatenated to foreign keys for identification by default
				print ("Ekg volt id: "+ str(e.ekgVoltId))
				print ("Ekg volt reading: " + str(e.voltage_reading))
				print ("Ekg tag: " + str(e.ekgtag))
				print ("P tag: " + str(e.ptag))
			return HttpResponse("Successfully stored records")
		else:

			return HttpResponseBadRequest("Sorry, there was an error in your request, please contact your admin for more details")
		


    #called through self.create using serializer
	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

			

	def perform_destroy(self, instance):
		if instance is not None:
			return instance.delete()
		return None


	def delete(self, request, *args, **kwargs):
		url_passed_id		= request.GET.get('id', None)
		json_data 			= {}
		body_				= request.body
		if is_json(body_):
			json_data 			= json.loads(request.body)
		new_passed_id 		= json_data.get('id', None)
		self.passed_id = url_passed_id or new_passed_id or None
		return self.destroy(request, *args, **kwargs)














#####################################################################################
# Class    : EkgVoltageReadingAPIView
# Purpose  : Implements Retrieval only of child records for data aquisition: Due to the nature of views, 
#			 a seperate view is required for this transaction to use the correct serializer to present child table
#			 data to the user
#			 
# Workflow : Maps the incoming response (get, post, put, patch, delete) to a method
#            defined below. 
#
#            If a detail view is request and no parameters are given, the 
#            get_queryset() method will then be called. 
#
#####################################################################################
class EkgVoltageReadingAPIView(
                         generics.ListAPIView):
	permission_classes          = [permissions.IsAuthenticated]
	authentication_classes      = [JSONWebTokenAuthentication]
	serializer_class            = EkgVoltageSerializer

	#Designed to retrieve all ekg data of a patient, or data based on a passed date
	def get_queryset(self):
		# print("Current date: " + str(datetime.now().date()))
		request = self.request
		# print("Data for user:" + str(request.user))
		json_data 			= {}
		body_				= request.body
		#get the json data of passed key's or they don't exist
		if is_json(body_):
			json_data 			= json.loads(request.body)
		passed_start_date = json_data.get('start_date', None)
		passed_end_date   = json_data.get('end_date', None)
		print("Start date passed  " + str(passed_start_date))
		print("End date passed  " + str(passed_end_date))
		qs = ""
		if passed_end_date is not None and passed_start_date is not None:#return objects of the date range
			qs = EkgVoltageReadings.objects.select_related('ekgId').filter(ekgId__user=request.user).filter(
		    ekgId__timestamp__gte = passed_start_date,
		    ekgId__timestamp__lt = passed_end_date,
			).distinct()
		else:															
			qs = EkgVoltageReadings.objects.all()	 #return all
		return qs

