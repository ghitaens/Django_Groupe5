from django.http import HttpResponse
from django.shortcuts import render
from .forms import InfosSalleForm,SearchForm
from .models import InfosSalle
from .models import SalleReserve
from django.contrib import messages
from django.db.models import Subquery



def homeemploye_view(request):
    return render(request, 'home_employe.html')

def insert_view(request):
    if request.method == 'POST':
        form = InfosSalleForm(request.POST)
        if form.is_valid():

            model_instance = InfosSalle(
                nom=form.cleaned_data['name'],
                nombre_invite=form.cleaned_data['guests_number'],
                machine_a_cafe=form.cleaned_data['cafe_machine'],
                tableau_blanc=form.cleaned_data['whiteboard'],
                wifi=form.cleaned_data['the_wifi'],
                projecteur=form.cleaned_data['projector']
            )
            model_instance.save()
            
            form = InfosSalleForm()
            messages.success(request, 'Salle enregistrée avec succès')
        else :
            messages.error(request, 'Erreur lors de l\'enregistrement de la salle')

    else:
        form = InfosSalleForm()
    return render(request, 'ajouter_salle.html', {'form': form})

def view_salle(request):
    salle = InfosSalle.objects.all()
    return render(request, 'liste_salle.html', {'salle': salle})

def view_reservation(request):
    reservation=SalleReserve.objects.all()
    return render(request,'salle_reserve.html',{'reservation':reservation})

def search_view(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            nombre_invite = form.cleaned_data['invite_nombre']
            date_f = form.cleaned_data['date']
            date_string = date_f.strftime("%Y-%m-%d")
            request.session['date_f'] = date_string
            request.session.save()
            machine_a_cafe = form.cleaned_data['la_machine_a_cafe']
            tableau_blanc = form.cleaned_data['le_tableau_blanc']
            wifi = form.cleaned_data['la_wifi']
            projecteur = form.cleaned_data['le_projecteur']
            

            

            # Search for matching records in the infos_salle table
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
                    salle_reserve=SalleReserve.objects.filter(nom=room.nom, date_evt=date_f)
            
                    if not salle_reserve:
                            reserved_room = SalleReserve(nom=room.nom, date_evt=date_f)
                            reserved_room.save()
                    
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
                    elif salle_reserve :
                        
                        reserved_rooms = SalleReserve.objects.filter(date_evt=date_f).values('nom')
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
    date_string = request.session.get('date_f')
    room_id = request.POST.get('room_id')
    room = InfosSalle.objects.get(id=room_id)
    reserved_room = SalleReserve(nom=room.nom, date_evt=date_string)
    reserved_room.save()
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