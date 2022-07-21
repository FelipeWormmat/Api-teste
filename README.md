# Instrução
O teste está hospedada no heroku, segue o link para acessarem( https://teste-dafitir.herokuapp.com/ )
e para consumir os endpoints da API( https://teste-dafitir.herokuapp.com/docs/ ).

No Frontend foi utilizado a ferramenta Django Template e na parte de BackEnd utilizei a APi com FastApi 
Python e Django Rest Framework.


Para rodar o projeto local, basta usar os comandos:

Primeiro criar um arquivo .env
Pode colocar conforme está aqui nessa instrução:

ANTES:

SECRET_KEY=123
DEBUG=TRUE

DEPOIS:

- `docker-compose build`

- `docker-compose up`