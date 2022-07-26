from core.models import Produto, CompareProduto, ContadorLoja
from core.api.filters import ProdutoFilterSet
from .serializers import (
    ProdutoSerializer, 
    CompareProdutoListSerializer, 
    CompareProdutoSerializer, 
    PromocaoLojaSerializer,
    ComparacaoSerializer, 
    ConcorrenciaLojaSerializer,
    MarcaSerializer,
    LojaSerializer,
)
from rest_framework.decorators import action
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from django.db.models import Count
from rest_framework.pagination import PageNumberPagination

class ProdutoViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):

    
    paginator = PageNumberPagination()
    paginator.page_size = 40
    queryset = Produto.objects.all().order_by('-promocao')
    serializer_class = ProdutoSerializer
    filter_class = ProdutoFilterSet

    @action(detail=False, methods=['GET'], url_path="marcas", url_name="marcas-produto")
    def produto(self, request):
        queryset = Produto.objects.values('marca').annotate(total=Count('marca')). order_by('marca')

        serializer = MarcaSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'], url_path="lojas", url_name="lojas-produto")
    def produto_lojas(self, request):
        queryset = Produto.objects.values('loja').annotate(total=Count('loja')). order_by('loja')

        serializer = LojaSerializer(queryset, many=True)
        return Response(serializer.data)

class CompareProdutoViewSet(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    serializer_class = CompareProdutoSerializer

    def get_queryset(self):
        if self.request.session.get('lista') is None:
            self.request.session['lista'] = {}

        self.compare_list = self.request.session['lista']
        self.session = self.request.session

        if 'session_key' in self.request.GET:
            sessao = self.request.GET['session_key']  
            session_key = sessao
        else:
            session_key = self.request.session.session_key

        if 'produto_id' in self.request.GET and 'session_key' in self.request.GET:
            produto = self.request.GET['produto_id']
            queryset = CompareProduto.objects.filter(produto_id=produto, session_key=session_key)  
        else:
            queryset = CompareProduto.objects.filter(session_key=session_key)
            
        return queryset

    def get_serializer_class(self):
        serializer_map = {
            "update": CompareProdutoSerializer,
            "partial_update": CompareProdutoSerializer,
            "create": CompareProdutoSerializer,
            "list": CompareProdutoListSerializer,
            "retrieve": CompareProdutoListSerializer
        }
        return serializer_map.get(self.action, super().get_serializer_class())
    
    def create(self, request, *args, **kwargs):
        
        data = request.data.copy()
        produto = data['produto']

        queryset = Produto.objects.get(pk=produto)
        preco_produto = queryset.preco_original
        preco_promocional = queryset.preco_promocional
        loja = queryset.loja

        if preco_promocional != 0:
            preco_produto = preco_promocional
            promocao = True
        else:
            preco_produto = preco_produto
            promocao = False 

        if data['session_key']:
            session_key = data['session_key']
        else:
            session_key = self.request.session.session_key

        data['session_key'] = session_key
        data['preco_produto'] = preco_produto
        data['promocao'] = promocao
        data['loja'] = loja

        serializer = CompareProdutoSerializer(data=data) 
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, *args, **kwargs):
        data = request.data.copy()

        instance = CompareProduto.objects.get(pk=kwargs['pk'])
        data['preco_produto'] = data['preco_produto']
        data['promocao'] = data['promocao']
        serializer = CompareProdutoSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
		

    @action(detail=False, methods=['DELETE'], url_path="produto/(?P<produto_id>[^/.]+)", url_name="compare-produto")
    def produto(self, request, produto_id):
        data = request.data.copy()
        
        try:
            session_key = data['session_key']
        except:
            session_key = self.request.session.session_key

        instance = CompareProduto.objects.get(produto_id=produto_id, session_key=session_key)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PromocaoLojaViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):

    serializer_class = PromocaoLojaSerializer
    
    def get_queryset(self):
        queryset = Produto.objects.values('loja').filter(promocao=True).order_by().annotate(quantidade_promo=Count('loja'))
        return queryset


class ComparacaoViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = ComparacaoSerializer

    def get_queryset(self):

        if 'session_key' in self.request.GET:
            session_key = self.request.GET['session_key']
        else:
            session_key = self.request.session.session_key
        queryset = CompareProduto.objects.raw(
            f'''select loja, MIN(preco_produto) OVER (PARTITION BY preco_produto), promocao, produto_id, id
            from core_compareproduto
            where session_key = '{session_key}'
            order by promocao asc limit 1'''
            )
        CompareProduto.objects.filter(session_key=session_key).update(comparado=True)
        try:
            for dado in queryset: dado.loja
            ConcorrenciaLojaViewSet.contador_loja(dado.loja)
            self.request.session.flush()
        except:
            return queryset
        return queryset 

class ConcorrenciaLojaViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):

    queryset = ContadorLoja.objects.all().order_by('-qtd_vezes')
    serializer_class = ConcorrenciaLojaSerializer

    def contador_loja(loja):
        data = ContadorLoja.objects.filter(loja=loja).values('loja', 'qtd_vezes')

        if data.exists():
            qtd_vezes = data[0]['qtd_vezes'] + 1
            data.update(qtd_vezes=qtd_vezes)
        else:
            ContadorLoja.objects.create(loja=loja, qtd_vezes=1)