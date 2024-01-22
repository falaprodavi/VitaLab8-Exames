from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib import auth


# Create your views here.

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:                
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem')
            return redirect('/usuarios/cadastro')
        
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'A senha dever ser maior que 6 caracteres')
            return redirect('/usuarios/cadastro')
        
        user = User.objects.filter(username=username)
        
        if user.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um usuário com o mesmo username')
            return redirect('/usuarios/cadastro')  
        
        try:
            # Username deve ser único!
            user = User.objects.create_user(
                first_name=primeiro_nome,
                last_name=ultimo_nome,
                username=username,
                email=email,
                password=senha,
            )
            messages.add_message(request, constants.SUCCESS, 'Cadastrado com sucesso')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/usuarios/cadastro')


        return redirect('/usuarios/cadastro')

def logar(request):    
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if user:
            login(request, user)
			# Acontecerá um erro ao redirecionar por enquanto, resolveremos nos próximos passos
            return redirect('/')
        else:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos')
            return redirect('/usuarios/login')
        
def logout(request) : 
    auth.logout(request)
    return redirect('/usuarios/login')
