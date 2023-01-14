from django.shortcuts import render
from .forms import InfosSalleForm,SearchForm
from .models import InfosSalle
from .models import SalleReserve
from django.contrib import messages
from django.db.models import Subquery



def homeemploye_view(request):
    return render(request, 'home_employe.html')

def insert_view(request):
    
    """
    Gère la soumission de formulaire pour la création de nouvelles salles et
    enregistre les données dans le modèle InfosSalle
    """
    if request.method == 'POST':
        form = InfosSalleForm(request.POST)
        if form.is_valid():
        # Créer une instance du modèle InfosSalle avec les données du formulaire
            model_instance = InfosSalle(
            nom=form.cleaned_data['name'],
            nombre_invite=form.cleaned_data['guests_number'],
            machine_a_cafe=form.cleaned_data['cafe_machine'],
            tableau_blanc=form.cleaned_data['whiteboard'],
            wifi=form.cleaned_data['the_wifi'],
            projecteur=form.cleaned_data['projector']
            )
        # Enregistrer l'instance dans la base de données
            model_instance.save()
        # Réinitialiser le formulaire    
            form = InfosSalleForm()
            
            messages.success(request, 'Salle enregistrée avec succès')
        else :
            messages.error(request, 'Erreur lors de l\'enregistrement de la salle')

    else:
        form = InfosSalleForm()
    return render(request, 'ajouter_salle.html', {'form': form})

def view_salle(request):
    #Affiche toutes les salles enregistrées dans la base de données
    salle = InfosSalle.objects.all()
    return render(request, 'liste_salle.html', {'salle': salle})

def view_reservation(request):
    #Affiche toutes les réservations de salles enregistrées dans la base de données
    reservation=SalleReserve.objects.all()
    return render(request,'salle_reserve.html',{'reservation':reservation})

def search_view(request):
    """
    Permet à l'utilisateur de rechercher une salle disponible en fonction de certains critères. 
    Si une salle est trouvée, elle est réservée pour la date spécifiée 
    et une page de reçu est affichée avec les détails de la réservation. 
    Si aucune salle n'est trouvée, une page est affichée avec les salles disponibles qui correspondent 
    le plus aux critères spécifiés.
    """
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            #Récupérer les données du formulaire
            nombre_invite = form.cleaned_data['invite_nombre']
            date_f = form.cleaned_data['date']
            """
            convertit la date récupérée depuis le formulaire (date_f) au format "année-mois-jour" (YYYY-MM-DD), 
            permet de stocker la date dans la session pour le futur usage dans la fonction form_submit.
            """
            date_string = date_f.strftime("%Y-%m-%d") 
            request.session['date_f'] = date_string
            request.session.save()
            
            machine_a_cafe = form.cleaned_data['la_machine_a_cafe']
            tableau_blanc = form.cleaned_data['le_tableau_blanc']
            wifi = form.cleaned_data['la_wifi']
            projecteur = form.cleaned_data['le_projecteur']
            

            #filtrer les salles disponibles en fonction des critères de l'utilisateur

            infos_salle_results = InfosSalle.objects.filter(
                nombre_invite=nombre_invite,
                machine_a_cafe=machine_a_cafe,
                tableau_blanc=tableau_blanc,
                wifi=wifi,
                projecteur=projecteur,
                en_construction=False, 
            )
            
            if infos_salle_results:
                for room in infos_salle_results:
                    # Recherche des salles réservées pour la date sélectionnée
                    salle_reserve=SalleReserve.objects.filter(nom=room.nom, date_evt=date_f)
            
                    if not salle_reserve:
                        # Si aucune salle n'est réservée pour cette date, on enregistre la réservation
                            reserved_room = SalleReserve(nom=room.nom, date_evt=date_f)
                            reserved_room.save()
                    
                            # Retourne la vue de confirmation de réservation
                            return render(request, 'receipt.html', {
                                'nombre_invite': nombre_invite,
                                'date': date_f,
                                'machine_a_cafe': machine_a_cafe,
                                'tableau_blanc': tableau_blanc,
                                'wifi': wifi,
                                'projecteur': projecteur,
                                'nom_t': room.nom,
                                'reserved_room':reserved_room,
                            })                        
                            
                    # Si la salle est déjà réservée pour cette date, on affiche les salles disponibles
                    elif salle_reserve :
                        """
                        Récupération des noms des salles réservées pour la date sélectionnée pour futur usage 
                        dans le stockage de données dans la table SalleReserve
                        """
                        reserved_rooms = SalleReserve.objects.filter(date_evt=date_f).values('nom')
                        
                        # Récupération des informations des salles disponibles (en excluant les salles réservées pour cette date)
                        available_rooms_infos = InfosSalle.objects.filter(en_construction=False).exclude(nom__in=Subquery(reserved_rooms))


                        return render(request, 'receipt.html', {
                        'message': "Nous avons aucune salle disponible avec tous les critères que vous demandez dans cette date.",
                        'available_rooms_infos': available_rooms_infos,
                            })

                        
            

            
            else :
                reserved_rooms = SalleReserve.objects.filter(date_evt=date_f).values('nom')
                available_rooms_infos = InfosSalle.objects.filter(en_construction=False).exclude(nom__in=Subquery(reserved_rooms))
                

                return render(request, 'receipt.html', {
                'message': "Nous avons aucune salle disponible avec tous les critères que vous demandez.",
                'available_rooms_infos': available_rooms_infos,
                    })
               
                                   
                
    else:
        form = SearchForm()
        return render(request, 'reserver_salle.html', {'form': form})
              

def form_submit(request):
    #récupère les données de la session pour obtenir la date sélectionnée par l'utilisateur
    date_string = request.session.get('date_f')
    #récupère l'ID de la salle sélectionnée dans le tableau des salles disponibles
    room_id = request.POST.get('room_id')
    """
    récupère l'objet InfosSalle correspondant à cet ID, crée un nouvel objet SalleReserve
    avec les informations de cette salle et de la date, et enregistre cet objet en base de données.
    """
    room = InfosSalle.objects.get(id=room_id)
    reserved_room = SalleReserve(nom=room.nom, date_evt=date_string)
    reserved_room.save()
    
    #affiche le reçu avec les informations de la réservation.
    return render(request, 'receipt.html', {
            'nombre_invite': room.nombre_invite,
            'date': date_string,
            'machine_a_cafe': room.machine_a_cafe,
            'tableau_blanc': room.tableau_blanc,
            'wifi': room.wifi,
            'projecteur': room.projecteur,
            'nom_t': room.nom,
            'reserved_room':reserved_room,
                                    })      