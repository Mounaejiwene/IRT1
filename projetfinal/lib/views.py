import os
import random
from django.http import FileResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password,check_password
from .forms import LivreForm
from .models import Livre, Library
from django.contrib.auth import  login, logout
from django.core.mail import send_mail
from Library import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

# Configuration de l'email
server = 'smtp-mail.outlook.com'
port = 587
email = os.environ.get('Sender_email')
password = os.environ.get('Sender_password')

# Authentification
def homecomm(request):
    
    return render(request,"Welcompage.html")
active =[]
def No_connected_librairies():
    global active
    active=[]
    return None
def Signin(request):
    if request.method=='POST':
        username_or_email = request.POST['credential']
        password = request.POST['password']

        library = Library.objects.filter(username = username_or_email).first()

        if library is None:
            library = Library.objects.filter(email=username_or_email).first()

        if library is not None:
            if check_password(password,library.password):
                login(request,library)
                active.append((library.id,library.is_active))
                return redirect('home')
            else:
                messages.error(request,"La librairie n'existe pas ou mot de passe incorrect.")
                return redirect('Signin')
        else:
             messages.error(request,"La librairie n'existe pas ou mot de passe incorrect.")
             return redirect('Signin')
    return render(request,'Signin.html')


def ktab(request, Id_livre):
    book = get_object_or_404(Livre, Id_livre=Id_livre)
    return render(request, 'detail_livre.html', {'book': book})

def listclient(request):
    query = request.GET.get('q')
    if query:
        livres = Livre.objects.filter(Name_book__icontains=query)
    else:
        livres = Livre.objects.all()
    return render(request, 'client.html', {'livres': livres, 'query': query})

def supprimer_livre(request, id_livre):
    if active[0][1]==True:
        livre = get_object_or_404(Livre, Id_livre=id_livre, Id_lib=active[0][0])
        if request.method == 'POST':
            livre.delete()
            messages.success(request, "Le livre a été supprimé avec succès.")
            return redirect('home')
        return render(request, 'confirmer_suppression.html', {'livre': livre})
    else:
        messages.error(request, "Vous devez vous connectez.")
        return redirect('Signin')


def modifier_livre(request, id_livre):
    if active[0][1]==True:
        livre = get_object_or_404(Livre, Id_livre=id_livre, Id_lib=active[0][0])
        if request.method == 'POST':
            form = LivreForm(request.POST, request.FILES, instance=livre)
            if form.is_valid():
                form.save()
                messages.success(request, "Le livre a été modifié avec succès.")
                return redirect('home')
            else:
                messages.error(request,"Informations Invalides")
        else:
            form = LivreForm(instance=livre)
            return render(request, 'modifier_livre.html', {'form': form, 'livre': livre})
    else:
        messages.error(request, "Vous devez vous connectez.")
        return redirect('Signin')

def ajouter_livre(request):
    if active[0][1]==True:
        if request.method == 'POST':
            form = LivreForm(request.POST, request.FILES)
            if form.is_valid():
                livre = form.save(commit=False)
                livre.Id_lib =Library.objects.get(id=active[0][0]) 
                livre.save()
                messages.success(request, "Le livre a été ajouté avec succès.")
                return redirect('home')
            else:
                messages.error(request, "Verifier la validité des informations du livre.")
        else:
            form = LivreForm()
            return render(request, 'ajouter un livre.html', {'form': form,'who':active[0][0]})

def home(request):
    if active[0][1]==True:
        idlib =  active[0][0]
        query = request.GET.get('q')
        if query:
            livres = Livre.objects.filter(Id_lib=active[0][0], Name_book__icontains=query)
        else:
            livres = Livre.objects.filter(Id_lib=active[0][0])
        return render(request, 'home.html', {'livres': livres, 'query': query, 'idlib':idlib})
    else:
        messages.error(request, "Vous devez vous connectez.")
        return redirect('Signin')




def supprimer_livre(request, id_livre):
    if active[0][1]==True:
        livre = get_object_or_404(Livre, Id_livre=id_livre, Id_lib=active[0][0])
        if request.method == 'POST':
            livre.delete()
            messages.success(request, "Le livre a été supprimé avec succès.")
            return redirect('home')
        return render(request, 'confirmer_suppression.html', {'livre': livre})
    else:
        messages.error(request, "Vous devez vous connectez.")
        return redirect('Signin')



def modifier_livre(request, id_livre):
    if active[0][1]==True:
        livre = get_object_or_404(Livre, Id_livre=id_livre, Id_lib=active[0][0])
        if request.method == 'POST':
            form = LivreForm(request.POST, request.FILES, instance=livre)
            if form.is_valid():
                form.save()
                messages.success(request, "Le livre a été modifié avec succès.")
                return redirect('home')
        else:
            form = LivreForm(instance=livre)
            return render(request, 'modifier_livre.html', {'form': form, 'livre': livre})
    else:
        messages.error(request, "Vous devez vous connectez.")
        return redirect('Signin')




def about_page(request):
    return render(request, 'about.html')



from django.shortcuts import get_object_or_404

def liste_livres(request):
    query = request.GET.get('q')
    if query:
        livres = Livre.objects.filter(Name_book__icontains=query)
    else:
        livres = Livre.objects.all()
    livres_list = []
    for livre in livres:
        livres_list.append({
            'Id_livre': livre.Id_livre,
            'Name_book': livre.Name_book,
            'Authour_name': livre.Authour_name,
            'Genre': livre.Genre,
            'Image': request.build_absolute_uri(livre.Image.url) if livre.Image else None,
            'Stock': livre.Stock,
            'Description': livre.Description,

            'Id_lib': livre.Id_lib.id,
            'Prix': livre.Prix,
            'library_name': livre.Id_lib.name_lib,  # Include library name
            'library_PHONE_NUMBER': livre.Id_lib.phone_number,  # Inclure le numéro de téléphone de la bibliothèque
        })
    return JsonResponse(livres_list, safe=False)

def detail_livre(request, book_name):
    try:
        book = get_object_or_404(Livre, Name_book=book_name)
        book_data = {
            'Id_livre': book.Id_livre,
            'Name_book': book.Name_book,
            'Authour_name': book.Authour_name,
            'Genre': book.Genre,
            'Image': request.build_absolute_uri(book.Image.url) if book.Image else None,
            'Stock': book.Stock,
            'Id_lib': book.Id_lib.id,
            'Prix': book.Prix,
            'library_name': book.Id_lib.name_lib,
        }
        return JsonResponse(book_data, safe=False)
    except Livre.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)


def filter_by_genre(request):
    genre = request.GET.get('genre')
    if genre:
        livres = Livre.objects.filter(Genre__iexact=genre)
    else:
        livres = Livre.objects.all()
    return render(request, 'client.html', {'livres': livres, 'selected_genre': genre})



def recherche(request):
    query = request.GET.get('q')
    livres = Livre.objects.all()

    if query:
        livres = livres.filter(Name_book__icontains=query)

    return render(request, 'resultat.html', {'livres': livres, 'query': query})








##Authentication system By 23-50##
signing_up = []
def erase_all():
    global signing_up
    signing_up=[]

    return None


def confirm_library(request):
    if request.method=='POST':
        code_value = request.POST['code']
        if str(code_value)==str(signing_up[1]):
            signing_up[0].save()
            erase_all()
            return redirect('Signin')
    return render(request,'Confirmer.html')

digits = [0,1,2,3,4,5,6,7,8,9]
alphabet_minuscules = [chr(i) for i in range(ord('a'), ord('z')+1)]
alphabet_maj = [chr(i) for i in range(ord('A'), ord('Z')+1)]

Alphanum_chars = digits + alphabet_minuscules + alphabet_maj

def is_thereDigit(code):
    for i in digits:
        if str(i) in code:
            return True
        else:
            return False


def generator(all_em):
    code=''
    for i in range(6):
        code+=str(random.choice(all_em))
    if is_thereDigit(code) and code.isalnum():
        return code
    else:
        return generator(all_em)



def Signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone_number']  # New phone_number field
        password = request.POST['password']
        secured_password = make_password(password)

        if Library.objects.filter(email=email).exists():
            messages.error(request, "Cet email est enregistré")
            return redirect('Signup')
        if Library.objects.filter(username=username).exists():
            messages.error(request, "Ce nom existe déjà")
            return redirect('Signup')
        if len(username) < 4:
            messages.error(request, "Ce nom est trop court")
            return redirect('Signup')
        if len(password) < 8:
            messages.error(request, "Le mot de passe doit contenir au moins 8 caractères")
            return redirect('Signup')
        
        if password.isnumeric():
            messages.error(request, 'Le mot de passe doit contenir des chiffres et des lettres')
            return redirect('Signup')
        if not password.isnumeric() and not is_thereDigit(password):
            messages.error(request,"Le mot de passe doit contenir des chiffres et des lettres")
       
        new_library = Library(
            name_lib=name,
            username=username,
            email=email,
            phone_number=phone_number,  # Add phone_number to the new Library instance
            password=secured_password
        )

        code = generator(Alphanum_chars)

        signing_up.append(new_library)
        signing_up.append(code)
        message = f"""Merci de choisir notre plateforme\nNous voudrons vérifier qu'il s'agit bien de vous\nVeuillez entrer le code de confirmation\n
        votre code de confirmation est le : {code}"""
        
        subject = "Code de confirmation"
        from_email = settings.EMAIL_HOST_USER
        to_list = [new_library.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)
        return redirect('confirm')
        
    return render(request, 'Signup.html')





    
def logout_lib(request):
   try:
    if active[0][1]==True:
        logout(request)
        No_connected_librairies()
        return redirect('Signin')
   except:
       return HttpResponse("Erreur de deconnexion !")


session =[]
def forgotten_password(request):
    code_recup = ''
    if request.method=='POST':
        email1 = request.POST['email']

        library = Library.objects.filter(email=email1).first()
        if library is not None:
            for k in range(6):
                code_recup+=str(random.choice(digits))

            session.append(code_recup)
            message = f"Vous avez oublié votre mot de passe \n pour le recuperer veuillez entrez le code de recupération suivant \n {code_recup}"
            from_email = settings.EMAIL_HOST_USER
            to_list = [email1]
            subject ="Code de recupération"
            send_mail(subject,message,from_email,to_list,fail_silently=False)
            try:
                url = f'/new_password/{library.id}'
                return redirect(url)
            except Exception as e:
                print(e)
    return render(request,'recuperer0.html')
    

def forgotten_password1(request,idlib):
    if request.method=='POST':
        code = request.POST['code']
        password = request.POST['pass1']
        conf_password = request.POST['pass2']
        secured_password = make_password(password)
        library = Library.objects.get(id=idlib)
        url = f'/new_password/{library.id}'

        if len(password)<8:
            messages.error(request,"Le mot de passe doit contenir au moins 8 caractères")
            return redirect(url)

        if str(password).isnumeric():
            messages.error(request,'Le mot de passe doit contenir des chiffres et des lettres')
            return redirect(url)

        if password!=conf_password:
            messages.error(request,"Le mot de passe ne correspond pas au mot de passe de confirmation!")
            return redirect(url)
        if code in session:
            if library is not None:
                library.password = secured_password
                library.save()
                return redirect('Signin')
        else:
                messages.error(request,"Le code de récupération est erroné!")
                return redirect(url)
                
            
    return render(request,'recuperer.html')
    

##Import export ##

def importCSV(request,idlib):
    if active[0][1]==True:
        if request.method == 'POST' and request.FILES['file']:
            csvfile = request.FILES['file']
            lines = csvfile.readlines()
            real_lines =[]
            for lin in lines:
                ligne = lin.strip()
                real_lines.append(ligne.decode("UTF-8"))
            
            lib = Library.objects.get(id=idlib)    
            
            try:
                if lib is not None:

                    for line in real_lines:
                        bloc = line.split(":")
                        
                        new_book = Livre(
                            Name_book = bloc[0],
                            Authour_name = bloc[1],
                            Genre = bloc[2],
                            Stock = bloc[3],
                            Id_lib=Library.objects.get(id=idlib),
                            Prix = bloc[4],
                            Image = bloc[5],


                        )
                        new_book.save()
                        print("kkkkkkkk")
                    return redirect('home')
            except Exception as e:
                print(e)
        return render(request,"import.html")
    else:
        messages.error(request, "Vous devez vous connectez.")
        return redirect('Signin')



def exportCSV(request,idlib):
    if active[0][1]==True:
        id=active[0][0]
        print(f"Le id hidden est: {active[0][0]}")
        Livres = Livre.objects.filter(Id_lib=idlib)
        f = open("exported/livres.csv",'w')
        for i in Livres:
            f.write(f"{i.Id_livre}:{i.Name_book}:{i.Authour_name}:{i.Genre}:{i.Stock}:{i.Prix}:{i.Image}"+"\n")
        f.close()

        file = open('exported/livres.csv',"rb")
        return FileResponse(file,
                    as_attachment=True,
                    filename="Livres.csv")
    else:
        messages.error(request, "Vous devez vous connectez.")
        return redirect('Signin')


##Import export ##











