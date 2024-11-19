from django.contrib import admin
from .models import Animal, Equipement

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('nom', 'espece', 'etat', 'equipement', 'image_preview')  # Inclut une prévisualisation de l'image
    search_fields = ('nom', 'espece')  # Ajoute une barre de recherche sur les champs spécifiés
    list_filter = ('etat', 'equipement')  # Filtres pour simplifier la recherche

    # Méthode pour afficher une prévisualisation de l'image dans l'interface admin
    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="width:50px; height:auto;">'
        return "Aucune image"
    image_preview.allow_tags = True  # Permet l'affichage HTML dans Django admin
    image_preview.short_description = "Image"

@admin.register(Equipement)
class EquipementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type', 'disponible')  # Ajout du champ `type`

