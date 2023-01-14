from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field


#Classe de formulaire d'ajout de salle
class InfosSalleForm(forms.Form):
    name = forms.CharField(max_length=255)
    guests_number = forms.IntegerField()
    cafe_machine = forms.BooleanField(required=False)
    whiteboard = forms.BooleanField(required=False)
    the_wifi = forms.BooleanField(required=False)
    projector = forms.BooleanField(required=False)
    # Méthode pour configurer l'affichage du formulaire en utilisant crispy
    def __init__(self, *args, **kwargs):
        # Créer un objet helper pour configurer l'affichage du formulaire
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))
        self.helper.layout = Layout(
            Field('name'),
            Field('guests_number'),
            Field('cafe_machine'),
            Field('whiteboard'),
            Field('the_wifi'),
            Field('projector'),
        )
    

#Classe de formulaire de recherche de salle   
class SearchForm(forms.Form):
    invite_nombre = forms.CharField(max_length=100)
    purpose = forms.CharField(max_length=200)
    date = forms.DateField()
    la_machine_a_cafe = forms.BooleanField(required=False)
    le_tableau_blanc = forms.BooleanField(required=False)
    la_wifi = forms.BooleanField(required=False)
    le_projecteur = forms.BooleanField(required=False)
    # Méthode pour configurer l'affichage du formulaire en utilisant crispy
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Créer un objet helper pour configurer l'affichage du formulaire
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Search'))
        self.helper.layout = Layout(
            Field('invite_nombre'),
            Field('purpose'),
            Field('date'),
            Field('la_machine_a_cafe'),
            Field('le_tableau_blanc'),
            Field('la_wifi'),
            Field('le_projecteur'),
        )
    

    


    
    
