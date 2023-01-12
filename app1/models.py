from django.db import models     

class InfosSalle(models.Model):
    nom = models.CharField(max_length=255)
    nombre_invite = models.IntegerField()
    machine_a_cafe = models.BooleanField()
    tableau_blanc = models.BooleanField()
    wifi = models.BooleanField()
    projecteur = models.BooleanField()
    en_construction=models.BooleanField(default=False)
    
    
class SalleReserve(models.Model):
    nom = models.CharField(max_length=255)
    date_evt = models.DateField()
    
    
