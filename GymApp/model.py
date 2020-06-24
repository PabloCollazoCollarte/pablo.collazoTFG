	#! /usr/bin/python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sqlite3
 
class Model:
	def __init__(self, database):
		self.conn = self.create_connection(database)
		self.create_db_grupos()
		self.create_db_users()
		self.create_db_lesiones()
		self.create_db_patologias()
		self.create_db_users_patologias()
		self.create_db_users_lesiones()
		self.create_db_ejercicios()
		self.create_db_ejercicios_lesion()
		self.create_db_ejercicios_patologia()
		self.create_db_material()
		self.create_db_material_ejercicio()
		self.create_db_sesiones()
		self.create_db_sesion_ejercicio()
		self.create_db_sesion_programada()
		self.create_db_sesion_programada_usuario()
		self.create_db_valoracion_personal()
		self.create_db_variaciones_peso()

	def create_connection(self,database):
		conn = None
		try:
			conn = sqlite3.connect(database)
			query = 'PRAGMA foreign_keys = ON'  #para activar el uso de claves foraneas
	          
			if conn is not None:
				c = conn.cursor()
				c.execute(query)
				conn.commit()
		except Exception as e:
			print(e)
		return conn

	def create_db_users(self):
		query = 'CREATE TABLE IF NOT EXISTS user' + \
	            '( id INTEGER PRIMARY KEY AUTOINCREMENT, '+ \
	            '  id_grupo INTEGER, ' + \
	            '  Apellidos TEXT NOT NULL, ' + \
	            '  Nombre TEXT NOT NULL, ' + \
	            '  Sexo TEXT NOT NULL, ' + \
	            '  DNI TEXT NOT NULL, ' + \
	            '  Foto BLOB, ' + \
	            '  FechaNac TIMESTAMP NOT NULL, ' + \
				'  domicilio TEXT NOT NULL, ' + \
				'  telefono TEXT NOT NULL, ' + \
				'  correo TEXT NOT NULL, ' + \
				'  buffer1 TEXT, ' + \
				'  Categoría TEXT NOT NULL, ' + \
				'  Peso TEXT NOT NULL, ' + \
				'  altura TEXT NOT NULL, ' + \
				' activo TEXT NOT NULL, '  + \
				'  FOREIGN KEY (id_grupo) REFERENCES grupos(id_grupo) ON DELETE SET NULL)'
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query)
				self.conn.commit()
			except Exception as e:
				print(e)

	def create_db_lesiones(self):
		query = 'CREATE TABLE IF NOT EXISTS lesiones' + \
	            '( id INTEGER PRIMARY KEY AUTOINCREMENT, '+ \
				' lesion TEXT NOT NULL UNIQUE)'
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query)
				self.conn.commit()
			except Exception as e:
				print(e)

	def create_db_patologias(self):
		query = 'CREATE TABLE IF NOT EXISTS patologias' + \
	            '( id INTEGER PRIMARY KEY AUTOINCREMENT, '+ \
				' patologia TEXT NOT NULL UNIQUE)'
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query)
				self.conn.commit()
			except Exception as e:
				print(e)

	def create_db_users_patologias(self):
		query = 'CREATE TABLE IF NOT EXISTS UserPatologias' + \
	            '( id INTEGER PRIMARY KEY AUTOINCREMENT, '+ \
	            ' userid INTEGER NOT NULL, '+ \
	            ' patologia TEXT NOT NULL, '+ \
				' FOREIGN KEY (userid) REFERENCES user(id) ON DELETE CASCADE, ' + \
				' FOREIGN KEY (patologia) REFERENCES patologias(patologia) ON DELETE CASCADE)'
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query)
				self.conn.commit()
			except Exception as e:
				print(e)

	def create_db_users_lesiones(self):
		query = 'CREATE TABLE IF NOT EXISTS UserLesiones' + \
	            '( id INTEGER PRIMARY KEY AUTOINCREMENT, '+ \
	            ' userid INTEGER NOT NULL, '+ \
	            ' lesion TEXT NOT NULL, '+ \
				' FOREIGN KEY (userid) REFERENCES user(id) ON DELETE CASCADE , ' + \
				' FOREIGN KEY (lesion) REFERENCES lesiones(lesion) ON DELETE CASCADE)'
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query)
				self.conn.commit()
			except Exception as e:
				print(e)

	def create_db_ejercicios(self):
		query = 'CREATE TABLE IF NOT EXISTS ejercicio' + \
	            '( nombre_ejercicio TEXT PRIMARY KEY, ' + \
	            '  descripcion TEXT, ' + \
	            '  foto BLOB, ' + \
	            '  titulo_video TEXT, ' + \
	            '  URL TEXT, ' + \
				' cargas TEXT NOT NULL)'
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query)
				self.conn.commit()
			except Exception as e:
				print(e)

	def create_db_ejercicios_lesion(self):
		query = 'CREATE TABLE IF NOT EXISTS ejercicio_lesion' + \
	            '( id INTEGER PRIMARY KEY AUTOINCREMENT, '+ \
	            ' nombre_ejercicio TEXT NOT NULL, '+ \
	            ' lesion TEXT NOT NULL, '+ \
	            ' FOREIGN KEY (nombre_ejercicio) REFERENCES ejercicio(nombre_ejercicio) ON DELETE CASCADE, ' + \
				' FOREIGN KEY (lesion) REFERENCES lesiones(lesion) ON DELETE CASCADE) '
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query)
				self.conn.commit()
			except Exception as e:
				print(e)

	def create_db_ejercicios_patologia(self):
			query = 'CREATE TABLE IF NOT EXISTS ejercicio_patologia' + \
		            '( id INTEGER PRIMARY KEY AUTOINCREMENT, '+ \
		            ' nombre_ejercicio TEXT NOT NULL, '+ \
	           		' patologia TEXT NOT NULL, '+ \
		            ' FOREIGN KEY (nombre_ejercicio) REFERENCES ejercicio(nombre_ejercicio) ON DELETE CASCADE, ' + \
					' FOREIGN KEY (patologia) REFERENCES patologias(patologia) ON DELETE CASCADE) '
			if self.conn is not None:
				try:
					c = self.conn.cursor()
					c.execute(query)
					self.conn.commit()
				except Exception as e:
					print(e)

	def create_db_material(self):
			query = 'CREATE TABLE IF NOT EXISTS material' + \
		            '( id INTEGER PRIMARY KEY AUTOINCREMENT, '+ \
					' nombre_material TEXT NOT NULL UNIQUE)'
			if self.conn is not None:
				try:
					c = self.conn.cursor()
					c.execute(query)
					self.conn.commit()
				except Exception as e:
					print(e)

	def create_db_material_ejercicio(self):
			query = 'CREATE TABLE IF NOT EXISTS material_ejercicio' + \
					 '( id INTEGER PRIMARY KEY AUTOINCREMENT, '+ \
					' nombre_material TEXT NOT NULL, '+ \
	           		' nombre_ejercicio TEXT NOT NULL, '+ \
					' FOREIGN KEY (nombre_ejercicio) REFERENCES ejercicio(nombre_ejercicio) ON DELETE CASCADE)'
			if self.conn is not None:
				try:
					c = self.conn.cursor()
					c.execute(query)
					self.conn.commit()
				except Exception as e:
					print(e)	

	def create_db_grupos(self):
			query = 'CREATE TABLE IF NOT EXISTS grupos' + \
					 '( id_grupo INTEGER PRIMARY KEY AUTOINCREMENT, '+ \
					' horario TEXT NOT NULL)'
			if self.conn is not None:
				try:
					c = self.conn.cursor()
					c.execute(query)
					self.conn.commit()
				except Exception as e:
					print(e)	

	def create_db_sesiones(self):
			query = 'CREATE TABLE IF NOT EXISTS sesion' + \
					 '( id_sesion INTEGER PRIMARY KEY AUTOINCREMENT, '+ \
					' objetivos TEXT, ' + \
					'cargas TEXT, ' + \
					' materiales TEXT)'
			if self.conn is not None:
				try:
					c = self.conn.cursor()
					c.execute(query)
					self.conn.commit()
				except Exception as e:
					print(e)	

	def create_db_sesion_ejercicio(self):
		query = 'CREATE TABLE IF NOT EXISTS sesion_ejercicio' + \
				 '( id_sesion INTEGER, '+ \
				 ' nombre_ejercicio TEXT, ' + \
				 'PRIMARY KEY (id_sesion, nombre_ejercicio), ' + \
				 ' FOREIGN KEY (nombre_ejercicio) REFERENCES ejercicio(nombre_ejercicio) ON DELETE CASCADE, ' + \
				 ' FOREIGN KEY (id_sesion) REFERENCES sesion(id_sesion) ON DELETE CASCADE) '
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query)
				self.conn.commit()
			except Exception as e:
				print(e)

	    #Sqlite no permite clave débil por lo tanto se emplea el constraint unique
	def create_db_sesion_programada(self):
		query = 'CREATE TABLE IF NOT EXISTS sesion_programada' + \
					 '( id_sesionprog INTEGER UNIQUE, '+ \
					 ' id_sesion INTEGER, '+ \
					 ' id_grupo INTEGER, ' + \
					 ' fecha TEXT, ' + \
					 ' vueltas TEXT, ' + \
					 ' calentamiento TEXT, ' + \
					 ' descanso TEXT, ' + \
					 ' ejercicio TEXT, ' + \
					 ' reposo TEXT, ' + \
					 ' valoracion TEXT, ' + \
					 ' PRIMARY KEY (id_sesionprog, id_sesion, id_grupo), ' + \
					 ' FOREIGN KEY (id_sesion) REFERENCES sesion(id_sesion) ON DELETE CASCADE, ' + \
					 ' FOREIGN KEY (id_grupo) REFERENCES grupos(id_grupo) ON DELETE CASCADE) '
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query)
				self.conn.commit()
			except Exception as e:
				print(e)

	def create_db_sesion_programada_usuario(self):
		query = 'CREATE TABLE IF NOT EXISTS sesion_programada_usuario' + \
					 '( id_sesionprog INTEGER, '+ \
					 ' id_sesion INTEGER, '+ \
					 ' id_grupo INTEGER, ' + \
					 ' id INTEGER, ' + \
					 ' fecha TEXT, ' + \
					 ' PRIMARY KEY (id_sesionprog, id_sesion, id_grupo, id),' + \
					 ' FOREIGN KEY (id_sesionprog) REFERENCES sesion_programada(id_sesionprog) ON DELETE CASCADE, ' + \
					 ' FOREIGN KEY (id_sesion) REFERENCES sesion(id_sesion) ON DELETE CASCADE, ' + \
					 ' FOREIGN KEY (id_grupo) REFERENCES grupos(id_grupo) ON DELETE CASCADE, ' + \
					 ' FOREIGN KEY (id) REFERENCES user(id) ON DELETE CASCADE) '
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query)
				self.conn.commit()
			except Exception as e:
				print(e)


	def create_db_valoracion_personal(self):
		query = 'CREATE TABLE IF NOT EXISTS valoracion_personal' + \
					 '( id_sesionprog INTEGER, '+ \
					 ' id INTEGER, '+ \
					 ' valoracionpersonal TEXT, '+ \
					 ' modEjer TEXT, '+ \
					 ' PRIMARY KEY (id_sesionprog, id, valoracionpersonal),' + \
					 ' FOREIGN KEY (id) REFERENCES user(id) ON DELETE CASCADE, ' + \
					 ' FOREIGN KEY (id_sesionprog) REFERENCES sesion_programada(id_sesionprog) ON DELETE CASCADE) '
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query)
				self.conn.commit()
			except Exception as e:
				print(e)

	def create_db_variaciones_peso(self):
		query = 'CREATE TABLE IF NOT EXISTS variaciones_peso' + \
					 '( peso TEXT, '+ \
					 ' dia TEXT, ' + \
					 ' userid INTEGER, ' + \
					 ' PRIMARY KEY (userid, dia, peso),' + \
					 ' FOREIGN KEY (userid) REFERENCES user(id) ON DELETE CASCADE) '
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query)
				self.conn.commit()
			except Exception as e:
				print(e)

	def insert_lesion(self, lesion):
		query = 'INSERT INTO lesiones' + \
                '(lesion)' + \
                ' VALUES(?)'
		values = [lesion]
		last_row_id = None
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, values)
				self.conn.commit()
				last_row_id = c.lastrowid
			except Exception as e:
				print(e)
		return last_row_id

	def insert_patologia(self, patologia):
		query = 'INSERT INTO patologias' + \
                '(patologia)' + \
                ' VALUES(?)'
		values = [patologia]
		last_row_id = None
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, values)
				self.conn.commit()
				last_row_id = c.lastrowid
			except Exception as e:
				print(e)
		return last_row_id

	def insert_user_patologia(self, userid, patologia):
		query = 'INSERT INTO UserPatologias' + \
                '(userid, patologia)' + \
                ' VALUES(?,?)'
		last_row_id = None
		values=(userid,patologia)
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, values)
				self.conn.commit()
				last_row_id = c.lastrowid
			except Exception as e:
				print(e)
		return last_row_id

	def insert_user_lesion(self, userid, lesion):
		query = 'INSERT INTO UserLesiones' + \
                '(userid, lesion)' + \
                ' VALUES(?,?)'
		last_row_id = None
		values=(userid,lesion)
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, values)
				self.conn.commit()
				last_row_id = c.lastrowid
			except Exception as e:
				print(e)
		return last_row_id

	def get_lesiones(self, palabra, LesionConcreta):
		query = 'SELECT lesion ' + \
		        'FROM lesiones ' + \
		        'WHERE lesion LIKE ?'
		work_time = None
		if palabra is None:
			value = ("%" + "%",)
		else:
			value = ("%" + palabra + "%",)
		if LesionConcreta:
			value = (palabra,)
		if self.conn is not None:
		    try:
		        c = self.conn.cursor()
		        c.execute(query, value)
		        rows = c.fetchall()
		        work_time = []
		        for row in rows:
		        	work_time.append(dict(lesion=row[0]))
		    except Exception as e:
		        print(e)
		return work_time

	def get_patologias(self, palabra, PatologiaConcreta):
		query = 'SELECT patologia ' + \
		        'FROM patologias ' + \
		        'WHERE patologia LIKE ?'
		work_time = None
		if palabra is None:
			value = ("%" + "%",)
		else:
			value = ("%" + palabra + "%",)
		if PatologiaConcreta:
			value = (palabra,)
		if self.conn is not None:
		    try:
		        c = self.conn.cursor()
		        c.execute(query, value)
		        rows = c.fetchall()
		        work_time = []
		        for row in rows:
		            work_time.append(dict(patologia=row[0]))
		    except Exception as e:
		        print(e)
		return work_time

	def get_user_lesiones(self, userid):
		query = 'SELECT lesion ' + \
                'FROM UserLesiones ' + \
                'WHERE userid = ?'
		values = (userid,)
		work_time = None
		success = False
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, values)
				rows = c.fetchall()
				work_time = []
				for row in rows:
					work_time.append(dict(lesion=row[0]))
			except Exception as e:
				print(e)
		return work_time

	def get_user_patologias(self, userid):
		query = 'SELECT patologia ' + \
                'FROM UserPatologias ' + \
                'WHERE userid = ?'
		values = (userid,)
		work_time = None
		success = False
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, values)
				rows = c.fetchall()
				work_time = []
				for row in rows:
					work_time.append(dict(patologia=row[0]))
			except Exception as e:
				print(e)
		return work_time

	def delete_user_lesiones(self, id, lesion):
	    query = 'DELETE FROM UserLesiones WHERE userid=? AND lesion=?'
	    values = (id,lesion)
	    result = None
	    if self.conn is not None:
	        try:
	            c = self.conn.cursor()
	            c.execute(query, values)
	            self.conn.commit()
	        except Exception as e:
	            print(e)

	def delete_user_patologias(self, id, patologia):
	    query = 'DELETE FROM UserPatologias WHERE userid=? AND patologia=?'
	    values = (id,patologia)
	    result = None
	    if self.conn is not None:
	        try:
	            c = self.conn.cursor()
	            c.execute(query, values)
	            self.conn.commit()
	        except Exception as e:
	            print(e)

	def insert_usuarios(self, objetos, ActualizacionFoto):
		if ActualizacionFoto: 	#por problemas de parsear el fichero de la foto, en caso de que no haya foto se elimina este campo de la peticion
			query = 'INSERT INTO user' + \
	                '(Apellidos, Nombre, Sexo, DNI, Foto, FechaNac, domicilio, telefono, correo, buffer1, Categoría, Peso, altura, activo)' + \
	                ' VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
		else:
			query = 'INSERT INTO user' + \
	                '(Apellidos, Nombre, Sexo, DNI, FechaNac, domicilio, telefono, correo, buffer1, Categoría, Peso, altura, activo)' + \
	                ' VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)'
		last_row_id = None
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, objetos)
				self.conn.commit()
				last_row_id = c.lastrowid
			except Exception as e:
				print(e)
		return last_row_id

	def get_usuarios(self):
		query = 'SELECT id, Apellidos, Nombre, Sexo, DNI, Foto, FechaNac, domicilio, telefono, correo, buffer1, Categoría, Peso, altura, activo ' + \
		        'FROM user'
		work_time = None
		if self.conn is not None:
		    try:
		        c = self.conn.cursor()
		        c.execute(query)
		        rows = c.fetchall()
		        work_time = []
		        for row in rows:
		            work_time.append(dict(id=row[0], Apellidos=row[1], Nombre=row[2], Sexo=row[3], DNI=row[4], Foto=row[5], FechaNac=row[6], domicilio=row[7], telefono=row[8],
		            	correo=row[9], buffer1=row[10], Categoría=row[11], Peso=row[12], altura=row[13], activo=row[14]))
		    except Exception as e:
		        print(e)
		return work_time

	def get_usuarios_por_nombre(self, nombre):
		query = 'SELECT id, Apellidos, Nombre ' + \
		        'FROM user ' + \
		        'WHERE Nombre LIKE ? and activo == "Sí"'
		values = ("%" + nombre + "%",)
		work_time = None
		if self.conn is not None:
		    try:
		        c = self.conn.cursor()
		        c.execute(query, values)
		        rows = c.fetchall()
		        work_time = []
		        for row in rows:
		            work_time.append(dict(id=row[0], Apellidos=row[1], Nombre=row[2]))
		    except Exception as e:
		        print(e)
		return work_time

	def get_usuarios_por_apellidos(self, apellidos):
		query = 'SELECT id, Apellidos, Nombre ' + \
		        'FROM user ' + \
		        'WHERE Apellidos LIKE ? '
		values = ("%" + apellidos + "%",)
		work_time = None
		if self.conn is not None:
		    try:
		        c = self.conn.cursor()
		        c.execute(query, values)
		        rows = c.fetchall()
		        work_time = []
		        for row in rows:
		            work_time.append(dict(id=row[0], Apellidos=row[1], Nombre=row[2]))
		    except Exception as e:
		        print(e)
		return work_time

	def get_usuarios_por_grupo(self, id_grupo):
		query = 'SELECT id, Apellidos, Nombre ' + \
		        'FROM user ' + \
		        'WHERE id_grupo = ? and activo == "Sí"'
		values = (id_grupo,)
		work_time = None
		if self.conn is not None:
		    try:
		        c = self.conn.cursor()
		        c.execute(query, values)
		        rows = c.fetchall()
		        work_time = []
		        for row in rows:
		            work_time.append(dict(id=row[0], Apellidos=row[1], Nombre=row[2]))
		    except Exception as e:
		        print(e)
		return work_time
  
	def get_user(self, id):
		query = 'SELECT id, Apellidos, Nombre, Sexo, DNI, Foto, FechaNac, domicilio, telefono, correo, buffer1, Categoría, Peso, altura, id_grupo ' + \
		        'FROM user ' + \
		        'WHERE id = ?'
		values = (id,)
		work_time = None
		if self.conn is not None:
		    try:
		        c = self.conn.cursor()
		        c.execute(query, values)
		        row = c.fetchone()
		        if row is not None:
		            work_time = dict(id=row[0], Apellidos=row[1], Nombre=row[2], Sexo=row[3], DNI=row[4], Foto=row[5], FechaNac=row[6], domicilio=row[7], telefono=row[8],
		            	correo=row[9], buffer1=row[10],Categoría=row[11], Peso=row[12],altura=row[13], id_grupo=row[14])
		    except Exception as e:
		        print(e)
		return work_time

	def update_user(self, objetos, ActualizacionFoto): #por problemas de parsear el fichero de la foto, en caso de que no haya foto se elimina este campo de la peticion
		if ActualizacionFoto:
			query = 'UPDATE user ' + \
		            'SET Apellidos = ?, ' + \
		            '    Nombre = ?, ' + \
		            '	 Sexo = ?, ' + \
		            '    DNI = ?, ' + \
		            '    Foto = ?, ' + \
		            '    FechaNac = ?, ' + \
					'    domicilio = ?, ' + \
					'    telefono = ?, ' + \
					'    correo = ?, ' + \
					'    buffer1 = ?, ' + \
					'    Categoría = ?, ' + \
					'    Peso = ?, ' + \
					'    altura = ? ' + \
					'WHERE id =?'
		else:
			query = 'UPDATE user ' + \
		            'SET Apellidos = ?, ' + \
		            '    Nombre = ?, ' + \
		            '	 Sexo = ?, ' + \
		            '    DNI = ?, ' + \
		            '    FechaNac = ?, ' + \
					'    domicilio = ?, ' + \
					'    telefono = ?, ' + \
					'    correo = ?, ' + \
					'    buffer1 = ?, ' + \
					'    Categoría = ?, ' + \
					'    Peso = ?, ' + \
					'    altura = ? ' + \
					'WHERE id =?'
		result = None
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, objetos)
				result = c.rowcount
				self.conn.commit()
			except Exception as e:
				print(e)
		return result

	def update_grupo_user(self, objetos):
		query = 'UPDATE user ' + \
	            'SET id_grupo = ? ' + \
				'WHERE id =?'
		result = None
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, objetos)
				result = c.rowcount
				self.conn.commit()
			except Exception as e:
				print(e)
		return result

	def update_peso_user(self, objetos):
		query = 'UPDATE user ' + \
	            'SET Peso = ? ' + \
				'WHERE id =?'
		result = None
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, objetos)
				result = c.rowcount
				self.conn.commit()
			except Exception as e:
				print(e)
		return result

	def get_peso(self, id):
			query = 'SELECT Peso ' + \
			        'FROM user ' + \
		       		'WHERE id = ?'
			values = (id,)
			work_time = None
			if self.conn is not None:
			    try:
			        c = self.conn.cursor()
			        c.execute(query, values)
			        row = c.fetchone()
			        if row is not None:
			            work_time = dict(peso=row[0])
			    except Exception as e:
			        print(e)
			return work_time

	def delete_user(self, id):
	    query = 'DELETE FROM user WHERE id=?'
	    values = (id,)
	    result = None
	    if self.conn is not None:
	        try:
	            c = self.conn.cursor()
	            c.execute(query, values)
	            self.conn.commit()
	        except Exception as e:
	            print(e)

	def update_active(self, activo, id):
		query = 'UPDATE user ' + \
		            'SET activo = ? ' + \
		            'WHERE id =?'
		values = (activo, id)
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, values)
				result = c.rowcount
				self.conn.commit()
			except Exception as e:
				print(e)

###################################################################################################EJERCICIOS

	def insert_ejercicio(self, objetos, ActualizacionFoto):
		if ActualizacionFoto: 	#por problemas de parsear el fichero de la foto, en caso de que no haya foto se elimina este campo de la peticion
			query = 'INSERT INTO ejercicio' + \
	                '(nombre_ejercicio, descripcion, foto, titulo_video, URL, cargas)' + \
	                ' VALUES(?,?,?,?,?,?)'
		else:
			query = 'INSERT INTO ejercicio' + \
	                '(nombre_ejercicio, descripcion, titulo_video, URL, cargas)' + \
	                ' VALUES(?,?,?,?,?)'
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, objetos)
				self.conn.commit()
				last_row_id = c.lastrowid
			except Exception as e:
				print(e)

	def get_ejercicios(self):
			query = 'SELECT nombre_ejercicio, descripcion, foto, titulo_video, URL, cargas ' + \
			        'FROM ejercicio'
			work_time = None
			if self.conn is not None:
			    try:
			        c = self.conn.cursor()
			        c.execute(query)
			        rows = c.fetchall()
			        work_time = []
			        for row in rows:
			            work_time.append(dict(nombre_ejercicio=row[0], descripcion=row[1], foto=row[2], titulo_video=row[3], URL=row[4], cargas=row[5]))
			    except Exception as e:
			        print(e)
			return work_time


	def get_ejercicio(self, nombre_ejercicio):
			query = 'SELECT nombre_ejercicio, descripcion, foto, titulo_video, URL, cargas ' + \
			        'FROM ejercicio ' + \
		       		'WHERE nombre_ejercicio = ?'
			values = (nombre_ejercicio,)
			work_time = None
			if self.conn is not None:
			    try:
			        c = self.conn.cursor()
			        c.execute(query, values)
			        row = c.fetchone()
			        if row is not None:
			            work_time = dict(nombre_ejercicio=row[0], descripcion=row[1], foto=row[2], titulo_video=row[3], URL=row[4], cargas=row[5])
			    except Exception as e:
			        print(e)
			return work_time


	def update_ejercicio(self, objetos, ActualizacionFoto): #por problemas de parsear el fichero de la foto, en caso de que no haya foto se elimina este campo de la peticion
		if ActualizacionFoto:
			query = 'UPDATE ejercicio ' + \
		            'SET descripcion = ?, ' + \
		            '	 foto = ?, ' + \
		            '    titulo_video = ?, ' + \
		            '    URL = ?, ' + \
		            '    cargas = ? ' + \
					'WHERE nombre_ejercicio =?'
		else:
			query = 'UPDATE ejercicio ' + \
		            'SET descripcion = ?, ' + \
		            '    titulo_video = ?, ' + \
		            '    URL = ?, ' + \
		            '    cargas = ? ' + \
					'WHERE nombre_ejercicio =?'
		result = None

		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, objetos)
				result = c.rowcount
				self.conn.commit()
			except Exception as e:
				print(e)
		return result

	def delete_ejercicio(self, nombre_ejercicio):
	    query = 'DELETE FROM ejercicio WHERE nombre_ejercicio=?'
	    values = (nombre_ejercicio,)
	    result = None
	    if self.conn is not None:
	        try:
	            c = self.conn.cursor()
	            c.execute(query, values)
	            self.conn.commit()
	        except Exception as e:
	            print(e)	

	def insert_ejercicio_lesion(self, nombre_ejercicio, lesion):
		query = 'INSERT INTO ejercicio_lesion' + \
                '(nombre_ejercicio, lesion)' + \
                ' VALUES(?,?)'
		last_row_id = None
		values=(nombre_ejercicio,lesion)
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, values)
				self.conn.commit()
				last_row_id = c.lastrowid
			except Exception as e:
				print(e)
		return last_row_id

	def insert_ejercicio_patologia(self, nombre_ejercicio, patologia):
		query = 'INSERT INTO ejercicio_patologia' + \
                '(nombre_ejercicio, patologia)' + \
                ' VALUES(?,?)'
		last_row_id = None
		values=(nombre_ejercicio,patologia)
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, values)
				self.conn.commit()
				last_row_id = c.lastrowid
			except Exception as e:
				print(e)
		return last_row_id
	
	def get_ejercicio_lesiones(self, nombre_ejercicio):
		query = 'SELECT lesion ' + \
                'FROM ejercicio_lesion ' + \
                'WHERE nombre_ejercicio = ?'
		values = (nombre_ejercicio,)
		work_time = None
		success = False
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, values)
				rows = c.fetchall()
				work_time = []
				for row in rows:
					work_time.append(dict(lesion=row[0]))
			except Exception as e:
				print(e)
		return work_time

	def get_ejercicio_patologias(self, nombre_ejercicio):
		query = 'SELECT patologia ' + \
                'FROM ejercicio_patologia ' + \
                'WHERE nombre_ejercicio = ?'
		values = (nombre_ejercicio,)
		work_time = None
		success = False
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, values)
				rows = c.fetchall()
				work_time = []
				for row in rows:
					work_time.append(dict(patologia=row[0]))
			except Exception as e:
				print(e)
		return work_time

	def delete_ejercicio_lesiones(self, nombre_ejercicio, lesion):
	    query = 'DELETE FROM ejercicio_lesion WHERE nombre_ejercicio=? AND lesion=?'
	    values = (nombre_ejercicio,lesion)
	    result = None
	    if self.conn is not None:
	        try:
	            c = self.conn.cursor()
	            c.execute(query, values)
	            self.conn.commit()
	        except Exception as e:
	            print(e)

	def delete_ejercicio_patologias(self, nombre_ejercicio, patologia):
	    query = 'DELETE FROM ejercicio_patologia WHERE nombre_ejercicio=? AND patologia=?'
	    values = (nombre_ejercicio, patologia)
	    result = None
	    if self.conn is not None:
	        try:
	            c = self.conn.cursor()
	            c.execute(query, values)
	            self.conn.commit()
	        except Exception as e:
	            print(e)


	def get_materiales(self):
			query = 'SELECT nombre_material ' + \
			        'FROM material order by nombre_material'
			work_time = None
			if self.conn is not None:
			    try:
			        c = self.conn.cursor()
			        c.execute(query)
			        rows = c.fetchall()
			        work_time = []
			        for row in rows:
			            work_time.append(row[0])
			    except Exception as e:
			        print(e)
			return work_time


	def get_materiales_ejercicio(self, nombre_ejercicio):
		query = 'SELECT nombre_material ' + \
                'FROM material_ejercicio ' + \
                'WHERE nombre_ejercicio = ?'
		values = (nombre_ejercicio,)
		work_time = None
		success = False
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, values)
				rows = c.fetchall()
				work_time = []
				for row in rows:
					work_time.append(dict(nombre_material=row[0]))
			except Exception as e:
				print(e)
		return work_time

	def insert_material_ejercicio(self, nombre_ejercicio, nombre_material):
		query = 'INSERT INTO material_ejercicio' + \
                '(nombre_ejercicio, nombre_material)' + \
                ' VALUES(?,?)'
		last_row_id = None
		values=(nombre_ejercicio,nombre_material)
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, values)
				self.conn.commit()
				last_row_id = c.lastrowid
			except Exception as e:
				print(e)
		return last_row_id

	def delete_ejercicio_materiales(self, nombre_ejercicio, nombre_material):
	    query = 'DELETE FROM material_ejercicio WHERE nombre_ejercicio=? AND nombre_material= ?'
	    values = (nombre_ejercicio, nombre_material)
	    result = None
	    if self.conn is not None:
	        try:
	            c = self.conn.cursor()
	            c.execute(query, values)
	            self.conn.commit()
	        except Exception as e:
	            print(e)

	def get_grupo(self, id_grupo):
			query = 'SELECT id_grupo, horario ' + \
			        'FROM grupos ' + \
		       		'WHERE id_grupo = ?'
			values = (id_grupo,)
			work_time = None
			if self.conn is not None:
			    try:
			        c = self.conn.cursor()
			        c.execute(query, values)
			        row = c.fetchone()
			        if row is not None:
			            work_time = dict(id_grupo=row[0], horario=row[1])
			    except Exception as e:
			        print(e)
			return work_time

	def get_grupos(self):
			query = 'SELECT id_grupo, horario ' + \
			        'FROM grupos order by id_grupo'
			work_time = None
			if self.conn is not None:
			    try:
			        c = self.conn.cursor()
			        c.execute(query)
			        rows = c.fetchall()
			        work_time = []
			        for row in rows:
			            work_time.append(dict(id_grupo=row[0], horario=row[1]))
			    except Exception as e:
			        print(e)
			return work_time

	def insert_grupo(self, horario):
		query = 'INSERT INTO grupos' + \
                '(horario)' + \
                ' VALUES(?)'
		last_row_id = None
		values=(horario,)
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, values)
				self.conn.commit()
				last_row_id = c.lastrowid
			except Exception as e:
				print(e)
		return last_row_id

	def update_grupo(self, objetos):
		query = 'UPDATE grupos ' + \
	            'SET horario = ? ' + \
				'WHERE id_grupo =?'
		result = None
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, objetos)
				result = c.rowcount
				self.conn.commit()
			except Exception as e:
				print(e)
		return result

	def delete_grupo(self, idgrupo):
	    query = 'DELETE FROM grupos WHERE id_grupo=?'
	    values = (idgrupo,)
	    result = None
	    if self.conn is not None:
	        try:
	            c = self.conn.cursor()
	            c.execute(query, values)
	            self.conn.commit()
	        except Exception as e:
	            print(e)	

	def insert_sesion(self, objetivos, cargas, materiales):
		query = 'INSERT INTO sesion' + \
                '(objetivos, cargas, materiales)' + \
                ' VALUES(?, ?, ?)'
		last_row_id = None
		values=(objetivos, cargas, materiales)
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, values)
				self.conn.commit()
				last_row_id = c.lastrowid
			except Exception as e:
				print(e)
		return last_row_id

	def get_sesion(self, id_sesion):
			query = 'SELECT id_sesion, objetivos, cargas, materiales ' + \
			        'FROM sesion ' + \
		       		'WHERE id_sesion = ?'
			values = (id_sesion,)
			work_time = None
			if self.conn is not None:
			    try:
			        c = self.conn.cursor()
			        c.execute(query, values)
			        row = c.fetchone()
			        if row is not None:
			            work_time = dict(id_sesion=row[0], objetivos=row[1], cargas=row[2], materiales=row[3])
			    except Exception as e:
			        print(e)
			return work_time

	def get_sesiones(self):
			query = 'SELECT id_sesion, objetivos, cargas, materiales ' + \
			        'FROM sesion'
			work_time = None
			if self.conn is not None:
			    try:
			        c = self.conn.cursor()
			        c.execute(query)
			        rows = c.fetchall()
			        work_time = []
			        for row in rows:
			            work_time.append(dict(id_sesion=row[0], objetivos=row[1], cargas=row[2], materiales=row[3]))
			    except Exception as e:
			        print(e)
			return work_time

	def delete_sesion(self, id_sesion):
	    query = 'DELETE FROM sesion WHERE id_sesion=?'
	    values = (id_sesion,)
	    result = None
	    if self.conn is not None:
	        try:
	            c = self.conn.cursor()
	            c.execute(query, values)
	            self.conn.commit()
	        except Exception as e:
	            print(e)

	def insert_sesion_ejercicio(self, idsesion, ejercicio):
		query = 'INSERT INTO sesion_ejercicio' + \
                '(id_sesion, nombre_ejercicio)' + \
                ' VALUES(?,?)'
		last_row_id = None
		values=(idsesion,ejercicio)
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, values)
				self.conn.commit()
				last_row_id = c.lastrowid
			except Exception as e:
				print(e)
		return last_row_id

	def get_sesion_ejercicios(self, id_sesion):
		query = 'SELECT nombre_ejercicio ' + \
                'FROM sesion_ejercicio ' + \
                'WHERE id_sesion = ?'
		values = (id_sesion,)
		work_time = None
		success = False
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, values)
				rows = c.fetchall()
				work_time = []
				for row in rows:
					work_time.append(dict(nombre_ejercicio=row[0]))
			except Exception as e:
				print(e)
		return work_time

	def delete_sesion_ejercicios(self, id_sesion, nombre_ejercicio):
	    query = 'DELETE FROM sesion_ejercicio WHERE id_sesion=? AND nombre_ejercicio=?'
	    values = (id_sesion,nombre_ejercicio)
	    result = None
	    if self.conn is not None:
	        try:
	            c = self.conn.cursor()
	            c.execute(query, values)
	            self.conn.commit()
	        except Exception as e:
	            print(e)

	def update_sesion(self, objetos):
		query = 'UPDATE sesion ' + \
	            'SET objetivos = ?, ' + \
	            'cargas = ?, ' + \
	            'materiales = ? ' + \
				'WHERE id_sesion =?'
		result = None
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, objetos)
				result = c.rowcount
				self.conn.commit()
			except Exception as e:
				print(e)
		return result

	def get_prog(self, id_prog):
			query = 'SELECT id_sesionprog, id_sesion, id_grupo, fecha, vueltas, calentamiento, descanso, ejercicio, reposo ' + \
			        'FROM sesion_programada ' + \
		       		'WHERE id_sesionprog = ?'
			values = (id_prog,)
			work_time = None
			if self.conn is not None:
			    try:
			        c = self.conn.cursor()
			        c.execute(query, values)
			        row = c.fetchone()
			        if row is not None:
			            work_time = dict(id_prog=row[0], id_sesion=row[1], id_grupo=row[2], fecha=row[3], vueltas=row[4], calentamiento=row[5], descanso=row[6], ejercicio=row[7], reposo=row[8])
			    except Exception as e:
			        print(e)
			return work_time

	def get_valoracion(self, id_prog):
			query = 'SELECT valoracion ' + \
			        'FROM sesion_programada ' + \
		       		'WHERE id_sesionprog = ?'
			values = (id_prog,)
			work_time = None
			if self.conn is not None:
			    try:
			        c = self.conn.cursor()
			        c.execute(query, values)
			        row = c.fetchone()
			        if row is not None:
			            work_time = dict(valoracion=row[0])
			    except Exception as e:
			        print(e)
			return work_time

	def get_progs(self):
			query = 'SELECT id_sesionprog, id_sesion, id_grupo, fecha, vueltas, calentamiento, descanso, ejercicio, reposo ' + \
			        'FROM sesion_programada '
			work_time = None
			if self.conn is not None:
			    try:
			        c = self.conn.cursor()
			        c.execute(query)
			        rows = c.fetchall()
			        work_time = []
			        for row in rows:
			            work_time.append(dict(id_prog=row[0], id_sesion=row[1], id_grupo=row[2], fecha=row[3], vueltas=row[4], calentamiento=row[5], descanso=row[6], ejercicio=row[7], reposo=row[8]))
			    except Exception as e:
			        print(e)
			return work_time

	def get_progs_from_grupo(self, id_grupo):
			query = 'SELECT *' + \
			        'FROM sesion_programada ' + \
			        ' WHERE id_grupo = ?'
			work_time = None
			values = (id_grupo,)
			if self.conn is not None:
			    try:
			        c = self.conn.cursor()
			        c.execute(query, values)
			        rows = c.fetchall()
			        work_time = []
			        for row in rows:
			            work_time.append(dict(id_sesionprog=row[0], id_sesion=row[1], id_grupo=row[2], fecha=row[3]))
			    except Exception as e:
			    	print(e)
			return work_time

	def insert_prog(self, objetos):
		query = 'INSERT INTO sesion_programada' + \
                '(id_sesionprog, id_sesion, id_grupo, fecha, vueltas, calentamiento, descanso, ejercicio, reposo, valoracion)' + \
                ' VALUES((SELECT IFNULL(MAX(id_sesionprog), 0) + 1 FROM sesion_programada),?,?,?,?,?,?,?,?,?)'
		last_row_id = None
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, objetos)
				self.conn.commit()
				last_row_id = c.lastrowid
			except Exception as e:
				print(e)
		return last_row_id

	def update_prog(self, objetos):
		query = 'UPDATE sesion_programada ' + \
	            'SET id_sesion = ?, ' + \
	            '    id_grupo = ?, ' + \
	            '	 fecha = ?, ' + \
	            '    vueltas = ?, ' + \
	            '    calentamiento = ?, ' + \
				'    descanso = ?, ' + \
				'    ejercicio = ?, ' + \
				'    reposo = ? ' + \
				'WHERE id_sesionprog =?'
		result = None
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, objetos)
				result = c.rowcount
				self.conn.commit()
			except Exception as e:
				print(e)
		return result

	def delete_prog(self, id_sesionprog):
	    query = 'DELETE FROM sesion_programada WHERE id_sesionprog=?'
	    values = (id_sesionprog,)
	    result = None
	    if self.conn is not None:
	        try:
	            c = self.conn.cursor()
	            c.execute(query, values)
	            self.conn.commit()
	        except Exception as e:
	            print(e)

	def insert_prog_usuario(self, objetos):
		query = 'INSERT INTO sesion_programada_usuario' + \
                '(id_sesionprog, id_sesion, id_grupo, id, fecha)' + \
                ' VALUES(?,?,?,?,?)'
		last_row_id = None
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, objetos)
				self.conn.commit()
				last_row_id = c.lastrowid
			except Exception as e:
				print(e)
		return last_row_id

	def update_prog_usuario(self, objetos):
		query = 'UPDATE sesion_programada_usuario ' + \
	            'SET id_sesion = ?, ' + \
	            '    id_grupo = ?, ' + \
	            '    fecha = ? ' + \
				'WHERE id_sesionprog =?'
		result = None
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, objetos)
				result = c.rowcount
				self.conn.commit()
			except Exception as e:
				print(e)
		return result

	def get_prog_from_usuario(self, id):
		query = 'SELECT id_sesionprog, id_sesion, id_grupo, fecha ' + \
                'FROM sesion_programada_usuario ' + \
                'WHERE id = ?'
		values = (id,)
		work_time = None
		success = False
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, values)
				rows = c.fetchall()
				work_time = []
				for row in rows:
					work_time.append(dict(id_sesionprog=row[0], id_sesion=row[1], id_grupo=row[2], fecha=row[3]))
			except Exception as e:
				print(e)
		return work_time

	def get_usuarios_from_prog(self, id_sesionprog):
		query = 'SELECT id ' + \
                'FROM sesion_programada_usuario ' + \
                'WHERE id_sesionprog = ?'
		values = (id_sesionprog,)
		work_time = None
		success = False
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, values)
				rows = c.fetchall()
				work_time = []
				for row in rows:
					work_time.append(dict(id=row[0]))
			except Exception as e:
				print(e)
		return work_time

	def get_activo(self, id):
		query = 'SELECT activo ' + \
                'FROM user ' + \
                'WHERE id = ?'
		values = (id,)
		work_time = None
		success = False
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, values)
				row = c.fetchone()
				if row is not None:
					work_time = dict(activo=row[0])
			except Exception as e:
				print(e)
		return work_time

	def delete_prog_usuario(self, id, id_sesionprog):
	    query = 'DELETE FROM sesion_programada_usuario WHERE id=? AND id_sesionprog=?'
	    values = (id,id_sesionprog)
	    result = None
	    if self.conn is not None:
	        try:
	            c = self.conn.cursor()
	            c.execute(query, values)
	            self.conn.commit()
	        except Exception as e:
	            print(e)

	def update_prog_valoracion(self, objetos):
		query = 'UPDATE sesion_programada ' + \
	            'SET valoracion = ? ' + \
				'WHERE id_sesionprog = ?'
		result = None
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, objetos)
				result = c.rowcount
				self.conn.commit()
			except Exception as e:
				print(e)
		return result

	def insert_valoracion_personal(self, objetos):
		query = 'INSERT INTO valoracion_personal' + \
                '(id_sesionprog, id, valoracionpersonal, modEjer)' + \
                ' VALUES(?,?,?,?)'
		last_row_id = None
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, objetos)
				self.conn.commit()
				last_row_id = c.lastrowid
			except Exception as e:
				print(e)
		return last_row_id

	def update_prog_valoracion_personal(self, objetos):
		query = 'UPDATE valoracion_personal ' + \
	            'SET valoracionpersonal = ? ,' + \
	            ' modEjer = ? ' + \
				'WHERE id_sesionprog = ? and id = ? '
		result = None
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, objetos)
				result = c.rowcount
				self.conn.commit()
			except Exception as e:
				print(e)
		return result

	def get_valoracion_personal(self, id_sesionprog, id):
			query = 'SELECT valoracionpersonal, modEjer ' + \
			        'FROM valoracion_personal ' + \
		       		'WHERE id_sesionprog = ? and id = ?'
			values = (id_sesionprog, id)
			work_time = None
			if self.conn is not None:
			    try:
			        c = self.conn.cursor()
			        c.execute(query, values)
			        row = c.fetchone()
			        if row is not None:
			            work_time = dict(valoracionpersonal=row[0], modEjer=row[1])
			    except Exception as e:
			        print(e)
			return work_time


	def insert_var_peso(self, peso , dia, userid):
		query = 'INSERT INTO variaciones_peso' + \
                '(peso, dia, userid)' + \
                ' VALUES(?,?,?)'
		values = (peso, dia,userid)
		last_row_id = None
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query, values)
				self.conn.commit()
				last_row_id = c.lastrowid
			except Exception as e:
				print(e)
		return last_row_id

	def get_variacion_peso(self, userid):
		query = 'SELECT peso, dia ' + \
                'FROM variaciones_peso ' + \
                'WHERE userid = ? '
		work_time = None
		success = False
		values = (userid,)
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query,values)
				rows = c.fetchall()
				work_time = []
				for row in rows:
					work_time.append(dict(peso=row[0], dia=row[1]))
			except Exception as e:
				print(e)
		return work_time

	def get_variacion_peso_evitarRepetidos(self, userid, peso, dia):
		query = 'SELECT peso, dia ' + \
                'FROM variaciones_peso ' + \
                'WHERE userid = ? and peso = ? and dia = ?'
		work_time = None
		success = False
		values = (userid,peso, dia)
		if self.conn is not None:
			try:
				c = self.conn.cursor()
				c.execute(query,values)
				rows = c.fetchall()
				work_time = []
				for row in rows:
					work_time.append(dict(peso=row[0], dia=row[1]))
			except Exception as e:
				print(e)
		return work_time