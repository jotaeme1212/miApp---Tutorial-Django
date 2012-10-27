from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'miSitio.views.home', name='home'),
    # url(r'^miSitio/', include('miSitio.foo.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^index/',     'accUsuarios.views.index',     name='home_index'),
    url(r'^acerca_de/', 'accUsuarios.views.acerca_de', name='home_acerca_de'),

    url(r'^ingreso/',         'accUsuarios.views.ingreso',         name='home_ingreso'),
    url(r'^cambio_clave/',    'accUsuarios.views.cambio_clave',    name='home_cambio_clave'),
    url(r'^salir/',           'accUsuarios.views.salir',           name='home_salir'),
    url(r'^acceso_denegado/', 'accUsuarios.views.acceso_denegado', name='home_acceso_denegado'),

    url(r'^tipo_usuarios/',              'accUsuarios.views.tipo_usuarios_index',  name='tipo_usuarios_index'),
    url(r'^tipo_usuarios_edit/(\d+)/',   'accUsuarios.views.tipo_usuarios_edit',   name='tipo_usuarios_edit'),
    url(r'^tipo_usuarios_delete/(\d+)/', 'accUsuarios.views.tipo_usuarios_delete', name='tipo_usuarios_delete'),
    url(r'^tipo_usuarios_excel/',        'accUsuarios.views.tipo_usuarios_excel',  name='tipo_usuarios_excel'),

    url(r'^menu/',              'accUsuarios.views.menu_index',  name='menu_index'),
    url(r'^menu_edit/(\d+)/',   'accUsuarios.views.menu_edit',   name='menu_edit'),
    url(r'^menu_delete/(\d+)/', 'accUsuarios.views.menu_delete', name='menu_delete'),

    url(r'^usuarios/',              'accUsuarios.views.usuarios_index',  name='usuarios_index'),
    url(r'^usuarios_edit/(\d+)/',   'accUsuarios.views.usuarios_edit',   name='usuarios_edit'),
    url(r'^usuarios_delete/(\d+)/', 'accUsuarios.views.usuarios_delete', name='usuarios_delete'),

    url(r'^menu_tipo_usuarios/',              'accUsuarios.views.menu_tipo_usuarios_index',  name='menu_tipo_usuarios_index'),
    url(r'^menu_tipo_usuarios_edit/(\d+)/',   'accUsuarios.views.menu_tipo_usuarios_edit',   name='menu_tipo_usuarios_edit'),
    url(r'^menu_tipo_usuarios_delete/(\d+)/', 'accUsuarios.views.menu_tipo_usuarios_delete', name='menu_tipo_usuarios_delete'),
)
