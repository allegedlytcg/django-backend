#########################################################################################
# File    : customApp__FitBit/models/auth.py
# Purpose : contains models for the fitbit authorization
# 
# Authors : @Charles Erd
# Date    : July 8th, 2019
#########################################################################################

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()                            #Acquire the user model 

#########################################################################################
# Class              : BloodPressureQuerySet
# Inherits From      : models.QuerySet
# What is a QuerySet : A QuerySet is a list of objects for a given model
#
#
# Purpose            : Leveraging out-of-the-box QuerySet manager
#########################################################################################
class BloodPressureQuerySet(models.QuerySet):
    pass


class BloodPressureManager(models.Manager):
	def get_queryset(self):
		return StatusQuerySet(self.model, using=self._db)



#########################################################################################
#Class         : BloodPressure
#Inherits From : models.Model
#Purpose         The model contains the essential fields and behaviors for the stored data
#                ... Each model maps to a database table
#
#Big Picture   : Django uses this model to create an automatically-generated database
#                ... access API
#########################################################################################
class BloodPressure(models.Model):
    user            	= models.ForeignKey(User, on_delete=models.CASCADE, blank = False, null=False)

    bpId                = models.AutoField(primary_key=True)

    dPressure           = models.IntegerField(blank = False, null=False)

    sPressure           = models.IntegerField(blank = False, null=False)

    heartRate           = models.IntegerField(blank = False, null=False)

    timestamp    		= models.DateTimeField(auto_now_add=True, null=False, blank=False) #date and time of the signal added to db



    def __str__(self):                                  #Sets the name of the object
        return str(self.dpressure) #display the sent ekg content when calling self.name
    class Meta:
        verbose_name = 'BloodPressure post'
        verbose_name_plural = 'BloodPressure posts'








#########################################################################################
# Class              : Deck
# Inherits From      : models.QuerySet
# What is a QuerySet : A QuerySet is a list of objects for a given model
#
#
# Purpose            : Leveraging out-of-the-box QuerySet manager
#########################################################################################
class DeckQuerySet(models.QuerySet):
    pass


class DeckManager(models.Manager):
    def get_queryset(self):
        return StatusQuerySet(self.model, using=self._db)



#########################################################################################
#Class         : Deck
#Inherits From : models.Model
#Purpose         The model contains the essential fields and behaviors for the stored data
#                ... Each model maps to a database table
#
#Big Picture   : Django uses this model to create an automatically-generated database
#                ... access API
#########################################################################################
class Deck(models.Model):
    user                = models.ForeignKey(User, on_delete=models.CASCADE, blank = False, null=False)

    deckId              = models.AutoField(primary_key=True)

    deckName            = models.TextField(max_length=3, null = False, blank= False)


    def __str__(self):                                  #Sets the name of the object
        return str(self.deckName) #display the sent deckName content when calling self.name
    class Meta:
        verbose_name = 'Deck post'
        verbose_name_plural = 'Deck posts'







#########################################################################################
# Class              : CardTransact
# Inherits From      : models.QuerySet
# What is a QuerySet : A QuerySet is a list of objects for a given model
#
#
# Purpose            : Leveraging out-of-the-box QuerySet manager
#########################################################################################
class CardTransactQuerySet(models.QuerySet):
    pass


class CardTransactManager(models.Manager):
    def get_queryset(self):
        return StatusQuerySet(self.model, using=self._db)



#########################################################################################
#Class         : CardTransact
#Inherits From : models.Model
#Purpose         The model contains the essential fields and behaviors for the stored data
#                ... Each model maps to a database table
#
#Big Picture   : Django uses this model to create an automatically-generated database
#                ... access API
#########################################################################################
class CardTransact(models.Model):

    cardTransactId      = models.AutoField(primary_key=True)

    deckId              = models.ForeignKey(Deck, on_delete=models.CASCADE, blank = False, null=False)

    cardId              = models.TextField(null = False, blank= False)#installed with pkm api


    def __str__(self):                                  #Sets the name of the object
        return str(self.cardTransactId) #display the sent deckName content when calling self.name
    class Meta:
        verbose_name = 'CardTransact post'
        verbose_name_plural = 'CardTransact posts'








