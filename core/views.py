from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.generic import DetailView, ListView
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages
from django.conf import settings
import requests, json


def home(request):
    return render(request, "core/base.html")  


def produtos(request):
    filtro = ''
    marca = request.GET.get('marca')
    descricao = request.GET.get('descricao')
    loja = request.GET.get('loja')
    
    if request.session.get('lista') is None:
        request.session['lista'] = {}

    if request.method == 'GET':
        if descricao:  
            filtro += f'?&descricao={descricao}'
        if marca:
            marca = marca.replace(' ', '+')
            filtro += f'?&marca={marca}'
        if loja:
            filtro += f'?&loja={loja}'
        url = f'{url_base}{filtro}'
    else:
        url = f'{url_base}'
    response = requests.get(url)
    data = response.json()['results']

    response_marcas = requests.get(url_marcas)
    data_marcas = response_marcas.json()

    response_lojas = requests.get(url_lojas)
    data_lojas = response_lojas.json()

    return render(request, "core/list_produto.html", {"produto_list": data, "data_marcas": data_marcas, "data_lojas": data_lojas})

def produto_compare(request, id):
    session_key = request.session.session_key
    data = {
        'produto': id,
        'session_key': session_key
    }

    session_key = request.session.session_key


    if len(response_prod.json()['results']) != 0:
        comparacao_id = response_prod.json()['results'][0]['id']
        preco_original = response_prod.json()['results'][0]['produto']['preco_original']
        preco_promocional = response_prod.json()['results'][0]['produto']['preco_promocional']

        if float(preco_promocional) > 0:
            preco_produto = preco_promocional
            promocao = True
        else: 
            preco_produto = preco_original
            promocao = False

        data = {
            'preco_produto': preco_produto,
            'promocao': promocao
        }

    if response.status_code == 201:
        messages.success(request, 'Produto adicionado com sucesso')
    else:
        messages.success(request, 'Produto atualizado com sucesso')

    return HttpResponseRedirect(reverse("core:compare"))

def compare(request):
    session_key = request.session.session_key
    data = response.json()
    return render(request, "core/comparacao.html", {"produto_list": data['results']})

def comparacao(request):
    
    session_key = request.session.session_key
    data = response.json()
    request.session.flush()
    return render(request, "core/result_comparacao.html", {"produto_list": data['results']})

def concorrencia(request):

    data = response.json()['results']
    data_promo = promocao_response.json()['results']

    context = {}

    lojas = [obj['loja'] for obj in data]
    quantidade = [int(obj['qtd_vezes']) for obj in data]
    lojas_promo = [obj['loja'] for obj in data_promo]
    quantidade_promo = [int(obj['quantidade_promo']) for obj in data_promo]

    context = {
        'lojas': json.dumps(lojas),
        'quantidade': json.dumps(quantidade),
        'lojas_promo': json.dumps(lojas_promo),
        'quantidade_promo':json.dumps(quantidade_promo),
    }

    return render(request, "core/concorrencia.html", context)   

def remove(request, id):
    session_key = request.session.session_key
    data = {
        'produto': id,
        'session_key': session_key
    }

    if response.status_code == 204:
        messages.success(request, 'Produto deletado com sucesso')
    else:
        messages.error(request, 'Error ao deletar')

    return HttpResponseRedirect(reverse("core:compare"))

  
     

