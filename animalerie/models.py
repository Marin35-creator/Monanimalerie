from django.db import models

class Equipement(models.Model):
    TYPES = [
        ('mangeoire', 'Mangeoire'),
        ('nid', 'Nid'),
        ('roue', 'Roue'),
        ('litière', 'Litière'),
    ]

    nom = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=50, choices=TYPES)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nom


class Animal(models.Model):
    ETATS = [
        ('affamé', 'Affamé'),
        ('repus', 'Repus'),
        ('fatigué', 'Fatigué'),
        ('endormi', 'Endormi'),
    ]

    nom = models.CharField(max_length=100)
    espece = models.CharField(max_length=100)
    etat = models.CharField(max_length=10, choices=ETATS, default='endormi')
    equipement = models.ForeignKey(Equipement, null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='animals/', blank=True, null=True) 

    def __str__(self):
        return f"{self.nom} ({self.espece}) - État : {self.etat}"

    def appliquer_action(self):
        """Appliquer une action en fonction de l'équipement assigné"""
        if self.equipement:
            if self.equipement.type == 'mangeoire':
                self.etat = 'repus'
            elif self.equipement.type == 'roue':
                self.etat = 'fatigué'
            elif self.equipement.type == 'nid':
                self.etat = 'endormi'
            self.save()
