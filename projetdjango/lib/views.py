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

@login_required(login_url='Signin')
def supprimer_livre(request, id_livre):
    livre = get_object_or_404(Livre, Id_livre=id_livre, Id_lib=request.user)
    if request.method == 'POST':
        livre.delete()
        messages.success(request, "Le livre a été supprimé avec succès.")
        return redirect('home')
    return render(request, 'confirmer_suppression.html', {'livre': livre})

@login_required(login_url='Signin')
def modifier_livre(request, id_livre):
    livre = get_object_or_404(Livre, Id_livre=id_livre, Id_lib=request.user)
    if request.method == 'POST':
        form = LivreForm(request.POST, request.FILES, instance=livre)
        if form.is_valid():
            form.save()
            messages.success(request, "Le livre a été modifié avec succès.")
            return redirect('home')
    else:
        form = LivreForm(instance=livre)
    return render(request, 'modifier_livre.html', {'form': form, 'livre': livre})
