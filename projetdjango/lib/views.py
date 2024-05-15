# employees/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import LivreForm
from .models import Livre,Library

from django.shortcuts import render, redirect
from .models import Livre
from .forms import LivreForm

def recherche(request):
    query = request.GET.get('q')
    livres = Livre.objects.all()

    if query:
        livres = livres.filter(Name_book__icontains=query)

    return render(request, 'resultat.html', {'livres': livres, 'query': query})

def liste_livres(request):
    livres = Livre.objects.all().select_related('Id_lib')
    return render(request, 'liste_livres.html', {'livres': livres})
    def ajouter_livre(request):
    if request.method == 'POST':
        form = LivreForm(request.POST, request.FILES)
        if form.is_valid():
            livre = form.save(commit=False)
            livre.Id_lib = request.user.library  
            livre.save()
            return redirect('page_accueil') 
    else:
        form = LivreForm()
    return render(request, 'ajouter un livre.html', {'form': form})
