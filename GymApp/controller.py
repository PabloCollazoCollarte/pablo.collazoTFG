#! /usr/bin/python3
# -*- coding: utf-8 -*-

import gi
import base64
import datetime
from datetime import date
from PIL import Image
import re 
import vlc
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Controller:
	def __init__(self, view, model):
		self.view = view
		self.model = model
		view.aviso(self)

	def on_iniciar(self, boton):
		gruposRegistrados = self.model.get_grupos()
		self.view.inicio()
		if gruposRegistrados is not None:
			for i in range(0, len(gruposRegistrados)):
				id_grupo = str(gruposRegistrados[i]["id_grupo"])
				horario = str(gruposRegistrados[i]["horario"])
				self.model.get_usuarios_por_grupo(id_grupo)
				self.view.filtro.get_model().append([id_grupo,horario]) #Introducir en la vista los datos de la BD	
		sesionesProgramadas = self.model.get_progs()
		if sesionesProgramadas is not None:
			for i in range(0, len(sesionesProgramadas)):
				idprog = str(sesionesProgramadas[i]["id_prog"])
				idsesion = str(sesionesProgramadas[i]["id_sesion"])
				fecha = str(sesionesProgramadas[i]["fecha"])
				idgrupo = str(sesionesProgramadas[i]["id_grupo"])
				sesion = self.model.get_sesion(int(idsesion))
				descripcion = sesion["objetivos"]
				self.view.filtro2.get_model().append([idprog,idsesion,fecha, idgrupo,descripcion]) #Introducir en la vista los datos de la BD	
		self.view.clickEnlaces(self)

	def on_usuarios(self, boton):
		usuariosRegistrados = self.model.get_usuarios()
		self.view.usuarios()
		if usuariosRegistrados is not None:
			for i in range(0, len(usuariosRegistrados)):
				id = str(usuariosRegistrados[i]["id"])
				Apellidos = str(usuariosRegistrados[i]["Apellidos"])
				Nombre = str(usuariosRegistrados[i]["Nombre"])
				DNI = str(usuariosRegistrados[i]["DNI"])
				telefono = str(usuariosRegistrados[i]["telefono"])
				correo = str(usuariosRegistrados[i]["correo"])
				activo = str(usuariosRegistrados[i]["activo"])
				self.view.filtroUsuarios.get_model().append([id,Apellidos,Nombre,DNI,telefono,correo,activo]) #Introducir en la vista los datos de la BD
		self.view.clickUsuarios(self)
		self.view.clickEnlaces(self)

	def activar_botones(self, seleccion):
		self.view.VerMod.set_sensitive(True)  #activamos los botones si se hace una selección de una fila
		self.view.deportivo.set_sensitive(True)
		self.view.Eliminar.set_sensitive(True)
		self.view.Activar.set_sensitive(True)
		self.view.clickSobreUsuarios(self)

	def on_usuario_seleccionado(self): #en caso de que se seleccione una fila
		conjunto, seleccionado = self.view.users.get_selection().get_selected()
		if seleccionado is not None:
			fila_selec = conjunto.convert_iter_to_child_iter(seleccionado)
			return (conjunto.get_model()[fila_selec])
			

	def on_NuevoUser(self, boton):
		self.view.Formulario_user(None)
		self.view.AccionesEnElFormUsuario(self)

	def on_elegir_foto(self, boton):
		self.view.seleccionar_foto(self)

	def on_catPatologias(self, boton, vieneDeValoracion, userid):
		data = self.model.get_patologias(None, False)
		patologia = []
		if data != []:
			for i in range(0, len(data)):
					patologia.append(str(data[i]["patologia"]))
			self.view.cataPatologias("", patologia, False, self, vieneDeValoracion, userid)

	def on_catLesiones(self, boton, vieneDeValoracion, userid):
		data = self.model.get_lesiones(None, False)
		lesion = []
		if data != []:
			for i in range(0, len(data)):
					lesion.append(str(data[i]["lesion"]))
			self.view.cataLesiones("", lesion, False, self, vieneDeValoracion, userid)

	def on_añadir_lesion(self, boton, vieneDeValoracion, userid):   
		palabrasIntroducidas = self.view.AñadirLesionEntrada.get_text()
		palabrasIntroducidasSeparadas = palabrasIntroducidas.split() 
		resultados = []
		for palabra in palabrasIntroducidasSeparadas:   #con esta lista aconsejaremos al usuario entradas YA DISPONIBLES y evitamos introducir lesiones ya existentes en su catálogo
			if self.model.get_lesiones(palabra, False) != []:
				resultadosSinIndice = lambda x: x.values()
				for elemento in self.model.get_lesiones(palabra, False):   #al devolver una lista  [{clave:valor},{clave:valor},...] nos quedamos con los valores
					if str(resultadosSinIndice(elemento)).split("'")[1] not in resultados:
						resultados += resultadosSinIndice(elemento)
		if resultados != []:
			self.view.advertenciaCatalogos(palabrasIntroducidas, resultados, "lesiones", self, vieneDeValoracion, userid)
		else:
			if vieneDeValoracion:
				self.añadirLesionaUser(userid, palabrasIntroducidas)
				return
			if self.ComprobarSiNoEsta(palabrasIntroducidas, "lesiones"):
				self.view.añadir_entrada(palabrasIntroducidas, "lesion") #sino se encuentra en el catalogo, la añadimos a la vista

	def añadirLesionaUser(self, userid, palabrasIntroducidas): 
		lesiones = self.model.get_user_lesiones(userid)
		for i in lesiones:
			if i["lesion"] == palabrasIntroducidas:
				self.view.error(11)
				return
		aux = []
		for i in self.model.get_lesiones(palabrasIntroducidas, True):
			aux.append(i["lesion"])
		if palabrasIntroducidas not in aux:
			self.on_añadir_a_Catalogo(None, palabrasIntroducidas, "lesion")  #sino se encuentra en el catalogo, la asociamos al usuario y al catalogo
		self.model.insert_user_lesion(int(userid), palabrasIntroducidas)

	def on_añadir_patologia(self, boton, vieneDeValoracion, userid):	
		palabrasIntroducidas = self.view.AñadirPatologiaEntrada.get_text()
		palabrasIntroducidasSeparadas = palabrasIntroducidas.split() 
		resultados = []
		for palabra in palabrasIntroducidasSeparadas:   #con esta lista aconsejaremos al usuario entradas YA DISPONIBLES y evitamos introducir lesiones ya existentes en su catálogo
			if self.model.get_patologias(palabra, False) != []:
				resultadosSinIndice = lambda x: x.values()
				for elemento in self.model.get_patologias(palabra, False):   #al devolver una lista  [{clave:valor},{clave:valor},...] nos quedamos con los valores
					if str(resultadosSinIndice(elemento)).split("'")[1] not in resultados:
						resultados += resultadosSinIndice(elemento)
		if resultados != []:
			self.view.advertenciaCatalogos(palabrasIntroducidas, resultados, "patologias", self, vieneDeValoracion, userid)
		else:
			if self.ComprobarSiNoEsta(palabrasIntroducidas, "patologias"):
				self.view.añadir_entrada(palabrasIntroducidas, "patologia") #sino se encuentra en el catalogo, la añadimos a la vista

	def ComprobarSiNoEsta(self, palabras, tipo):
		if(tipo == "lesiones"):
			clase = self.view.lesiones
		else:
			clase = self.view.patologias
		Fuera = True
		if clase.get_children() != []:
			i = 0
			while (Fuera and i<len(clase.get_children())):			#comprobamos que no se encuentra ya en la propia lista de la vista
				lesion = clase.get_children()[i].get_child().get_label()
				if palabras == lesion:
					self.view.YaPuestaEnLista()
					Fuera = False
				i+=1
		return Fuera

	def on_añadir_Seguro(self, boton, data, tipo, vieneDeValoracion, userid):
		if vieneDeValoracion:
			self.añadirLesionaUser(userid, data)
			return
		if tipo == "lesion":
			if self.ComprobarSiNoEsta(data, "lesiones"):
				self.view.añadir_entrada(data, "lesion")
		else:
			if self.ComprobarSiNoEsta(data, "patologias"):
				self.view.añadir_entrada(data, "patologia")
		self.view.catalogo.destroy()

	def on_borrar_lesion(self, boton):
		seleccionado = self.view.lesiones.get_selected_row()  #coger la lesion seleccionada
		if seleccionado is not None:
			self.view.lesiones.remove(seleccionado)
			

	def on_borrar_patologia(self, boton):
		seleccionado = self.view.patologias.get_selected_row()  #coger la lesion seleccionada
		if seleccionado is not None:
			self.view.patologias.remove(seleccionado) 
			

	def on_añadir_a_Catalogo(self, boton, data, tipo):
		if tipo == "patologia":
			self.model.insert_patologia(data)

		else:
			self.model.insert_lesion(data)

	def on_guardar_en_BD(self, boton):    #especificacion de interaccion con la BD de usuarios en caso de MODIFICACIÓN
		return self.on_Interactuar_con_BD("insertar", boton)

	def on_actualizar_en_BD(self, boton):	#especificacion de interaccion con la BD de usuarios en caso de CREACIÓN
		return self.on_Interactuar_con_BD("modificar", boton)

	def on_Interactuar_con_BD(self, accion, boton):   #Esta funcion generaliza la de AÑADIR y la de MODIFICAR un usuario
		guardar = self.view.datosAGuardar()
		if guardar is None:
			return
		if accion is "insertar":
			(Apellidos, Nombre, Hombre, Mujer, DNI, foto, FechaNac, domicilio, telefono, correo, buffer1, Categoría, Peso, altura, lesiones, patologias) = guardar
		else:
			(Apellidos, Nombre, Hombre, Mujer, DNI, foto, FechaNac, domicilio, telefono, correo, buffer1, Categoría, Peso, altura, lesiones, patologias, id) = guardar
		
		if Hombre.get_active():
			Sexo = "H"
		else:
			Sexo ="M"
		start, end = buffer1.get_bounds()
		texto = buffer1.get_text(start, end, True)
		if ((Apellidos == "") or (Nombre == "") or (DNI == "") or (FechaNac == "") or (domicilio == "") or (telefono == "") or (correo == "")  or (Categoría == None) or (Peso == "") or (altura == "")):
			self.view.error(4)
			return

		self.view.FechaNac.get_style_context().remove_class('error')
		self.view.DNI.get_style_context().remove_class('error')
		self.view.telefono.get_style_context().remove_class('error')
		self.view.Peso.get_style_context().remove_class('error')
		self.view.altura.get_style_context().remove_class('error')
		self.view.correo.get_style_context().remove_class('error')

		if(self._Comprobardate(FechaNac.strip()) == None):    #comprobamos que la fecha esta correcta
			self.view.error(1)
			self.view.FechaNac.get_style_context().add_class('error')
			return

		if self.validoDNI(DNI) == False:   #comprobacion dni
			self.view.error(1)
			self.view.DNI.get_style_context().add_class('error')
			return

		if self.comprobarTelefono(telefono) == False:   #comprobacion telefono es un número
			self.view.error(1)
			self.view.telefono.get_style_context().add_class('error')
			return

		if self.comprobarNumero(Peso) == False:
			self.view.error(1)
			self.view.Peso.get_style_context().add_class('error')
			return
		else:
			Peso = self.comprobarNumero(Peso)

		if self.comprobarNumero(altura) == False:
			self.view.error(1)
			self.view.altura.get_style_context().add_class('error')
			return
		else:
			altura = self.comprobarNumero(altura)

		if self.checkEmail(correo) == False:		#comprobamos el formato del email
			self.view.error(1)
			self.view.correo.get_style_context().add_class('error')
			return

		ActualizacionFoto = False	
		if isinstance(foto, str):   #comprobamos que la variable de la foto es un str y no vacía para que no de error en la funcion open
			ActualizacionFoto = True
			with open(foto, "rb") as image_file:
				 encoded_string = base64.b64encode(image_file.read())

		if accion is "insertar":
			if ActualizacionFoto:   #POR PROBLEMAS DE ACTUALIZACION DE LA FOTO, COMPROBAMOS SI ESTA HA SIDO CAMBIADA (NO ES VACIA O LA MISMA)
									#EN CASO DE QUE NO HAYA FOTO, NO SE ENVÍA
				objetos = (Apellidos, Nombre, Sexo, DNI, encoded_string, FechaNac, domicilio, telefono, correo, texto, Categoría, Peso, altura, "Sí")
			else:
				objetos = (Apellidos, Nombre, Sexo, DNI, FechaNac, domicilio, telefono, correo, texto, Categoría, Peso, altura, "Sí")

			idUsuario = self.model.insert_usuarios(objetos, ActualizacionFoto)

			fecha = date.today()
			fecha = fecha.strftime("%Y%m%d")
			self.model.insert_var_peso(str(Peso), str(fecha), int(idUsuario))   #para disponer de un peso inicial en la gráfica de hist. deportivo

			if lesiones.get_children() != []:
				for i in range(0, len(lesiones.get_children())):
					lesion = lesiones.get_children()[i].get_child().get_label()
					aux = []
					for i in self.model.get_lesiones(lesion, True):
						aux.append(i["lesion"])
					if lesion not in aux:
						self.on_añadir_a_Catalogo(None, lesion, "lesion")  #sino se encuentra en el catalogo, la asociamos al usuario y al catalogo
					self.model.insert_user_lesion(idUsuario, lesion)
					
			if patologias.get_children() != []:
				for i in range(0, len(patologias.get_children())):
					patologia = patologias.get_children()[i].get_child().get_label()
					aux = []
					for i in self.model.get_patologias(patologia, True):
						aux.append(i["patologia"])
					if patologia not in aux:
						self.on_añadir_a_Catalogo(None, patologia, "patologia")  #sino se encuentra en el catalogo, la asociamos al usuario y al catalogo
					self.model.insert_user_patologia(idUsuario, patologia)
					
		else:
			if ActualizacionFoto:
				objetos = (Apellidos, Nombre, Sexo, DNI, encoded_string, FechaNac, domicilio, telefono, correo, texto, Categoría, Peso, altura, id)
			else:
				objetos = (Apellidos, Nombre, Sexo, DNI, FechaNac, domicilio, telefono, correo, texto, Categoría, Peso, altura, id)
			self.model.update_user(objetos, ActualizacionFoto)

			fecha = date.today()
			fecha = fecha.strftime("%Y%m%d")
			objetos = (str(Peso), str(fecha), int(id))
			if self.model.get_variacion_peso_evitarRepetidos(int(id), str(Peso), fecha) == []:
				self.model.insert_var_peso(str(Peso), fecha, int(id))

			if lesiones.get_children() != []:				#COMPROBACION EN CASO DE ACTUALIZACIONES DE SU LISTA DE LESIONS/PATOLOGIAS EN VISTA Y EN MODELO(BD)
				for i in range(0, len(lesiones.get_children())):
					lesion = lesiones.get_children()[i].get_child().get_label()
					lista = []
					for j in self.model.get_lesiones(lesion, True):  #si la lesion concreta no se encuentra en el catalogo, se introduce
						lista.append(j["lesion"])
					if lesion not in lista:      
						self.on_añadir_a_Catalogo(None, lesion, "lesion")  
					lista = []
					for j in self.model.get_user_lesiones(id):
						lista.append(j["lesion"])
					if lesion not in lista:
						a = self.model.insert_user_lesion(id, lesion)

			Borrar = []
			for i in (self.model.get_user_lesiones(id)):		#COMPROBACION DE SI SE BORRO ALGUNA ENTRADA EN LA VISTA, COMPARANDOLA CON LO GUARDADO EN LA BD
				if self.model.get_user_lesiones(id) != []:					#en caso de que YA estuviera vacia en BD no hay que comprobar borrados en ella
					j=0
					NoEncontrado = True
					while(j<len(lesiones.get_children()) and NoEncontrado):
						lesion = lesiones.get_children()[j].get_child().get_label()
						NoEncontrado = (lesion != i["lesion"])
						j+=1
					if NoEncontrado:
						Borrar.append(i["lesion"])
			
			for j in Borrar:
				self.model.delete_user_lesiones(id, j)

			if patologias.get_children() != []:        #COMPROBACION EN CASO DE ACTUALIZACIONES DE SU LISTA DE LESIONS/PATOLOGIAS EN VISTA Y EN MODELO(BD)
				for i in range(0, len(patologias.get_children())):
					patologia = patologias.get_children()[i].get_child().get_label()
					lista = []
					for j in self.model.get_patologias(patologia, True):  #si la lesion concreta no se encuentra en el catalogo, se introduce
						lista.append(j["patologia"])
					if patologia not in lista:      
						self.on_añadir_a_Catalogo(None, patologia, "patologia")  
					lista = []
					for j in self.model.get_user_patologias(id):
						lista.append(j["patologia"])
					if patologia not in lista:
						a = self.model.insert_user_patologia(id, patologia)

			Borrar = []
			for i in (self.model.get_user_patologias(id)):		#COMPROBACION DE SI SE BORRO ALGUNA ENTRADA EN LA VISTA, COMPARANDOLA CON LO GUARDADO EN LA BD
				j=0		
				NoEncontrado = True
				if self.model.get_user_patologias(id) != []:					#en caso de que YA estuviera vacia en BD no hay que comprobar borrados en ella
					while(j<len(patologias.get_children()) and NoEncontrado):
						patologia = patologias.get_children()[j].get_child().get_label()
						NoEncontrado = (patologia != i["patologia"])
						j+=1
					if NoEncontrado:
						Borrar.append(i["patologia"])
			for j in Borrar:
				self.model.delete_user_patologias(id, j)

		self.on_usuarios(boton)
		      
	def checkEmail(self, email): 
		regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
		if(re.search(regex,email)):  
			return True
          
		else:  
			return False

	def _Comprobardate(self, text):   #comprobamos que el formato de la fecha es correcto
		try:
			return datetime.datetime.strptime(text, "%x")
		except ValueError:
			return None

	def validoDNI(self, dni):    					#comprobacion DNI
	    tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
	    dig_ext = "XYZ"
	    reemp_dig_ext = {'X':'0', 'Y':'1', 'Z':'2'}
	    numeros = "1234567890"
	    dni = dni.upper()
	    if len(dni) == 9:
	        dig_control = dni[8]
	        dni = dni[:8]
	        if dni[0] in dig_ext:
	            dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
	        return len(dni) == len([n for n in dni if n in numeros]) \
	            and tabla[int(dni)%23] == dig_control
	    return False

	def on_ActualizarUser(self, boton):
		datos_user = self.model.get_user((self.on_usuario_seleccionado())[0])
		if datos_user is not None:
			datos_user['lesiones'] = []
			datos_user['patologias'] = []
			if self.model.get_user_lesiones(datos_user["id"]) != []:
				datos_user['lesiones'] = self.model.get_user_lesiones(datos_user["id"])  #cogemos las lesiones del usuario a actualizar/ver
			if self.model.get_user_patologias(datos_user["id"]) != []:
				datos_user['patologias'] = self.model.get_user_patologias(datos_user["id"])    #cogemos las patologias del usuario a actualizar/ver
			self.view.Formulario_user(datos_user)

		self.view.AccionesEnElFormUsuario(self)

	def comprobarTelefono(self, num):
		try:
			int(num)
			return True
		except ValueError:
			return False

	def comprobarNumero(self, num):
		try:
			float(num)
			if str(num).find(".") < 0:
				return str(num) + ".0"
			else:
				return str(num)
		except ValueError:
			return False

	def on_eliminar_user(self, boton):
		datos_user = self.model.get_user((self.on_usuario_seleccionado())[0])
		if datos_user is not None:
			self.view.Emergente_eliminar(self,datos_user["id"])


	def emergente_decision(self, boton, id_respuesta, id):    #depende de el boton pulsado en la emergente, se borra un usuario o no
		if id_respuesta == Gtk.ResponseType.YES:
			self.model.delete_user(id)
			self.on_usuarios(boton)

	def on_activar_user(self, boton):
		datos_user = self.model.get_user((self.on_usuario_seleccionado())[0])
		if datos_user is not None:
			if self.on_usuario_seleccionado()[6] == "Sí":
				self.model.update_active("No", datos_user["id"])
			else:
				self.model.update_active("Sí", datos_user["id"])
			self.on_usuarios(boton)

	def on_deportivo(self, boton):
		idusuarioSeleccionado = self.on_usuario_seleccionado()[0]
		sesionesRegistrados = self.model.get_progs_from_grupo(self.model.get_user(idusuarioSeleccionado)["id_grupo"])
		sesionesIndividuales = self.model.get_prog_from_usuario((self.on_usuario_seleccionado())[0])
		sesionesRegistrados += sesionesIndividuales
		self.view.deportivoVista(self, int(idusuarioSeleccionado))
		if sesionesRegistrados is not None:
			for i in range(0, len(sesionesRegistrados)):
				id_prog = sesionesRegistrados[i]["id_sesionprog"]
				fecha = sesionesRegistrados[i]["fecha"]
				idsesion = self.model.get_prog(str(id_prog))["id_sesion"]
				postpersonal = self.model.get_valoracion_personal(id_prog, int(idusuarioSeleccionado))["valoracionpersonal"]
				self.view.filtroSesionesUsuarios.get_model().append([str(id_prog),str(idsesion),fecha,postpersonal]) #Introducir en la vista los datos de la BD

		pesosAux = self.model.get_variacion_peso(int(idusuarioSeleccionado))
		pesos = []
		fechas = []
		for i in pesosAux:
			pesos.append(float(i["peso"]))
			fechas.append(i["dia"])
		fechasAux = []
		for j in fechas:
			j = j[:4] + '-' + j[4:]
			j = j[:7] + '-' + j[7:]
			fechasAux.append(j)
		self.view.MostrarGraficaPeso(pesos, fechasAux)

	def CambiarPeso(self, pesonuevo, userid, sesionid):
		fechaSesion = self.model.get_prog(sesionid)["fecha"]
		diaGuardado = fechaSesion.split("/", 1)[0]
		mesGuardado = fechaSesion.split("/", 1)[1].split("/")[0]
		anoGuardado = fechaSesion.split("/", 2)[2]
		fecha = date(int(anoGuardado), int(mesGuardado), int(diaGuardado))
		fecha = fecha.strftime("%Y%m%d")
		if self.model.get_variacion_peso_evitarRepetidos(userid, str(pesonuevo), fecha) == []:
			self.model.insert_var_peso(str(pesonuevo), fecha, int(userid))


	def on_valoracion_seleccionado(self): #en caso de que se seleccione una fila
		conjunto, seleccionado = self.view.sesionesusers.get_selection().get_selected()
		if seleccionado is not None:
			fila_selec = conjunto.convert_iter_to_child_iter(seleccionado)
			return (conjunto.get_model()[fila_selec])

	def on_aceptarDeportivo(self, boton):
		self.on_usuarios(boton)

	def activar_botones_userSesion(self, seleccion, iduser):
		self.view.postVal.set_sensitive(True)  #activamos los botones si se hace una selección de una fila
		self.view.clicksobreusers(self, iduser)

	def on_valpersonal(self, boton, iduser, idsesion, idsesionprog):
		if idsesion == None:
			ejercicios = self.model.get_sesion_ejercicios(self.on_valoracion_seleccionado()[1])
		else:
			ejercicios = self.model.get_sesion_ejercicios(idsesion)
		ejerciciosnecesarios = []
		for i in ejercicios:
			ejerciciosnecesarios.append(i["nombre_ejercicio"])
		datos = []
		if idsesionprog == None:
			valores = self.model.get_valoracion_personal(self.on_valoracion_seleccionado()[0], iduser)
		else:
			valores = self.model.get_valoracion_personal(idsesionprog, iduser)
		valores["peso"] = self.model.get_peso(iduser)["peso"]
		if idsesion == None and idsesionprog == None:
			self.view.valpersonalVista(self.on_valoracion_seleccionado()[1], ejerciciosnecesarios, self, self.on_valoracion_seleccionado()[0], iduser, valores)
		else:
			self.view.valpersonalVista(idsesion, ejerciciosnecesarios, self, idsesionprog, iduser, valores)

	def on_guardar_valoracionespersonal(self, widget, sesionid, userid):
		start, end = self.view.bufferpers.get_bounds()
		texto = self.view.bufferpers.get_text(start, end, True)
		objetos = (str(self.view.pesocambiador.get_value()), int(userid))
		self.model.update_peso_user(objetos)
		objetos = (self.view.val.get_text(), texto, sesionid, userid)
		self.model.update_prog_valoracion_personal(objetos)
		self.CambiarPeso(self.view.pesocambiador.get_value(), userid, sesionid)
		widget.set_sensitive(False)

	def on_userValora_seleccionado(self): #en caso de que se seleccione una fila
		conjunto, seleccionado = self.view.usuariostreev.get_selection().get_selected()
		if seleccionado is not None:
			fila_selec = conjunto.convert_iter_to_child_iter(seleccionado)
			return (conjunto.get_model()[fila_selec])

	def activar_botones_valoracion(self, seleccion):
		self.view.valPersonal.set_sensitive(True)  #activamos los botones si se hace una selección de una fila

	def on_personal(self, boton, sesionid, sesionidprog):
		id_user = self.model.get_user((self.on_userValora_seleccionado())[0])["id"]
		self.on_valpersonal(boton, id_user, sesionid, sesionidprog)

	def permitir_guardado(self, boton, botonGuardado):
		botonGuardado.set_sensitive(True)

#########################################################################################################################

	def on_ejercicios(self, boton):
		if hasattr(self.view, 'player'):
			if self.view.player.get_state() == vlc.State.Playing:
				self.view.player.stop()
		ejerciciosRegistrados = self.model.get_ejercicios()
		self.view.ejercicios()
		if ejerciciosRegistrados is not None:
			for i in range(0, len(ejerciciosRegistrados)):
				nombre_ejercicio = str(ejerciciosRegistrados[i]["nombre_ejercicio"])
				descripcion = str(ejerciciosRegistrados[i]["descripcion"])
				foto = str(ejerciciosRegistrados[i]["foto"])
				titulo_video = str(ejerciciosRegistrados[i]["titulo_video"])
				URL = str(ejerciciosRegistrados[i]["URL"])
				cargas = str(ejerciciosRegistrados[i]["cargas"])
				materialesUtilizados = ""
				for i in self.model.get_materiales_ejercicio(nombre_ejercicio):
					materialesUtilizados = str(i["nombre_material"])  + ", " + materialesUtilizados 
				self.view.filtroEjercicios.get_model().append([nombre_ejercicio,descripcion, materialesUtilizados,cargas]) #Introducir en la vista los datos de la BD
		self.view.clickEjercicios(self)
		self.view.clickEnlaces(self)

	def on_ejercicio_seleccionado(self): #en caso de que se seleccione una fila
		conjunto, seleccionado = self.view.ejerciciosTree.get_selection().get_selected()
		if seleccionado is not None:
			fila_selec = conjunto.convert_iter_to_child_iter(seleccionado)
			return (conjunto.get_model()[fila_selec])

	def on_eliminar_ejercicio(self, boton):
		datos_ejercicio = self.model.get_ejercicio((self.on_ejercicio_seleccionado())[0])
		if datos_ejercicio is not None:
			self.view.Emergente_eliminar_Ejercicio(self,datos_ejercicio["nombre_ejercicio"])


	def emergente_decision_ejercicio(self, boton, id_respuesta, nombreej):    #depende de el boton pulsado en la emergente, se borra un ejercicio o no
		if id_respuesta == Gtk.ResponseType.YES:
			self.model.delete_ejercicio(nombreej)
			self.on_ejercicios(boton)

	def activar_botonesEjercicio(self, seleccion):
		self.view.Eliminar.set_sensitive(True)
		self.view.VerMod.set_sensitive(True)
		self.view.clickSobreEjercicios(self)

	def on_NuevoEjercicio(self, boton):
		materiales = self.model.get_materiales()
		self.view.Formulario_Ejercicio(materiales, None, self)
		self.view.AccionesEnElFormEjercicio(self)

	def accionesvideo(self, button, accion):
		if accion == "PlayPausa":
			if self.view.estadoVideo == "Stop":
				self.view.player.play()
				self.view.estadoVideo = "Play"
			else:
				self.view.player.pause()
		else:
			self.view.player.stop()
			self.view.estadoVideo = "Stop"

	def configVideo(self, widget, video):
		self.view.vlcInstance = vlc.Instance("--no-xlib")
		self.view.player = self.view.vlcInstance.media_player_new()
		win_id = widget.get_window().get_xid()
		self.view.player.set_xwindow(win_id)
		self.view.player.set_mrl(video)
		self.view.video = video
		self.view.player.play()
		self.view.is_player_active = True
		self.view.vlcInstance.release()
			

	def insertarVideoFoto(self, button):
		if button.get_filename() is not None:
			if len(self.view.multimediaBox.get_children()) != 2:			

				if button.get_filename().endswith('jpeg') or button.get_filename().endswith('jpg') or \
				   button.get_filename().endswith('png'):
					if (len(self.view.multimediaBox.get_children()) == 1 and self.view.multimediaBox.get_children()[0].get_children()[0].get_name() == "GtkDrawingArea") \
					or	len(self.view.multimediaBox.get_children()) == 0:
						self.view.insertarFoto(button)
						
					else:
						self.view.error(7)
						button.unselect_all()
						return

				elif button.get_filename().endswith('mp4') or button.get_filename().endswith('mpg') or \
					 button.get_filename().endswith('webm'):
					if (len(self.view.multimediaBox.get_children()) == 1 and self.view.multimediaBox.get_children()[0].get_children()[0].get_name() == "GtkImage") \
					or	len(self.view.multimediaBox.get_children()) == 0:
						self.view.insertarVideo(button.get_filename(), self)
						
					else:
						self.view.error(7)
						self.view.botonFotoVideo.unselect_all()
						return
				else:
					self.view.error(1)
					self.view.botonFotoVideo.unselect_all()
					return

			else:
				self.view.error(6)
				self.view.botonFotoVideo.unselect_all()
				return

	def on_scale_moved(self, boton):
		if (self.view.aeroScale.get_value() + self.view.coordScale.get_value() + self.view.equiScale.get_value() + self.view.frzScale.get_value()) > 100:
			self.view.error(5)
			while((self.view.aeroScale.get_value() + self.view.coordScale.get_value() + self.view.equiScale.get_value() + self.view.frzScale.get_value()) > 100):
				boton.set_value(boton.get_value()-1)
			return

	def on_ActualizarEjercicio(self, boton):
		materiales = self.model.get_materiales()
		datos_ejercicio = self.model.get_ejercicio((self.on_ejercicio_seleccionado())[0])
		if datos_ejercicio is not None:
			datos_ejercicio['lesiones'] = []
			datos_ejercicio['patologias'] = []
			datos_ejercicio['materiales'] = ""
			if self.model.get_ejercicio_lesiones(datos_ejercicio["nombre_ejercicio"]) != []:
				datos_ejercicio['lesiones'] = self.model.get_ejercicio_lesiones(datos_ejercicio["nombre_ejercicio"])  #cogemos las lesiones del usuario a actualizar/ver
			if self.model.get_ejercicio_patologias(datos_ejercicio["nombre_ejercicio"]) != []:
				datos_ejercicio['patologias'] = self.model.get_ejercicio_patologias(datos_ejercicio["nombre_ejercicio"])    #cogemos las patologias del usuario a actualizar/ver
			if self.model.get_materiales_ejercicio(datos_ejercicio["nombre_ejercicio"]) != []:
				datos_ejercicio['materiales'] = self.model.get_materiales_ejercicio(datos_ejercicio["nombre_ejercicio"])    #cogemos las patologias del usuario a actualizar/ver
			self.view.Formulario_Ejercicio(materiales, datos_ejercicio, self)
		self.view.AccionesEnElFormEjercicio(self)

	def avisoModif(self, boton, campo):
		self.view.error(8)
		self.view.NombreEj.set_text(campo)


	def on_guardar_en_BD_ejercicios(self, boton):    #especificacion de interaccion con la BD de ejercicios en caso de MODIFICACIÓN
		return self.on_Interactuar_con_BD_ejercicios("insertar", boton)

	def on_actualizar_en_BD_ejercicios(self, boton):	#especificacion de interaccion con la BD de ejercicios en caso de CREACIÓN
		return self.on_Interactuar_con_BD_ejercicios("modificar", boton)

	def on_Interactuar_con_BD_ejercicios(self, accion, boton):   #Esta funcion generaliza la de AÑADIR y la de MODIFICAR un usuario
		guardar = self.view.datosAGuardarDeEjercicios()
		if guardar is None:
			return
		(nombre_ejercicio, descripcion, imagen, video, listaURLS, cargas, materiales, lesiones, patologias) = guardar
		start, end = descripcion.get_bounds()
		texto = descripcion.get_text(start, end, True)
		ActualizacionFoto = False	
		if isinstance(imagen, str):   #comprobamos que la variable de la foto es un str y no vacía para que no de error en la funcion open
			ActualizacionFoto = True
			with open(imagen, "rb") as image_file:
				 encoded_string = base64.b64encode(image_file.read())
		if hasattr(self.view, 'player'):
			if self.view.player.get_state() == vlc.State.Playing:
				self.view.player.stop()
		if nombre_ejercicio == "":
			self.view.error(4)
			return
		if accion is "insertar":
			if ActualizacionFoto:   #POR PROBLEMAS DE ACTUALIZACION DE LA FOTO, COMPROBAMOS SI ESTA HA SIDO CAMBIADA (NO ES VACIA O LA MISMA)
									#EN CASO DE QUE NO HAYA FOTO, NO SE ENVÍA
				objetos = (nombre_ejercicio, texto, encoded_string, str(video), str(listaURLS), cargas)
			else:
				objetos = (nombre_ejercicio, texto, str(video), str(listaURLS), cargas)
			self.model.insert_ejercicio(objetos, ActualizacionFoto)
			if lesiones.get_children() != []:
				for i in range(0, len(lesiones.get_children())):
					lesion = lesiones.get_children()[i].get_child().get_label()
					aux = []
					for i in self.model.get_lesiones(lesion, True):
						aux.append(i["lesion"])
					if lesion not in aux:
						self.on_añadir_a_Catalogo(None, lesion, "lesion")  #sino se encuentra en el catalogo, la asociamos al usuario y al catalogo
					self.model.insert_ejercicio_lesion(nombre_ejercicio, lesion)
			if patologias.get_children() != []:
				for i in range(0, len(patologias.get_children())):
					patologia = patologias.get_children()[i].get_child().get_label()
					aux = []
					for i in self.model.get_patologias(patologia, True):
						aux.append(i["patologia"])
					if patologia not in aux:
						self.on_añadir_a_Catalogo(None, patologia, "patologia")  #sino se encuentra en el catalogo, la asociamos al usuario y al catalogo
					self.model.insert_ejercicio_patologia(nombre_ejercicio, patologia)

			if materiales != []:
				for i in range(0, len(materiales)):
					material = materiales[i].get_label()
					self.model.insert_material_ejercicio(nombre_ejercicio, material)

		else:
			if ActualizacionFoto:
				objetos = (texto, encoded_string, str(video), str(listaURLS), cargas, nombre_ejercicio)
			else:
				objetos = (texto, str(video), str(listaURLS), cargas, nombre_ejercicio)
			self.model.update_ejercicio(objetos, ActualizacionFoto)



			if lesiones.get_children() != []:				#COMPROBACION EN CASO DE ACTUALIZACIONES DE SU LISTA DE LESIONS/PATOLOGIAS EN VISTA Y EN MODELO(BD)
				for i in range(0, len(lesiones.get_children())):
					lesion = lesiones.get_children()[i].get_child().get_label()
					lista = []
					for j in self.model.get_lesiones(lesion, True):  #si la lesion concreta no se encuentra en el catalogo, se introduce
						lista.append(j["lesion"])
					if lesion not in lista:      
						self.on_añadir_a_Catalogo(None, lesion, "lesion")  
					lista = []
					for j in self.model.get_ejercicio_lesiones(nombre_ejercicio):
						lista.append(j["lesion"])
					if lesion not in lista:
						a = self.model.insert_ejercicio_lesion(nombre_ejercicio, lesion)

			Borrar = []
			for i in (self.model.get_ejercicio_lesiones(nombre_ejercicio)):		#COMPROBACION DE SI SE BORRO ALGUNA ENTRADA EN LA VISTA, COMPARANDOLA CON LO GUARDADO EN LA BD
				if self.model.get_ejercicio_lesiones(nombre_ejercicio) != []:					#en caso de que YA estuviera vacia en BD no hay que comprobar borrados en ella
					j=0
					NoEncontrado = True
					while(j<len(lesiones.get_children()) and NoEncontrado):
						lesion = lesiones.get_children()[j].get_child().get_label()
						NoEncontrado = (lesion != i["lesion"])
						j+=1
					if NoEncontrado:
						Borrar.append(i["lesion"])
			
			for j in Borrar:
				self.model.delete_ejercicio_lesiones(nombre_ejercicio, j)

			if materiales != []:        #COMPROBACION EN CASO DE ACTUALIZACIONES DE SU LISTA DE LESIONS/PATOLOGIAS EN VISTA Y EN MODELO(BD)
				for i in range(0, len(materiales)):
					material = materiales[i].get_label()
					lista = []
					for j in self.model.get_materiales_ejercicio(nombre_ejercicio):
						lista.append(j["nombre_material"])
					if material not in lista:
						a = self.model.insert_material_ejercicio(nombre_ejercicio, material)

			Borrar = []
			for i in (self.model.get_materiales_ejercicio(nombre_ejercicio)):		#COMPROBACION DE SI SE BORRO ALGUNA ENTRADA EN LA VISTA, COMPARANDOLA CON LO GUARDADO EN LA BD
				j=0		
				NoEncontrado = True
				if self.model.get_materiales_ejercicio(nombre_ejercicio) != []:					#en caso de que YA estuviera vacia en BD no hay que comprobar borrados en ella
					while(j<len(materiales) and NoEncontrado):
						material = materiales[j].get_label()
						NoEncontrado = (material != i["nombre_material"])
						j+=1
					if NoEncontrado:
						Borrar.append(i["nombre_material"])
			for j in Borrar:
				self.model.delete_ejercicio_materiales(nombre_ejercicio, j)



			if patologias.get_children() != []:        #COMPROBACION EN CASO DE ACTUALIZACIONES DE SU LISTA DE LESIONS/PATOLOGIAS EN VISTA Y EN MODELO(BD)
				for i in range(0, len(patologias.get_children())):
					patologia = patologias.get_children()[i].get_child().get_label() 
					lista = []
					for j in self.model.get_patologias(patologia, True):  #si la lesion concreta no se encuentra en el catalogo, se introduce
						lista.append(j["patologia"])
					if patologia not in lista:      
						self.on_añadir_a_Catalogo(None, patologia, "patologia")

					lista = []
					for j in self.model.get_ejercicio_patologias(nombre_ejercicio):
						lista.append(j["patologia"])
					if patologia not in lista:
						a = self.model.insert_ejercicio_patologia(nombre_ejercicio, patologia)

			Borrar = []
			for i in (self.model.get_ejercicio_patologias(nombre_ejercicio)):		#COMPROBACION DE SI SE BORRO ALGUNA ENTRADA EN LA VISTA, COMPARANDOLA CON LO GUARDADO EN LA BD
				j=0		
				NoEncontrado = True
				if self.model.get_ejercicio_patologias(nombre_ejercicio) != []:					#en caso de que YA estuviera vacia en BD no hay que comprobar borrados en ella
					while(j<len(patologias.get_children()) and NoEncontrado):
						patologia = patologias.get_children()[j].get_child().get_label()
						NoEncontrado = (patologia != i["patologia"])
						j+=1
					if NoEncontrado:
						Borrar.append(i["patologia"])
			for j in Borrar:
				self.model.delete_ejercicio_patologias(nombre_ejercicio, j)

		self.on_ejercicios(boton)

#############################################################################################################################GRUPOS

	def on_grupos(self, boton):
		gruposRegistrados = self.model.get_grupos()
		self.view.grupo()
		if gruposRegistrados is not None:
			for i in range(0, len(gruposRegistrados)):
				id_grupo = str(gruposRegistrados[i]["id_grupo"])
				horario = str(gruposRegistrados[i]["horario"])
				usuariosDelGrupo = ""
				for i in range(len(self.model.get_usuarios_por_grupo(id_grupo))-1):
					usuariosDelGrupo += str(self.model.get_usuarios_por_grupo(id_grupo)[i]["Nombre"])  + " " +  str(self.model.get_usuarios_por_grupo(id_grupo)[i]["Apellidos"]) + " - " 
				if len(self.model.get_usuarios_por_grupo(id_grupo)) != 0:
					usuariosDelGrupo += str(self.model.get_usuarios_por_grupo(id_grupo)[len(self.model.get_usuarios_por_grupo(id_grupo))-1]["Nombre"])  + " " +  str(self.model.get_usuarios_por_grupo(id_grupo)[len(self.model.get_usuarios_por_grupo(id_grupo))-1]["Apellidos"])
				self.model.get_usuarios_por_grupo(id_grupo)
				self.view.filtroGrupos.get_model().append([id_grupo,horario, usuariosDelGrupo]) #Introducir en la vista los datos de la BD
		self.view.clickGrupos(self)
		self.view.clickEnlaces(self)

	def on_grupo_seleccionado(self): #en caso de que se seleccione una fila
		conjunto, seleccionado = self.view.gruposTree.get_selection().get_selected()
		if seleccionado is not None:
			fila_selec = conjunto.convert_iter_to_child_iter(seleccionado)
			return (conjunto.get_model()[fila_selec])

	def on_eliminar_grupo(self, boton):
		datos_grupo = self.model.get_grupo((self.on_grupo_seleccionado())[0])
		if datos_grupo is not None:
			self.view.Emergente_eliminar_Grupo(self, str(datos_grupo["id_grupo"]))


	def emergente_decision_grupo(self, boton, id_respuesta, idgrupo):    #depende de el boton pulsado en la emergente, se borra un ejercicio o no
		if id_respuesta == Gtk.ResponseType.YES:
			self.model.delete_grupo(idgrupo)
			self.on_grupos(boton)

	def activar_botonesGrupo(self, seleccion):
		self.view.Eliminar.set_sensitive(True)
		self.view.VerMod.set_sensitive(True)
		self.view.clickSobreGrupos(self)

	def on_NuevoGrupo(self, boton):
		self.view.Formulario_Grupo(None)
		self.view.AccionesEnElFormGrupo(self)

	def on_ActualizarGrupo(self, boton):
		datos_grupo = self.model.get_grupo((self.on_grupo_seleccionado())[0])
		if datos_grupo is not None:
			usuarios = self.model.get_usuarios_por_grupo(datos_grupo["id_grupo"])
			if usuarios != []:
				datos_grupo["usuario"] = []
				for i in usuarios:
					datos_grupo["usuario"].append(str(i["id"]) + " - " + i["Nombre"] + " " + i["Apellidos"])
			self.view.Formulario_Grupo(datos_grupo)
			self.view.AccionesEnElFormGrupo(self)

	def on_guardar_en_BD_grupos(self, boton):    #especificacion de interaccion con la BD de grupos en caso de MODIFICACIÓN
		return self.on_Interactuar_con_BD_grupos("insertar", boton)

	def on_actualizar_en_BD_grupos(self, boton):	#especificacion de interaccion con la BD de grupos en caso de CREACIÓN
		return self.on_Interactuar_con_BD_grupos("modificar", boton)

	def on_Interactuar_con_BD_grupos(self, accion, boton):   #Esta funcion generaliza la de AÑADIR y la de MODIFICAR un usuario
		guardar = self.view.datosAGuardarDeGrupos()
		if guardar is None:
			return
		if accion is "insertar":
			(usuariosSeleccionados, horario) = guardar
		else:
			(idgrupo, usuariosSeleccionados, horario) = guardar
		if usuariosSeleccionados.get_children() == []:
			self.view.error(4)
			return

		if horario.get_iter_first() == None:
			self.view.error(4)
			return

		iterador = horario.get_iter_first()
		siguiente = horario.iter_next(iterador)

		cadenaHorario = ""
		while horario.iter_next(iterador) != None:
			cadenaHorario += horario[iterador][0] + " "
			cadenaHorario += horario[iterador][1] + ","
			iterador = horario.iter_next(iterador)
		cadenaHorario += horario[iterador][0] + " "
		cadenaHorario += horario[iterador][1]

		if accion is "insertar":
			idgrupo = self.model.insert_grupo(cadenaHorario)
			for i in usuariosSeleccionados.get_children():
				objetos = (int(idgrupo), int(i.get_children()[0].get_label().split(" ")[0]))
				self.model.update_grupo_user(objetos)

		else:
			objetos = (cadenaHorario, int(idgrupo))
			self.model.update_grupo(objetos)

			if usuariosSeleccionados.get_children() != []:	#COMPROBACION EN CASO DE ACTUALIZACIONES DE SU LISTA DE USUARIOS EN VISTA Y EN MODELO(BD)
				for i in range(0, len(usuariosSeleccionados.get_children())):
					idusuario = int(usuariosSeleccionados.get_children()[i].get_child().get_label().split(" ")[0])
					objetos = (int(idgrupo), idusuario)
					self.model.update_grupo_user(objetos)

			Borrar = []
			for i in (self.model.get_usuarios()):		#COMPROBACION DE SI SE BORRO ALGUNA ENTRADA EN LA VISTA, COMPARANDOLA CON LO GUARDADO EN LA BD
				if self.model.get_usuarios() != []:					#en caso de que YA estuviera vacia en BD no hay que comprobar borrados en ella
					j=0
					NoEncontrado = True
					while(j<len(usuariosSeleccionados.get_children()) and NoEncontrado):
						usuario = int(usuariosSeleccionados.get_children()[j].get_child().get_label().split(" ")[0])
						NoEncontrado = (usuario != i["id"])
						j+=1
					if NoEncontrado:
						Borrar.append(i["id"])
			
			for j in Borrar:
				objetos = (None, j)
				self.model.update_grupo_user(objetos)

		self.on_grupos(boton)

	def on_buscar_usuario(self, boton):
		if self.view.usersEncontrados.get_children() != []:
			for i in range(len(self.view.usersEncontrados.get_children())):
				self.view.usersEncontrados.get_children()[0].destroy()
		usuario = self.view.busqUsuario.get_text()
		usuarios = self.model.get_usuarios_por_nombre(usuario)
		if usuarios != []:
			usuarios.append(self.model.get_usuarios_por_apellidos(usuario))
		else:
			usuarios = self.model.get_usuarios_por_apellidos(usuario)
		if usuario != "":
			if usuarios != []:
				for i in range(len(usuarios)):
					if usuarios[i] != []:
						id = usuarios[i]["id"]
						Nombre = str(usuarios[i]["Nombre"])
						Apellidos = str(usuarios[i]["Apellidos"])
						self.view.resultadosUsuario(id, Apellidos, Nombre)		

	def on_insertar_usuario(self, boton, usersYaAlmacenados):
		usuariosSeleccionados = self.view.usersEncontrados.get_selected_rows()
		aux = []
		for i in usersYaAlmacenados:
			aux.append(i.get_children()[0].get_label())
		for i in range(len(usuariosSeleccionados)):
			self.view.usersEncontrados.remove(usuariosSeleccionados[i])
			if usuariosSeleccionados[i].get_children()[0].get_label() not in aux:
				for j in usuariosSeleccionados:
					aux.append(j.get_children()[0].get_label())
				self.view.usersSeleccionados.add(usuariosSeleccionados[i])
			self.view.usersSeleccionados.unselect_all()

	def on_quitar_usuario(self, boton):
		usersSeleccionados = self.view.usersSeleccionados.get_selected_rows()
		for i in range(len(usersSeleccionados)):
			
			usersSeleccionados[0].destroy()
			self.view.usersSeleccionados.unselect_all()

	def on_insertar_dias(self, boton):
		self.view.nuevoHorario()

	def on_eliminar_dias(self, boton):
		conjunto, seleccionado = self.view.resumen.get_selection().get_selected()
		if seleccionado is not None:
			fila_selec = conjunto.convert_iter_to_child_iter(seleccionado)
			self.view.liststore.remove(fila_selec)


################################################################################################################SESIONES

	def on_sesiones(self, boton):
		sesionesRegistradas = self.model.get_sesiones()
		self.view.sesion()
		if sesionesRegistradas is not None:
			for i in range(0, len(sesionesRegistradas)):
				idsesion = str(sesionesRegistradas[i]["id_sesion"])
				objetivos = str(sesionesRegistradas[i]["objetivos"])
				ejerciciosUtilizados = ""
				materiales = str(sesionesRegistradas[i]["materiales"])
				for i in self.model.get_sesion_ejercicios(int(idsesion)):
					ejerciciosUtilizados = str(i["nombre_ejercicio"])  + ", " + ejerciciosUtilizados 
				self.view.filtroSesiones.get_model().append([idsesion,objetivos, ejerciciosUtilizados,materiales]) #Introducir en la vista los datos de la BD
		self.view.clickSesiones(self)
		self.view.clickEnlaces(self)

	def on_NuevaSesion(self, boton):
		ejercicios_guardados = self.model.get_ejercicios()
		self.view.Formulario_Sesion(self, None, ejercicios_guardados)
		self.view.AccionesEnElFormSesion(self)

	def on_ActualizarSesion(self, boton):
		ejercicios_guardados = self.model.get_ejercicios()
		datos_sesion = self.model.get_sesion((self.on_sesion_seleccionado())[0])
		if datos_sesion is not None:
			ejercicios = self.model.get_sesion_ejercicios(datos_sesion["id_sesion"])
			if ejercicios != []:
				datos_sesion["ejercicio"] = []
				for i in ejercicios:
					datos_sesion["ejercicio"].append(str(i["nombre_ejercicio"]))
			self.view.Formulario_Sesion(self, datos_sesion, ejercicios_guardados)
			self.view.AccionesEnElFormSesion(self)

	def activar_botonesSesion(self, seleccion):
		self.view.Eliminar.set_sensitive(True)
		self.view.VerMod.set_sensitive(True)
		self.view.clickSobreSesiones(self)

	def on_sesion_seleccionado(self): #en caso de que se seleccione una fila
		conjunto, seleccionado = self.view.SesionesTree.get_selection().get_selected()
		if seleccionado is not None:
			fila_selec = conjunto.convert_iter_to_child_iter(seleccionado)
			return (conjunto.get_model()[fila_selec])

	def on_eliminar_sesion(self, boton):
		datos_sesion = self.model.get_sesion((self.on_sesion_seleccionado())[0])
		if datos_sesion is not None:
			self.view.Emergente_eliminar_Sesion(self,datos_sesion["id_sesion"])


	def emergente_decision_sesion(self, boton, id_respuesta, idsesion):    #depende de el boton pulsado en la emergente, se borra una sesion o no
		if id_respuesta == Gtk.ResponseType.YES:
			self.model.delete_sesion(idsesion)
			self.on_sesiones(boton)


	def on_guardar_en_BD_sesiones(self, boton):    #especificacion de interaccion con la BD de sesiones en caso de MODIFICACIÓN
		return self.on_Interactuar_con_BD_sesiones("insertar", boton)

	def on_actualizar_en_BD_sesiones(self, boton):	#especificacion de interaccion con la BD de sesiones en caso de CREACIÓN
		return self.on_Interactuar_con_BD_sesiones("modificar", boton)

	def on_Interactuar_con_BD_sesiones(self, accion, boton):   #Esta funcion generaliza la de AÑADIR y la de MODIFICAR una sesion
		guardar = self.view.datosAGuardarDeSesiones()
		if guardar is None:
			return
		if accion is "insertar":
			(objetivos, ejerciciosSeleccionados, cargas, materialesUtilizados) = guardar
		else:
			(idsesion, objetivos, ejerciciosSeleccionados, cargas, materialesUtilizados) = guardar

		start, end = objetivos.get_bounds()
		objetivos = objetivos.get_text(start, end, True)
		if ejerciciosSeleccionados.get_children() == []:
			self.view.error(4)
			return

		materiales = ""
		for i in materialesUtilizados.get_children():
			 materiales += i.get_children()[0].get_text() + ", "

		if accion is "insertar":
			idsesion = self.model.insert_sesion(str(objetivos), str(cargas), materiales)
			for i in ejerciciosSeleccionados.get_children():
				self.model.insert_sesion_ejercicio(int(idsesion), i.get_children()[0].get_text())

		else:
			objetos = (objetivos, cargas, materiales, int(idsesion))
			self.model.update_sesion(objetos)

			if ejerciciosSeleccionados.get_children() != []:				#COMPROBACION EN CASO DE ACTUALIZACIONES DE SU LISTA DE LESIONS/PATOLOGIAS EN VISTA Y EN MODELO(BD)
				for i in range(0, len(ejerciciosSeleccionados.get_children())):
					ejercicio = ejerciciosSeleccionados.get_children()[i].get_child().get_label()
					lista = []
					for j in self.model.get_sesion_ejercicios(int(idsesion)):
						lista.append(j["nombre_ejercicio"])
					if ejercicio not in lista:
						a = self.model.insert_sesion_ejercicio(int(idsesion), ejercicio)

			Borrar = []
			for i in (self.model.get_sesion_ejercicios(int(idsesion))):		#COMPROBACION DE SI SE BORRO ALGUNA ENTRADA EN LA VISTA, COMPARANDOLA CON LO GUARDADO EN LA BD
				if self.model.get_sesion_ejercicios(int(idsesion)) != []:					#en caso de que YA estuviera vacia en BD no hay que comprobar borrados en ella
					j=0
					NoEncontrado = True
					while(j<len(ejerciciosSeleccionados.get_children()) and NoEncontrado):
						ejercicio = ejerciciosSeleccionados.get_children()[j].get_child().get_label()
						NoEncontrado = (ejercicio != i["nombre_ejercicio"])
						j+=1
					if NoEncontrado:
						Borrar.append(i["nombre_ejercicio"])
			
			for j in Borrar:
				self.model.delete_sesion_ejercicios(idsesion, j)
			
		self.on_sesiones(boton)

	def ejercicioNuevo(self, boton, ejerciciosSeleccionados, ejercicioNuevo):

		if ejercicioNuevo == None:
			ejercicioNuevo = self.view.añadirEjericicioEntrada.get_active_text()
			if ejercicioNuevo == None:
				return
		aux = []
		for i in ejerciciosSeleccionados:
			aux.append(i.get_children()[0].get_label())
		if ejercicioNuevo in aux:
			return
		label = Gtk.Label(ejercicioNuevo)
		fila = Gtk.ListBoxRow()
		fila.add(label)
		self.view.ejerciciosSeleccionados.add(fila)
		materiales_necesarios = self.model.get_materiales_ejercicio(label.get_text()) #cogemos sus materiales
		for i in materiales_necesarios:
			aux = []
			for j in self.view.materialesUtilizados:
				aux.append(j.get_children()[0].get_label())
			if i["nombre_material"] not in aux:
				label2 = Gtk.Label(i["nombre_material"])
				fila2 = Gtk.ListBoxRow()
				fila2.add(label2)
				self.view.materialesUtilizados.add(fila2)

		lesiones_asociadas = self.model.get_ejercicio_lesiones(label.get_text()) #cogemos sus lesiones/patologías
		for i in lesiones_asociadas:
			aux = []
			for j in self.view.incompatibilidades:
				aux.append(j.get_children()[0].get_label())
			if i["lesion"] not in aux:
				label3 = Gtk.Label(i["lesion"])
				fila3 = Gtk.ListBoxRow()
				fila3.add(label3)
				self.view.incompatibilidades.add(fila3)

		patologias_asociadas = self.model.get_ejercicio_patologias(label.get_text()) #cogemos sus lesiones/patologías
		for i in patologias_asociadas:
			aux = []
			for j in self.view.incompatibilidades:
				aux.append(j.get_children()[0].get_label())
			if i["patologia"] not in aux:
				label4 = Gtk.Label(i["patologia"])
				fila4 = Gtk.ListBoxRow()
				fila4.add(label4)
				self.view.incompatibilidades.add(fila4)

		self.CambiarGrafica()
		self.view.win.show_all()

	def eliminarejerc(self, boton):
		ejerciciosSeleccionados = self.view.ejerciciosSeleccionados.get_selected_rows()
		for i in range(len(ejerciciosSeleccionados)):
			
			materiales_necesarios = self.model.get_materiales_ejercicio(ejerciciosSeleccionados[0].get_children()[0].get_text())
			for i in materiales_necesarios:				#cuando eliminamos un ejercicio de la vista, eliminamos tambien sus materiales
				for j in self.view.materialesUtilizados.get_children():
					if i["nombre_material"] == j.get_children()[0].get_text():
						j.destroy()

			lesiones_asociadas = self.model.get_ejercicio_lesiones(ejerciciosSeleccionados[0].get_children()[0].get_text())
			for i in lesiones_asociadas:				#cuando eliminamos un ejercicio de la vista, eliminamos tambien sus lesiones
				for j in self.view.incompatibilidades.get_children():
					if i["lesion"] == j.get_children()[0].get_text():
						j.destroy()

			patologias_asociadas = self.model.get_ejercicio_patologias(ejerciciosSeleccionados[0].get_children()[0].get_text())
			for i in patologias_asociadas:				#cuando eliminamos un ejercicio de la vista, eliminamos tambien sus patologias
				for j in self.view.incompatibilidades.get_children():
					if i["patologia"] == j.get_children()[0].get_text():
						j.destroy()
			
			ejerciciosSeleccionados[0].destroy()
			self.CambiarGrafica()
			self.view.ejerciciosSeleccionados.unselect_all()


	def CambiarGrafica(self):
		aero=0
		coord=0
		equi=0
		frz=0
		for i in self.view.ejerciciosSeleccionados.get_children():
			cargas = self.model.get_ejercicio(i.get_children()[0].get_text())["cargas"]
			aero += int(cargas.split(".0%")[0])
			coord += int(cargas.split(".0% /")[1])
			equi += int(cargas.split(".0% /", 3)[2])
			frz += int(cargas.split(".0% /", 3)[3].split(".")[0])
		if len(self.view.ejerciciosSeleccionados.get_children()) == 0:
			self.view.CambiarGraficaVista(0, 0, 0, 0)
		else:
			aero = aero / len(self.view.ejerciciosSeleccionados.get_children())
			coord = coord / len(self.view.ejerciciosSeleccionados.get_children())
			equi = equi / len(self.view.ejerciciosSeleccionados.get_children())
			frz = frz / len(self.view.ejerciciosSeleccionados.get_children())
			self.view.CambiarGraficaVista(aero, coord, equi, frz)

######################################################################################################################################

	def on_programacion(self, boton):
			sesionesProgramadas = self.model.get_progs()
			self.view.programacion()
			if sesionesProgramadas is not None:
				for i in range(0, len(sesionesProgramadas)):
					idprog = str(sesionesProgramadas[i]["id_prog"])
					idsesion = str(sesionesProgramadas[i]["id_sesion"])
					fecha = str(sesionesProgramadas[i]["fecha"])
					idgrupo = str(sesionesProgramadas[i]["id_grupo"])
					sesion = self.model.get_sesion(int(idsesion))
					descripcion = sesion["objetivos"]
					self.view.filtroProg.get_model().append([idprog,idsesion,fecha, idgrupo,descripcion]) #Introducir en la vista los datos de la BD
			self.view.clickProgramacion(self)
			self.view.clickEnlaces(self)

	def on_NuevaProg(self, boton):
		materiales = self.model.get_materiales()
		grupos = self.model.get_grupos()
		self.filtrado = []  #usado para el filtrado de seleccion de sesiones
		self.view.Formulario_Prog(grupos, materiales, None, None, self)
		self.view.AccionesEnElFormProg(self)
		return

	def activar_botonesProg(self, seleccion):
			if self.on_prog_seleccionado() != None:
				self.view.VerMod.set_sensitive(True)  #activamos los botones si se hace una selección de una fila
				self.view.Eliminar.set_sensitive(True)
				datos_prog = self.model.get_prog((self.on_prog_seleccionado())[0])
				day = datos_prog["fecha"].split("/", 1)[0]
				month= datos_prog["fecha"].split("/", 1)[1].split("/")[0]
				year = datos_prog["fecha"].split("/", 2)[2]
				today = date.today()
				dia = today.strftime("%d")
				mes = today.strftime("%m")
				ano = today.strftime("%Y")
				fechaHoy = date(int(ano), int(mes), int(dia))
				fecha = date(int(year), int(month), int(day))
				if fechaHoy >= fecha:
					self.view.postsesion.set_sensitive(True)
				else:
					self.view.postsesion.set_sensitive(False)
				self.view.clickSobreProg(self)

	def on_ActualizarProg(self, boton):
		self.filtrado = []  #usado para el filtrado de seleccion de sesiones
		materiales = self.model.get_materiales()
		grupos = self.model.get_grupos()
		datos_prog = self.model.get_prog((self.on_prog_seleccionado())[0])
		usuarios_prog = self.model.get_usuarios_from_prog(datos_prog["id_prog"])
		users = []
		for i in usuarios_prog:
			if self.model.get_activo(i["id"])["activo"] == "Sí":
				usuario = self.model.get_user(i["id"])
				if usuario != []:
					users.append(str(usuario["id"]) + " - " + usuario["Nombre"] + " " + usuario["Apellidos"])

		if datos_prog is not None:
			self.view.Formulario_Prog(grupos, materiales, datos_prog, users, self)
		self.view.AccionesEnElFormProg(self)

	def on_prog_seleccionado(self): #en caso de que se seleccione una fila
		conjunto, seleccionado = self.view.prog.get_selection().get_selected()
		if seleccionado is not None:
			fila_selec = conjunto.convert_iter_to_child_iter(seleccionado)
			return (conjunto.get_model()[fila_selec])

	def on_eliminar_prog(self, boton):
		datos_prog = self.model.get_prog((self.on_prog_seleccionado())[0])
		if datos_prog is not None:
			self.view.Emergente_eliminar_prog(self, datos_prog["id_prog"])

	def emergente_decision_prog(self, boton, id_respuesta, id):    #depende de el boton pulsado en la emergente, se borra un usuario o no
		if id_respuesta == Gtk.ResponseType.YES:
			self.model.delete_prog(int(id))
			self.on_programacion(boton)
	
	def on_guardar_en_BD_prog(self, boton):    #especificacion de interaccion con la BD de programacion en caso de MODIFICACIÓN
		return self.on_Interactuar_con_BD_prog("insertar", boton)

	def on_actualizar_en_BD_prog(self, boton):	#especificacion de interaccion con la BD de programacion en caso de CREACIÓN
		return self.on_Interactuar_con_BD_prog("modificar", boton)

	def on_Interactuar_con_BD_prog(self, accion, boton):   #Esta funcion generaliza la de AÑADIR y la de MODIFICAR un programacion
		guardar = self.view.datosAGuardarDeProg()
		if guardar is None:
			return

		if accion is "insertar":
			(idsesion, idgrupo, fecha, vueltas, calentamiento, descanso, duracion, reposo, usuariosSeleccionados) = guardar
		else:
			(idprog, idsesion, idgrupo, fecha, vueltas, calentamiento, descanso, duracion, reposo, usuariosSeleccionados) = guardar

		if idsesion == None or idgrupo == None or vueltas == "" or calentamiento == "" or descanso == "" or duracion == "" or reposo == "":
			self.view.error(4)
			return


		if self.on_comprobar_numeros(boton, True)[0] != True:
			return

		usuariosgrupo = (self.model.get_usuarios_por_grupo(int(idgrupo)))
		usuariosAux= usuariosSeleccionados.get_children()
		usuariosEnSesion = []
		if usuariosAux !=[]:
			for i in usuariosAux:
				x = {}
				x["id"] = int(i.get_child().get_label().split(" ")[0])
				usuariosEnSesion.append(x)
		usuariosEnSesion += usuariosgrupo


		(ano, mes, dia) = fecha
		fecha = date(int(ano), int(mes)+1, int(dia))
		fecha = fecha.strftime("%d/%m/%Y")

		dias = self.model.get_grupo(int(idgrupo))["horario"].split(",")
		diasSemana = []
		for i in dias:
			diasSemana.append(i.split(" ")[0])	

		dia = fecha.split("/", 1)[0]
		month = fecha.split("/", 1)[1].split("/")[0]
		ano = fecha.split("/", 2)[2]
		data = date(int(ano), int(month), int(dia))
		if self.week(data.weekday()) not in diasSemana:
			self.noseguarda = False
			self.view.avisoDiasGrupo("grupo " + idgrupo, self)
			if self.noseguarda:
				return

		if accion is "insertar":
			objetos = (int(idsesion.get_children()[0].get_text()), int(idgrupo), str(fecha), str(vueltas), str(calentamiento), str(descanso), str(duracion), str(reposo), "")
			idprog = self.model.insert_prog(objetos)

			for i in usuariosSeleccionados.get_children():
				objetos = (idprog, int(idsesion.get_children()[0].get_text()), int(idgrupo), int(i.get_children()[0].get_label().split(" ")[0]), str(fecha))
				self.model.insert_prog_usuario(objetos)

			for j in usuariosEnSesion:
				objetos2 = (idprog, int(j["id"]), "", "")
				self.model.insert_valoracion_personal(objetos2)
		else:
			objetos = (int(idsesion.get_children()[0].get_text()), int(idgrupo), str(fecha), str(vueltas), str(calentamiento), str(descanso), str(duracion), str(reposo), int(idprog))
			self.model.update_prog(objetos)
			objetos2 = (int(idsesion.get_children()[0].get_text()), int(idgrupo), str(fecha), int(idprog))
			self.model.update_prog_usuario(objetos2)

			for j in usuariosEnSesion:
				objetos2 = ("", "", idprog, int(j["id"]))
				resultado = self.model.update_prog_valoracion_personal(objetos2)
				if resultado == 0:
					objetos2 = (idprog, int(j["id"]), "", "")
					self.model.insert_valoracion_personal(objetos2)

			if usuariosSeleccionados.get_children() != []:				#COMPROBACION EN CASO DE ACTUALIZACIONES DE SU LISTA DE USUARIOS EN VISTA Y EN MODELO(BD)
				for i in range(0, len(usuariosSeleccionados.get_children())):
					lista = []
					for j in self.model.get_usuarios_from_prog(int(idprog)):
						lista.append(str(j["id"]))
					if str(usuariosSeleccionados.get_children()[i].get_child().get_label().split(" ")[0]) not in lista:
						objetos = (int(idprog), int(idsesion.get_children()[0].get_text()), int(idgrupo), int(usuariosSeleccionados.get_children()[i].get_child().get_label().split(" ")[0]), str(fecha))
						self.model.insert_prog_usuario(objetos)

			Borrar = []
			for i in (self.model.get_usuarios_from_prog(int(idprog))):		#COMPROBACION DE SI SE BORRO ALGUNA ENTRADA EN LA VISTA, COMPARANDOLA CON LO GUARDADO EN LA BD
				if self.model.get_usuarios_from_prog(int(idprog)) != []:					#en caso de que YA estuviera vacia en BD no hay que comprobar borrados en ella
					j=0
					NoEncontrado = True
					while(j<len(usuariosSeleccionados.get_children()) and NoEncontrado):
						usuario = usuariosSeleccionados.get_children()[j].get_child().get_label().split(" ")[0]
						NoEncontrado = (int(usuario) != i["id"])
						j+=1
					if NoEncontrado:
						Borrar.append(i["id"])
			
			for j in Borrar:
				self.model.delete_prog_usuario(j, int(idprog))

		ejerciciosIncluidos = self.model.get_sesion_ejercicios(int(idsesion.get_children()[0].get_text()))

		lesiones = []
		for i in ejerciciosIncluidos:
			if self.model.get_ejercicio_lesiones(i["nombre_ejercicio"]) not in lesiones:
				lesiones +=(self.model.get_ejercicio_lesiones(i["nombre_ejercicio"])) 
		for q in lesiones:
			for x in usuariosEnSesion:
				lesionesuser = self.model.get_user_lesiones(int(x["id"]))
				for j in lesionesuser:
					if q == j:
						self.view.avisoLesion(int(x["id"]))

		patologias = []
		for i in ejerciciosIncluidos:
			if self.model.get_ejercicio_patologias(i["nombre_ejercicio"]) not in patologias:
				patologias +=(self.model.get_ejercicio_patologias(i["nombre_ejercicio"])) 
		for q in patologias:
			for x in usuariosEnSesion:
				patologiasuser = self.model.get_user_patologias(int(x["id"]))
				for j in patologiasuser:
					if q == j:
						self.view.avisoLesion(int(x["id"]))

		self.on_programacion(boton)

	def week(self, i):
		switcher= {0:'Lunes', 1:'Martes', 2:'Miércoles', 3:'Jueves', 4:'Viernes', 5:'Sábado', 6:'Domingo'}
		return switcher.get(i,"Invalid day of week")

	def emergente_decision_fecha(self, boton, id_respuesta):
		if id_respuesta == Gtk.ResponseType.NO:
			self.noseguarda = True

	def on_filtrar(self, widget, path):
		current_value = self.view.store[path][1]
        # change the boolean value of the selected row in the model
		self.view.store[path][1] = not current_value
        # new current value!
		current_value = not current_value
        # if length of the path is 1 (that is, if we are selecting a general item)
		if len(path) == 1:
			# get the iter associated with the path
			piter = self.view.store.get_iter(path)
			# get the iter associated with its first child
			citer = self.view.store.iter_children(piter)
			# while there are children, change the state of their boolean value
			# to the value of the general item
			while citer is not None:
				self.view.store[citer][1] = current_value
				citer = self.view.store.iter_next(citer)
        # if the length of the path is not 1 (that is, if we are selecting a
        # specific item)
		elif len(path) != 1:
			# get the first child of the parent of the book (the first book of
			# the general item)
			citer = self.view.store.get_iter(path)
			piter = self.view.store.iter_parent(citer)
			citer = self.view.store.iter_children(piter)

			if current_value:
				self.filtrado.append(self.view.store[path][0] +" "+ self.view.store[piter][0])   #añadimos a una lista aux de filtros para utilizarla en vista
			else:
				self.filtrado.remove(self.view.store[path][0] +" "+ self.view.store[piter][0])  #quitamos de la lista de filtros para reiniciarlo

			# check if all the children are selected
			all_selected = True
			while citer is not None:
				if self.view.store[citer][1] == False:
					all_selected = False
					break
				citer = self.view.store.iter_next(citer)
			# if they do, the general item as well is selected; otherwise it is not
			self.view.store[piter][1] = all_selected

	def on_buscar_sesiones(self, boton):
		for i in self.view.sesionResultante.get_children():     #reiniciamos los resultados para volver a actuar con el filtro
			i.destroy()
		sesionesdisp = self.model.get_sesiones()

		if self.filtrado == []:
			for i in sesionesdisp:
				str(i['id_sesion'])
				fila = Gtk.ListBoxRow()
				fila.add(Gtk.Label(str(i['id_sesion'])))
				self.view.sesionResultante.add(fila)

		for i in self.filtrado:
			aux = []
			for x in self.view.sesionResultante: 
				aux.append(x.get_children()[0].get_label())
			for j in sesionesdisp:
				if str(j['id_sesion']) not in aux:
					if i.endswith("Aeróbico"):     #filtrado en funcion de los campos introducidos
						if int(j['cargas'].split("%")[0].split(".")[0]) >= int(i.split(" ")[0].split("%")[0].split("=")[1]):
							fila = Gtk.ListBoxRow()
							fila.add(Gtk.Label(str(j['id_sesion'])))
							self.view.sesionResultante.add(fila)
					if i.endswith("Coordinación"):
						if int(j['cargas'].split("%")[1].split("/")[1].split(".")[0]) >= int(i.split(" ")[0].split("%")[0].split("=")[1]):
							fila = Gtk.ListBoxRow()
							fila.add(Gtk.Label(str(j['id_sesion'])))
							self.view.sesionResultante.add(fila)
					if i.endswith("Equilibrio"):
						if int(j['cargas'].split("%")[2].split("/")[1].split(".")[0]) >= int(i.split(" ")[0].split("%")[0].split("=")[1]):
							fila = Gtk.ListBoxRow()
							fila.add(Gtk.Label(str(j['id_sesion'])))
							self.view.sesionResultante.add(fila)
					if i.endswith("Fuerza"):
						if int(j['cargas'].split("%")[3].split("/")[1].split(".")[0]) >= int(i.split(" ")[0].split("%")[0].split("=")[1]):
							fila = Gtk.ListBoxRow()
							fila.add(Gtk.Label(str(j['id_sesion'])))
							self.view.sesionResultante.add(fila)
					if i.endswith("Materiales"):
						x=0
						while j['materiales'].split(", ")[x] != "":
							if j['materiales'].split(", ")[x] == i.split("Materiales")[0].strip():
								fila = Gtk.ListBoxRow()
								fila.add(Gtk.Label(str(j['id_sesion'])))
								self.view.sesionResultante.add(fila)
							x+=1
		self.view.win.show_all()

	def on_sesionElegida(self, sesiones, sesionPulsada):
		if sesionPulsada != None:
			sesion = self.model.get_sesion(int(sesionPulsada.get_children()[0].get_label()))
			ejercicios = self.model.get_sesion_ejercicios(int(sesionPulsada.get_children()[0].get_label()))
			self.view.Objetivos.set_text(sesion["objetivos"])
			self.view.Materiales.set_text(sesion["materiales"])
			texto = ""
			for i in ejercicios:
				texto += i["nombre_ejercicio"] + ", "
			self.view.Ejercicios.set_text(texto)
		else:
			self.view.Objetivos.set_text("")
			self.view.Materiales.set_text("")
			self.view.Ejercicios.set_text("")

	def on_sumaTiempo(self, boton):
		calentmin=0
		descamin=0
		duramin=0
		repmin=0
		calents=0
		descas=0
		duras=0
		reps=0
		vueltas=0

		sesionPulsada = self.view.sesionResultante.get_selected_row()
		if sesionPulsada == None:
			self.view.error(9)
			return

		if self.view.vueltas1.get_text() == "" or self.view.calent1.get_text() == "" or self.view.descanso1.get_text() == "" or self.view.duracion1.get_text() == "" or self.view.reposo1.get_text() == "":
			return

		(correcto, reps, repmin, duras, duramin, descas, descamin, calents, calentmin, vueltas) = self.on_comprobar_numeros(boton, False)
		if correcto != True:
			self.view.tiempoTotal.set_label("")
			return

		numEjercicios = len(self.model.get_sesion_ejercicios(int(sesionPulsada.get_children()[0].get_label())))

		if vueltas != 1:
			minutos = calentmin + (numEjercicios - 1) * descamin * vueltas + numEjercicios * duramin * vueltas +  repmin * (vueltas - 1)
			segundos = calents + (numEjercicios - 1) * descas * vueltas + numEjercicios * duras * vueltas + (vueltas - 1) * reps
		else:
			minutos = calentmin + descamin * (numEjercicios - 1) + numEjercicios * duramin
			segundos = calents + descas  * (numEjercicios - 1) + numEjercicios * duras
		minExtra=0
		segExtra=0
		if segundos > 59 :
				minExtra = segundos // 60
				segExtra = segundos % 60
		else:
			segExtra = segundos
		self.view.tiempoTotal.set_label(str(minutos + minExtra) + " min " + str(segExtra) + " s")
		self.view.win.show_all()

	def on_comprobar_numeros(self, boton, mostrarError):
		calentmin=0
		descamin=0
		duramin=0
		repmin=0
		calents=0
		descas=0
		duras=0
		reps=0
		vueltas=0
		if self.comprobarTelefono(self.view.vueltas1.get_text()) == True:
			vueltas = int(self.view.vueltas1.get_text())
		elif (mostrarError):
			self.view.error(1)
			return (False, None,None, None, None, None, None, None, None, None)
		else:
			return (False, None,None, None, None, None, None, None, None, None)

		if self.view.calent1.get_text().endswith("min"):
			if self.comprobarTelefono(self.view.calent1.get_text().split("min")[0].strip()) == True:
				calentmin = int(self.view.calent1.get_text().split("min")[0].strip())
			elif (mostrarError):
				self.view.error(1)
				return (False, None,None, None, None, None, None, None, None, None)
			else:
				return (False, None,None, None, None, None, None, None, None, None)
			
		elif self.view.calent1.get_text().endswith("s"):
			if self.comprobarTelefono(self.view.calent1.get_text().split("s")[0].strip()) == True:
				calents = int(self.view.calent1.get_text().split("s")[0].strip())
			elif (mostrarError):
				self.view.error(1)
				return (False, None,None, None, None, None, None, None, None, None)
			else:
				return (False, None,None, None, None, None, None, None, None, None)
		elif (mostrarError):
			self.view.error(1)
			return (False, None,None, None, None, None, None, None, None, None)
		else:
			return (False, None,None, None, None, None, None, None, None, None)

		if self.view.descanso1.get_text().endswith("min"):
			if self.comprobarTelefono(self.view.descanso1.get_text().split("min")[0].strip()) == True:
				descamin = int(self.view.descanso1.get_text().split("min")[0].strip())
			elif (mostrarError):
				self.view.error(1)
				return (False, None,None, None, None, None, None, None, None, None)
			else:
				return (False, None,None, None, None, None, None, None, None, None)
		elif self.view.descanso1.get_text().endswith("s"):
			if self.comprobarTelefono(self.view.descanso1.get_text().split("s")[0].strip()) == True:
				descas = int(self.view.descanso1.get_text().split("s")[0].strip())
			elif (mostrarError):
				self.view.error(1)
				return (False, None,None, None, None, None, None, None, None, None)
			else:
				return (False, None,None, None, None, None, None, None, None, None)
		elif (mostrarError):
			self.view.error(1)
			return (False, None,None, None, None, None, None, None, None, None)
		else:
			return (False, None,None, None, None, None, None, None, None, None)

		if self.view.duracion1.get_text().endswith("min"):
			if self.comprobarTelefono(self.view.duracion1.get_text().split("min")[0].strip()) == True:
				duramin = int(self.view.duracion1.get_text().split("min")[0].strip())
			elif (mostrarError):
				self.view.error(1)
				return (False, None,None, None, None, None, None, None, None, None)
			else:
				return (False, None,None, None, None, None, None, None, None, None)
		elif self.view.duracion1.get_text().endswith("s"):
			if self.comprobarTelefono(self.view.duracion1.get_text().split("s")[0].strip()) == True:
				duras = int(self.view.duracion1.get_text().split("s")[0].strip())
			elif (mostrarError):
				self.view.error(1)
				return (False, None,None, None, None, None, None, None, None, None)
			else:
				return (False, None,None, None, None, None, None, None, None, None)
		elif (mostrarError):
			self.view.error(1)
			return (False, None,None, None, None, None, None, None, None, None)
		else:
			return (False, None,None, None, None, None, None, None, None, None)

		if self.view.reposo1.get_text().endswith("min"):
			if self.comprobarTelefono(self.view.reposo1.get_text().split("min")[0].strip()) == True:
				repmin = int(self.view.reposo1.get_text().split("min")[0].strip())
			elif (mostrarError):
				self.view.error(1)
				return (False, None,None, None, None, None, None, None, None, None)
			else:
				return (False, None,None, None, None, None, None, None, None, None)
		elif self.view.reposo1.get_text().endswith("s"):
			if self.comprobarTelefono(self.view.reposo1.get_text().split("s")[0].strip()) == True:
				reps = int(self.view.reposo1.get_text().split("s")[0].strip())
			elif (mostrarError):
				self.view.error(1)
				return (False, None,None, None, None, None, None, None, None, None)
			else:
				return (False, None,None, None, None, None, None, None, None, None)
		elif (mostrarError):
			self.view.error(1)
			return (False, None,None, None, None, None, None, None, None, None)
		else:
			return (False, None,None, None, None, None, None, None, None, None)

		return (True, reps,repmin, duras, duramin, descas, descamin, calents, calentmin, vueltas)

	def on_postsesion_prog(self, boton):
		ejercicios = self.model.get_sesion_ejercicios((self.on_prog_seleccionado())[1])
		usuariosdegrupo = self.model.get_usuarios_por_grupo((self.on_prog_seleccionado())[3])
		if self.model.get_valoracion(self.on_prog_seleccionado()[0]) != None:
			valoracion = self.model.get_valoracion((self.on_prog_seleccionado())[0])["valoracion"]
		else:
			valoracion = ""
		usuarios = []
		for i in usuariosdegrupo:
			usuarios.append(i["id"])
		if self.model.get_usuarios_from_prog((self.on_prog_seleccionado())[0]) != []:
			aux = self.model.get_usuarios_from_prog((self.on_prog_seleccionado())[0])
			for j in aux:
				usuarios.append(j["id"])
		if ejercicios is not None:
			ejercicio = []
			for i in range(0, len(ejercicios)):
				ejercicio.append(str(ejercicios[i]["nombre_ejercicio"]))

		if usuarios is not None:
			nombre = []	
			apellidos = []
			usersid = []
			for i in range(0, len(usuarios)):
				nombre.append(self.model.get_user(usuarios[i])["Nombre"])
				apellidos.append(self.model.get_user(usuarios[i])["Apellidos"])
				usersid.append(str(self.model.get_user(usuarios[i])["id"]))
		self.view.postsesionProg(str((self.on_prog_seleccionado())[0]), str((self.on_prog_seleccionado())[2]), ejercicio, nombre, apellidos, self, valoracion, self.on_prog_seleccionado()[1], usersid)

	def on_guardar_valoraciones(self, widget, sesion):
		start, end = self.view.bufferValoracion.get_bounds()
		texto = self.view.bufferValoracion.get_text(start, end, True)
		objetos = (texto, int(sesion))
		self.model.update_prog_valoracion(objetos)
		widget.set_sensitive(False)