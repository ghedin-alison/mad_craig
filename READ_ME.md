# Projeto South Park
**Exibe imagens dos personagens**

## Codificando:
Criar o projeto(southpark) e a venv

##### No terminal:
```unix 
pip install django
pip install djangorestframework
```
##### No terminal:
```unix 
django-admin startproject admin .
python manage.py runserver
```

### Docker
Criar na raiz do projeto Dockerfile e docker-compose.yml<br> 
##### No Dockefile:<br>
```unix
FROM python:3.9
ENV PYTHONBUFFERED 1
WORKDIR /app
```
##### No terminal:
```unix 
pip freeze requirements.txt
```
##### No Dockefile:
```unix
COPY requirements.txt /app/requirements.txt
COPY . /app

CMD python manage.py runserver 0.0.0.0:8000
```

##### No docker-compose.yml
Apontar a versão do docker-compose e onde está o Dockerfile(context e dockerfile) que será utilizado
```unix
version: '3.8'
services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile
```
No mesmo nivel de build especificar 
 - A porta do localhost e do dockerfile
 - Volumes(mudanças ocorridas no dockerfile, refletem no projeto e vice-versa)

```unix
    ports:
      - 8000:8000
    volumes:
      - .:/app
```

### Rodar o projeto no container
Se o projeto ainda estiver rodando, CTRL + C no terminal

No terminal, dentro diretório que tem o docker-compose(raiz):
```unix
sudo docker-compose up
```
Se o docker compose não estiver instalado, seguir o link:<br>
[docker-compose](https://docs.docker.com/compose/install/)

*Acessar novamente a localhost na porta 8000 e já é possível ver o projeto rodando com o docker*
*É possivel parar o container e dar um restart com "sudo docker-compose up"*

### Conectar com database
Remover "db.sqlite3" para utilizar mysql via docker

##### No docker-compose.yml
No mesmo vível de backend:
 - Criar a imagem da versão do mysql
 - Criar variaveis e password para o banco de dados
 - Criar o volume, diretorio do banco de dados
 - Apontar para uma porta que não esteja conflitando com uma instalação na maquina
```unix
  db:
    image: mysql:5.7.22
    restart: always
    environment:
      MYSQL_DATABASE: admin
      MYSQL_USER: root
      MYSQL_PASSWORD: root
      MYSQL_ROOT_PASSWORD: root
    volumes:
      - .dbdata:/var/lib/mysql
    ports:
      - 33066:3306
```
##### No docker-compose.yml
Dentro de backend, adicionar uma dependência do banco de dados:
```unix
 - depends_on:
      - db
```

*Parar e reiniciar o docker-compose*

*Instalar o DBeaver para gerenciar os bancos de dados*

### Adicionar tabelas ao banco de dados

Entrar no container
##### No terminal
```unix
 docker-compose exec backend sh
 python manage.py startapp pictures
```
Com isso temos o diretorio do app pictures criado no projeto.
Possui a estrutura básica de um app django com models, tests, views, etc

##### No diretório admin
Adicionar o projeto criado nas configurações(settings) do admin:
```unix
INSTALLED_APPS = [...
    'rest_framework',
    'corsheadears',
    'pictures'
]
MIDDLEWARE = [...
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheadears.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
...
]

...

CORS_ORIGIN_ALLOW_ALL = True

...

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'admin',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'db',
        'PORT': '3306',
    }
}

```

Agora vamos começar a alterar as models pra criar tabelas.

*Se houver problemas para alteração dos arquivos no pycharm:*<br>
Ao tentar alterar arquivos estava retornando a mensagem "Clear Read-only Status"
Pra resolver, executar no terminal que tem a instancia do docker aberta:
```unix
chmod -R 777 ./
```

Criar as classes

##### No terminal, instancia do docker
```unix
 python manage.py makemigrations
 python manage.py migrate
```
Agora o banco de dados está funcionando no DBeaver

### Serializers
Dentro do diretório do app pictures criar serializers.py
```python
from rest_framework import serializers
from .models import Pictures


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pictures
        fields = '__all__'
```

No arquivo views.py
```python
from rest_framework import viewsets

# Create your views here.
class PicturesViewSet(viewsets.ViewSet):
    def list(self, request):  # /api/pictures(get request)
        pass

    def create(self, request):  # /api/pictures(post request)
        pass

    def retrieve(self, request, pk=None):  # /api/pictures/<str:id>
        pass

    def update(self, request, pk=None):  # /api/pictures/<str:id>
        pass

    def delete(self, request, pk=None):  # /api/pictures/<str:id>
        pass

```

Criar o arquivo urls.py no diretorio do app<br>
Copiar o urls.py do admin

```python
from django.urls import path
from .views import PicturesViewSet

urlpatterns = [
    path('pictures', PicturesViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('pictures/<str:pk>', PicturesViewSet.as_view({
        'get': 'retrieve',
        'post': 'update',
        'delete': 'destroy',
    })),
]
```


No urls.py do admin incluir o path do projeto:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('pictures.urls')),
]

```

Nesse ponto já é possível testar no postman: <br>
Dar um get http://localhost:8000/api/pictures <br>
Não há retorno de informações ainda pq não carregamos as bases <br>

Adicionando mais funções ao views.py

```python
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Pictures
from .serializers import PictureSerializer


# Create your views here.
class PicturesViewSet(viewsets.ViewSet):
    def list(self, request):  # /api/pictures(get request)
        pictures = Pictures.objects.all()
        serializer = PictureSerializer(pictures, many=True)
        return Response(serializer.data)

    def create(self, request):  # /api/pictures(post request)
        serializer = PictureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):  # /api/pictures/<str:id>
        pass

    def update(self, request, pk=None):  # /api/pictures/<str:id>
        pass

    def destroy(self, request, pk=None):  # /api/pictures/<str:id>
        pass

```

Agora é possível testar o post e o get em sequencia no postman <br>

Adicionada a classe User, tanto na view como em url.<br>

Versao subiu para o github.


