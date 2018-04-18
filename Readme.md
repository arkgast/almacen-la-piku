# Almacen La Piku

Sistema para manejo de inventario

https://almacen-la-piku.herokuapp.com

### Usuarios de prueba

**Administrador**
* usuario: admin
* contraseña: admin

**Secretaria**
* usuario: secretaria
* contraseña: secretaria

## Instalación
### Local

    $ git clone https://github.com/arkgast/almacen-la-piku
    $ cd almacen-la-piku
    $ virtualenv env --prompt=[almacen]
    $ pip install -r requirements.txt
    $ echo 'export DJANGO_SETTINGS_MODULE=almacen.settings_dev' >> env/bin/activate
    $ python manage.py migrate
    $ python manage.py createsuperuser # escribir usuario y contraseña
    $ python manage.py runserver 9000

> Nota: Borrar las últimas 5 líneas del archivo **requirements.txt** ya que esos requerimientos solo se usan en producción.

Ahora ir a http://localhost:9000

### Heroku

    $ git clone https://github.com/arkgast/almacen-la-piku
    $ cd almacen-la-piku
    $ heroku create nombre-de-la-url
    $ git push heroku master

> Nota: Es necesario tener instalado [heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)

## Caracteristicas

* Manejo de grupos
* Manejo de usuarios
* Manejo de proveedores
* Manejo de clientes
* Manejo de pedidos
* Manejo de devoluciones

## Licencia

MIT
