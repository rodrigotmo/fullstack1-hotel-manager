from urllib.parse import urlencode
from django.shortcuts import render
from clientes.models import Cliente
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ClienteForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def clientes(request):
    query = request.GET.get('busca', '')
    if query:
        clientes = Cliente.objects.filter(nome__icontains=query)
    else:
        clientes = Cliente.objects.all()
    return render(request, 'cliente/clientes.html', {'clientes': clientes, 'query': query})

@login_required
def ordenar_clientes(request, campo):
    query = request.GET.get('busca', '')
    if query:
        clientes = Cliente.objects.filter(nome__icontains=query)
    else:
        clientes = Cliente.objects.all()
    clientes = clientes.order_by(campo)
    return render(request, 'cliente/clientes.html', {'clientes': clientes, 'query': query})

@login_required
def cadastrar_cliente(request):
    reserva_flag = (request.GET.get('reserva') == 'true' or request.POST.get('reserva') == 'true')
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            if Cliente.objects.filter(documento=form.cleaned_data['documento']).exists():
                messages.error(request, 'Cliente já cadastrado.')
                return redirect('clientes')

            cliente = Cliente(
                documento=form.cleaned_data['documento'],
                nome=form.cleaned_data['nome'],
                telefone=form.cleaned_data['telefone'],
                endereco=form.cleaned_data['endereco'],
            )
            cliente.save()
            messages.success(request, 'Cliente cadastrado com sucesso.')
            
            if reserva_flag:
                return redirect(reverse('reserva_inicial') + '?' + urlencode({'cliente_id': cliente.id}))
            else:
                return redirect('clientes')
            
    else:
        form = ClienteForm()

    return render(request, 'cliente/cadastro.html', {'form': form})

@login_required
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            documento = form.cleaned_data['documento']
            if Cliente.objects.exclude(id=id).filter(documento=documento).exists():
                messages.error(request, 'Cliente já cadastrado.')
                return redirect('editar_cliente', id=id)

            cliente.nome = form.cleaned_data['nome']
            cliente.documento = documento
            cliente.telefone = form.cleaned_data['telefone']
            cliente.endereco = form.cleaned_data['endereco']
            cliente.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('clientes')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'cliente/cadastro.html', {'form': form, 'cliente': cliente})

@login_required
def desativar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.ativo = False
    cliente.save()
    messages.success(request, "Cliente desativado com sucesso!")
    return redirect('clientes')

@login_required
def ativar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.ativo = True
    cliente.save()
    messages.success(request, "Cliente ativado com sucesso!")
    return redirect('clientes')

