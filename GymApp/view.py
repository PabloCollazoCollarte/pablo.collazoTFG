#! /usr/bin/python3
# -*- coding: utf-8 -*-

import gi
import os
from datetime import date
import base64
import numpy as np
from gi.repository import Gio
from gi.repository import GdkPixbuf
from PIL import Image
import matplotlib
matplotlib.use('GTK3Agg')
import matplotlib.pyplot as plotter
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
gi.require_version('GdkX11', '3.0')
from gi.repository import GdkX11
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class View:
	def __init__(self):

		Titulo = Gtk.Image.new_from_file("./Titulo.png")

		Aceptarbox = Gtk.ButtonBox.new(Gtk.Orientation.HORIZONTAL)
		Aceptar = Gtk.Button(label= "Comenzar >")
		self.Aceptar=Aceptar   
		self.Aceptar.set_sensitive(True)
		Aceptarbox.add(self.Aceptar)     #boton Aceptar con su buttonBox

		grupo = Gtk.Grid(margin=30, column_spacing=10, row_spacing=10)
		grupo.attach(Titulo, 20, 0, 1, 1)
		grupo.attach(Aceptarbox, 20, 40, 1, 1)

		win = Gtk.Window(title=("GymApp"))  #ventana
		win.set_default_size(100,10)
		win.set_icon_from_file("./Titulo.png")
		win.add(grupo)
		win.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
		win.connect('delete-event', Gtk.main_quit)
		#win.add(encaje)
		win.show_all()
		self.win=win

	def aviso(self, controller):
		self.Aceptar.connect('clicked', controller.on_iniciar)

###################################################################################################################################################
###################################################################################################################################################

	def aplicar_filtro_aux(self, conjunto, iter, data): #Aplica el filtro en la lista creada para ello
			return True

	def inicio(self):
		win = self.win	#para borrar los atributos de la clase y ahorrar memoria
		self.__dict__.clear()
		self.win = win
		self.win.get_child().destroy() #destruimos ventana de inicio

		Ini = Gtk.ToggleButton(label=("Inicio"))
		self.Ini = Ini
		self.Ini.set_active(True)
		Programacion = Gtk.ToggleButton(label=("Programación"))
		self.Programacion = Programacion
		Grupos = Gtk.ToggleButton(label=("Grupos"))
		self.Grupos = Grupos
		Usuarios = Gtk.ToggleButton(label=("Usuarios"))
		self.Usuarios = Usuarios
		Sesiones = Gtk.ToggleButton(label=("Sesiones"))
		self.Sesiones = Sesiones
		Ejercicios = Gtk.ToggleButton(label=("Ejercicios"))
		self.Ejercicios = Ejercicios

		links = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=10)  #barra navegacion
		links.pack_start(self.Ini, False, False, 0)
		links.pack_start(self.Programacion, False, False, 0)
		links.pack_start(self.Grupos, False, False, 0)
		links.pack_start(self.Usuarios, False, False, 0)
		links.pack_start(self.Sesiones, False, False, 0)
		links.pack_start(self.Ejercicios, False, False, 0)

		l1 = Gtk.Label()
		l1.set_markup("<big><b>Inicio</b></big>")  #texto
		l2 = Gtk.Label("Bienvenido a GymApp.\nHaga click en una de las opciones de la barra\nde navegación para acceder.")
		l3 = Gtk.Label()
		l3.set_markup("<i>Grupos disponibles:</i>")
		l4 = Gtk.Label()
		l4.set_markup("<i>Próximas sesiones programadas:</i>")

		liststore = Gtk.ListStore(str, str) #que contiene el filtro
		self.liststore = liststore

		filtro = liststore.filter_new() #Hace un filtrado de liststore. Crea otro liststore para aplicar el filtro
		self.filtro = filtro
		filtro.set_visible_func(self.aplicar_filtro_aux) #Filtra el liststore nuevo según lo que indique la función


		grupos = Gtk.TreeView(filtro, headers_visible=True) #Lista grupos

		#Crear columna 1
		renderer_text = Gtk.CellRendererText()

		column_text1 = Gtk.TreeViewColumn(("Grupo"), renderer_text, text=0)

		#Crear columna 2
		renderer_text2 = Gtk.CellRendererText()
		column_text2 = Gtk.TreeViewColumn(("Horario"), renderer_text2, text=1)

		grupos.append_column(column_text1)
		grupos.append_column(column_text2)

		self.grupos = grupos

		ventana_scroll = Gtk.ScrolledWindow(expand=True, margin=20)
		ventana_scroll.set_size_request(400, 100)
		ventana_scroll.add(grupos)

		liststore2 = Gtk.ListStore(str, str, str, str, str) #que contiene el filtro
		self.liststore2 = liststore2

		filtro2 = liststore2.filter_new() #Hace un filtrado de liststore. Crea otro liststore para aplicar el filtro
		self.filtro2 = filtro2
		filtro2.set_visible_func(self.aplicar_filtro_aux) #Filtra el liststore nuevo según lo que indique la función


		sesiones = Gtk.TreeView(filtro2, headers_visible=True) #Lista grupos

		#Crear columna x
		renderer_textx = Gtk.CellRendererText()

		column_textx = Gtk.TreeViewColumn(("Sesión programada"), renderer_textx, text=0)

		#Crear columna 1
		renderer_text1 = Gtk.CellRendererText()

		column_text1 = Gtk.TreeViewColumn(("Sesión"), renderer_text1, text=1)

		#Crear columna 2
		renderer_text2 = Gtk.CellRendererText()
		column_text2 = Gtk.TreeViewColumn(("Fecha"), renderer_text2, text=2)

		#Crear columna 3
		renderer_text3 = Gtk.CellRendererText()

		column_text3 = Gtk.TreeViewColumn(("Grupo"), renderer_text3, text=3)

		#Crear columna 4
		renderer_text4 = Gtk.CellRendererText()
		column_text4 = Gtk.TreeViewColumn(("Descripción"), renderer_text4, text=4)

		sesiones.append_column(column_textx)
		sesiones.append_column(column_text1)
		sesiones.append_column(column_text2)
		sesiones.append_column(column_text3)
		sesiones.append_column(column_text4)

		self.sesiones = sesiones

		ventana_scroll2 = Gtk.ScrolledWindow(expand=True, margin=20)
		ventana_scroll2.set_size_request(800, 300)
		ventana_scroll2.add(sesiones)


		inicio = Gtk.Grid(margin=0, column_spacing=10, row_spacing=10)  #colocacion de elementos anteriores
		inicio.attach(links, 0, 0, 1, 1)	
		inicio.attach_next_to(l1, links, Gtk.PositionType.BOTTOM, 1, 1)
		inicio.attach_next_to(l2, l1, Gtk.PositionType.BOTTOM, 1, 1)
		inicio.attach_next_to(l4, l2, Gtk.PositionType.BOTTOM, 1, 1)
		inicio.attach_next_to(ventana_scroll2, l4, Gtk.PositionType.BOTTOM, 2, 1)
		inicio.attach_next_to(l3, l1, Gtk.PositionType.RIGHT, 1, 1)
		inicio.attach_next_to(ventana_scroll, l3, Gtk.PositionType.BOTTOM, 1, 1)

		self.win.set_default_size(1000,500)
		self.win.add(inicio)
		self.win.show_all()

	def clickEnlaces(self, controller): 
		self.Ini.connect("toggled", controller.on_iniciar)
		self.Programacion.connect("toggled", controller.on_programacion)
		self.Grupos.connect("toggled", controller.on_grupos)
		self.Usuarios.connect("toggled", controller.on_usuarios)
		self.Sesiones.connect("toggled", controller.on_sesiones)
		self.Ejercicios.connect("toggled", controller.on_ejercicios)

###################################################################################################################################################
###################################################################################################################################################

	def usuarios(self):
		win = self.win	#para borrar los atributos de la clase y ahorrar memoria
		self.__dict__.clear()
		self.win = win
		self.win.resize(1000,550)
		self.win.get_child().destroy() #destruimos elemetos de inicio

		Ini = Gtk.ToggleButton(label=("Inicio"))
		self.Ini = Ini
		Programacion = Gtk.ToggleButton(label=("Programación"))
		self.Programacion = Programacion
		Grupos = Gtk.ToggleButton(label=("Grupos"))
		self.Grupos = Grupos
		Usuarios = Gtk.ToggleButton(label=("Usuarios"))
		self.Usuarios = Usuarios
		self.Usuarios.set_active(True)
		Sesiones = Gtk.ToggleButton(label=("Sesiones"))
		self.Sesiones = Sesiones
		Ejercicios = Gtk.ToggleButton(label=("Ejercicios"))
		self.Ejercicios = Ejercicios

		links = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=10)  #barra navegacion
		links.pack_start(self.Ini, False, False, 0)
		links.pack_start(self.Programacion, False, False, 0)
		links.pack_start(self.Grupos, False, False, 0)
		links.pack_start(self.Usuarios, False, False, 0)
		links.pack_start(self.Sesiones, False, False, 0)
		links.pack_start(self.Ejercicios, False, False, 0)

		l1 = Gtk.Label()
		l1.set_markup("<big><b>Usuarios</b></big>")  #texto

		liststoreUsuarios = Gtk.ListStore(str, str, str, str, str, str, str) #que contiene el filtro
		self.liststoreUsuarios = liststoreUsuarios

		filtroUsuarios = liststoreUsuarios.filter_new() #Hace un filtrado de liststore. Crea otro liststore para aplicar el filtro
		filtroUsuarios.set_visible_func(self.aplicar_filtro_usuarios) #Filtra el liststore nuevo según lo que indique la función
		self.filtroUsuarios = filtroUsuarios
		self.filtroUsuarios_inicio = ""

		busqueda = Gtk.SearchEntry(width_chars=8)
		self.busqueda = busqueda
		Etiq_busqueda = Gtk.Label(label = ("Filtrar por Apellidos/Nombre/Email:"))   #entrada para filtrar

		BusquedaUsers = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		BusquedaUsers.pack_start(Etiq_busqueda, False, False, 0)
		BusquedaUsers.pack_start(self.busqueda, True, True, 0)

		users = Gtk.TreeView(filtroUsuarios, headers_visible=True) #Lista grupos

		#Crear columna x
		renderer_textx = Gtk.CellRendererText()
		column_textx = Gtk.TreeViewColumn(("id"), renderer_textx, text=0)

		#Crear columna 0
		renderer_text = Gtk.CellRendererText()
		column_text0 = Gtk.TreeViewColumn(("Apellidos"), renderer_text, text=1)

		#Crear columna 1
		renderer_text1 = Gtk.CellRendererText()
		column_text1 = Gtk.TreeViewColumn(("Nombre"), renderer_text1, text=2)

		#Crear columna 2
		renderer_text2 = Gtk.CellRendererText()
		column_text2 = Gtk.TreeViewColumn(("DNI"), renderer_text2, text=3)

		#Crear columna 3
		renderer_text3 = Gtk.CellRendererText()
		column_text3 = Gtk.TreeViewColumn(("Teléfono"), renderer_text3, text=4)

		#Crear columna 4
		renderer_text4 = Gtk.CellRendererText()
		column_text4 = Gtk.TreeViewColumn(("Correo electrónico"), renderer_text4, text=5)

		#Crear columna 5
		renderer_text5 = Gtk.CellRendererText()
		column_text5 = Gtk.TreeViewColumn(("Activo"), renderer_text5, text=6)

		users.append_column(column_textx)
		users.append_column(column_text0)
		users.append_column(column_text1)
		users.append_column(column_text2)
		users.append_column(column_text3)
		users.append_column(column_text4)
		users.append_column(column_text5)

		self.users = users

		ventana_scroll = Gtk.ScrolledWindow(expand=True, margin=20)
		ventana_scroll.set_size_request(400, 100)
		ventana_scroll.add(users)

		VerMod = Gtk.Button(label=("Ver/Modificar"))
		self.VerMod = VerMod
		deportivo = Gtk.Button(label=("Hist. deportivo y estadísticas"))
		self.deportivo = deportivo
		Eliminar = Gtk.Button(label=("Eliminar"))
		self.Eliminar = Eliminar
		Activar = Gtk.Button(label=("Activar/desactivar usuario"))
		self.Activar = Activar

		botones = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=12)  #botones para utilizar con usuarios
		botones.pack_start(self.VerMod, False, False, 0)
		botones.pack_start(self.deportivo, False, False, 0)
		botones.pack_start(self.Eliminar, False, False, 0)
		botones.pack_start(self.Activar, False, False, 0)

		UserNuevo = Gtk.Button()
		self.UserNuevo = UserNuevo
		image = Gtk.Image.new_from_file("./add.svg")
		self.UserNuevo.add(image)

		usuariosGrid = Gtk.Grid(margin=5, column_spacing=5, row_spacing=10)  #colocacion de elementos anteriores
		usuariosGrid.attach(links, 0, 0, 1, 1)
		usuariosGrid.attach_next_to(BusquedaUsers, links, Gtk.PositionType.BOTTOM, 1, 1)
		usuariosGrid.attach_next_to(l1, BusquedaUsers, Gtk.PositionType.BOTTOM, 1, 1)
		usuariosGrid.attach_next_to(ventana_scroll, l1, Gtk.PositionType.BOTTOM, 20, 10)
		usuariosGrid.attach_next_to(botones, ventana_scroll, Gtk.PositionType.BOTTOM, 1, 1)
		usuariosGrid.attach_next_to(UserNuevo, botones, Gtk.PositionType.RIGHT, 1, 1)

		self.VerMod.set_sensitive(False)
		self.deportivo.set_sensitive(False)
		self.Eliminar.set_sensitive(False)
		self.Activar.set_sensitive(False)
		self.UserNuevo.set_sensitive(True)

		self.win.add(usuariosGrid)
		self.win.show_all()

	def clickUsuarios(self, controller):
		self.UserNuevo.connect("clicked", controller.on_NuevoUser)
		self.users.get_selection().connect("changed", controller.activar_botones) #si seleccionas un usuario
		self.busqueda.connect('changed', self.filtro_cambiado)

	def clickSobreUsuarios(self, controller):
		self.VerMod.connect("clicked", controller.on_ActualizarUser)
		self.deportivo.connect("clicked", controller.on_deportivo)
		self.Eliminar.connect("clicked", controller.on_eliminar_user)
		self.Activar.connect("clicked", controller.on_activar_user)

	def aplicar_filtro_usuarios(self, conjunto, iter, data):
		if self.filtroUsuarios_inicio == "":	
			return True
		else:
			return (((conjunto[iter][1]).startswith(self.filtroUsuarios_inicio)) or ((conjunto[iter][2]).startswith(self.filtroUsuarios_inicio))
					or ((conjunto[iter][5]).startswith(self.filtroUsuarios_inicio))) #Filtrar por apellidos, nombre o email

	def filtro_cambiado(self, entrada):
		self.filtroUsuarios_inicio = entrada.get_text()
		self.users.get_model().refilter()  #esta funcion controla que se cambia el texto del filtro

	def deportivoVista(self, controller, iduser):
		win = self.win	#para borrar los atributos de la clase y ahorrar memoria
		self.__dict__.clear()
		self.win = win
		self.win.get_child().destroy() #destruimos ventana de inicio
		l1 = Gtk.Label()
		l1.set_markup("<b>Evolución de peso</b>")  #texto
		boxgrafica = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.boxgrafica = boxgrafica
		
		l2 = Gtk.Label()
		l2.set_markup("<b>Historial de sesiones</b>")  #texto		

		liststoreSesionesUser = Gtk.ListStore(str, str, str, str) #que contiene el filtro
		self.liststoreSesionesUser = liststoreSesionesUser

		filtroSesionesUsuarios = liststoreSesionesUser.filter_new() #Hace un filtrado de liststore. Crea otro liststore para aplicar el filtro
		filtroSesionesUsuarios.set_visible_func(self.aplicar_filtro_sesionesusuarios) #Filtra el liststore nuevo según lo que indique la función
		self.filtroSesionesUsuarios = filtroSesionesUsuarios
		self.filtroSesionesUsuarios_inicio = ""

		busqueda = Gtk.SearchEntry(width_chars=25)
		busqueda.set_placeholder_text("Buscar por nº de sesión programada/fecha")
		busqueda = busqueda
		busqueda.connect('changed', self.filtro_cambiado_SesionUser)

		BusquedasesionesUsers = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)	
		BusquedasesionesUsers.pack_start(l2, True, True, 0)
		BusquedasesionesUsers.pack_start(busqueda, True, True, 0)


		sesionesusers = Gtk.TreeView(filtroSesionesUsuarios, headers_visible=True) #Lista grupos

		#Crear columna x
		renderer_textj = Gtk.CellRendererText()
		column_textj = Gtk.TreeViewColumn(("Id programada"), renderer_textj, text=0)

		#Crear columna x
		renderer_textx = Gtk.CellRendererText()
		column_textx = Gtk.TreeViewColumn(("Sesión"), renderer_textx, text=1)

		#Crear columna 0
		renderer_text = Gtk.CellRendererText()
		column_text0 = Gtk.TreeViewColumn(("Fecha"), renderer_text, text=2)

		#Crear columna 1
		renderer_text1 = Gtk.CellRendererText()
		column_text1 = Gtk.TreeViewColumn(("Valoración post-sesión"), renderer_text1, text=3)

		sesionesusers.append_column(column_textj)
		sesionesusers.append_column(column_textx)
		sesionesusers.append_column(column_text0)
		sesionesusers.append_column(column_text1)

		self.sesionesusers = sesionesusers

		ventana_scroll = Gtk.ScrolledWindow(expand=True, margin=20)
		ventana_scroll.set_size_request(400, 100)
		ventana_scroll.add(sesionesusers)

		postVal = Gtk.Button("Añadir post-valoración")
		self.postVal = postVal
		self.postVal.set_sensitive(False)

		self.sesionesusers.get_selection().connect("changed", controller.activar_botones_userSesion, iduser) #si seleccionas un usuario
		aceptadodeportivo = Gtk.Button("Aceptar")
		self.aceptadodeportivo = aceptadodeportivo
		self.aceptadodeportivo.connect("clicked", controller.on_aceptarDeportivo)

		SesUserGrid = Gtk.Grid(margin=20, column_spacing=10, row_spacing=10)  #colocacion de elementos anteriores
		SesUserGrid.attach(l1, 0, 0, 2, 5)
		SesUserGrid.attach_next_to(boxgrafica, l1, Gtk.PositionType.BOTTOM, 5, 20)
		SesUserGrid.attach_next_to(BusquedasesionesUsers, boxgrafica, Gtk.PositionType.BOTTOM, 5, 1)
		SesUserGrid.attach_next_to(ventana_scroll, BusquedasesionesUsers, Gtk.PositionType.BOTTOM, 8, 6)
		SesUserGrid.attach_next_to(postVal, ventana_scroll, Gtk.PositionType.BOTTOM, 1, 1)
		SesUserGrid.attach_next_to(aceptadodeportivo, postVal, Gtk.PositionType.RIGHT, 1, 1)
		self.SesUserGrid = SesUserGrid
		self.win.add(SesUserGrid)
		self.win.show_all()

	def clicksobreusers(self, controller, iduser):
		self.postVal.connect("clicked", controller.on_valpersonal, iduser, None, None)

	def aplicar_filtro_sesionesusuarios(self, conjunto, iter, data):
		if self.filtroSesionesUsuarios_inicio == "":	
			return True
		else:
			return (((conjunto[iter][0]).startswith(self.filtroSesionesUsuarios_inicio)) or ((conjunto[iter][1]).startswith(self.filtroSesionesUsuarios_inicio))) #Filtrar por apellidos, nombre o email

	def filtro_cambiado_SesionUser(self, entrada):
		self.filtroSesionesUsuarios_inicio = entrada.get_text()
		self.sesionesusers.get_model().refilter()  #esta funcion controla que se cambia el texto del filtro

	def MostrarGraficaPeso(self, pesos, fechas):
		figureObject, axesObject = plotter.subplots()
		if len(pesos) > 7:
			while len(pesos) > 7:
				pesos.pop(0)
				fechas.pop(0)

		axesObject.plot(fechas, pesos)
		self.axesObject = axesObject
		plotter.figure(figsize=(100,100))
		canvas = FigureCanvas(figureObject)
		self.boxgrafica.pack_start(canvas, True, True, 0)
		self.win.show_all()

	def valpersonalVista(self, sesion, ejerciciosnecesarios, controller, sesionid, userid, valores):
		dialogo = Gtk.Dialog("Detalle sesión " + sesion, self.win,Gtk.DialogFlags.MODAL|Gtk.DialogFlags.DESTROY_WITH_PARENT,(Gtk.STOCK_OK, Gtk.ResponseType.OK))
		dialogo.set_default_size(50,5)
		self.dialogo = dialogo
		contenido = dialogo.get_content_area()
		liststore = Gtk.ListStore(int, str) #que contiene el filtro
		self.liststore = liststore

		filtroeje = liststore.filter_new() #Hace un filtrado de liststore. Crea otro liststore para aplicar el filtro
		self.filtroeje = filtroeje
		filtroeje.set_visible_func(self.aplicar_filtro_aux) #Filtra el liststore nuevo según lo que indique la función


		ejerciciostreev = Gtk.TreeView(filtroeje, headers_visible=True) #Lista de ejercicios
		ejerciciostreev.get_selection().set_mode(0)
		#Crear columna 1
		renderer_text = Gtk.CellRendererText()

		column_text1 = Gtk.TreeViewColumn(("Nº"), renderer_text, text=0)

		#Crear columna 2
		renderer_text2 = Gtk.CellRendererText()
		column_text2 = Gtk.TreeViewColumn(("Ejercicio"), renderer_text2, text=1)

		ejerciciostreev.append_column(column_text1)
		ejerciciostreev.append_column(column_text2)

		self.ejerciciostreev = ejerciciostreev

		if ejerciciosnecesarios != []:
			for i in range(0, len(ejerciciosnecesarios)):
				self.filtroeje.get_model().append([i, ejerciciosnecesarios[i]])

		ventana_scroll = Gtk.ScrolledWindow(expand=True, margin=5)
		ventana_scroll.set_size_request(300, 100)
		ventana_scroll.add(ejerciciostreev)

		l1 = Gtk.Label()
		l1.set_markup("<b>valoración post-sesión</b>")  #texto
		val = Gtk.Entry(width_chars=30)	
		self.val = val

		InfoAdi = Gtk.Label()
		InfoAdi.set_markup("<b>Modificaciones de ejercicios:</b>")

		scrolled_window = Gtk.ScrolledWindow(expand=False)    #cuadro de texto
		scrolled_window.set_border_width(5)	
        # we scroll only if needed
		scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        # a text buffer (stores text)
		bufferpers = Gtk.TextBuffer()
		self.bufferpers = bufferpers

        # a textview (displays the buffer)
		textview = Gtk.TextView(buffer=bufferpers)

        # textview is scrolled
		scrolled_window.add(textview)

		Boxvaloraciones = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin=0)
		Boxvaloraciones.pack_start(l1, False, False, 0)
		Boxvaloraciones.pack_start(val, False, False, 0)
		Boxvaloraciones.pack_start(InfoAdi, False, False, 0)
		Boxvaloraciones.pack_start(scrolled_window, False, False, 0)


		pesocambiado = Gtk.Label("Peso nuevo adquirido:")

		pesocambiador = Gtk.SpinButton(adjustment=Gtk.Adjustment(0, 0, 500, 0.5, 10, 0), digits=1)
		self.pesocambiador = pesocambiador

		pesoBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		pesoBox.pack_start(pesocambiado, False, False, 0)
		pesoBox.pack_start(pesocambiador, False, False, 0)

		AñadirLesionEntrada = Gtk.Entry(width_chars=30)	
		self.AñadirLesionEntrada = AñadirLesionEntrada
		self.AñadirLesionEntrada.set_placeholder_text("Añadir lesión adquirida...")
		lesionnueva = Gtk.Button("Añadir")
		lesionnueva.connect('clicked', controller.on_añadir_lesion, True, userid)

		lesionadqBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		lesionadqBox.pack_start(AñadirLesionEntrada, False, False, 0)
		lesionadqBox.pack_start(lesionnueva, False, False, 0)

		catalogover = Gtk.Button("Consultar catálogo de lesiones")
		catalogover.connect('clicked', controller.on_catLesiones, True, userid)

		if valores != None:
			val.set_text(valores["valoracionpersonal"]) 
			bufferpers.set_text(valores["modEjer"]) 
			pesocambiador.set_value(float(valores["peso"]))

		botonguardar = Gtk.Button("Guardar")
		botonguardar.set_sensitive(False)
		botonguardar.connect('clicked', controller.on_guardar_valoracionespersonal, sesionid, userid)

		pesocambiador.connect("value-changed", controller.permitir_guardado, botonguardar)
		val.connect("changed", controller.permitir_guardado, botonguardar)
		bufferpers.connect("changed", controller.permitir_guardado, botonguardar)

		valGrid = Gtk.Grid(margin=20, column_spacing=10, row_spacing=10)  #colocacion de elementos anteriores
		valGrid.attach(ventana_scroll, 0, 0, 2, 5)
		valGrid.attach_next_to(Boxvaloraciones, ventana_scroll, Gtk.PositionType.RIGHT, 5, 8)
		valGrid.attach_next_to(pesoBox, Boxvaloraciones, Gtk.PositionType.BOTTOM, 3, 1)
		valGrid.attach_next_to(lesionadqBox, pesoBox, Gtk.PositionType.BOTTOM, 5, 1)
		valGrid.attach_next_to(catalogover, lesionadqBox, Gtk.PositionType.BOTTOM, 1, 1)
		valGrid.attach_next_to(botonguardar, catalogover, Gtk.PositionType.BOTTOM, 1, 1)		
		contenido.add(valGrid)
		dialogo.show_all()
		dialogo.run()
		dialogo.destroy()

###################################################################################################################################################
###################################################################################################################################################

	def Formulario_user(self, datos_usuario):
		win = self.win	#para borrar los atributos de la clase y ahorrar memoria
		self.__dict__.clear()
		self.win = win
		self.win.get_child().destroy() #destruimos ventana de inicio
		l1 = Gtk.Label()
		l1.set_markup("<big><b>Formulario de usuario</b></big>")  #texto

		Apellidos = Gtk.Entry(width_chars=50)	
		self.Apellidos = Apellidos
		Etiq_ap = Gtk.Label(label = ("Apellidos:")) 
		AP = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		AP.pack_start(Etiq_ap, False, False, 0)
		AP.pack_start(Apellidos, False, False, 0)

		Nombre = Gtk.Entry(width_chars=50)
		self.Nombre = Nombre
		Etiq_nom = Gtk.Label(label = ("Nombre:"))
		Etiq_Sexo = Gtk.Label(label = ("Sexo:"))
		Hombre = Gtk.RadioButton.new_with_label_from_widget(None, "H")
		self.Hombre = Hombre
		Mujer = Gtk.RadioButton.new_from_widget(Hombre)
		self.Mujer = Mujer
		Mujer.set_label("M")
		DNI = Gtk.Entry(width_chars=20)
		self.DNI = DNI
		Etiq_DNI = Gtk.Label(label = ("DNI:"))


		fila2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		fila2.pack_start(Etiq_nom, False, False, 0)
		fila2.pack_start(Nombre, False, False, 0)
		fila2.pack_start(Etiq_Sexo, False, False, 0)
		fila2.pack_start(Hombre, False, False, 0)
		fila2.pack_start(Mujer, False, False, 0)
		fila2.pack_start(Etiq_DNI, False, False, 0)
		fila2.pack_start(DNI, False, False, 0)

		foto = Gtk.Image.new_from_file("./foto.png")
		self.foto = foto
		self.FotoSeleccionada = None
		self.id = None

		CambiarFoto = Gtk.Button("Cambiar foto")
		self.CambiarFoto = CambiarFoto

		FechaNac = Gtk.Entry(width_chars=20)
		self.FechaNac = FechaNac
		FechaNac.set_placeholder_text("E.g.: 10/10/10")
		Etiq_fecha = Gtk.Label(label = ("Fecha de nacimiento:"))
		fila3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		fila3.pack_start(Etiq_fecha, False, False, 0)
		fila3.pack_start(FechaNac, False, False, 0)


		domicilio = Gtk.Entry(width_chars=50)
		self.domicilio = domicilio
		Etiq_domicilio = Gtk.Label(label = ("Domicilio:"))
		fila4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		fila4.pack_start(Etiq_domicilio, False, False, 0)
		fila4.pack_start(domicilio, False, False, 0)

		telefono = Gtk.Entry(width_chars=20)
		self.telefono = telefono
		Etiq_telefono = Gtk.Label(label = ("Teléfono:"))
		correo = Gtk.Entry(width_chars=30)
		self.correo = correo
		Etiq_correo = Gtk.Label(label = ("Correo electrónico:"))

		InfoAdi = Gtk.Label()
		InfoAdi.set_markup("<b>  Información adicional:</b>")

		scrolled_window = Gtk.ScrolledWindow(expand=False)    #cuadro de texto
		scrolled_window.set_border_width(5)	
        # we scroll only if needed
		scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        # a text buffer (stores text)
		buffer1 = Gtk.TextBuffer()
		self.buffer1 = buffer1

        # a textview (displays the buffer)
		textview = Gtk.TextView(buffer=buffer1)

        # textview is scrolled
		scrolled_window.add(textview)

		fila5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=5)
		fila5.pack_start(Etiq_telefono, False, False, 0)
		fila5.pack_start(telefono, False, False, 0)
		fila5.pack_start(Etiq_correo, False, False, 0)
		fila5.pack_start(correo, False, False, 0)

		categoria = Gtk.ListStore(str)
		categoria.append([("Estudiante")])
		categoria.append([("PAS")])
		Etiq_categoria = Gtk.Label(label = ("Categoría:"))
		Categoría = Gtk.ComboBoxText(model = categoria)
		self.Categoría = Categoría
		cell = Gtk.CellRendererText()
		Categoría.pack_start(cell, False)

		Peso = Gtk.Entry(width_chars=5)
		self.Peso = Peso
		Etiq_peso = Gtk.Label(label = ("Peso actual:"))
		altura = Gtk.Entry(width_chars=5)
		self.altura = altura
		Peso.set_placeholder_text(("En kg"))
		Etiq_altura = Gtk.Label(label = ("Altura:"))
		altura.set_placeholder_text(("En cm"))
		fila6 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		fila6.pack_start(Etiq_categoria, False, False, 0)
		fila6.pack_start(Categoría, False, False, 0)
		fila6.pack_start(Etiq_peso, False, False, 0)
		fila6.pack_start(Peso, False, False, 0)
		fila6.pack_start(Etiq_altura, False, False, 0)
		fila6.pack_start(altura, False, False, 0)

		fila7 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		etiq_lesiones = Gtk.Label("Lesiones:")
		lesiones = Gtk.ListBox()
		self.lesiones = lesiones

		scrolled_windowLesiones = Gtk.ScrolledWindow()    #cuadro de texto
		scrolled_windowLesiones.set_propagate_natural_width(True)	
        # we scroll only if needed
		scrolled_windowLesiones.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolled_windowLesiones.add(lesiones)

		etiq_patologias = Gtk.Label("Patologías:")
		patologias = Gtk.ListBox()
		self.patologias = patologias

		scrolled_windowPatologias = Gtk.ScrolledWindow()    #cuadro de texto
		scrolled_windowPatologias.set_propagate_natural_width(True)	
        # we scroll only if needed
		scrolled_windowPatologias.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolled_windowPatologias.add(patologias)

		fila7.pack_start(etiq_lesiones, True, True, 0)
		fila7.pack_start(etiq_patologias, True, True, 0)
		
		filaAux = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

		filaAux.pack_start(scrolled_windowLesiones, True, True, 0)
		filaAux.pack_start(scrolled_windowPatologias, True, True, 0)

		fila8 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		Borrarlesion = Gtk.Button("Borrar")
		self.Borrarlesion = Borrarlesion
		Borrarpatologia = Gtk.Button("Borrar")
		self.Borrarpatologia = Borrarpatologia
		fila8.pack_start(Borrarlesion, True, False, 0)
		fila8.pack_start(Borrarpatologia, True, False, 0)

		fila9a = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
		fila9b = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
		Añadirlesion = Gtk.Button("Añadir")
		self.Añadirlesion = Añadirlesion
		AñadirLesionEntrada = Gtk.Entry(width_chars=30)
		self.AñadirLesionEntrada = AñadirLesionEntrada
		AñadirPatologia = Gtk.Button("Añadir")
		self.AñadirPatologia = AñadirPatologia
		AñadirPatologiaEntrada = Gtk.Entry(width_chars=30)
		self.AñadirPatologiaEntrada = AñadirPatologiaEntrada

		fila9a.pack_start(Añadirlesion, True, False, 0)
		fila9a.pack_start(AñadirLesionEntrada, True, False, 0)
		fila9b.pack_start(AñadirPatologia, True, False, 0)
		fila9b.pack_start(AñadirPatologiaEntrada, True, False, 0)

		fila10 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		CatLesiones = Gtk.Button("Consultar catálogo de lesiones")
		self.CatLesiones = CatLesiones
		CatPatologias = Gtk.Button("Consultar catálogo de patologías")
		self.CatPatologias = CatPatologias

		fila10.pack_start(CatLesiones, True, False, 0)
		fila10.pack_start(CatPatologias, True, False, 0)

		fila11 = Gtk.HBox(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		self.modificado = None
		self.aceptado = None
		if datos_usuario is not None: 
			modificado = Gtk.Button("Guardar")
			self.modificado = modificado
			botonAceptado = modificado
		else:
			aceptado = Gtk.Button("Guardar")
			self.aceptado = aceptado
			botonAceptado = aceptado
		cancelado = Gtk.Button("Cancelar")
		self.cancelado = cancelado
		fila11.pack_end(cancelado, False, False, 0)	
		#fila11.pack_end(aceptado, False, False, 0)
		fila11.set_center_widget(botonAceptado)

		if datos_usuario is not None:     #en el caso de que entremos para MODIFICAR un usuario existente
			self.Apellidos.set_text(datos_usuario["Apellidos"]) 
			self.Nombre.set_text(datos_usuario["Nombre"])
			if datos_usuario["Sexo"] == "M":
				self.Mujer.set_active(True)
			self.DNI.set_text(datos_usuario["DNI"])
			if datos_usuario['lesiones'] != []:
				for i in range(0, len(datos_usuario['lesiones'])):
					self.añadir_entrada(str(datos_usuario['lesiones'][i]['lesion']) , "lesion")
			if datos_usuario['patologias'] != []:
				for i in range(0, len(datos_usuario['patologias'])):
					self.añadir_entrada(str(datos_usuario['patologias'][i]["patologia"]) , "patologia")

			FotoAux = (datos_usuario["Foto"])
			if FotoAux is not None:
				foto_codificada = base64.b64decode(FotoAux)
				stream = Gio.MemoryInputStream().new_from_data(foto_codificada)
				image = GdkPixbuf.Pixbuf.new_from_stream_at_scale(stream, 150, 175, True, None)
				FotoS = Gtk.Image()

				FotoS.set_from_pixbuf(image)
				self.foto = FotoS  #lo cambio para incluirlo en el grid
 
			self.FechaNac.set_text(str(datos_usuario["FechaNac"]))
			self.domicilio.set_text(str(datos_usuario["domicilio"]))
			self.telefono.set_text(str(datos_usuario["telefono"]))
			self.correo.set_text(str(datos_usuario["correo"]))
			self.buffer1.set_text(datos_usuario["buffer1"])
			if datos_usuario["Categoría"] == "Estudiante":
				self.Categoría.set_active(0)
			else:
				self.Categoría.set_active(1)
			self.Peso.set_text(str(datos_usuario["Peso"]))
			self.altura.set_text(str(datos_usuario["altura"]))
			self.id = datos_usuario["id"]


		CreacusuariosGrid = Gtk.Grid(margin=20, column_spacing=10, row_spacing=10)  #colocacion de elementos anteriores
		CreacusuariosGrid.attach(l1, 10, 0, 20, 1)
		CreacusuariosGrid.attach_next_to(AP, l1, Gtk.PositionType.BOTTOM, 15, 1)
		CreacusuariosGrid.attach_next_to(fila2, AP, Gtk.PositionType.BOTTOM, 15, 1)
		CreacusuariosGrid.attach_next_to(self.foto, l1, Gtk.PositionType.RIGHT, 5, 2)
		CreacusuariosGrid.attach_next_to(self.CambiarFoto, self.foto, Gtk.PositionType.BOTTOM, 5, 1)
		CreacusuariosGrid.attach_next_to(fila3, fila2, Gtk.PositionType.BOTTOM, 15, 1)
		CreacusuariosGrid.attach_next_to(fila4, fila3, Gtk.PositionType.BOTTOM, 15, 1)
		CreacusuariosGrid.attach_next_to(fila5, fila4, Gtk.PositionType.BOTTOM, 15, 1)
		CreacusuariosGrid.attach_next_to(fila6, fila5, Gtk.PositionType.BOTTOM, 15	, 1)
		CreacusuariosGrid.attach_next_to(fila7, fila6, Gtk.PositionType.BOTTOM, 20, 3)
		CreacusuariosGrid.attach_next_to(filaAux, fila7, Gtk.PositionType.BOTTOM, 20, 10)
		CreacusuariosGrid.attach_next_to(fila8, filaAux, Gtk.PositionType.BOTTOM, 20, 1)
		CreacusuariosGrid.attach_next_to(fila9a, fila8, Gtk.PositionType.BOTTOM, 10, 1)
		CreacusuariosGrid.attach_next_to(fila9b, fila9a, Gtk.PositionType.RIGHT, 10, 1)
		CreacusuariosGrid.attach_next_to(fila10, fila9a, Gtk.PositionType.BOTTOM, 20, 1)
		CreacusuariosGrid.attach_next_to(fila11, fila10, Gtk.PositionType.BOTTOM, 20, 2)
		CreacusuariosGrid.attach_next_to(InfoAdi, fila3, Gtk.PositionType.RIGHT, 5, 1)
		CreacusuariosGrid.attach_next_to(scrolled_window, InfoAdi, Gtk.PositionType.BOTTOM, 10, 2)
		self.CreacusuariosGrid = CreacusuariosGrid

		self.win.add(CreacusuariosGrid)
		self.win.show_all()

	def añadir_entrada(self, entrada, tipo):
		fila = Gtk.ListBoxRow()
		if tipo == "lesion":
			fila.add(Gtk.Label(entrada.strip()))
			self.lesiones.add(fila)
			self.lesiones.show_all()
		else:
			fila.add(Gtk.Label(entrada.strip()))
			self.patologias.add(fila)
			self.patologias.show_all()

	def cataLesiones(self, palabrasIntroducidas, data, VieneDeComprobacion, controller, vieneDeValoracion, userid):   #en el caso de que la funcion se llamara para comprobar existencia de entradas
		return self.catalogos("Catálogo de lesiones", palabrasIntroducidas, data, "lesion", VieneDeComprobacion, controller, vieneDeValoracion, userid)

	def cataPatologias(self, palabrasIntroducidas, data, VieneDeComprobacion, controller, vieneDeValoracion, userid):
		return self.catalogos("Catálogo de patologías",palabrasIntroducidas, data, "patologia", VieneDeComprobacion, controller, False, "")

	def catalogos(self, titulo, palabrasIntroducidas, data, tipo, VieneDeComprobacion, controller, vieneDeValoracion, userid):
		catalogo = Gtk.Dialog(titulo, self.win, Gtk.DialogFlags.DESTROY_WITH_PARENT)
		self.catalogo = catalogo
		catalogo.add_button('Aceptar', Gtk.ResponseType.OK)
		contenido = catalogo.get_content_area()    #es un gtk.box
		Lista = Gtk.ListBox()
		if data is not None:
			listaDeChecks = []
			for i in range(0, len(data)):
				elemento = data[i]
				entrada = Gtk.ListBoxRow()
				check = Gtk.CheckButton(elemento)
				entrada.add(check)
				Lista.add(entrada)
				listaDeChecks.append(check)

		scrolled_windowLista = Gtk.ScrolledWindow()    #cuadro de texto
		scrolled_windowLista.set_propagate_natural_width(True)	
        # we scroll only if needed
		scrolled_windowLista.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolled_windowLista.add(Lista)
		Grid = Gtk.Grid(margin=20, column_spacing=10, row_spacing=10)
		Grid.attach(scrolled_windowLista, 0, 3, 30, 40)
		if VieneDeComprobacion:
			boton = Gtk.Button('No encuentro el valor deseado, introducir en el catálogo >>')
			boton.connect("clicked", controller.on_añadir_Seguro, palabrasIntroducidas, tipo, vieneDeValoracion, userid)
			Grid.attach_next_to(boton, scrolled_windowLista, Gtk.PositionType.BOTTOM, 1, 2)
		contenido.pack_start(Grid, True, True, 5)
		
		Grid.show_all()
		respuesta = catalogo.run()
 
		if respuesta == Gtk.ResponseType.OK:     #comprobamos que checks se han introducido para añadirlos a la bd del usuario
			for a in range(0, len(listaDeChecks)):
				if listaDeChecks[a].get_active():
					controller.on_añadir_Seguro(self, data[a], tipo, vieneDeValoracion, userid)
		catalogo.destroy()

	def advertenciaCatalogos(self, palabrasIntroducidas, resultados, tipo, controller, vieneDeValoracion, userid):
		if vieneDeValoracion:	
			advertencia = Gtk.MessageDialog(self.dialogo, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK,
											"\nEl catálogo ya dispone de algunas entradas que coinciden con lo introducido.") 
		else:
			advertencia = Gtk.MessageDialog(self.win, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK,
											"\nEl catálogo ya dispone de algunas entradas que coinciden con lo introducido.") 
		advertencia.format_secondary_text("Compruebe si alguna de ellas coincide con lo deseado para evitar introducir repetidos")
		advertencia.run()
		advertencia.destroy()
		if tipo == "lesiones":
			self.cataLesiones(palabrasIntroducidas, resultados, True, controller, vieneDeValoracion, userid)
		else:
			self.cataPatologias(palabrasIntroducidas, resultados, True, controller, vieneDeValoracion, userid)

	def	YaPuestaEnLista(self):
		advertencia = Gtk.MessageDialog(self.win, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK,
										"\nError.") 
		advertencia.format_secondary_text("Este elemento ya se encuentra en la lista")
		advertencia.run()
		advertencia.destroy()		

	def datosAGuardar(self):
		if self.id is not None:   #para diferenciar el caso de una actualizacion y una entrada nueva
			return (self.Apellidos.get_text().strip(), self.Nombre.get_text().strip(), self.Hombre, self.Mujer, self.DNI.get_text().strip(), self.FotoSeleccionada,
						self.FechaNac.get_text().strip(), self.domicilio.get_text().strip(), self.telefono.get_text().strip(), self.correo.get_text().strip(),
						self.buffer1, self.Categoría.get_active_text(), self.Peso.get_text().strip(), self.altura.get_text().strip(), self.lesiones, self.patologias, self.id)
		else:
			return (self.Apellidos.get_text().strip(), self.Nombre.get_text().strip(), self.Hombre, self.Mujer, self.DNI.get_text().strip(), self.FotoSeleccionada,
						self.FechaNac.get_text().strip(), self.domicilio.get_text().strip(), self.telefono.get_text().strip(), self.correo.get_text().strip(),
						self.buffer1, self.Categoría.get_active_text(), self.Peso.get_text().strip(), self.altura.get_text().strip(), self.lesiones, self.patologias)

	def Emergente_eliminar(self, controller, id):
		ventanaemergente = Gtk.MessageDialog(self.win, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, "\n¿Está seguro de que desea eliminar al usuario " + str(id) + "?") 
		ventanaemergente.connect("response", controller.emergente_decision, id)
		ventanaemergente.run()
		ventanaemergente.destroy()

	def AccionesEnElFormUsuario(self, controller):
		self.CambiarFoto.connect('clicked', controller.on_elegir_foto)
		if self.aceptado is not None:
			self.aceptado.connect('clicked', controller.on_guardar_en_BD)
		else:
			self.modificado.connect('clicked', controller.on_actualizar_en_BD)
		self.cancelado.connect('clicked', controller.on_usuarios)
		self.CatPatologias.connect('clicked', controller.on_catPatologias,  False, "")
		self.CatLesiones.connect('clicked', controller.on_catLesiones, False, "")
		self.Añadirlesion.connect('clicked', controller.on_añadir_lesion, False, "")
		self.AñadirPatologia.connect('clicked', controller.on_añadir_patologia, False, "")
		self.Borrarlesion.connect('clicked', controller.on_borrar_lesion)
		self.Borrarpatologia.connect('clicked', controller.on_borrar_patologia)

	def seleccionar_foto(self, widget):
		Seleccionarfoto = Gtk.FileChooserDialog("Seleccione una foto", self.win, Gtk.FileChooserAction.OPEN,
    		(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        	Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

		self.add_filters(Seleccionarfoto)
		response = Seleccionarfoto.run()
		if response == Gtk.ResponseType.OK:
			FotoSeleccionada = Seleccionarfoto.get_filename()
			self.FotoSeleccionada = FotoSeleccionada
			fotoAnterior = self.CreacusuariosGrid.get_child_at(30,1)
			pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(FotoSeleccionada, 150, 175, True)

			fotoAnterior.set_from_pixbuf(pixbuf)         #cambio la foto por la que se selecciona en archivos
		Seleccionarfoto.destroy()


	def add_filters(self, Seleccionarfoto):  #para añadir filtros en el diálogo de selección de imagen
		filter_png = Gtk.FileFilter()
		filter_png.set_name("Imágenes png")
		filter_png.add_mime_type("image/png")
		Seleccionarfoto.add_filter(filter_png)

		filter_jpeg = Gtk.FileFilter()
		filter_jpeg.set_name("Imágenes jpeg")
		filter_jpeg.add_mime_type("image/jpeg")
		Seleccionarfoto.add_filter(filter_jpeg)

		filter_any = Gtk.FileFilter()
		filter_any.set_name("Any files")
		filter_any.add_pattern("*")
		Seleccionarfoto.add_filter(filter_any)
#####################################################################################################################EJERCICIOS

	def ejercicios(self):
		win = self.win	#para borrar los atributos de la clase y ahorrar memoria
		self.__dict__.clear()
		self.win = win
		self.win.unmaximize()
		self.win.resize(800,550)
		self.win.get_child().destroy() #destruimos elemetos de inicio

		Ini = Gtk.ToggleButton(label=("Inicio"))
		self.Ini = Ini
		Programacion = Gtk.ToggleButton(label=("Programación"))
		self.Programacion = Programacion
		Grupos = Gtk.ToggleButton(label=("Grupos"))
		self.Grupos = Grupos
		Usuarios = Gtk.ToggleButton(label=("Usuarios"))
		self.Usuarios = Usuarios
		Sesiones = Gtk.ToggleButton(label=("Sesiones"))
		self.Sesiones = Sesiones
		Ejercicios = Gtk.ToggleButton(label=("Ejercicios"))
		self.Ejercicios = Ejercicios
		self.Ejercicios.set_active(True)

		links = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=10)  #barra navegacion
		links.pack_start(self.Ini, False, False, 0)
		links.pack_start(self.Programacion, False, False, 0)
		links.pack_start(self.Grupos, False, False, 0)
		links.pack_start(self.Usuarios, False, False, 0)
		links.pack_start(self.Sesiones, False, False, 0)
		links.pack_start(self.Ejercicios, False, False, 0)

		l1 = Gtk.Label()
		l1.set_markup("<big><b>Ejercicios</b></big>")  #texto

		liststoreEjercicios = Gtk.ListStore(str, str, str, str) #que contiene el filtro
		self.liststoreEjercicios = liststoreEjercicios

		filtroEjercicios = liststoreEjercicios.filter_new() #Hace un filtrado de liststore. Crea otro liststore para aplicar el filtro
		filtroEjercicios.set_visible_func(self.aplicar_filtro_aux) #Filtra el liststore nuevo según lo que indique la función
		self.filtroEjercicios = filtroEjercicios
		self.filtroEjercicios_inicio = ""

		ejerciciosTree = Gtk.TreeView(filtroEjercicios, headers_visible=True) #Lista grupos

		#Crear columna x
		renderer_textx = Gtk.CellRendererText()
		column_textx = Gtk.TreeViewColumn(("Ejercicio"), renderer_textx, text=0)

		#Crear columna 0
		renderer_text = Gtk.CellRendererText()
		column_text0 = Gtk.TreeViewColumn(("Descripción"), renderer_text, text=1)

		#Crear columna 1
		renderer_text1 = Gtk.CellRendererText()
		column_text1 = Gtk.TreeViewColumn(("Materiales"), renderer_text1, text=2)

		#Crear columna 2
		renderer_text2 = Gtk.CellRendererText()
		column_text2 = Gtk.TreeViewColumn(("Carga Aeróbica/Coordinación/Equilibrio/Fuerza"), renderer_text2, text=3)


		ejerciciosTree.append_column(column_textx)
		ejerciciosTree.append_column(column_text0)
		ejerciciosTree.append_column(column_text1)
		ejerciciosTree.append_column(column_text2)

		self.ejerciciosTree = ejerciciosTree

		ventana_scroll = Gtk.ScrolledWindow(expand=True, margin=20)
		ventana_scroll.set_size_request(1000, 100)
		ventana_scroll.add(ejerciciosTree)

		VerMod = Gtk.Button(label=("Ver/Modificar"))
		self.VerMod = VerMod
		Eliminar = Gtk.Button(label=("Eliminar"))
		self.Eliminar = Eliminar

		botones = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=12)  #botones para utilizar con usuarios
		botones.pack_start(self.VerMod, False, False, 0)
		botones.pack_start(self.Eliminar, False, False, 0)

		EjercicioNuevo = Gtk.Button("Añadir nuevo ejercicio")
		self.EjercicioNuevo = EjercicioNuevo

		ejerciciosGrid = Gtk.Grid(margin=5, column_spacing=5, row_spacing=10)  #colocacion de elementos anteriores
		ejerciciosGrid.attach(links, 0, 0, 1, 1)
		ejerciciosGrid.attach_next_to(l1, links, Gtk.PositionType.BOTTOM, 1, 1)
		ejerciciosGrid.attach_next_to(ventana_scroll, l1, Gtk.PositionType.BOTTOM, 15, 10)
		ejerciciosGrid.attach_next_to(botones, ventana_scroll, Gtk.PositionType.BOTTOM, 1, 1)
		ejerciciosGrid.attach_next_to(EjercicioNuevo, botones, Gtk.PositionType.RIGHT, 1, 1)

		self.VerMod.set_sensitive(False)
		self.Eliminar.set_sensitive(False)
		self.EjercicioNuevo.set_sensitive(True)

		self.win.add(ejerciciosGrid)
		self.win.show_all()

	def Emergente_eliminar_Ejercicio(self, controller, nombreej):
		ventanaemergente = Gtk.MessageDialog(self.win, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, "\n¿Está seguro de que desea eliminar el ejercicio " + nombreej + "?") 
		ventanaemergente.connect("response", controller.emergente_decision_ejercicio, nombreej)
		ventanaemergente.run()
		ventanaemergente.destroy()

	def clickEjercicios(self, controller):
		self.EjercicioNuevo.connect("clicked", controller.on_NuevoEjercicio)
		self.ejerciciosTree.get_selection().connect("changed", controller.activar_botonesEjercicio) #si seleccionas un ejercicio 

	def clickSobreEjercicios(self, controller):
		self.Eliminar.connect("clicked", controller.on_eliminar_ejercicio)
		self.VerMod.connect("clicked", controller.on_ActualizarEjercicio)

	def Formulario_Ejercicio(self, materiales, datos_ejercicio, controller):
		win = self.win	#para borrar los atributos de la clase y ahorrar memoria
		self.__dict__.clear()
		self.win = win
		self.win.maximize()
		self.win.get_child().destroy() #destruimos ventana de inicio
		l1 = Gtk.Label()
		l1.set_markup("<big><b>Formulario de Ejercicio</b></big>")  #texto

		NombreEj = Gtk.Entry(width_chars=30)	
		self.NombreEj = NombreEj
		Etiq_NombreEj = Gtk.Label(label = ("Nombre:")) 
		NE = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		NE.pack_start(Etiq_NombreEj, False, False, 0)
		NE.pack_start(NombreEj, False, False, 0)

		scrolled_window = Gtk.ScrolledWindow(expand=False)    #cuadro de texto
		scrolled_window.set_border_width(5)	
        # we scroll only if needed
		scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        # a text buffer (stores text)
		Descripicion = Gtk.TextBuffer()
		self.Descripicion = Descripicion

        # a textview (displays the buffer)
		textview = Gtk.TextView(buffer=Descripicion)

        # textview is scrolled
		scrolled_window.add(textview)

		Etiq_descrip = Gtk.Label(label = ("Descripción:")) 
		descripBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		descripBox.pack_start(Etiq_descrip, False, False, 0)
		descripBox.pack_start(scrolled_window, True, True, 0)

		Etiq_materiales = Gtk.Label(label = ("Materiales: ")) 
		materialesBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0, margin=0)
		materialesBox.pack_start(Etiq_materiales, False, False, 0)
		self.materialesBox = materialesBox
		añadirmaterial = Gtk.Button("Añadir")
		self.añadirmaterial= añadirmaterial
		self.materiales = []

		mat = Gtk.ListStore(str)   #introducimos la lista de materiales en el menú desplegable
		for i in materiales:
			mat.append([i])
		añadirmaterialEntrada = Gtk.ComboBoxText(model = mat)
		self.añadirmaterialEntrada = añadirmaterialEntrada
		añadirmaterialBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		añadirmaterialBox.pack_start(añadirmaterialEntrada, False, False, 0)
		añadirmaterialBox.pack_start(añadirmaterial, False, False, 0)

		Realiz = Gtk.Label("Realización:")
		botonFotoVideo = Gtk.FileChooserButton(title="Añadir un vídeo/foto...")
		botonFotoVideo.set_width_chars(9)
		self.botonFotoVideo = botonFotoVideo
		self.add_filtersExpl(botonFotoVideo)
		EnlaceFoto = Gtk.Entry(width_chars=30)
		EnlaceFoto.set_placeholder_text(("Añadir enlace de explicación..."))
		self.EnlaceFoto = EnlaceFoto
		botonEnlace = Gtk.Button(label= "Añadir")
		self.botonEnlace = botonEnlace

		realizacionBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		realizacionBox.pack_start(Realiz, False, False, 0)
		realizacionBox.pack_start(botonFotoVideo, False, False, 0)
		self.realizacionBox = realizacionBox

		boxSelecEnlaces = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		boxSelecEnlaces.pack_start(EnlaceFoto, False, False, 0)
		boxSelecEnlaces.pack_start(botonEnlace, False, False, 0)

		multimediaBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=10)
		multimediaBox.set_spacing(35)
		self.multimediaBox = multimediaBox
		self.imagenEjercicio = None
		self.video = None

		emptyContainer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=10)

		enlacesBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin=0)
		etiqEnlaces = Gtk.Label()
		etiqEnlaces.set_markup("<i>Enlaces añadidos:</i>")
		borradoEnlaces = Gtk.Button("Borrar enlaces")
		self.borradoEnlaces = borradoEnlaces
		enlacesBox.pack_start(etiqEnlaces, False, False, 0)
		enlacesBox.pack_start(borradoEnlaces, False, False, 0)
		self.enlacesBox = enlacesBox
		self.listaURLS = []

		evitarLesiones = Gtk.Label("Evitar lesiones:")
		evitarPatologias = Gtk.Label("Evitar patologías:")
		fila6 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		fila6.pack_start(evitarLesiones, True, True, 0)
		fila6.pack_start(evitarPatologias, True, True, 0)

		fila7 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

		lesiones = Gtk.ListBox()
		self.lesiones = lesiones

		scrolled_windowLesiones = Gtk.ScrolledWindow()    #cuadro de texto
		scrolled_windowLesiones.set_propagate_natural_width(True)	
        # we scroll only if needed
		scrolled_windowLesiones.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolled_windowLesiones.add(lesiones)

		patologias = Gtk.ListBox()
		self.patologias = patologias

		scrolled_windowPatologias = Gtk.ScrolledWindow()    #cuadro de texto
		scrolled_windowPatologias.set_propagate_natural_width(True)	
        # we scroll only if needed
		scrolled_windowPatologias.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolled_windowPatologias.add(patologias)

		fila7.pack_start(scrolled_windowLesiones, True, True, 0)
		fila7.pack_start(scrolled_windowPatologias, True, True, 0)

		fila8 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		Borrarlesion = Gtk.Button("Borrar")
		self.Borrarlesion = Borrarlesion
		Borrarpatologia = Gtk.Button("Borrar")
		self.Borrarpatologia = Borrarpatologia
		fila8.pack_start(Borrarlesion, True, False, 0)
		fila8.pack_start(Borrarpatologia, True, False, 0)

		fila9 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		Añadirlesion = Gtk.Button("Añadir")
		self.Añadirlesion = Añadirlesion
		AñadirLesionEntrada = Gtk.Entry(width_chars=30)
		self.AñadirLesionEntrada = AñadirLesionEntrada
		AñadirPatologia = Gtk.Button("Añadir")
		self.AñadirPatologia = AñadirPatologia
		AñadirPatologiaEntrada = Gtk.Entry(width_chars=30)
		self.AñadirPatologiaEntrada = AñadirPatologiaEntrada

		fila9.pack_start(Añadirlesion, False, False, 0)
		fila9.pack_start(AñadirLesionEntrada, False, False, 0)
		fila9.pack_start(AñadirPatologia, False, False, 0)
		fila9.pack_start(AñadirPatologiaEntrada, False, False, 0)

		fila10 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		CatLesiones = Gtk.Button("Consultar catálogo de lesiones")
		self.CatLesiones = CatLesiones
		CatPatologias = Gtk.Button("Consultar catálogo de patologías")
		self.CatPatologias = CatPatologias

		fila10.pack_start(CatLesiones, True, False, 0)
		fila10.pack_start(CatPatologias, True, False, 0)

		boxComun = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5, margin = 5)
		boxComun.pack_start(fila8, True, False, 0)
		boxComun.pack_start(fila9, True, False, 0)
		boxComun.pack_start(fila10, True, False, 0)

		nota = Gtk.Label()
		nota.set_markup("<i>Introduzca las cargas con ayuda de las flechas o arrastrando con el ratón:</i>")
		carga  = Gtk.Label("Carga(%):        -aeróbico:")
		ajuste = Gtk.Adjustment(0, 0, 100, 5, 10, 0)
		ajuste1 = Gtk.Adjustment(0, 0, 100, 5, 10, 0)
		ajuste2 = Gtk.Adjustment(0, 0, 100, 5, 10, 0)
		ajuste3 = Gtk.Adjustment(0, 0, 100, 5, 10, 0)
		aeroScale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=ajuste, digits=0)
		aeroScale.set_hexpand(True)
		aeroScale.set_value(0)
		self.aeroScale = aeroScale
		coordLabel  = Gtk.Label("                    -coordinación:")
		coordScale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=ajuste1, digits=0)
		coordScale.set_hexpand(True)
		coordScale.set_value(0)
		self.coordScale = coordScale
		equiLabel  = Gtk.Label("                            -equilibrio:")
		equiScale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=ajuste2, digits=0)
		equiScale.set_hexpand(True)
		equiScale.set_value(0)
		self.equiScale = equiScale
		frzLabel  = Gtk.Label("                                   -fuerza:")
		frzScale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=ajuste3, digits=0)		
		frzScale.set_hexpand(True)
		frzScale.set_value(0)
		self.frzScale = frzScale


		aerobico = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		aerobico.pack_start(carga, False, False, 0)
		aerobico.pack_start(aeroScale, True, True, 0)

		coord = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		coord.pack_start(coordLabel, False, False, 0)
		coord.pack_start(coordScale, True, True, 0)

		equi = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		equi.pack_start(equiLabel, False, False, 0)
		equi.pack_start(equiScale, True, True, 0)

		frz = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		frz.pack_start(frzLabel, False, False, 0)
		frz.pack_start(frzScale, True, True, 0)

		botonesAceptado = Gtk.HBox(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		self.modificado = None
		self.aceptado = None
		if datos_ejercicio is not None: 
			modificado = Gtk.Button("Guardar")
			self.modificado = modificado
			botonAceptado = modificado
		else:
			aceptado = Gtk.Button("Guardar")
			self.aceptado = aceptado
			botonAceptado = aceptado
		cancelado = Gtk.Button("Cancelar")
		self.cancelado = cancelado
		botonesAceptado.pack_end(cancelado, False, False, 0)	
		botonesAceptado.set_center_widget(botonAceptado)

		if datos_ejercicio is not None:     #en el caso de que entremos para MODIFICAR un ejercicio existente
			self.NombreEj.set_text(datos_ejercicio["nombre_ejercicio"]) 
			self.NombreEj.connect('changed', controller.avisoModif, datos_ejercicio["nombre_ejercicio"])
			self.Descripicion.set_text(datos_ejercicio["descripcion"])

			for i in datos_ejercicio['materiales']:

				infobar = Gtk.InfoBar()
				infobar.set_show_close_button(True)
				infobar.connect("response", self.on_infobar_response)
				label = Gtk.Label(i["nombre_material"])
				content = infobar.get_content_area()
				content.add(label)
				self.materiales.append(label)
				self.materialesBox.pack_start(infobar, False, False, 0)
				self.materialesBox.show_all()

			if datos_ejercicio['lesiones'] != []:
				for i in range(0, len(datos_ejercicio['lesiones'])):
					self.añadir_entrada(str(datos_ejercicio['lesiones'][i]['lesion']) , "lesion")
			if datos_ejercicio['patologias'] != []:
				for i in range(0, len(datos_ejercicio['patologias'])):
					self.añadir_entrada(str(datos_ejercicio['patologias'][i]["patologia"]) , "patologia")

			FotoAux = (datos_ejercicio["foto"])
			if FotoAux is not None:
				foto_codificada = base64.b64decode(FotoAux)
				stream = Gio.MemoryInputStream().new_from_data(foto_codificada)
				image = GdkPixbuf.Pixbuf.new_from_stream_at_scale(stream, 150, 175, True, None)
				FotoS = Gtk.Image()

				FotoS.set_from_pixbuf(image)
				self.insertarFoto(FotoS)

			videoAux = (datos_ejercicio["titulo_video"])
			if videoAux != "None":
				self.insertarVideo(videoAux, controller)
				self.video = videoAux

			enlaAuxiliar = (datos_ejercicio["URL"])
			if enlaAuxiliar != "[]":
				i=1
				while(enlaAuxiliar.split("'")[i-1] != "]"):
					enlaceNuevo = Gtk.LinkButton(label=enlaAuxiliar.split("'")[i])
					self.enlacesBox.pack_start(enlaceNuevo, False, False, 0)
					self.listaURLS.append(enlaAuxiliar.split("'")[i])
					i = i+2

			aeroScale.set_value(float(datos_ejercicio["cargas"].split("%")[0]))
			coordScale.set_value(float(datos_ejercicio["cargas"].split("%")[1].split("/")[1]))
			equiScale.set_value(float(datos_ejercicio["cargas"].split("%")[2].split("/")[1]))
			frzScale.set_value(float(datos_ejercicio["cargas"].split("%")[3].split("/")[1]))

		grid = Gtk.Grid(margin=30, column_spacing=5, row_spacing=15)  #colocacion de elementos anteriores
		self.grid = grid
		grid.attach(l1, 0, 0, 4, 1)
		grid.attach_next_to(NE, l1, Gtk.PositionType.BOTTOM, 1, 1)
		grid.attach_next_to(descripBox, NE, Gtk.PositionType.BOTTOM, 8, 8)
		grid.attach_next_to(materialesBox, descripBox, Gtk.PositionType.BOTTOM, 8, 1)
		grid.attach_next_to(añadirmaterialBox, materialesBox, Gtk.PositionType.BOTTOM, 1, 1)
		grid.attach_next_to(emptyContainer, añadirmaterialBox, Gtk.PositionType.RIGHT, 5, 1)
		grid.attach_next_to(realizacionBox, añadirmaterialBox, Gtk.PositionType.BOTTOM, 1, 1)
		grid.attach_next_to(multimediaBox, realizacionBox, Gtk.PositionType.BOTTOM, 3, 10)		
		grid.attach_next_to(boxSelecEnlaces, emptyContainer, Gtk.PositionType.RIGHT, 5, 1)
		grid.attach_next_to(enlacesBox, boxSelecEnlaces, Gtk.PositionType.BOTTOM, 1, 5)
		grid.attach_next_to(nota, multimediaBox, Gtk.PositionType.BOTTOM, 2, 1)
		grid.attach_next_to(aerobico, nota, Gtk.PositionType.BOTTOM, 2, 1)
		grid.attach_next_to(coord, aerobico, Gtk.PositionType.BOTTOM, 2, 1)
		grid.attach_next_to(equi, coord, Gtk.PositionType.BOTTOM, 2, 1)
		grid.attach_next_to(frz, equi, Gtk.PositionType.BOTTOM, 2, 1)
		grid.attach_next_to(fila6, enlacesBox, Gtk.PositionType.BOTTOM, 4, 3)
		grid.attach_next_to(fila7, fila6, Gtk.PositionType.BOTTOM, 4, 6)
		grid.attach_next_to(boxComun, fila7, Gtk.PositionType.BOTTOM, 4, 2)
		grid.attach_next_to(botonesAceptado, frz, Gtk.PositionType.BOTTOM, 3, 4)

		scrolled_windowForm = Gtk.ScrolledWindow()    #cuadro de texto	
        # we scroll only if needed
		scrolled_windowForm.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		scrolled_windowForm.add(grid)

		self.win.add(scrolled_windowForm)
		self.win.show_all()

	def add_filtersExpl(self, SeleccionarExplicacion):  #para añadir filtros en el diálogo de selección de imagen
		filter_png = Gtk.FileFilter()
		filter_png.set_name("Imágenes png")
		filter_png.add_mime_type("image/png")
		SeleccionarExplicacion.add_filter(filter_png)

		filter_jpeg = Gtk.FileFilter()
		filter_jpeg.set_name("Imágenes jpeg")
		filter_jpeg.add_mime_type("image/jpeg")
		SeleccionarExplicacion.add_filter(filter_jpeg)

		filter_jpg = Gtk.FileFilter()
		filter_jpg.set_name("Imágenes jpg")
		filter_jpg.add_mime_type("image/jpg")
		SeleccionarExplicacion.add_filter(filter_jpg)

		filter_mp4 = Gtk.FileFilter()
		filter_mp4.set_name("Vídeos mp4")
		filter_mp4.add_mime_type("video/mp4")
		SeleccionarExplicacion.add_filter(filter_mp4)

		filter_mpeg = Gtk.FileFilter()
		filter_mpeg.set_name("Vídeos mpeg")
		filter_mpeg.add_mime_type("video/mpeg")
		SeleccionarExplicacion.add_filter(filter_mpeg)

		filter_any = Gtk.FileFilter()
		filter_any.set_name("Any files")
		filter_any.add_pattern("*")
		SeleccionarExplicacion.add_filter(filter_any)

	def AccionesEnElFormEjercicio(self,controller):
		self.añadirmaterial.connect('clicked', self.materialNuevo)
		self.botonFotoVideo.connect('selection-changed', controller.insertarVideoFoto)
		self.botonEnlace.connect('clicked', self.insertarEnlace)
		self.borradoEnlaces.connect('clicked', self.borrar_Enlaces)
		self.CatPatologias.connect('clicked', controller.on_catPatologias,  False, "")
		self.CatLesiones.connect('clicked', controller.on_catLesiones, False, "")
		self.Añadirlesion.connect('clicked', controller.on_añadir_lesion, False, "")
		self.AñadirPatologia.connect('clicked', controller.on_añadir_patologia, False, "")
		self.Borrarlesion.connect('clicked', controller.on_borrar_lesion)
		self.Borrarpatologia.connect('clicked', controller.on_borrar_patologia)
		self.aeroScale.connect('value-changed', controller.on_scale_moved)
		self.coordScale.connect('value-changed', controller.on_scale_moved)
		self.equiScale.connect('value-changed', controller.on_scale_moved)
		self.frzScale.connect('value-changed', controller.on_scale_moved)
		if self.aceptado is not None:
			self.aceptado.connect('clicked', controller.on_guardar_en_BD_ejercicios)
		else:
			self.modificado.connect('clicked', controller.on_actualizar_en_BD_ejercicios)
		self.cancelado.connect('clicked', controller.on_ejercicios)

	def borrar_Enlaces(self, boton):
		enlacesAux = self.enlacesBox.get_children()
		for i in range(len(self.enlacesBox.get_children())-2):
			self.enlacesBox.get_children()[2].destroy()
		self.win.show_all()

	def insertarEnlace(self, boton):
		self.listaURLS.append(self.EnlaceFoto.get_text())
		enlaceNuevo = Gtk.LinkButton(label=self.EnlaceFoto.get_text())
		self.enlacesBox.pack_start(enlaceNuevo, False, False, 0)
		self.win.show_all()

	def borradoFoto(self, boton):
		self.imagenBorra.destroy()
		self.imagenEjercicio = None

	def borradoVideo(self, boton, controller):
		controller.accionesvideo(boton, "Stop")
		self.videoBorra.destroy()
		self.video = None

	def insertarFoto(self, foto):
		if (isinstance(foto, Gtk.Image)): 
			imagen = foto
		else:
			pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(foto.get_filename(), 200, 225, True)
			imagen = Gtk.Image()
			imagen.set_from_pixbuf(pixbuf)
			self.imagenEjercicio = foto.get_filename()
		
		self.imagen = imagen
		
		borrado = Gtk.Button(label="Borrar")
		imagenBorra = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin=0)
		self.imagenBorra = imagenBorra
		imagenBorra.pack_start(imagen, False, False, 0)
		imagenBorra.pack_start(borrado, False, False, 0)
		borrado.connect('clicked', self.borradoFoto)
		self.multimediaBox.pack_start(imagenBorra, False, False, 0)
		self.win.show_all()

	def insertarVideo(self, video, controller):
		if os.path.isfile(video):
			draw_area = Gtk.DrawingArea()
			draw_area.connect("realize",controller.configVideo, video)
			draw_area.set_size_request(300,300)   
			self.draw_area = draw_area
			play_button = Gtk.Button("Play/Pausa")
			play_button.connect('clicked', controller.accionesvideo, "PlayPausa")
			self.play_button = play_button
			estadoVideo = ""
			self.estadoVideo = estadoVideo
			stop_button = Gtk.Button("Stop")
			stop_button.connect('clicked', controller.accionesvideo, "Stop")
			self.stop_button = stop_button
			borrado2 = Gtk.Button(label="Borrar")

			PlayBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
			#multimediaBox.pack_start(fotoejemplo, False, False, 0)
			PlayBox.pack_start(play_button, False, False, 0)
			PlayBox.pack_start(stop_button, False, False, 0)
			PlayBox.pack_start(borrado2, False, False, 0)

			videoBorra = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin=0)
			self.videoBorra = videoBorra
			videoBorra.pack_start(draw_area, False, False, 0)
			videoBorra.pack_start(PlayBox, False, False, 0)
			borrado2.connect('clicked', self.borradoVideo, controller)
			self.multimediaBox.pack_start(videoBorra, False, False, 0)
			self.win.show_all()
		else:
			self.error(10)
			return


	def materialNuevo(self, boton):
		infobar = Gtk.InfoBar()
		infobar.set_show_close_button(True)
		infobar.connect("response", self.on_infobar_response)
		label = Gtk.Label(self.añadirmaterialEntrada.get_active_text())
		content = infobar.get_content_area()
		content.add(label)
		self.materiales.append(label)
		self.materialesBox.pack_start(infobar, False, False, 0)
		self.materialesBox.show_all()

	def on_infobar_response(self, infobar, response_id):
		self.materiales.remove(infobar.get_content_area().get_children()[0])
		infobar.destroy()
		
		

	def datosAGuardarDeEjercicios(self):
			return (self.NombreEj.get_text().strip(), self.Descripicion, self.imagenEjercicio, self.video,
				self.listaURLS, str(self.aeroScale.get_value()) + "% /" + str(self.coordScale.get_value()) + "% /" + str(self.equiScale.get_value()) + "% /" + str(self.frzScale.get_value()) + "%", self.materiales,
				self.lesiones, self.patologias)


###############################################################################################################GRUPOS

	def grupo(self):
		win = self.win	#para borrar los atributos de la clase y ahorrar memoria
		self.__dict__.clear()
		self.win = win
		self.win.resize(1000,550)
		self.win.get_child().destroy() #destruimos elemetos de inicio

		Ini = Gtk.ToggleButton(label=("Inicio"))
		self.Ini = Ini
		Programacion = Gtk.ToggleButton(label=("Programación"))
		self.Programacion = Programacion
		Grupos = Gtk.ToggleButton(label=("Grupos"))
		self.Grupos = Grupos
		Usuarios = Gtk.ToggleButton(label=("Usuarios"))
		self.Usuarios = Usuarios
		Sesiones = Gtk.ToggleButton(label=("Sesiones"))
		self.Sesiones = Sesiones
		Ejercicios = Gtk.ToggleButton(label=("Ejercicios"))
		self.Ejercicios = Ejercicios
		self.Grupos.set_active(True)

		links = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=10)  #barra navegacion
		links.pack_start(self.Ini, False, False, 0)
		links.pack_start(self.Programacion, False, False, 0)
		links.pack_start(self.Grupos, False, False, 0)
		links.pack_start(self.Usuarios, False, False, 0)
		links.pack_start(self.Sesiones, False, False, 0)
		links.pack_start(self.Ejercicios, False, False, 0)

		l1 = Gtk.Label()
		l1.set_markup("<big><b>Grupos de entrenamiento</b></big>")  #texto

		liststoreGrupos = Gtk.ListStore(str, str, str) #que contiene el filtro
		self.liststoreGrupos = liststoreGrupos

		filtroGrupos = liststoreGrupos.filter_new() #Hace un filtrado de liststore. Crea otro liststore para aplicar el filtro
		filtroGrupos.set_visible_func(self.aplicar_filtro_aux) #Filtra el liststore nuevo según lo que indique la función
		self.filtroGrupos = filtroGrupos
		self.filtroGrupos_inicio = ""

		gruposTree = Gtk.TreeView(filtroGrupos, headers_visible=True) #Lista grupos

		#Crear columna x
		renderer_textx = Gtk.CellRendererText()
		column_textx = Gtk.TreeViewColumn(("Grupo"), renderer_textx, text=0)

		#Crear columna 0
		renderer_text = Gtk.CellRendererText()
		column_text0 = Gtk.TreeViewColumn(("Horario"), renderer_text, text=1)

		#Crear columna 1
		renderer_text1 = Gtk.CellRendererText()
		column_text1 = Gtk.TreeViewColumn(("Integrantes"), renderer_text1, text=2)


		gruposTree.append_column(column_textx)
		gruposTree.append_column(column_text0)
		gruposTree.append_column(column_text1)


		self.gruposTree = gruposTree

		ventana_scroll = Gtk.ScrolledWindow(expand=True, margin=20)
		ventana_scroll.set_size_request(400, 100)
		ventana_scroll.add(gruposTree)

		VerMod = Gtk.Button(label=("Ver/Modificar"))
		self.VerMod = VerMod
		Eliminar = Gtk.Button(label=("Eliminar"))
		self.Eliminar = Eliminar

		botones = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=12)  #botones para utilizar con usuarios
		botones.pack_start(self.VerMod, False, False, 0)
		botones.pack_start(self.Eliminar, False, False, 0)

		GrupoNuevo = Gtk.Button("Añadir nuevo grupo")
		self.GrupoNuevo = GrupoNuevo

		gruposGrid = Gtk.Grid(margin=5, column_spacing=5, row_spacing=10)  #colocacion de elementos anteriores
		gruposGrid.attach(links, 0, 0, 1, 1)
		gruposGrid.attach_next_to(l1, links, Gtk.PositionType.BOTTOM, 1, 1)
		gruposGrid.attach_next_to(ventana_scroll, l1, Gtk.PositionType.BOTTOM, 20, 10)
		gruposGrid.attach_next_to(botones, ventana_scroll, Gtk.PositionType.BOTTOM, 1, 1)
		gruposGrid.attach_next_to(GrupoNuevo, botones, Gtk.PositionType.RIGHT, 1, 1)

		self.VerMod.set_sensitive(False)
		self.Eliminar.set_sensitive(False)
		self.GrupoNuevo.set_sensitive(True)

		self.win.add(gruposGrid)
		self.win.show_all()


	def clickGrupos(self, controller):
		self.GrupoNuevo.connect("clicked", controller.on_NuevoGrupo)
		self.gruposTree.get_selection().connect("changed", controller.activar_botonesGrupo) #si seleccionas un grupo 

	def clickSobreGrupos(self, controller):
		self.Eliminar.connect("clicked", controller.on_eliminar_grupo)
		self.VerMod.connect("clicked", controller.on_ActualizarGrupo)

	def Formulario_Grupo(self, datos_grupo):
		win = self.win	#para borrar los atributos de la clase y ahorrar memoria
		self.__dict__.clear()
		self.win = win
		self.win.get_child().destroy() #destruimos ventana de inicio
		l1 = Gtk.Label()
		l1.set_markup("<big><b>Formulario de grupos de entrenamiento</b></big>")  #texto
		l1Box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		l1Box.pack_start(l1, False, False, 0)

		self.idgrupo = ""
		busqUsuario = Gtk.SearchEntry(width_chars=8)
		busqUsuario.set_placeholder_text("Nombre/Apellidos")
		busqUsuario.set_width_chars(20)
		self.busqUsuario = busqUsuario
		Etiq_busqUsuario = Gtk.Label(label = ("Usuarios:")) 
		botonBusq = Gtk.Button(label="Buscar")
		self.botonBusq = botonBusq
		busBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		busBox.pack_start(Etiq_busqUsuario, False, False, 0)
		busBox.pack_start(busqUsuario, False, False, 0)
		busBox.pack_start(botonBusq, False, False, 0)

		etiq = Gtk.Label()
		etiq.set_markup("<i>Usuario seleccionados:</i>")
		usersSelec = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		usersSelec.pack_start(etiq, False, False, 0)

		usersEncontrados = Gtk.ListBox()
		usersEncontrados.set_selection_mode(Gtk.SelectionMode(3))
		self.usersEncontrados = usersEncontrados

		scrolled_windowusersEncontrados = Gtk.ScrolledWindow()    #cuadro de texto
		scrolled_windowusersEncontrados.set_propagate_natural_width(True)	
        # we scroll only if needed
		scrolled_windowusersEncontrados.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolled_windowusersEncontrados.add(usersEncontrados)

		usersEncontradosBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		usersEncontradosBox.pack_start(scrolled_windowusersEncontrados, True, True, 0)

		insertarUser = Gtk.Button(label="Añadir >>")
		self.insertarUser = insertarUser
		eliminarUser = Gtk.Button(label="Eliminar")
		self.eliminarUser = eliminarUser
		botonesBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin=0)
		botonesBox.pack_start(insertarUser, False, False, 0)
		botonesBox.pack_start(eliminarUser, False, False, 0)

		usersSeleccionados = Gtk.ListBox()
		usersSeleccionados.set_selection_mode(Gtk.SelectionMode(3))
		self.usersSeleccionados = usersSeleccionados

		scrolled_windowusersSeleccionados = Gtk.ScrolledWindow()    #cuadro de texto
		scrolled_windowusersSeleccionados.set_propagate_natural_width(True)	
        # we scroll only if needed
		scrolled_windowusersSeleccionados.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolled_windowusersSeleccionados.add(usersSeleccionados)

		selec = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		selec.pack_start(scrolled_windowusersSeleccionados, True, True, 0)

		Etiq_horario = Gtk.Label(label = ("Horario:")) 
		Etiq_horarioBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		Etiq_horarioBox.pack_start(Etiq_horario, False, False, 0)

		Etiq_busqUsuario1 = Gtk.Label(label = ("Inicio")) 
		etiqueta1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		etiqueta1.pack_start(Etiq_busqUsuario1, False, False, 0)
		Etiq_busqUsuario2 = Gtk.Label(label = ("Fin")) 
		etiqueta2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		etiqueta2.pack_start(Etiq_busqUsuario2, False, False, 0)

		horaInicio = Gtk.SpinButton(adjustment=Gtk.Adjustment(0, 0, 23, 1, 3, 0), digits=0)
		self.horaInicio = horaInicio
		separacion1 = Gtk.Label(label = (":")) 
		minutosInicio = Gtk.SpinButton(adjustment=Gtk.Adjustment(0, 00, 59, 15, 15, 0), digits=0)
		minutosInicio.set_text('{:02d}'.format(int(minutosInicio.get_adjustment().get_value())))
		minutosInicio.connect('changed', self.ponerCeros)
		self.minutosInicio =  minutosInicio

		horaFin = Gtk.SpinButton(adjustment=Gtk.Adjustment(0, 0, 23, 1, 3, 0), digits=0)
		self.horaFin = horaFin
		separacion2 = Gtk.Label(label = (":")) 
		minutosFin = Gtk.SpinButton(adjustment=Gtk.Adjustment(0, 00, 59, 15, 15, 0), digits=0)
		minutosFin.set_text('{:02d}'.format(int(minutosInicio.get_adjustment().get_value())))
		minutosFin.connect('changed', self.ponerCeros)
		self.minutosFin = minutosFin

		hora_inicio = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		hora_inicio.pack_start(horaInicio, False, False, 0)
		hora_inicio.pack_start(separacion1, False, False, 0)
		hora_inicio.pack_start(minutosInicio, False, False, 0)

		hora_fin = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		hora_fin.pack_start(horaFin, False, False, 0)
		hora_fin.pack_start(separacion2, False, False, 0)
		hora_fin.pack_start(minutosFin, False, False, 0)

		Etiq_dias = Gtk.Label(label = ("Días:")) 
		Etiq_diasBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		Etiq_diasBox.pack_start(Etiq_dias, False, False, 0)
		
		diasEncontrados = Gtk.ListBox()
		diasEncontrados.set_selection_mode(Gtk.SelectionMode(3))
		self.diasEncontrados = diasEncontrados

		lunes = Gtk.ListBoxRow()
		martes = Gtk.ListBoxRow()
		miercoles = Gtk.ListBoxRow()
		jueves = Gtk.ListBoxRow()
		viernes = Gtk.ListBoxRow()
		sabado = Gtk.ListBoxRow()
		domingo = Gtk.ListBoxRow()
		check = Gtk.Label("Lunes")
		check1 = Gtk.Label("Martes")
		check2 = Gtk.Label("Miércoles")
		check3 = Gtk.Label("Jueves")
		check4 = Gtk.Label("Viernes")
		check5 = Gtk.Label("Sábado")
		check6 = Gtk.Label("Domingo")
		lunes.add(check)
		martes.add(check1)
		miercoles.add(check2)
		jueves.add(check3)
		viernes.add(check4)
		sabado.add(check5)
		domingo.add(check6)
		diasEncontrados.add(lunes)
		diasEncontrados.add(martes)
		diasEncontrados.add(miercoles)
		diasEncontrados.add(jueves)
		diasEncontrados.add(viernes)
		diasEncontrados.add(sabado)
		diasEncontrados.add(domingo)
		self.diasEncontrados = diasEncontrados

		scrolled_windowdias = Gtk.ScrolledWindow()    #cuadro de texto
		scrolled_windowdias.set_propagate_natural_width(True)	
        # we scroll only if needed
		scrolled_windowdias.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolled_windowdias.add(diasEncontrados)

		diasBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		diasBox.pack_start(scrolled_windowdias, True, True, 0)

		insertardias = Gtk.Button(label="Añadir >>")
		self.insertardias = insertardias
		eliminardias= Gtk.Button(label="Eliminar")
		self.eliminardias = eliminardias
		botonesDiasBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin=0)
		botonesDiasBox.pack_start(insertardias, False, False, 0)
		botonesDiasBox.pack_start(eliminardias, False, False, 0)

		liststore = Gtk.ListStore(str, str) #que contiene el filtro
		self.liststore = liststore

		filtro = liststore.filter_new() #Hace un filtrado de liststore. Crea otro liststore para aplicar el filtro
		self.filtro = filtro
		filtro.set_visible_func(self.aplicar_filtro_aux) #Filtra el liststore nuevo según lo que indique la función


		resumen = Gtk.TreeView(filtro, headers_visible=True) #Lista grupos
		#resumen.get_selection().set_mode(Gtk.SelectionMode(3))

		#Crear columna 1
		renderer_text = Gtk.CellRendererText()

		column_text1 = Gtk.TreeViewColumn(("Día"), renderer_text, text=0)

		#Crear columna 2
		renderer_text2 = Gtk.CellRendererText()
		column_text2 = Gtk.TreeViewColumn(("Horario"), renderer_text2, text=1)

		resumen.append_column(column_text1)
		resumen.append_column(column_text2)

		self.resumen = resumen

		ventana_scrollresumen = Gtk.ScrolledWindow(expand=True, margin=20)
		ventana_scrollresumen.set_size_request(400, 100)
		ventana_scrollresumen.add(resumen)

		botonesAceptado = Gtk.HBox(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		self.modificado = None
		self.aceptado = None
		if datos_grupo is not None: 
			modificado = Gtk.Button("Guardar")
			self.modificado = modificado
			botonAceptado = modificado
		else:
			aceptado = Gtk.Button("Guardar")
			self.aceptado = aceptado
			botonAceptado = aceptado
		cancelado = Gtk.Button("Cancelar")
		self.cancelado = cancelado
		botonesAceptado.pack_end(cancelado, False, False, 0)	
		botonesAceptado.set_center_widget(botonAceptado)

		if datos_grupo is not None:
			self.idgrupo = str(datos_grupo["id_grupo"])
			for i in range(len(datos_grupo["usuario"])):
				fila = Gtk.ListBoxRow()
				fila.add(Gtk.Label(datos_grupo["usuario"][i]))
				self.usersSeleccionados.add(fila)

			horarios = datos_grupo["horario"].split(",")
			for i in horarios:
				self.filtro.get_model().append([i.split(" ")[0], i.split(" ", 1)[1]])
			self.win.show_all()


		grid = Gtk.Grid(margin=30, column_spacing=10, row_spacing=10)  #colocacion de elementos anteriores
		self.grid = grid
		grid.attach(l1Box, 10, 0, 20, 1)
		grid.attach_next_to(busBox, l1Box, Gtk.PositionType.BOTTOM, 8, 1)
		grid.attach_next_to(usersEncontradosBox, busBox, Gtk.PositionType.BOTTOM, 5, 10)
		grid.attach_next_to(botonesBox, usersEncontradosBox, Gtk.PositionType.RIGHT, 1, 10)
		grid.attach_next_to(selec, botonesBox, Gtk.PositionType.RIGHT, 14, 10)
		grid.attach_next_to(usersSelec, selec, Gtk.PositionType.TOP, 14, 1)
		grid.attach_next_to(Etiq_horarioBox, usersEncontradosBox, Gtk.PositionType.BOTTOM, 1, 1)
		grid.attach_next_to(etiqueta1, Etiq_horarioBox, Gtk.PositionType.RIGHT, 1, 1)	
		grid.attach_next_to(hora_inicio, etiqueta1, Gtk.PositionType.BOTTOM, 8, 1)
		grid.attach_next_to(etiqueta2, hora_inicio, Gtk.PositionType.BOTTOM, 1, 1)
		grid.attach_next_to(hora_fin, etiqueta2, Gtk.PositionType.BOTTOM, 8, 1)
		grid.attach_next_to(diasBox, hora_fin, Gtk.PositionType.BOTTOM, 5, 10)
		grid.attach_next_to(Etiq_diasBox, diasBox, Gtk.PositionType.LEFT, 1, 1)
		grid.attach_next_to(botonesDiasBox, hora_inicio, Gtk.PositionType.RIGHT, 5, 3)
		grid.attach_next_to(ventana_scrollresumen, botonesDiasBox, Gtk.PositionType.RIGHT, 8, 10)
		grid.attach_next_to(botonesAceptado, diasBox, Gtk.PositionType.BOTTOM, 2, 1)
		
		self.win.add(grid)
		self.win.show_all()

	def ponerCeros(self, spin_button):
		if spin_button.get_adjustment().get_value() == 0:
			spin_button.set_text('{:02d}'.format(int(spin_button.get_adjustment().get_value())))
		self.win.show_all()	

	def AccionesEnElFormGrupo(self, controller):
		self.botonBusq.connect('clicked', controller.on_buscar_usuario)
		if self.aceptado is not None:
			self.aceptado.connect('clicked', controller.on_guardar_en_BD_grupos)
		else:
			self.modificado.connect('clicked', controller.on_actualizar_en_BD_grupos)
		self.cancelado.connect('clicked', controller.on_grupos)
		self.insertarUser.connect('clicked', controller.on_insertar_usuario, self.usersSeleccionados)
		self.eliminarUser.connect('clicked', controller.on_quitar_usuario)
		self.insertardias.connect('clicked', controller.on_insertar_dias)
		self.eliminardias.connect('clicked', controller.on_eliminar_dias)


	def datosAGuardarDeGrupos(self):
		if self.idgrupo != "":   #para diferenciar el caso de una actualizacion y una entrada nueva
			return (self.idgrupo, self.usersSeleccionados, self.resumen.get_model())
		else:
			return (self.usersSeleccionados, self.resumen.get_model())


	def resultadosUsuario(self, id, Apellidos, Nombre):
		resultado = Gtk.Label(str(id) + " - " + Nombre + " " + Apellidos)
		fila = Gtk.ListBoxRow()
		fila.add(resultado)
		self.usersEncontrados.add(fila)
		self.win.show_all()

	def nuevoHorario(self):
		diasSeleccionados = self.diasEncontrados.get_selected_rows()
		horaInicio = self.horaInicio.get_text()
		minutosInicio = self.minutosInicio.get_text()
		horaFinal = self.horaFin.get_text()
		minutosFinal = self.minutosFin.get_text()
		self.diasEncontrados.unselect_all()
		horario = str(horaInicio) + ":" + str(minutosInicio) + " - " + str(horaFinal) + ":" + str(minutosFinal)
		for i in diasSeleccionados:
			self.filtro.get_model().append([i.get_children()[0].get_label(), horario])

	def Emergente_eliminar_Grupo(self, controller, idgrupo):
		ventanaemergente = Gtk.MessageDialog(self.win, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, "\n¿Está seguro de que desea eliminar el grupo " + idgrupo + "?") 
		ventanaemergente.connect("response", controller.emergente_decision_grupo, idgrupo)
		ventanaemergente.run()
		ventanaemergente.destroy()

############################################################################################################################################SESIONES
	
	def sesion(self):
		win = self.win	#para borrar los atributos de la clase y ahorrar memoria
		self.__dict__.clear()
		self.win = win
		self.win.resize(1000,550)
		self.win.get_child().destroy() #destruimos elemetos de inicio

		Ini = Gtk.ToggleButton(label=("Inicio"))
		self.Ini = Ini
		Programacion = Gtk.ToggleButton(label=("Programación"))
		self.Programacion = Programacion
		Grupos = Gtk.ToggleButton(label=("Grupos"))
		self.Grupos = Grupos
		Usuarios = Gtk.ToggleButton(label=("Usuarios"))
		self.Usuarios = Usuarios
		Sesiones = Gtk.ToggleButton(label=("Sesiones"))
		self.Sesiones = Sesiones
		Ejercicios = Gtk.ToggleButton(label=("Ejercicios"))
		self.Ejercicios = Ejercicios
		self.Sesiones.set_active(True)

		links = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=10)  #barra navegacion
		links.pack_start(self.Ini, False, False, 0)
		links.pack_start(self.Programacion, False, False, 0)
		links.pack_start(self.Grupos, False, False, 0)
		links.pack_start(self.Usuarios, False, False, 0)
		links.pack_start(self.Sesiones, False, False, 0)
		links.pack_start(self.Ejercicios, False, False, 0)

		l1 = Gtk.Label()
		l1.set_markup("<big><b>Sesiones</b></big>")  #texto

		busqueda = Gtk.SearchEntry(width_chars=8)
		self.busqueda = busqueda
		Etiq_busqueda = Gtk.Label(label = ("Filtrar por nº de sesión:"))   #entrada para filtrar

		BusquedaUsers = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		BusquedaUsers.pack_start(Etiq_busqueda, False, False, 0)
		BusquedaUsers.pack_start(self.busqueda, True, True, 0)

		liststoreSesiones = Gtk.ListStore(str, str, str, str) #que contiene el filtro
		self.liststoreSesiones = liststoreSesiones

		filtroSesiones = liststoreSesiones.filter_new() #Hace un filtrado de liststore. Crea otro liststore para aplicar el filtro
		filtroSesiones.set_visible_func(self.aplicar_filtro_sesiones) #Filtra el liststore nuevo según lo que indique la función
		self.filtroSesiones = filtroSesiones
		self.filtroSesiones_inicio = ""

		SesionesTree = Gtk.TreeView(filtroSesiones, headers_visible=True) #Lista grupos

		#Crear columna x
		renderer_textx = Gtk.CellRendererText()
		column_textx = Gtk.TreeViewColumn(("Sesión"), renderer_textx, text=0)

		#Crear columna 0
		renderer_text = Gtk.CellRendererText()
		column_text0 = Gtk.TreeViewColumn(("Objetivos"), renderer_text, text=1)

		#Crear columna 1
		renderer_text1 = Gtk.CellRendererText()
		column_text1 = Gtk.TreeViewColumn(("Ejercicios"), renderer_text1, text=2)

		#Crear columna 2
		renderer_text2 = Gtk.CellRendererText()
		column_text2 = Gtk.TreeViewColumn(("Materiales"), renderer_text2, text=3)


		SesionesTree.append_column(column_textx)
		SesionesTree.append_column(column_text0)
		SesionesTree.append_column(column_text1)
		SesionesTree.append_column(column_text2)


		self.SesionesTree = SesionesTree

		ventana_scroll = Gtk.ScrolledWindow(expand=True, margin=20)
		ventana_scroll.set_size_request(400, 100)
		ventana_scroll.add(SesionesTree)

		VerMod = Gtk.Button(label=("Ver/Modificar"))
		self.VerMod = VerMod
		Eliminar = Gtk.Button(label=("Eliminar"))
		self.Eliminar = Eliminar

		botones = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=12)  #botones para utilizar con usuarios
		botones.pack_start(self.VerMod, False, False, 0)
		botones.pack_start(self.Eliminar, False, False, 0)

		SesionNuevo = Gtk.Button("Añadir nueva sesión")
		self.SesionNuevo = SesionNuevo

		sesionesGrid = Gtk.Grid(margin=5, column_spacing=5, row_spacing=10)  #colocacion de elementos anteriores
		sesionesGrid.attach(links, 0, 0, 1, 1)
		sesionesGrid.attach_next_to(l1, links, Gtk.PositionType.BOTTOM, 1, 1)
		sesionesGrid.attach_next_to(BusquedaUsers, l1, Gtk.PositionType.BOTTOM, 1, 1)
		sesionesGrid.attach_next_to(ventana_scroll, BusquedaUsers, Gtk.PositionType.BOTTOM, 20, 10)
		sesionesGrid.attach_next_to(botones, ventana_scroll, Gtk.PositionType.BOTTOM, 1, 1)
		sesionesGrid.attach_next_to(SesionNuevo, botones, Gtk.PositionType.RIGHT, 1, 1)

		self.VerMod.set_sensitive(False)
		self.Eliminar.set_sensitive(False)
		self.SesionNuevo.set_sensitive(True)

		self.win.add(sesionesGrid)
		self.win.show_all()


	def aplicar_filtro_sesiones(self, conjunto, iter, data):
		if self.filtroSesiones_inicio == "":	
			return True
		else:
			return (((conjunto[iter][0]).startswith(self.filtroSesiones_inicio))) #Filtrar nº de sesion

	def filtro_cambiadoses(self, entrada):
		self.filtroSesiones_inicio = entrada.get_text()
		self.SesionesTree.get_model().refilter()  #esta funcion controla que se cambia el texto del filtro

	def clickSesiones(self, controller):
		self.SesionNuevo.connect("clicked", controller.on_NuevaSesion)
		self.SesionesTree.get_selection().connect("changed", controller.activar_botonesSesion) #si seleccionas una sesion
		self.busqueda.connect('changed', self.filtro_cambiadoses)

	def clickSobreSesiones(self, controller):
		self.Eliminar.connect("clicked", controller.on_eliminar_sesion)
		self.VerMod.connect("clicked", controller.on_ActualizarSesion)

	def Emergente_eliminar_Sesion(self, controller, idsesion):
		ventanaemergente = Gtk.MessageDialog(self.win, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, "\n¿Está seguro de que desea eliminar la sesión " + str(idsesion) + "?") 
		ventanaemergente.connect("response", controller.emergente_decision_sesion, idsesion)
		ventanaemergente.run()
		ventanaemergente.destroy()

	def Formulario_Sesion(self, controller, datos_sesion, ejercicios_guardados):
		win = self.win	#para borrar los atributos de la clase y ahorrar memoria
		self.__dict__.clear()
		self.win = win
		self.win.get_child().destroy() #destruimos ventana de inicio
		l1 = Gtk.Label()
		l1.set_markup("<big><b>Formulario de Sesión</b></big>")  #texto
		l1Box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		l1Box.pack_start(l1, False, False, 0)

		self.idsesion = ""
		scrolled_window = Gtk.ScrolledWindow(expand=False)    #cuadro de texto
		scrolled_window.set_border_width(5)	
        # we scroll only if needed
		scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        # a text buffer (stores text)
		Objetivos = Gtk.TextBuffer()
		self.Objetivos = Objetivos

        # a textview (displays the buffer)
		textview = Gtk.TextView(buffer=Objetivos)

        # textview is scrolled
		scrolled_window.add(textview)

		Etiq_Objetivos = Gtk.Label(label = ("Objetivos:")) 
		ObjetivosBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		ObjetivosBox.pack_start(Etiq_Objetivos, False, False, 0)
		ObjetivosBox.pack_start(scrolled_window, True, True, 0)

		Etiq_ejerciciosSesion = Gtk.Label(label = ("Ejercicio: ")) 
		añadirejercicio = Gtk.Button("Añadir")
		self.añadirejercicio= añadirejercicio
		eliminarejercicio = Gtk.Button("Eliminar")
		self.eliminarejercicio= eliminarejercicio
		Etiq_materialesSesion = Gtk.Label(label = ("Materiales:")) 
		ejercicios = []
		boxEngadir = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5, margin=0)
		boxEngadir.pack_start(añadirejercicio, False, False, 0)
		boxEngadir.pack_start(eliminarejercicio, False, False, 0)
		boxmaterial = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5, margin=0)
		boxmaterial.pack_start(Etiq_materialesSesion, False, False, 0)

		mat = Gtk.ListStore(str)   #introducimos la lista de ejercicios en el menú desplegable
		for i in ejercicios_guardados:
			mat.append([i["nombre_ejercicio"]])
		añadirEjericicioEntrada = Gtk.ComboBoxText(model = mat)
		self.añadirEjericicioEntrada = añadirEjericicioEntrada
		ejerciciosBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5, margin=0)
		ejerciciosBox.pack_start(Etiq_ejerciciosSesion, False, False, 0)
		ejerciciosBox.pack_start(añadirEjericicioEntrada, True, True, 0)
		self.ejerciciosBox = ejerciciosBox

		ejerciciosSeleccionados = Gtk.ListBox()
		ejerciciosSeleccionados.set_selection_mode(Gtk.SelectionMode(3))
		self.ejerciciosSeleccionados = ejerciciosSeleccionados

		scrolled_windowusersEncontrados = Gtk.ScrolledWindow()    #cuadro de texto
		scrolled_windowusersEncontrados.set_propagate_natural_width(True)	
        # we scroll only if needed
		scrolled_windowusersEncontrados.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolled_windowusersEncontrados.add(ejerciciosSeleccionados)

		materialesUtilizados = Gtk.ListBox()
		materialesUtilizados.set_selection_mode(Gtk.SelectionMode(0))
		self.materialesUtilizados = materialesUtilizados

		scrolled_windowusersMateriales = Gtk.ScrolledWindow()    #cuadro de texto
		scrolled_windowusersMateriales.set_propagate_natural_width(True)	
        # we scroll only if needed
		scrolled_windowusersMateriales.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolled_windowusersMateriales.add(materialesUtilizados)

		ejerciciosSeleccionadosBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=40, margin=0)
		ejerciciosSeleccionadosBox.pack_start(scrolled_windowusersEncontrados, True, True, 0)
		ejerciciosSeleccionadosBox.pack_start(scrolled_windowusersMateriales, True, True, 0)


		Etiq_materialesSesion = Gtk.Label(label = ("Suma de cargas:")) 
		box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.box = box

		self.CambiarGraficaVista(0, 0, 0, 0)


		incompatibilidades_label = Gtk.Label(label = ("incompatibilidades:")) 

		incompatibilidades = Gtk.ListBox()
		incompatibilidades.set_selection_mode(Gtk.SelectionMode(0))
		self.incompatibilidades = incompatibilidades

		scrolled_windowusersincompatibilidades = Gtk.ScrolledWindow()    #cuadro de texto
		scrolled_windowusersincompatibilidades.set_propagate_natural_width(True)	
        # we scroll only if needed
		scrolled_windowusersincompatibilidades.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolled_windowusersincompatibilidades.add(incompatibilidades)

		incompBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1, margin=0)
		incompBox.pack_start(incompatibilidades_label, False, False, 0)
		incompBox.pack_start(scrolled_windowusersincompatibilidades, True, True, 10)

		botonesAceptado = Gtk.HBox(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		self.modificado = None
		self.aceptado = None
		if datos_sesion is not None: 
			modificado = Gtk.Button("Guardar")
			self.modificado = modificado
			botonAceptado = modificado
		else:
			aceptado = Gtk.Button("Guardar")
			self.aceptado = aceptado
			botonAceptado = aceptado
		cancelado = Gtk.Button("Cancelar")
		self.cancelado = cancelado
		botonesAceptado.pack_end(cancelado, False, False, 0)	
		botonesAceptado.set_center_widget(botonAceptado)

		if datos_sesion is not None:
			self.idsesion = str(datos_sesion["id_sesion"])
			for i in range(len(datos_sesion["ejercicio"])):
				controller.ejercicioNuevo(None, self.ejerciciosSeleccionados, datos_sesion["ejercicio"][i])
			self.Objetivos.set_text(datos_sesion["objetivos"])


		grid = Gtk.Grid(margin=20, column_spacing=10, row_spacing=10)  #colocacion de elementos anteriores
		self.grid = grid
		grid.attach(l1Box, 0, 0, 10, 2)
		grid.attach_next_to(ObjetivosBox, l1Box, Gtk.PositionType.BOTTOM, 80, 10)
		grid.attach_next_to(ejerciciosBox, ObjetivosBox, Gtk.PositionType.BOTTOM, 4, 1)
		grid.attach_next_to(boxEngadir, ejerciciosBox, Gtk.PositionType.BOTTOM, 14, 1)
		grid.attach_next_to(boxmaterial, boxEngadir, Gtk.PositionType.RIGHT, 1, 1)
		grid.attach_next_to(ejerciciosSeleccionadosBox, boxEngadir, Gtk.PositionType.BOTTOM, 40, 15)
		grid.attach_next_to(self.box, ejerciciosSeleccionadosBox, Gtk.PositionType.RIGHT, 40, 30)
		grid.attach_next_to(incompBox, ejerciciosSeleccionadosBox, Gtk.PositionType.BOTTOM, 41, 15)
		grid.attach_next_to(botonesAceptado, incompBox, Gtk.PositionType.BOTTOM, 2, 1)
		

		self.win.add(grid)	
		self.win.show_all()


	def CambiarGraficaVista(self, aero, coord, equi, frz):
		cargas = 'Aeróbico', 'Coordinación', 'Equilibrio', 'Fuerza'
		self.cargas = cargas
		porcentajes = [aero, coord, equi, frz]
		if len(self.box.get_children()) != 0 :
			self.box.get_children()[0].destroy()
			self.box.remove(self.box.get_children()[0])
		if not (aero == 0 and coord == 0 and equi == 0 and frz == 0):
			figureObject, axesObject = plotter.subplots()
			axesObject.pie(porcentajes,labels=cargas,autopct='%1.2f',startangle=90)
			axesObject.axis('equal')  
			self.axesObject = axesObject
			canvas = FigureCanvas(figureObject)
			plotter.figure(figsize=[100,100])
			self.cargas = str(aero) + "% /" + str(coord) + "% /" + str(equi) + "% /" + str(frz) + "%"
			self.box.pack_start(canvas, True, True, 0)
			self.win.show_all()


	def AccionesEnElFormSesion(self, controller):
		self.añadirejercicio.connect('clicked', controller.ejercicioNuevo, self.ejerciciosSeleccionados, None)
		self.eliminarejercicio.connect('clicked', controller.eliminarejerc)
		if self.aceptado is not None:
			self.aceptado.connect('clicked', controller.on_guardar_en_BD_sesiones)
		else:
			self.modificado.connect('clicked', controller.on_actualizar_en_BD_sesiones)
		self.cancelado.connect('clicked', controller.on_sesiones)

	def datosAGuardarDeSesiones(self):
		if self.idsesion != "":   #para diferenciar el caso de una actualizacion y una entrada nueva
			return (self.idsesion, self.Objetivos, self.ejerciciosSeleccionados, self.cargas, self.materialesUtilizados)
		else:
			return (self.Objetivos, self.ejerciciosSeleccionados, self.cargas, self.materialesUtilizados)


#############################################################################################################################################################

	def programacion(self):
		win = self.win	#para borrar los atributos de la clase y ahorrar memoria
		self.__dict__.clear()
		self.win = win
		self.win.resize(1000,550)
		self.win.get_child().destroy() #destruimos elemetos de inicio

		Ini = Gtk.ToggleButton(label=("Inicio"))
		self.Ini = Ini
		Programacion = Gtk.ToggleButton(label=("Programación"))
		self.Programacion = Programacion
		self.Programacion.set_active(True)
		Grupos = Gtk.ToggleButton(label=("Grupos"))
		self.Grupos = Grupos
		Usuarios = Gtk.ToggleButton(label=("Usuarios"))
		self.Usuarios = Usuarios
		Sesiones = Gtk.ToggleButton(label=("Sesiones"))
		self.Sesiones = Sesiones
		Ejercicios = Gtk.ToggleButton(label=("Ejercicios"))
		self.Ejercicios = Ejercicios

		links = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=10)  #barra navegacion
		links.pack_start(self.Ini, False, False, 0)
		links.pack_start(self.Programacion, False, False, 0)
		links.pack_start(self.Grupos, False, False, 0)
		links.pack_start(self.Usuarios, False, False, 0)
		links.pack_start(self.Sesiones, False, False, 0)
		links.pack_start(self.Ejercicios, False, False, 0)

		l1 = Gtk.Label()
		l1.set_markup("<big><b>Programación de Sesiones</b></big>")  #texto

		liststoreProg = Gtk.ListStore(str, str, str, str, str) #que contiene el filtro
		self.liststoreProg= liststoreProg

		filtroProg = liststoreProg.filter_new() #Hace un filtrado de liststore. Crea otro liststore para aplicar el filtro
		filtroProg.set_visible_func(self.aplicar_filtro_prog) #Filtra el liststore nuevo según lo que indique la función
		self.filtroProg = filtroProg
		self.Aux1 = False
		self.Aux2 = False
		self.filtroProg_inicio1 = ""
		self.filtroProg_inicio2 = ""

		busqueda = Gtk.SearchEntry(width_chars=8)
		busqueda.set_placeholder_text("Id sesión")
		self.busqueda = busqueda

		busqueda2 = Gtk.SearchEntry(width_chars=8)
		busqueda2.set_placeholder_text("Id grupo")
		self.busqueda2 = busqueda2

		checkHechas = Gtk.CheckButton("Mostrar hechas")
		self.checkHechas = checkHechas
		checkProximas = Gtk.CheckButton("Mostrar próximas")
		self.checkProximas = checkProximas
		checks = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin=10)
		checks.pack_start(self.checkHechas, True, True, 0)
		checks.pack_start(self.checkProximas, True, True, 0)

		BusquedaUsers = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		BusquedaUsers.pack_start(self.busqueda, True, True, 0)
		BusquedaUsers.pack_start(self.busqueda2, True, True, 0)

		prog = Gtk.TreeView(filtroProg, headers_visible=True) #Lista grupos

		#Crear columna 3
		renderer_text3 = Gtk.CellRendererText()
		column_text3 = Gtk.TreeViewColumn(("Sesión programada"), renderer_text3, text=0)

		#Crear columna x
		renderer_textx = Gtk.CellRendererText()
		column_textx = Gtk.TreeViewColumn(("Sesión"), renderer_textx, text=1)

		#Crear columna 0
		renderer_text = Gtk.CellRendererText()
		column_text0 = Gtk.TreeViewColumn(("Fecha"), renderer_text, text=2)

		#Crear columna 1
		renderer_text1 = Gtk.CellRendererText()
		column_text1 = Gtk.TreeViewColumn(("Grupo"), renderer_text1, text=3)

		#Crear columna 2
		renderer_text2 = Gtk.CellRendererText()
		column_text2 = Gtk.TreeViewColumn(("Descripción"), renderer_text2, text=4)

		prog.append_column(column_text3)
		prog.append_column(column_textx)
		prog.append_column(column_text0)
		prog.append_column(column_text1)
		prog.append_column(column_text2)

		self.prog = prog

		ventana_scroll = Gtk.ScrolledWindow(expand=True, margin=20)
		ventana_scroll.set_size_request(400, 100)
		ventana_scroll.add(prog)

		VerMod = Gtk.Button(label=("Ver/Modificar"))
		self.VerMod = VerMod
		Eliminar = Gtk.Button(label=("Eliminar"))
		self.Eliminar = Eliminar
		postsesion = Gtk.Button(label=("Comentarios post-sesión"))
		self.postsesion = postsesion

		botones = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=12)  #botones para utilizar con usuarios
		botones.pack_start(self.VerMod, False, False, 0)
		botones.pack_start(self.Eliminar, False, False, 0)
		botones.pack_start(self.postsesion, False, False, 0)

		ProgNuevo = Gtk.Button("Añadir nueva sesión programada")
		self.ProgNuevo = ProgNuevo

		progGrid = Gtk.Grid(margin=5, column_spacing=5, row_spacing=10)  #colocacion de elementos anteriores
		progGrid.attach(links, 0, 0, 1, 1)
		progGrid.attach_next_to(l1, links, Gtk.PositionType.BOTTOM, 1, 1)
		progGrid.attach_next_to(BusquedaUsers, l1, Gtk.PositionType.BOTTOM, 1, 1)
		progGrid.attach_next_to(ventana_scroll, BusquedaUsers, Gtk.PositionType.BOTTOM, 3, 8)
		progGrid.attach_next_to(checks, ventana_scroll, Gtk.PositionType.RIGHT, 1, 1)
		progGrid.attach_next_to(botones, ventana_scroll, Gtk.PositionType.BOTTOM, 1, 1)
		progGrid.attach_next_to(ProgNuevo, botones, Gtk.PositionType.RIGHT, 1, 1)

		self.VerMod.set_sensitive(False)
		self.Eliminar.set_sensitive(False)
		self.postsesion.set_sensitive(False)
		self.ProgNuevo.set_sensitive(True)

		self.win.add(progGrid)
		self.win.show_all()

	def aplicar_filtro_prog(self, conjunto, iter, data):
		if self.Aux1 and self.Aux2:
			return True
		if self.Aux1:
			return self.on_proximas(None, conjunto, iter)
		if self.Aux2:
			return self.on_Hechas(None, conjunto, iter)
		if self.filtroProg_inicio1 == "" and self.filtroProg_inicio2 == "":	
			return True
		elif self.filtroProg_inicio1 == "":															#Filtrar por id sesion o id grupo
			return ((conjunto[iter][3]).startswith(self.filtroProg_inicio2))
		else:
			return (((conjunto[iter][1]).startswith(self.filtroProg_inicio1)))


	def clickProgramacion(self, controller):
		self.ProgNuevo.connect("clicked", controller.on_NuevaProg)
		self.busqueda.connect('changed', self.filtro_cambiado1)
		self.busqueda2.connect('changed', self.filtro_cambiado2)
		self.prog.get_selection().connect("changed", controller.activar_botonesProg) #si seleccionas una sesion programada
		self.checkProximas.connect("toggled", self.refiltrar)
		self.checkHechas.connect("toggled", self.refiltrar)

	def refiltrar(self, boton):
		self.Aux1 = self.checkProximas.get_active()
		self.Aux2 = self.checkHechas.get_active()
		self.prog.get_model().refilter()

	def on_proximas(self, boton, conjunto, iter):
		if self.checkProximas.get_active():
			today = date.today()
			dia = today.strftime("%d")
			mes = today.strftime("%m")
			ano = today.strftime("%Y")
			fechaHoy = date(int(ano), int(mes), int(dia))
			diaGuardado = conjunto[iter][2].split("/", 1)[0]
			mesGuardado = conjunto[iter][2].split("/", 1)[1].split("/")[0]
			anoGuardado = conjunto[iter][2].split("/", 2)[2]
			fecha = date(int(anoGuardado), int(mesGuardado), int(diaGuardado))
			return (fecha >= fechaHoy)

	def on_Hechas(self, boton, conjunto, iter):
		if self.checkHechas.get_active():
			today = date.today()
			dia = today.strftime("%d")
			mes = today.strftime("%m")
			ano = today.strftime("%Y")
			fechaHoy = date(int(ano), int(mes), int(dia))
			diaGuardado = conjunto[iter][2].split("/", 1)[0]
			mesGuardado = conjunto[iter][2].split("/", 1)[1].split("/")[0]
			anoGuardado = conjunto[iter][2].split("/", 2)[2]
			fecha = date(int(anoGuardado), int(mesGuardado), int(diaGuardado))

			return (fecha <= fechaHoy)

	def clickSobreProg(self, controller):
		self.VerMod.connect("clicked", controller.on_ActualizarProg)
		self.Eliminar.connect("clicked", controller.on_eliminar_prog)
		self.postsesion.connect("clicked", controller.on_postsesion_prog)

	def filtro_cambiado1(self, entrada):
		self.filtroProg_inicio1 = entrada.get_text()
		self.prog.get_model().refilter()  #esta funcion controla que se cambia el texto del filtro

	def filtro_cambiado2(self, entrada):
		self.filtroProg_inicio2 = entrada.get_text()
		self.prog.get_model().refilter()  #esta funcion controla que se cambia el texto del filtro

	def Formulario_Prog(self, grupos, materiales, datos_prog, usuarios_prog, controller):
		win = self.win	#para borrar los atributos de la clase y ahorrar memoria
		self.__dict__.clear()
		self.win = win
		self.win.get_child().destroy() #destruimos ventana de inicio
		l1 = Gtk.Label()
		l1.set_markup("<big><b>Programación de Sesión</b></big>")  #texto
		l1Box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		l1Box.pack_start(l1, False, False, 0)

		self.idprog = None
		etiq2 = Gtk.Label()
		etiq2.set_markup("<i>Busque por nº de grupo o por nombre/apellidos de usuario:</i>")
		etiq2Box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5, margin=0)
		etiq2Box.pack_start(etiq2, False, False, 0)

		mat = Gtk.ListStore(str)   #introducimos la lista de grupos en el menú desplegable
		for i in grupos:
			mat.append([str(i["id_grupo"])])
		grupoSelec = Gtk.ComboBoxText(model = mat)
		self.grupoSelec = grupoSelec

		busqUsuario = Gtk.SearchEntry(width_chars=8)
		busqUsuario.set_placeholder_text("Nombre/Apellidos")
		busqUsuario.set_width_chars(20)
		self.busqUsuario = busqUsuario
		Etiq_busqUsuario = Gtk.Label(label = ("Grupo nº:")) 
		botonBusq = Gtk.Button(label="Buscar usuarios")
		self.botonBusq = botonBusq
		busBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		busBox.pack_start(Etiq_busqUsuario, False, False, 0)
		busBox.pack_start(grupoSelec, False, False, 0)
		busBox.pack_start(busqUsuario, False, False, 0)
		busBox.pack_start(botonBusq, False, False, 0)

		etiq = Gtk.Label()
		etiq.set_markup("<i>Usuario seleccionados:</i>")
		usersSelec = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5, margin=0)
		usersSelec.pack_start(etiq, False, False, 0)

		usersEncontrados = Gtk.ListBox()
		usersEncontrados.set_selection_mode(Gtk.SelectionMode(3))
		self.usersEncontrados = usersEncontrados

		scrolled_windowusersEncontrados = Gtk.ScrolledWindow()    #cuadro de texto
		scrolled_windowusersEncontrados.set_propagate_natural_width(True)	
        # we scroll only if needed
		scrolled_windowusersEncontrados.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolled_windowusersEncontrados.add(usersEncontrados)

		usersEncontradosBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		usersEncontradosBox.pack_start(scrolled_windowusersEncontrados, True, True, 0)

		insertarUser = Gtk.Button(label="Añadir >>")
		self.insertarUser = insertarUser
		eliminarUser = Gtk.Button(label="Eliminar")
		self.eliminarUser = eliminarUser
		botonesBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5, margin=0)
		botonesBox.pack_start(insertarUser, False, False, 0)
		botonesBox.pack_start(eliminarUser, False, False, 0)

		usersSeleccionados = Gtk.ListBox()
		usersSeleccionados.set_selection_mode(Gtk.SelectionMode(3))
		self.usersSeleccionados = usersSeleccionados

		scrolled_windowusersSeleccionados = Gtk.ScrolledWindow()    #cuadro de texto
		scrolled_windowusersSeleccionados.set_propagate_natural_width(True)	
        # we scroll only if needed
		scrolled_windowusersSeleccionados.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolled_windowusersSeleccionados.add(usersSeleccionados)
		
		calendario = Gtk.Calendar()
		self.calendario = calendario

		selec = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5, margin=0)
		selec.pack_start(scrolled_windowusersSeleccionados, True, True, 0)

		calendarioBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1, margin=0)
		calendarioBox.pack_start(calendario, False, False, 0)		

		etiq1 = Gtk.Label()
		etiq1.set_markup("<i>Búsqueda de sesiones:</i>")
		etiq1Box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		etiq1Box.pack_start(etiq1, False, False, 0)

		store = Gtk.TreeStore(str, bool)
		# add row
		row1 = store.append(None, ['Materiales', False])
		 #add child rows
		for i in materiales:
			store.append(row1,[i, False])
      	 # add another row
		row2 = store.append(None, ['Aeróbico', False])
		i=0
		while i <= 100:
			store.append(row2,[">=" + str(i) + "%", False])
			i+=10
		row3 = store.append(None, ['Equilibrio', False])
		i=0
		while i <= 100:
			store.append(row3,[">=" + str(i) + "%", False])
			i+=10
		row4 = store.append(None, ['Coordinación', False])
		i=0
		while i <= 100:
			store.append(row4,[">=" + str(i) + "%", False])
			i+=10
		row5 = store.append(None, ['Fuerza', False])
		i=0
		while i <= 100:
			store.append(row5,[">=" + str(i) + "%", False])
			i+=10

		self.store = store
		treeview = Gtk.TreeView(store)
		tvcolumn = Gtk.TreeViewColumn('Filtro')
		treeview.append_column(tvcolumn)
		tvcolumn2 = Gtk.TreeViewColumn('aplicar')
		treeview.append_column(tvcolumn2)

		cell = Gtk.CellRendererText()
		tvcolumn.pack_start(cell, True)
		tvcolumn.add_attribute(cell, 'text', 0)
		cell2 = Gtk.CellRendererToggle()
		tvcolumn2.pack_start(cell2, True)
		tvcolumn2.add_attribute(cell2, 'active', 1)
		self.cell2 = cell2

		scrolled_windowfiltro = Gtk.ScrolledWindow()    #cuadro de texto
		scrolled_windowfiltro.set_propagate_natural_width(True)	
        # we scroll only if needed
		scrolled_windowfiltro.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolled_windowfiltro.add(treeview)

		filtro = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		filtro.pack_start(scrolled_windowfiltro, True, True, 0)

		sesionResultante = Gtk.ListBox()
		sesionResultante.set_selection_mode(Gtk.SelectionMode(2))
		self.sesionResultante = sesionResultante

		scrolled_windowsesionResultante= Gtk.ScrolledWindow()    #cuadro de texto
		scrolled_windowsesionResultante.set_propagate_natural_width(True)	
        # we scroll only if needed
		scrolled_windowsesionResultante.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolled_windowsesionResultante.add(sesionResultante)

		insertarFiltro = Gtk.Button(label="Mostrar sesiones >>")
		self.insertarFiltro = insertarFiltro
		etiq3 = Gtk.Label()
		etiq3.set_markup("<i>Seleccione una sesión:</i>")
		botonesFiltroBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin=0)
		botonesFiltroBox.pack_start(insertarFiltro, False, False, 0)
		botonesFiltroBox.pack_start(etiq3, False, False, 0)

		resumenSesion = Gtk.Notebook()
		resumenSesion.set_tab_pos(Gtk.PositionType.TOP)

		objBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin=0)
		scrolled_windowObj = Gtk.ScrolledWindow(expand=False)    #cuadro de texto
		scrolled_windowObj.set_border_width(5)	
        # we scroll only if needed
		scrolled_windowObj.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        # a text buffer (stores text)
		Objetivos = Gtk.TextBuffer()
		self.Objetivos = Objetivos
        # a textview (displays the buffer)
		textviewObj = Gtk.TextView(buffer=Objetivos)
		textviewObj.set_editable(False)
        # textview is scrolled
		scrolled_windowObj.add(textviewObj)
		objBox.pack_start(scrolled_windowObj, False, False, 0)

		matBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin=0)
		scrolled_windowMat = Gtk.ScrolledWindow(expand=False)    #cuadro de texto
		scrolled_windowMat.set_border_width(5)	
        # we scroll only if needed
		scrolled_windowMat.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        # a text buffer (stores text)
		Materiales = Gtk.TextBuffer()
		self.Materiales = Materiales
        # a textview (displays the buffer)
		textviewMat = Gtk.TextView(buffer=Materiales)
		textviewMat.set_editable(False)
        # textview is scrolled
		scrolled_windowMat.add(textviewMat)
		matBox.pack_start(scrolled_windowMat, False, False, 0)

		ejeBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin=0)
		scrolled_windowEje = Gtk.ScrolledWindow(expand=False)    #cuadro de texto
		scrolled_windowEje.set_border_width(5)	
        # we scroll only if needed
		scrolled_windowEje.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        # a text buffer (stores text)
		Ejercicios = Gtk.TextBuffer()
		self.Ejercicios = Ejercicios
        # a textview (displays the buffer)
		textviewEje = Gtk.TextView(buffer=Ejercicios)
		textviewEje.set_editable(False)
        # textview is scrolled
		scrolled_windowEje.add(textviewEje)
		ejeBox.pack_start(scrolled_windowEje, False, False, 0)


		resumenSesion.append_page(objBox)
		resumenSesion.set_tab_label_text(objBox, "Objetivos")
		resumenSesion.append_page(matBox)
		resumenSesion.set_tab_label_text(matBox, "Materiales")
		resumenSesion.append_page(ejeBox)
		resumenSesion.set_tab_label_text(ejeBox, "Ejercicios")

		etiq3 = Gtk.Label()
		etiq3.set_markup("<i>Rellene las duraciones indicando su unidad (min ó s).</i>")
		etiq3Box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		etiq3Box.pack_start(etiq3, False, False, 0)

		conjunto = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=0)
		conjunto.pack_start(botonesFiltroBox, False, False, 0)
		conjunto.pack_start(scrolled_windowsesionResultante, True, True, 0)
		conjunto.pack_start(resumenSesion, True, True, 0)

		vueltas = Gtk.Label("Vueltas:")
		vueltas1 = Gtk.Entry(width_chars=5)
		self.vueltas1 = vueltas1
		calent = Gtk.Label("Calentamiento:")
		calent1 = Gtk.Entry(width_chars=6)
		self.calent1 = calent1
		calent1.set_placeholder_text(("min/s"))
		descanso = Gtk.Label("Descanso:")
		descanso1 = Gtk.Entry(width_chars=6)
		self.descanso1 = descanso1
		descanso1.set_placeholder_text(("min/s"))
		duracion = Gtk.Label("Duración ejercicio:")
		duracion1 = Gtk.Entry(width_chars=6)
		self.duracion1 = duracion1
		duracion1.set_placeholder_text(("min/s"))
		reposo = Gtk.Label("Reposo:")
		reposo1 = Gtk.Entry(width_chars=6)
		self.reposo1 = reposo1
		reposo1.set_placeholder_text(("min/s"))
		total = Gtk.Label("Tiempo de la sesión:")
		tiempoTotal = Gtk.Label()
		self.tiempoTotal = tiempoTotal

		duraciones = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
		duraciones.pack_start(vueltas, False, False, 0)
		duraciones.pack_start(vueltas1, False, False, 0)
		duraciones.pack_start(calent, False, False, 0)
		duraciones.pack_start(calent1, False, False, 0)
		duraciones.pack_start(descanso, False, False, 0)
		duraciones.pack_start(descanso1, False, False, 0)
		duraciones.pack_start(duracion, False, False, 0)
		duraciones.pack_start(duracion1, False, False, 0)
		duraciones.pack_start(reposo, False, False, 0)
		duraciones.pack_start(reposo1, False, False, 0)
		duraciones.pack_start(total, False, False, 0)
		duraciones.pack_start(tiempoTotal, False, False, 0)

		botonesAceptado = Gtk.HBox(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		self.modificado = None
		self.aceptado = None
		if datos_prog is not None: 
			modificado = Gtk.Button("Guardar")
			self.modificado = modificado
			botonAceptado = modificado
		else:
			aceptado = Gtk.Button("Guardar")
			self.aceptado = aceptado
			botonAceptado = aceptado
		cancelado = Gtk.Button("Cancelar")
		self.cancelado = cancelado
		botonesAceptado.pack_end(cancelado, False, False, 0)	
		botonesAceptado.set_center_widget(botonAceptado)

		if datos_prog is not None: 
			self.idprog = datos_prog["id_prog"]
			modelo = grupoSelec.get_model()
			for i in range(len(modelo)):
				if str(modelo[i][0]) == str(datos_prog["id_grupo"]):
					grupoSelec.set_active(i)

			for i in range(len(usuarios_prog)):
				fila = Gtk.ListBoxRow()
				fila.add(Gtk.Label(usuarios_prog[i]))
				self.usersSeleccionados.add(fila)
			

			dia = datos_prog["fecha"].split("/", 1)[0]
			month= datos_prog["fecha"].split("/", 1)[1].split("/")[0]
			ano = datos_prog["fecha"].split("/", 2)[2]
			calendario.select_month(int(month)-1, int(ano))
			calendario.select_day(int(dia))
			fila = Gtk.ListBoxRow()
			fila.add(Gtk.Label(str(datos_prog["id_sesion"])))
			sesionResultante.add(fila)	
			sesionResultante.select_row(fila)
			controller.on_sesionElegida(None, fila)
			vueltas1.set_text(str(datos_prog["vueltas"]))
			calent1.set_text(str(datos_prog["calentamiento"]))
			descanso1.set_text(str(datos_prog["descanso"]))
			duracion1.set_text(str(datos_prog["ejercicio"]))
			reposo1.set_text(str(datos_prog["reposo"]))

		grid = Gtk.Grid(margin=25, column_spacing=10, row_spacing=10)  #colocacion de elementos anteriores
		self.grid = grid
		grid.attach(l1Box, 10, 0, 11, 1)
		grid.attach_next_to(etiq2Box, l1Box, Gtk.PositionType.BOTTOM, 10, 1)
		grid.attach_next_to(busBox, etiq2Box, Gtk.PositionType.BOTTOM, 6, 1)
		grid.attach_next_to(usersEncontradosBox, busBox, Gtk.PositionType.BOTTOM, 5, 10)
		grid.attach_next_to(botonesBox, usersEncontradosBox, Gtk.PositionType.RIGHT, 1, 5)
		grid.attach_next_to(selec, botonesBox, Gtk.PositionType.RIGHT, 5, 10)
		grid.attach_next_to(usersSelec, selec, Gtk.PositionType.TOP, 5, 1)
		grid.attach_next_to(calendarioBox, selec, Gtk.PositionType.BOTTOM, 2, 6)
		grid.attach_next_to(etiq1Box, usersEncontradosBox, Gtk.PositionType.BOTTOM, 1, 1)
		grid.attach_next_to(filtro, etiq1Box, Gtk.PositionType.BOTTOM, 5, 6)
		grid.attach_next_to(conjunto, filtro, Gtk.PositionType.BOTTOM, 11, 12)
		grid.attach_next_to(etiq3Box, conjunto, Gtk.PositionType.BOTTOM, 10, 1)
		grid.attach_next_to(duraciones, etiq3Box, Gtk.PositionType.BOTTOM, 10, 1)		
		grid.attach_next_to(botonesAceptado, duraciones, Gtk.PositionType.BOTTOM, 2, 1)
		
		self.win.add(grid)
		self.win.show_all()

	def AccionesEnElFormProg(self, controller):
		controller.on_sumaTiempo(None)
		self.botonBusq.connect('clicked', controller.on_buscar_usuario)
		if self.aceptado is not None:
			self.aceptado.connect('clicked', controller.on_guardar_en_BD_prog)
		else:
			self.modificado.connect('clicked', controller.on_actualizar_en_BD_prog)
		self.insertarUser.connect('clicked', controller.on_insertar_usuario, self.usersSeleccionados)
		self.eliminarUser.connect('clicked', controller.on_quitar_usuario)
		self.cell2.connect('toggled', controller.on_filtrar)
		self.insertarFiltro.connect('clicked', controller.on_buscar_sesiones)
		self.cancelado.connect('clicked', controller.on_programacion)
		self.sesionResultante.connect('row-selected', controller.on_sesionElegida)
		
		self.vueltas1.connect('changed', controller.on_sumaTiempo)
		self.calent1.connect('changed', controller.on_sumaTiempo)
		self.descanso1.connect('changed', controller.on_sumaTiempo)
		self.duracion1.connect('changed', controller.on_sumaTiempo)
		self.reposo1.connect('changed', controller.on_sumaTiempo)

	def datosAGuardarDeProg(self):
		if self.idprog != None:   #para diferenciar el caso de una actualizacion y una entrada nueva
			return (str(self.idprog), self.sesionResultante.get_selected_row(), self.grupoSelec.get_active_text(), self.calendario.get_date(),
					self.vueltas1.get_text(), self.calent1.get_text(), self.descanso1.get_text(), self.duracion1.get_text(), self.reposo1.get_text(), self.usersSeleccionados)
		else:
			return (self.sesionResultante.get_selected_row(), self.grupoSelec.get_active_text(), self.calendario.get_date(),
					self.vueltas1.get_text(), self.calent1.get_text(), self.descanso1.get_text(), self.duracion1.get_text(), self.reposo1.get_text(), self.usersSeleccionados)

	def Emergente_eliminar_prog(self, controller, idprog):
		ventanaemergente = Gtk.MessageDialog(self.win, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, "\n¿Está seguro de que desea eliminar la sesión programada " + str(idprog) + "?") 
		ventanaemergente.connect("response", controller.emergente_decision_prog, idprog)
		ventanaemergente.run()
		ventanaemergente.destroy()

	def avisoLesion(self, userid):
		ventanaemergente = Gtk.MessageDialog(self.win, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "\nEl usuario " + str(userid) + " seleccionado para esta sesión dispone de ejercicios contraindicados por lesión y/o patología.") 
		ventanaemergente.run()
		ventanaemergente.destroy()

	def avisoDiasGrupo(self, id, controller):
		ventanaemergente = Gtk.MessageDialog(self.win, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.YES_NO, "\nEl " + str(id) + " no tiene como horario habitual esta fecha. ¿Desea continuar con la asignación?") 
		ventanaemergente.connect("response", controller.emergente_decision_fecha)
		ventanaemergente.run()
		ventanaemergente.destroy()	

	def postsesionProg(self, sesionprog, sesion, ejerciciosnecesarios, nombrenecesarios, apellidosnecesarios, controller, valoracion, sesionid, usersid):
		dialogo = Gtk.Dialog("Detalle sesión " + sesion, self.win,Gtk.DialogFlags.MODAL|Gtk.DialogFlags.DESTROY_WITH_PARENT,(Gtk.STOCK_OK, Gtk.ResponseType.OK))
		dialogo.set_default_size(50,5)
		contenido = dialogo.get_content_area()

		l1 = Gtk.Label("Ejercicios hechos:")

		liststore = Gtk.ListStore(int, str) #que contiene el filtro
		self.liststore = liststore

		filtroeje = liststore.filter_new() #Hace un filtrado de liststore. Crea otro liststore para aplicar el filtro
		self.filtroeje = filtroeje
		filtroeje.set_visible_func(self.aplicar_filtro_aux) #Filtra el liststore nuevo según lo que indique la función


		ejerciciostreev = Gtk.TreeView(filtroeje, headers_visible=True) #Lista de ejercicios
		ejerciciostreev.get_selection().set_mode(0)

		#Crear columna 1
		renderer_text = Gtk.CellRendererText()

		column_text1 = Gtk.TreeViewColumn(("Nº"), renderer_text, text=0)

		#Crear columna 2
		renderer_text2 = Gtk.CellRendererText()
		column_text2 = Gtk.TreeViewColumn(("Ejercicio"), renderer_text2, text=1)

		ejerciciostreev.append_column(column_text1)
		ejerciciostreev.append_column(column_text2)

		self.ejerciciostreev = ejerciciostreev

		ventana_scroll = Gtk.ScrolledWindow(expand=True, margin=5)
		ventana_scroll.set_size_request(300, 100)
		ventana_scroll.add(ejerciciostreev)

		Box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin=10)
		Box1.pack_start(l1, False, False, 0)
		Box1.pack_start(ventana_scroll, False, False, 0)

		l2 = Gtk.Label("Usuarios implicados:")

		liststore2 = Gtk.ListStore(str, str, str) #que contiene el filtro
		self.liststore2 = liststore2

		filtro2 = liststore2.filter_new() #Hace un filtrado de liststore. Crea otro liststore para aplicar el filtro
		self.filtro2 = filtro2
		filtro2.set_visible_func(self.aplicar_filtro_aux) #Filtra el liststore nuevo según lo que indique la función


		usuariostreev = Gtk.TreeView(filtro2, headers_visible=True) #Lista de usuarios

		#Crear columna 1
		renderer_text0 = Gtk.CellRendererText()

		column_text0 = Gtk.TreeViewColumn(("Id"), renderer_text0, text=0)

		#Crear columna 1
		renderer_textu = Gtk.CellRendererText()

		column_text1u = Gtk.TreeViewColumn(("Nombre"), renderer_textu, text=1)

		#Crear columna 2
		renderer_text2u = Gtk.CellRendererText()
		column_text2u = Gtk.TreeViewColumn(("Apellidos"), renderer_text2u, text=2)

		usuariostreev.append_column(column_text0)
		usuariostreev.append_column(column_text1u)
		usuariostreev.append_column(column_text2u)

		self.usuariostreev = usuariostreev

		ventana_scroll2 = Gtk.ScrolledWindow(expand=True, margin=5)
		ventana_scroll2.set_size_request(300, 100)
		ventana_scroll2.add(usuariostreev)

		etiq = Gtk.Label()
		etiq.set_markup("<i>Seleccione uno para acceder</i>")
		self.etiq = etiq

		valPersonal = Gtk.Button(label=("Valoración personal >>"))
		self.valPersonal = valPersonal
		self.valPersonal.set_sensitive(False)
		valPersonal.connect("clicked", controller.on_personal, sesionid, sesionprog)

		Box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin=10)
		Box2.pack_start(l2, False, False, 0)
		Box2.pack_start(ventana_scroll2, False, False, 0)
		Box2.pack_start(etiq, False, False, 0)
		Box2.pack_start(valPersonal, False, False, 0)

		etiq1 = Gtk.Label()
		etiq1.set_markup("Valoración post-sesión:")
		self.etiq1 = etiq1

		scrolled_windowpostsesion = Gtk.ScrolledWindow(expand=False)    #cuadro de texto
		scrolled_windowpostsesion.set_border_width(5)	
        # we scroll only if needed
		scrolled_windowpostsesion.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        # a text buffer (stores text)
		bufferValoracion = Gtk.TextBuffer()
		self.bufferValoracion = bufferValoracion
		if valoracion != "":
			self.bufferValoracion.set_text(valoracion)

        # a textview (displays the buffer)
		textview = Gtk.TextView(buffer=bufferValoracion)

        # textview is scrolled
		scrolled_windowpostsesion.add(textview)

		if ejerciciosnecesarios is not None:
			for i in range(0, len(ejerciciosnecesarios)):
				self.filtroeje.get_model().append([i, ejerciciosnecesarios[i]])

		if nombrenecesarios is not None and apellidosnecesarios is not None:
			for i in range(0, len(nombrenecesarios)):
				self.filtro2.get_model().append([usersid[i], nombrenecesarios[i], apellidosnecesarios[i]])

		guardarpost = Gtk.Button(label=("Guardar"))
		guardarpost.set_sensitive(False)
		guardarpost.connect("clicked", controller.on_guardar_valoraciones, sesionprog)
		usuariostreev.get_selection().connect("changed", controller.activar_botones_valoracion)
		bufferValoracion.connect("changed", controller.permitir_guardado, guardarpost)

		BoxPostSesion = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin=10)
		BoxPostSesion.pack_start(etiq1, True, True, 0)
		BoxPostSesion.pack_start(scrolled_windowpostsesion, True, True, 0)
		grid = Gtk.Grid(margin=5, column_spacing=5, row_spacing=5)
		grid.attach(Box1, 0, 0, 2, 5)
		grid.attach_next_to(Box2, Box1, Gtk.PositionType.RIGHT, 2, 5)
		grid.attach_next_to(BoxPostSesion, Box1, Gtk.PositionType.BOTTOM, 6, 6)
		grid.attach_next_to(guardarpost, BoxPostSesion, Gtk.PositionType.BOTTOM, 1, 1)
		contenido.add(grid)
		dialogo.show_all()
		dialogo.run()
		dialogo.destroy()

	def error(self, error):
		if (error == 1):
			Mensaje= Gtk.MessageDialog(self.win, 0, Gtk.MessageType.WARNING,Gtk.ButtonsType.OK, ("\nFormato introducido incorrecto"))
		elif (error == 3):
			Mensaje= Gtk.MessageDialog(self.win, 0, Gtk.MessageType.WARNING,Gtk.ButtonsType.OK, ("\nEntrada no encontrada"))
		elif (error == 4):
			Mensaje= Gtk.MessageDialog(self.win, 0, Gtk.MessageType.WARNING,Gtk.ButtonsType.OK, ("\nImposible añadir cambio, algún campo está vacío"))
		elif (error == 5):
			Mensaje= Gtk.MessageDialog(self.win, 0, Gtk.MessageType.WARNING,Gtk.ButtonsType.OK, ("\nLa suma de las cargas debe dar 100%"))
		elif (error == 6):
			Mensaje= Gtk.MessageDialog(self.win, 0, Gtk.MessageType.WARNING,Gtk.ButtonsType.OK, ("\nEl máximo de elementos multimedia a añadir son dos"))
		elif (error == 7):
			Mensaje= Gtk.MessageDialog(self.win, 0, Gtk.MessageType.WARNING,Gtk.ButtonsType.OK, ("\nYa hay un elemento de este tipo"))
		elif (error == 8):
			Mensaje = Gtk.MessageDialog(self.win, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK,("\nModificación no permitida; debe borrar y crear de nuevo")) 
		elif (error == 9):
			Mensaje= Gtk.MessageDialog(self.win, 0, Gtk.MessageType.WARNING,Gtk.ButtonsType.OK, ("\nSeleccione antes una sesión"))
		elif (error == 10):
			Mensaje= Gtk.MessageDialog(self.win, 0, Gtk.MessageType.WARNING,Gtk.ButtonsType.OK, ("\nEl vídeo a mostrar se ha movido de directorio y no se encuentra en el path almacenado. Introduzcalo de nuevo."))
		else:
			Mensaje= Gtk.MessageDialog(self.win, 0, Gtk.MessageType.WARNING,Gtk.ButtonsType.OK, ("\nLesión ya disponible en el usuario"))
		Mensaje.run()
		Mensaje.destroy()