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
from cardapp.models import Deck, CardTransact
from .serializers.serializers_deck import DeckSerializer
from .serializers.serializers_cardtransact import CardTransactSerializer


#########################EkgAPIView############################################################
# Class    : DeckAPIView
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

# def validate_child_records(passed_voltages, ekgtags, ptags, json_data):#batch validation for voltages for an 'all or none' effect
# 	try:
# 		dumbyEkgId 		 = {'ekgId': 1}#safe because no values are actually saved here
# 		json_data.update(dumbyEkgId)

# 		print('\n\n\n')
# 		for indice in range(0, len(passed_voltages)):
# 			voltage_value = passed_voltages[indice]
# 			ekgtag_value  = ekgtags[indice]
# 			ptag_value	  = ptags[indice]
# 			#kept for debugging purposes
# 			# print("Voltage value at indice:" + str(indice) + ": is of value: " + str(voltage_value))
# 			# print("ekgtag_value value at indice:" + str(indice) + ": is of value: "  + str(ekgtag_value))
# 			# print("ptag_value value at indice:" + str(indice) +": is of value: " + str(ptag_value))
# 			volt_pair   = {'voltage_reading': voltage_value}
# 			ekgtag_pair	= {'ekgtag': ekgtag_value}
# 			ptag_pair   = {'ptag': ptag_value}

# 			json_data.update(volt_pair)
# 			json_data.update(ekgtag_pair)
# 			json_data.update(ptag_pair)


# 			ekgVoltageSerializer = EkgVoltageSerializer(data=json_data)	
# 			if ekgVoltageSerializer.is_valid():

# 				json_data.pop('voltage_reading', None)#remove to make room for the next voltage reading
# 				json_data.pop('ekgtag', None)#remove to make room for the next ekgtag
# 				json_data.pop('ptag', None)#remove to make room for the next ptag
				
# 			else:
# 				return False
# 		json_data.pop('ekgId', None)
# 		return True
# 	except:
# 		return False
	


class DeckAPIView(mixins.CreateModelMixin,
 generics.ListAPIView):


	permission_classes= [permissions.IsAuthenticated]
	authentication_classes= [JSONWebTokenAuthentication]
	serializer_class 		= DeckSerializer




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
		passed_id 		  = json_data.get('deckId', None) 
		if passed_id is not None:												 #return object of id
			qs = Deck.objects.all().filter(user=request.user).filter(id = passed_id)
		# elif passed_end_date is not None and passed_start_date is not None:#return objects of the date range
		# 	qs = Ekg.objects.all().filter(user=request.user).filter(
		#     timestamp__gte = passed_start_date,
		#     timestamp__lt = passed_end_date,
		# 	).distinct()
		else:															
			qs = Deck.objects.all().filter(user=request.user)	 #return all ekg records
		return qs






	#Original initialization of deck data
	def post(self, request, *args, **kwargs):
		request = self.request
		print("Post method initiates here")
		body_	= request.body
		if is_json(body_):
			# print("the original json data is: " + str(request.body) + " of type: " +str(type(request.body)))
			# print('\n\n\n')
			json_data 		= json.loads(request.body)
			passed_deckid  = json_data.get('deckId', None)

			#initialize junk deck id's used by pokemon api
			passed_ids     = {}
			for i in range(0,60):
			    tempstring = str(i+1)
			    passed_ids[i] = "base1-" + tempstring


			try:
				#TODO FIX THIS BULL SHIT
				#TODO FIX THIS BULL SHIT
				#TODO FIX THIS BULL SHIT
				#TODO FIX THIS BULL SHIT
				#TODO FIX THIS BULL SHIT
				#TODO FIX THIS BULL SHIT
				#TODO FIX THIS BULL SHIT
				#TODO FIX THIS BULL SHIT



				#TODO FIX THIS BULL SHIT
				#TODO FIX THIS BULL SHIT
				#TODO FIX THIS BULL SHIT
				#TODO FIX THIS BULL SHIT
				#TODO FIX THIS BULL SHIT
				#TODO FIX THIS BULL SHIT
				#TODO FIX THIS BULL SHIT








				returned_response 	 = self.create(request, *args, **kwargs) #creates the parent Deck record
				content_of_response  = returned_response.data
				new_deckId 			 = content_of_response.get('deckId')#gets the parent id value for the child table(EkgVoltageReadings)
				json_for_child 		 = {'deckId': new_deckId}#comment out for unit test to illustrate parent id validation for newly added record
				# print("ekg id from response is: "+ str(new_ekgId) +" and of type: "+ str(type(new_ekgId)) )
				json_data.update(json_for_child)#supplies key-value pair needed for cardtransact serializer/table
				for indice in range(0, len(passed_ids)):

					cardId_value  = passed_ids[indice]

					cardId_pair   = {'cardId': cardId_value}

					json_data.update(cardId_pair)

					cardTransactSerializer = CardTransactSerializer(data=json_data)	
					cardTransactSerializer.is_valid()#must be called before save, regardless that we've already validated prior to this
					cardTransactSerializer.save()
					json_data.pop('cardId', None)#remove to make room for the next cardId issued in default deck
			except Exception as e: 
				# print(e)
				print("Invalid data was sent")
				return HttpResponseBadRequest("Caught at attempt of creation of deck and child records: error was" + str(e))



			#verify voltages were stored
			qs = CardTransact.objects.all().filter(deckId= new_deckId)
			for e in qs:#.filter(ekgId = new_ekgId):
				print ("CardTransactId is" + str(e.cardTransactId_id))#_id is concatenated to foreign keys for identification by default
				print ("CardId is: "+ str(e.cardId))
				print ("Deck id is: " + str(e.deckId))
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
# Class    : CardTransactAPIView
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
class CardTransactAPIView(
                         generics.ListAPIView):
	permission_classes          = [permissions.IsAuthenticated]
	authentication_classes      = [JSONWebTokenAuthentication]
	serializer_class            = CardTransactSerializer

	#Designed to retrieve all cards of a particular deck
	def get_queryset(self):
		# print("Current date: " + str(datetime.now().date()))
		request = self.request
		# print("Data for user:" + str(request.user))
		json_data 			= {}
		body_				= request.body
		#get the json data of passed key's or they don't exist
		if is_json(body_):
			json_data 			= json.loads(request.body)
		passed_deckid = json_data.get('deckId', None)
		
		qs = ""
		if passed_deckid is not None :#return objects of the date range
			qs = CardTransact.objects.select_related('deckId').filter(deckId__user=request.user).distinct()
		else:															
			return none #if no deck id is passed, we can't return a valid deck
		return qs

