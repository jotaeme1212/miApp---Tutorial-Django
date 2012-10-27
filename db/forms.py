from django import forms
from db.models import TipoUsuario, Usuario, Menu, MenuTipoUsuario

#-------------------------- Formularios de ingreso, no tienen BD asociada --------------------------

class IngresoForm(forms.Form):
	usuario = forms.CharField(error_messages = {'required': 'Debe ingresar un usuario'})
	clave   = forms.CharField(widget = forms.PasswordInput(),
							  error_messages = {'required': 'Debe ingresar una clave'})

class CambioPwdForm(forms.Form):
	actual = forms.CharField(widget = forms.PasswordInput(),
							 error_messages = {'required': 'Debe ingresar la clave actual'})
	nueva = forms.CharField(widget = forms.PasswordInput(),
							error_messages = {'required': 'Debe ingresar la clave nueva'})
	repetida = forms.CharField(widget = forms.PasswordInput(),
							   error_messages = {'required': 'Debe ingresar la clave repetida'})

	# Las validaciones para campos son clean_<nombre_campo>
	# Si el metodo se llama clean es para todos los campos juntos

	def clean_repetida(self):
		nueva = self.cleaned_data.get('nueva')
		repetida = self.cleaned_data.get('repetida')
		if nueva != repetida:
			raise forms.ValidationError('Clave nueva y repetida deben ser iguales')
		return repetida

#-------------------------- Formularios para las tablas de la BD --------------------------

class TipoUsuarioForm(forms.ModelForm):
	class Meta:
		model = TipoUsuario

	def clean_nombre(self):
		nombre = self.cleaned_data.get('nombre')
		if len(nombre) < 3:
			raise forms.ValidationError('El nombre debe tener mas de 3 caracteres')
		return nombre

class UsuarioForm(forms.ModelForm):
	class Meta:
		model = Usuario

class MenuForm(forms.ModelForm):
	class Meta:
		model = Menu

class MenuTipoUsuarioForm(forms.ModelForm):
	class Meta:
		model = MenuTipoUsuario
