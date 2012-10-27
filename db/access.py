from django.http import HttpResponseRedirect
from db.models import Menu

# Define si tiene acceso controlando solamente el login
def my_login_required(f):

	def wrap(request, *args, **kwargs):
		if 'usuario' not in request.session:
			return HttpResponseRedirect('/acceso_denegado/')
		return f(request, *args, **kwargs)

	wrap.__doc__ = f.__doc__
	wrap.__name__ = f.__name__
	return wrap

# Define si tiene acceso controlando login y acceso por menu
def my_access_required(f):

	def wrap(request, *args, **kwargs):

		# Para tener acceso por menu siempre hay que estar logueado
		if 'usuario' not in request.session:
			return HttpResponseRedirect('/acceso_denegado/')

		# Esta logueado, controla acceso por menu
		tipo_usuario = request.session['usuario'].tipousuario.id
		accion = f.__name__

		try:
			menu = Menu.objects.get(action = accion)
			menu.tipousuarios.get(id = tipo_usuario)
		except:
			return HttpResponseRedirect('/acceso_denegado/')

		return f(request, *args, **kwargs)

	wrap.__doc__ = f.__doc__
	wrap.__name__ = f.__name__
	return wrap
