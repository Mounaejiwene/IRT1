##IMPORTS##
import random
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password,check_password
from .models import Library
from django.contrib.auth import login,logout
from django.core.mail import send_mail
from Library import settings
from django.contrib import messages
##IMPORTS##



signing_up = []
def erase_all():
    global signing_up
    signing_up=[]

    return None


def confirm_library(request):
    if request.method=='POST':
        code_value = request.POST['code']
        if code_value==str(signing_up[1]):
            signing_up[0].save()
            erase_all()
            messages.success(request,"Votre compte a été bien créé")
            return redirect('Signin')
        else:
            messages.error(request,"Le code est incorrect!")
            return redirect('Signup')
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
    code=''
   
    if request.method =='POST':
        name = request.POST['name']
        username = request.POST['username']
        email =request.POST['email']
        password = request.POST['password']
        secured_password = make_password(password)


        if Library.objects.filter(email=email):
            messages.error(request,"Cet email est enregisté")
            return redirect('Signup')
        if Library.objects.filter(username=username):
            messages.error(request,"Cet nom existe dejà")
            return redirect('Signup')
        
        if len(username)<4:
            messages.error(request,"Ce nom est trop court")
        if len(password)<8:
            messages.error(request,"Le mot de passe doit contenir au moins 8 caractères")
            return redirect('Signup')

        if not str(password).isalnum() and not is_thereDigit(str(password)):
            messages.error(request,'Le mot de passe doit contenir des chiffres et des lettres')
            return redirect('Signup')

        new_library = Library(
            name_lib = name,
            username=username,
            email = email,
            password = secured_password
        )

        code = generator(Alphanum_chars)


        signing_up.append(new_library)
        signing_up.append(code)
        message = f"""
            Merci de choisir notre plateforme \n 
            Nous voudrons verifier qu'il s'agit bien de vous
            \nVeuillez entrez le code de confirmation \n votre code de confirmation est le : {code}"""
        
        subject="Code de confirmation"
        from_email  = settings.EMAIL_HOST_USER
        to_list=[new_library.email]
        send_mail(subject,message,from_email,to_list,fail_silently=False)
        return redirect('confirm')
        
    return render (request,'Signup.html')


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
                return redirect('Home')
            else:
                messages.error(request,"La librairie n'existe pas ou mot de passe incorrect.")
                return redirect('Signin')
        else:
             messages.error(request,"La librairie n'existe pas ou mot de passe incorrect.")
             return redirect('Signin')
    return render(request,'Signin.html')





def home(request):
        try:
            if active[0][1]==True:
                librairie = Library.objects.get(id=active[0][0]).name_lib
                return render(request,'Homepage_idea.html',{'name':librairie})
        except:
            return HttpResponse("Connectez-vous d'abord!")
        return HttpResponse("Connectez-vous d'abord!")
    

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

        if not str(password).isalnum() and not is_thereDigit(str(password)):
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
    


