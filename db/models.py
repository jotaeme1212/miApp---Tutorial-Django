from django.db import models
from django.core.exceptions import ValidationError

from db.managers import TipoUsuarioManager, UsuarioManager, MenuManager, MenuTipoUsuarioManager

# ---------------------------------------------------------------------

# ------------ Modelo Tipo Usuario ------------
			
class TipoUsuario(models.Model):

    def validate_vacio_nulo(valor):
        if (valor == '') or (valor == None) or (len(valor) < 3):
            raise ValidationError(u'%s no se puede' % valor)

    nombre     = models.CharField(max_length=100, validators = [validate_vacio_nulo])
    created    = models.DateTimeField(auto_now_add = True) # Usar datetime.date.today() - import datetime
    updated    = models.DateTimeField(auto_now = True)

    objects = TipoUsuarioManager() # Para usar managers

    def __unicode__(self):
        return u'%s' % (self.nombre)

# ---------------------------------------------------------------------

# ------------ Modelo Usuario ------------

class Usuario(models.Model):
    tipousuario = models.ForeignKey(TipoUsuario)
    nombre      = models.CharField(max_length=100)
    login       = models.CharField(max_length=100)
    clave       = models.CharField(max_length=100)
    email       = models.EmailField()
    created     = models.DateTimeField(auto_now_add = True) # Usar datetime.date.today() - import datetime
    updated     = models.DateTimeField(auto_now = True)

    objects = UsuarioManager() # Para usar managers

    def __unicode__(self):
        return u'%s - %s' % (self.login, self.nombre)

    # La clase Meta interna es para especificar metadatos adicionales de un modelo
    class Meta:
        ordering = ['tipousuario', 'nombre']

# ---------------------------------------------------------------------

# ------------ Modelo Menu ------------

class Menu(models.Model):
    nombre     = models.CharField(max_length=100)
    url        = models.CharField(max_length=100, blank=True, null=True)
    action     = models.CharField(max_length=100, blank=True, null=True)
    icono      = models.CharField(max_length=100, blank=True, null=True)
    padre      = models.IntegerField()
    orden      = models.IntegerField()
    created    = models.DateTimeField(auto_now_add = True) # Usar datetime.date.today() - import datetime
    updated    = models.DateTimeField(auto_now = True)
    tipousuarios = models.ManyToManyField(TipoUsuario, blank=True, null=True)

    objects = MenuManager() # Para usar managers

    def __unicode__(self):
        return u'%s' % (self.nombre)

    # La clase Meta interna es para especificar metadatos adicionales de un modelo
    class Meta:
        ordering = ['padre', 'orden']

# ---------------------------------------------------------------------

# ------------ Modelo Menu Usuario Tipo ------------
# Este modelo no era necesario, pero lo creo (accediendo a la tabla) para poder usar
# el matenimiento de accesos (y no solamente entrar por el menu a crear los accesos)

class MenuTipoUsuario(models.Model):
    menu        = models.ForeignKey(Menu)
    tipousuario = models.ForeignKey(TipoUsuario)

    objects = MenuTipoUsuarioManager() # Para usar managers

    class Meta:
        db_table = u'db_menu_tipousuarios' # Esto si queremos usar nombres propios y no los de Django
        ordering = ['tipousuario', 'menu']
