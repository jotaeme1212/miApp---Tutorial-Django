from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from db.forms import IngresoForm, CambioPwdForm, TipoUsuarioForm, MenuForm, UsuarioForm, MenuTipoUsuarioForm
from db.models import Usuario, TipoUsuario, Menu, MenuTipoUsuario
from db.access import my_login_required, my_access_required
from django.forms.widgets import CheckboxSelectMultiple
import xlwt # Se instala desde el terminal con: sudo pip install xlwt

#------------------------------------ Opciones de Home --------------------------------

def index(request):
	return render_to_response('home/index.html', locals(), context_instance = RequestContext(request))

@my_login_required
def acerca_de(request):
	return render_to_response('home/acerca_de.html', locals(), context_instance = RequestContext(request))

def ingreso(request):
	# formulario - msg_no - ver_error - lista_err: se deben llamar asi, el include las referencian con ese nombre
	valido = False
	ver_error = False
	msg_no  = 'Ingreso no valido'
	lista_err = []

	if request.method == 'POST':
		formulario = IngresoForm(request.POST)
		valido = formulario.is_valid()
		if valido:
			usuario = formulario.cleaned_data['usuario']
			clave = formulario.cleaned_data['clave']
			usrLog = Usuario.objects.login_ok(usuario, clave)
			if usrLog != None:
				request.session['usuario'] = usrLog
				return HttpResponseRedirect('/index/')
			else:
				ver_error = True
		else:
			ver_error = True
			# Arma una lista con errores
			for field in formulario:
				for error in field.errors:
					lista_err.append(field.label + ': ' + error)
	else:
		formulario = IngresoForm()

	return render_to_response('home/ingreso.html', locals(), context_instance = RequestContext(request))

@my_login_required
def cambio_clave(request):
	# formulario - msg_no - ver_error - lista_err: se deben llamar asi, el include las referencian con ese nombre
	valido = False
	ver_error = False
	msg_no = 'Cambio de clave no valido'
	lista_err = []

	if request.method == 'POST':
		formulario = CambioPwdForm(request.POST)
		valido = formulario.is_valid()
		if valido:
			actual = formulario.cleaned_data['actual']
			nueva = formulario.cleaned_data['nueva']
			repetida = formulario.cleaned_data['repetida']
			cambio = Usuario.objects.cambiar_clave(request.session['usuario'].id, actual, nueva)
			if cambio: return HttpResponseRedirect('/index/')
			else: ver_error = True
		else:
			ver_error = True
			# Arma una lista con errores
			for field in formulario:
				for error in field.errors:
					lista_err.append(field.label + ': ' + error)
	else:
		formulario = CambioPwdForm()

	return render_to_response('home/cambio_clave.html', locals(), context_instance = RequestContext(request))

@my_login_required
def salir(request):
	del request.session['usuario']
	return HttpResponseRedirect('/index/')

#------------------------------------ Vistas de errores de acceso y validacion --------------------------

def acceso_denegado(request):
	return render_to_response('home/acceso_denegado.html', context_instance = RequestContext(request))

def csrf_rejected(request, reason = ''):
	contexto = {'reason' : reason}
	return render_to_response('home/csrf.html', contexto)

#------------------------------------ Vistas de Tipo de Usuarios --------------------------

@my_access_required
def tipo_usuarios_index(request):
	lista = TipoUsuario.objects.todos()
	return render_to_response('tipo_usuarios/index.html', locals(), context_instance = RequestContext(request))

def tipo_usuarios_edit(request, registro):
	# formulario - msg_no - ver_error - lista_err: se deben llamar asi, el include las referencian con ese nombre
	valido = False
	ver_error = False
	msg_ok = 'Operacion Exitosa'
	msg_no = 'No se pudo realizar la operacion'
	lista_err = []

	try:
		tusuario = TipoUsuario.objects.get(id = registro)
	except:
		tusuario = TipoUsuario()

	if request.method == 'POST':
		formulario = TipoUsuarioForm(request.POST, instance = tusuario)
		valido = formulario.is_valid()
		if valido:
			formulario.save()
			nombre = formulario.cleaned_data['nombre']
		else:
			ver_error = True
			# Arma una lista con errores
			for field in formulario:
				for error in field.errors:
					lista_err.append(field.label + ': ' + error)
	else:
		formulario = TipoUsuarioForm(instance = tusuario)

	# locals() es un diccionario con todas las variables locales y sus valores
	return render_to_response('tipo_usuarios/edit.html', locals(), context_instance = RequestContext(request))

def tipo_usuarios_delete(request, registro):
	tusuario = TipoUsuario.objects.get(id = registro)
	tusuario.delete()
	return HttpResponseRedirect('/tipo_usuarios/')

def tipo_usuarios_excel(request):
	response = HttpResponse(mimetype = 'application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename=file.xls'

	# Formatos estandar, de fecha y fecha hora
	default_style = xlwt.Style.default_style
	datetime_style = xlwt.easyxf(num_format_str = 'dd/mm/yyyy hh:mm')
	date_style = xlwt.easyxf(num_format_str = 'dd/mm/yyyy')

	# Crea el archivo excel y la hoja para los datos
	wb = xlwt.Workbook()
	ws = wb.add_sheet('Hoja1')

	# Columnas del encabezado
	ws.write(0, 0, 'ID')
	ws.write(0, 1, 'Nombre')
	ws.write(0, 2, 'Creado')
	ws.write(0, 3, 'Modificado')

	# Registros
	lista = TipoUsuario.objects.todos()
	fila = 0
	for registro in lista:
		# Para saber el tipo de un valor hacer: if isinstance(val, datetime):
		fila = fila + 1
		ws.write(fila, 0, registro.id, style = default_style)
		ws.write(fila, 1, registro.nombre, style = default_style)
		ws.write(fila, 2, registro.created, style = datetime_style)
		ws.write(fila, 3, registro.updated, style = date_style)

	wb.save(response)
	return response

#------------------------------------ Vistas de Menu --------------------------

@my_access_required
def menu_index(request):
	lista = Menu.objects.todos()
	return render_to_response('menu/index.html', locals(), context_instance = RequestContext(request))

def menu_edit(request, registro):
	# formulario - msg_no - ver_error - lista_err: se deben llamar asi, el include las referencian con ese nombre
	valido = False
	ver_error = False
	msg_ok = 'Operacion Exitosa'
	msg_no = 'No se pudo realizar la operacion'
	lista_err = []

	# Redefine el campo ManyToMany (por defecto lista multiple) a lista de checkbox
	MenuForm.base_fields['tipousuarios'].widget = CheckboxSelectMultiple(choices=MenuForm.base_fields['tipousuarios'].choices)

	try:
		menu = Menu.objects.get(id = registro)
	except:
		menu = Menu()

	if request.method == 'POST':
		formulario = MenuForm(request.POST, instance = menu)
		valido = formulario.is_valid()
		if valido:
			formulario.save()
			nombre = formulario.cleaned_data['nombre']
		else:
			ver_error = True
			# Arma una lista con errores
			for field in formulario:
				for error in field.errors:
					lista_err.append(field.label + ': ' + error)
	else:
		formulario = MenuForm(instance = menu)

	# locals() es un diccionario con todas las variables locales y sus valores
	return render_to_response('menu/edit.html', locals(), context_instance = RequestContext(request))

def menu_delete(request, registro):
	menu = Menu.objects.get(id = registro)
	menu.delete()
	return HttpResponseRedirect('/menu/')

#------------------------------------ Vistas de Accesos --------------------------

@my_access_required
def menu_tipo_usuarios_index(request):
	lista = MenuTipoUsuario.objects.todos()
	return render_to_response('menu_tipo_usuarios/index.html', locals(), context_instance = RequestContext(request))

def menu_tipo_usuarios_edit(request, registro):
	# formulario - msg_no - ver_error - lista_err: se deben llamar asi, el include las referencian con ese nombre
	valido = False
	ver_error = False
	msg_ok = 'Operacion Exitosa'
	msg_no = 'No se pudo realizar la operacion'
	lista_err = []

	try:
		acc = MenuTipoUsuario.objects.get(id = registro)
	except:
		acc = MenuTipoUsuario()

	if request.method == 'POST':
		formulario = MenuTipoUsuarioForm(request.POST, instance = acc)
		valido = formulario.is_valid()
		if valido:
			formulario.save()
			nombre = str(formulario.cleaned_data['tipousuario']) + ' - ' + str(formulario.cleaned_data['menu'])
		else:
			ver_error = True
			# Arma una lista con errores
			for field in formulario:
				for error in field.errors:
					lista_err.append(field.label + ': ' + error)
	else:
		formulario = MenuTipoUsuarioForm(instance = acc)

	# locals() es un diccionario con todas las variables locales y sus valores
	return render_to_response('menu_tipo_usuarios/edit.html', locals(), context_instance = RequestContext(request))

def menu_tipo_usuarios_delete(request, registro):
	acc = MenuTipoUsuario.objects.get(id = registro)
	acc.delete()
	return HttpResponseRedirect('/menu_tipo_usuarios/')

#------------------------------------ Vistas de Usuarios --------------------------

@my_access_required
def usuarios_index(request):
	lista = Usuario.objects.todos()
	return render_to_response('usuarios/index.html', locals(), context_instance = RequestContext(request))

def usuarios_edit(request, registro):
	# formulario - msg_no - ver_error - lista_err: se deben llamar asi, el include las referencian con ese nombre
	valido = False
	ver_error = False
	msg_ok = 'Operacion Exitosa'
	msg_no = 'No se pudo realizar la operacion'
	lista_err = []

	try:
		usuario = Usuario.objects.get(id = registro)
	except:
		usuario = Usuario()

	if request.method == 'POST':
		formulario = UsuarioForm(request.POST, instance = usuario)
		valido = formulario.is_valid()
		if valido:
			formulario.save()
			nombre = formulario.cleaned_data['nombre']
		else:
			ver_error = True
			# Arma una lista con errores
			for field in formulario:
				for error in field.errors:
					lista_err.append(field.label + ': ' + error)
	else:
		formulario = UsuarioForm(instance = usuario)

	# locals() es un diccionario con todas las variables locales y sus valores
	return render_to_response('usuarios/edit.html', locals(), context_instance = RequestContext(request))

def usuarios_delete(request, registro):
	usuario = Usuario.objects.get(id = registro)
	usuario.delete()
	return HttpResponseRedirect('/usuarios/')
