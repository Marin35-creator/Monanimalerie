from django.shortcuts import render, get_object_or_404, redirect
from .models import Animal, Equipement
from .forms import AssignEquipementForm
from django.contrib import messages

def home(request):
    """Affiche la liste des animaux et des équipements."""
    animals = Animal.objects.all()
    equipments = Equipement.objects.all()

    # Ajouter les animaux qui occupent chaque équipement
    for equipement in equipments:
        equipement.occupant = Animal.objects.filter(equipement=equipement).first()  # Récupérer le premier animal occupant

    return render(request, 'animalerie/home.html', {'animals': animals, 'equipments': equipments})

def animal_detail(request, animal_id):
    """Affiche les détails d'un animal et permet de l'assigner à un équipement."""
    animal = get_object_or_404(Animal, id=animal_id)
    form = AssignEquipementForm(instance=animal)

    if request.method == 'POST':
        old_equipement = animal.equipement  # Stocker l'ancien équipement
        form = AssignEquipementForm(request.POST, instance=animal)
        if form.is_valid():
            animal = form.save(commit=False)
            new_equipement = animal.equipement

            if new_equipement.type != "litière" and not new_equipement.disponible:
                 messages.error(request, f"L'équipement {new_equipement.nom} est déjà occupé.")
                 return redirect('action_not_allowed', animal_id=animal.id)


            # Logique métier pour l'action
            if new_equipement:
                if new_equipement.type == 'mangeoire' and animal.etat == 'affamé':
                    animal.etat = 'repus'
                    new_equipement.disponible = False
                elif new_equipement.type == 'roue' and animal.etat == 'repus':
                    animal.etat = 'fatigué'
                    new_equipement.disponible = False
                elif new_equipement.type == 'nid' and animal.etat == 'fatigué':
                    animal.etat = 'endormi'
                    new_equipement.disponible = False
                elif new_equipement.type == 'litière':
                    # Si l'animal est dans le nid et endormi, il devient affamé
                    if old_equipement and old_equipement.type == "nid" and animal.etat == "endormi":
                        animal.etat = "affamé"
                else:
                    messages.error(request, f"L'état actuel de {animal.nom} ne permet pas cette action.")
                    return redirect('action_not_allowed', animal_id=animal.id)

                # Libérer l'ancien équipement si nécessaire
                if old_equipement and old_equipement.type != 'litière':
                    old_equipement.disponible = True
                    old_equipement.save()

            animal.save()
            if new_equipement and new_equipement.type != "litière":
                new_equipement.save()
            return redirect('animal_detail', animal_id=animal.id)

    return render(request, 'animalerie/animal_detail.html', {'animal': animal, 'form': form})



def assign_animal_to_equipement(request, animal_id):
    """
    Assigne un équipement à un animal via un formulaire.
    """
    animal = get_object_or_404(Animal, id=animal_id)
    old_equipement = animal.equipement  # Stocker l'ancien équipement

    if request.method == 'POST':
        form = AssignEquipementForm(request.POST)
        if form.is_valid():
            new_equipement = form.cleaned_data['equipement']

            if new_equipement.type != "litière" and not new_equipement.disponible:
                messages.error(request, f"L'équipement {new_equipement.nom} est déjà occupé.")
                return redirect('action_not_allowed', animal_id=animal.id)

            # Libérer l'ancien équipement (sauf pour la litière)
            if old_equipement and old_equipement.type != "litière":
                old_equipement.disponible = True
                old_equipement.save()

            # Assigner le nouvel équipement à l'animal
            animal.equipement = new_equipement

            # Appliquer l'action et mettre à jour l'état de l'animal et de l'équipement
            if new_equipement.type == "mangeoire" and animal.etat == "affamé":
                animal.etat = "repus"
                new_equipement.disponible = False
            elif new_equipement.type == "roue" and animal.etat == "repus":
                animal.etat = "fatigué"
                new_equipement.disponible = False
            elif new_equipement.type == "nid" and animal.etat == "fatigué":
                animal.etat = "endormi"
                new_equipement.disponible = False
            elif new_equipement.type == "litière":
                # Si l'animal était "endormi" dans le "nid", il devient "affamé" en allant dans la litière
                if old_equipement and old_equipement.type == "nid" and animal.etat == "endormi":
                    animal.etat = "affamé"
                # Sinon, l'animal conserve son état actuel
                pass
            else:
                # Si l'action n'est pas permise
                messages.error(request, f"L'état actuel de {animal.nom} ne permet pas cette action.")
                return redirect('action_not_allowed', animal_id=animal.id)

            # Sauvegarder l'animal et le nouvel équipement
            animal.save()
            if new_equipement.type != "litière":
                new_equipement.disponible = False
                new_equipement.save()

            return redirect('home')
    else:
        form = AssignEquipementForm()

    return render(request, 'animalerie/assign_equipment.html', {'form': form, 'animal': animal})


def action_not_allowed(request, animal_id):
    """
    Affiche un message lorsque l'action n'est pas permise pour un animal.
    """
    animal = get_object_or_404(Animal, id=animal_id)
    return render(request, 'animalerie/action_not_allowed.html', {'animal': animal})
