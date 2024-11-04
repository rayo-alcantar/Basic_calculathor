﻿# calc.py
import wx
import webbrowser
import sys
import requests
import sympy as sp
from packaging import version

import os
import threading
import math
import subprocess


from operaciones import Aritmetica, Conversion, Trigonometria, CambioBases, Geometria, Quimica, Estadistica

VERSION = '1.0'

class Calculadora(wx.Frame):
	"""Ventana principal de la calculadora."""
	def __init__(self):
		super().__init__(None, title=f"Calculadora básica {VERSION}", size=(400, 300))

		# Crear el menú
		self.crear_menu()

		# Crear el panel principal
		panel = wx.Panel(self)
		vbox = wx.BoxSizer(wx.VERTICAL)

		# Botón de Operaciones
		btn_operaciones = wx.Button(panel, label="&Operaciones")
		btn_operaciones.Bind(wx.EVT_BUTTON, self.mostrar_categorias)
		vbox.Add(btn_operaciones, flag=wx.EXPAND|wx.ALL, border=10)
		
		btn_documentacion = wx.Button(panel, label="&Leer Documentación")
		btn_documentacion.Bind(wx.EVT_BUTTON, self.abrir_documentacion)
		vbox.Add(btn_documentacion, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=10)
		
		panel.SetSizer(vbox)
		self.Centre()
		self.Show()

		# Comprobar actualizaciones al iniciar
		self.comprobar_actualizaciones()

	def comprobar_actualizaciones(self):
		"""Comprueba si hay una nueva versión disponible en GitHub."""
		def check_update():
			try:
				response = requests.get('https://api.github.com/repos/rayo-alcantar/Basic_calculathor/releases/latest')
				if response.status_code == 200:
					data = response.json()
					ultima_version = data['tag_name'].lstrip('v')  # Obtener el número de versión sin la 'v'
					
					# Obtener la URL y nombre del primer asset de la release
					assets = data.get('assets', [])
					if assets:
						url_asset = assets[0]['browser_download_url']
						asset_name = assets[0]['name']
						# Ruta completa del archivo zip descargado
						ruta_zip = os.path.join(os.getcwd(), asset_name)
					else:
						asset_name = None
						ruta_zip = None

					# Comparar versiones utilizando packaging.version
					if version.parse(ultima_version) > version.parse(VERSION):
						# La versión disponible es más reciente
						# Verificar si el zip está presente
						if ruta_zip and os.path.exists(ruta_zip):
							wx.CallAfter(self.mostrar_error_zip_no_descomprimido)
						else:
							wx.CallAfter(self.notificar_nueva_version, ultima_version, url_asset, asset_name)
					else:
						# La versión disponible no es más reciente
						# Si hay un zip presente, eliminarlo silenciosamente
						if ruta_zip and os.path.exists(ruta_zip):
							try:
								os.remove(ruta_zip)
							except Exception as e:
								print(f"Error al eliminar el archivo zip: {e}")
				else:
					print("No se pudo comprobar si hay actualizaciones.")
			except Exception as e:
				print(f"Error al comprobar actualizaciones: {e}")
		threading.Thread(target=check_update).start()

	def mostrar_error_zip_no_descomprimido(self):
		"""Muestra un error indicando que el archivo zip no ha sido descomprimido."""
		mensaje = ("Se ha detectado que hay una actualización descargada pero no descomprimida.\n"
				   "Por favor, descomprima el archivo zip descargado para actualizar a la última versión.")
		wx.MessageBox(mensaje, "Actualización pendiente", wx.OK | wx.ICON_ERROR)

	def notificar_nueva_version(self, ultima_version, url_asset, asset_name):
		"""Notifica al usuario que hay una nueva versión y ofrece descargarla."""
		mensaje = (f"Hay una nueva versión disponible: {ultima_version}\n"
				   "¿Desea descargarla ahora?")
		dialogo = wx.MessageDialog(self, mensaje, "Actualización disponible", wx.YES_NO | wx.ICON_QUESTION)
		respuesta = dialogo.ShowModal()
		if respuesta == wx.ID_YES:
			self.descargar_actualizacion(ultima_version, url_asset, asset_name)
		dialogo.Destroy()

	def descargar_actualizacion(self, ultima_version, url_asset, asset_name):
		"""Descarga la actualización y guía al usuario para instalarla."""
		# Crear un diálogo de progreso
		self.progress_dialog = wx.ProgressDialog(
			"Descargando actualización",
			"Por favor, espere mientras se descarga la actualización...",
			maximum=100,
			parent=self,
			style=wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME
		)

		def download():
			try:
				respuesta = requests.get(url_asset, stream=True)
				total_size = int(respuesta.headers.get('content-length', 0))
				downloaded_size = 0
				if respuesta.status_code == 200:
					# Guardar el archivo descargado con su nombre original
					nombre_archivo = asset_name
					with open(nombre_archivo, 'wb') as archivo:
						for chunk in respuesta.iter_content(chunk_size=1024):
							if chunk:
								archivo.write(chunk)
								downloaded_size += len(chunk)
								# Calcular el porcentaje de progreso
								porcentaje = int(downloaded_size * 100 / total_size)
								# Actualizar la barra de progreso
								wx.CallAfter(self.update_progress, porcentaje)
					wx.CallAfter(self.informar_descarga_exitosa, nombre_archivo)
				else:
					wx.CallAfter(self.mostrar_error_descarga, "No se pudo descargar la actualización.")
			except Exception as e:
				wx.CallAfter(self.mostrar_error_descarga, f"Error al descargar la actualización: {e}")
		threading.Thread(target=download).start()

	def update_progress(self, porcentaje):
		"""Actualiza la barra de progreso."""
		self.progress_dialog.Update(porcentaje, f"Descargando... {porcentaje}% completado")

	def informar_descarga_exitosa(self, nombre_archivo):
		"""Informa al usuario que la descarga fue exitosa y cómo actualizar."""
		# Cerrar el diálogo de progreso
		if hasattr(self, 'progress_dialog'):
			self.progress_dialog.Destroy()
	
		mensaje = (
			f"La nueva versión se ha descargado como '{nombre_archivo}'.\n\n"
			"La aplicación se actualizará automáticamente y se cerrará; al finalizar la actualización, por favor abre de nuevo el programa. Si el acceso directo del escritorio no funciona, prueba buscar calculadora básica en el menú inicio.\n"
			"pulse enter para continuar..."
		)
		wx.MessageBox(mensaje, "Descarga completada", wx.OK | wx.ICON_INFORMATION)
	
		# Ejecutar el ejecutable de actualización
		if getattr(sys, 'frozen', False):
			# Si la aplicación está empaquetada
			current_dir = os.path.dirname(sys.executable)
		else:
			# Si se está ejecutando desde el script
			current_dir = os.path.dirname(os.path.abspath(__file__))
	
		update_exe = os.path.join(current_dir, 'update.exe')
		zip_path = os.getcwd()
	
		# Verificar que update.exe existe
		if not os.path.exists(update_exe):
			wx.MessageBox("El actualizador 'update.exe' no se encontró.", "Error", wx.OK | wx.ICON_ERROR)
			return
	
		# Ejecutar el ejecutable de actualización en un nuevo proceso
		try:
			subprocess.Popen([update_exe, nombre_archivo, zip_path], shell=False)
		except Exception as e:
			wx.MessageBox(f"Error al ejecutar el actualizador: {e}", "Error", wx.OK | wx.ICON_ERROR)
			return
	
		# Asegurar que la aplicación se cierra completamente
		self.Destroy()
		wx.GetApp().ExitMainLoop()
		sys.exit(0)

	def mostrar_error_descarga(self, mensaje_error):
		"""Muestra un mensaje de error si la descarga falla."""
		# Cerrar el diálogo de progreso si existe
		if hasattr(self, 'progress_dialog'):
			self.progress_dialog.Destroy()
		wx.MessageBox(mensaje_error, "Error de descarga", wx.OK | wx.ICON_ERROR)

	def crear_menu(self):
		"""Crea el menú de opciones."""
		menubar = wx.MenuBar()
		menu_opciones = wx.Menu()
		menu_acerca_de = menu_opciones.Append(wx.ID_ABOUT, "&Acerca de\tCtrl+A", "Información del desarrollador")
		self.Bind(wx.EVT_MENU, self.mostrar_acerca_de, menu_acerca_de)

		# Agregar el menú para crear acceso directo
		menu_crear_acceso_directo = menu_opciones.Append(wx.ID_ANY, "&Crear Acceso Directo", "Crea un acceso directo en el escritorio")
		self.Bind(wx.EVT_MENU, self.crear_acceso_directo, menu_crear_acceso_directo)

		menubar.Append(menu_opciones, "&Opciones")
		self.SetMenuBar(menubar)

	def crear_acceso_directo(self, event):
		"""Crea un acceso directo en el escritorio."""
		try:
			# Importar aquí para evitar errores si el módulo no está instalado
			import pythoncom
			import win32com.client

			# Obtener la ruta al escritorio
			def get_desktop_path():
				"""Obtiene la ruta al escritorio del usuario."""
				try:
					from ctypes import windll, create_unicode_buffer
					CSIDL_DESKTOPDIRECTORY = 0x10
					MAX_PATH = 260
					buf = create_unicode_buffer(MAX_PATH)
					windll.shell32.SHGetFolderPathW(None, CSIDL_DESKTOPDIRECTORY, None, 0, buf)
					return buf.value
				except Exception:
					return os.path.join(os.environ["USERPROFILE"], "Desktop")

			desktop_path = get_desktop_path()
			nombre_acceso = "Calculadora Básica.lnk"
			ruta_acceso = os.path.join(desktop_path, nombre_acceso)
			
			# Obtener la ruta completa al ejecutable
			if getattr(sys, 'frozen', False):
				# Si está empaquetado con PyInstaller
				ruta_ejecutable = sys.executable
			else:
				# Si se está ejecutando desde el script
				ruta_ejecutable = os.path.abspath(__file__)

			shell = win32com.client.Dispatch("WScript.Shell")
			shortcut = shell.CreateShortCut(ruta_acceso)
			shortcut.Targetpath = ruta_ejecutable
			shortcut.WorkingDirectory = os.path.dirname(ruta_ejecutable)
			shortcut.IconLocation = ruta_ejecutable
			shortcut.save()
			
			wx.MessageBox("Se ha creado el acceso directo en el escritorio.", "Acceso Directo", wx.OK | wx.ICON_INFORMATION)
		except Exception as e:
			wx.MessageBox(f"No se pudo crear el acceso directo: {e}", "Error", wx.OK | wx.ICON_ERROR)

	def abrir_documentacion(self, event):
		"""Abre la documentación en el navegador web predeterminado."""
		# Obtener la ruta completa al archivo documentacion.html
		if getattr(sys, 'frozen', False):
			# Si la aplicación está empaquetada con PyInstaller
			ruta_base = sys._MEIPASS
		else:
			# Si se está ejecutando de forma normal
			ruta_base = os.path.dirname(os.path.abspath(__file__))
		ruta_html = os.path.join(ruta_base, 'documentacion.html')
		# Abrir el archivo en el navegador web predeterminado
		webbrowser.open(f'file://{ruta_html}')

	def mostrar_acerca_de(self, event):
		"""Muestra la información del desarrollador."""
		info = ("Programa simple para realizar una calculadora accesible con lector de pantalla.\n"
				"Nombre del desarrollador: Ángel Alcántar.\n"
				"Email: rayoalcantar@gmail.com.\nTodos los derechos reservados.")
		wx.MessageBox(info, "Acerca de", wx.OK | wx.ICON_INFORMATION)


	def mostrar_categorias(self, event):
		"""Muestra las categorías de operaciones disponibles."""
		categorias = ['Aritmética', 'Conversión de Unidades', 'Trigonometría', 'Cambio de Bases', 'Geometría', 'Química', 'estadística']
		dlg = wx.SingleChoiceDialog(self, 'Seleccione una categoría:', 'Categorías', categorias)
		if dlg.ShowModal() == wx.ID_OK:
			seleccion = dlg.GetStringSelection()
			if seleccion == 'Aritmética':
				self.operaciones_aritmeticas()
			elif seleccion == 'Conversión de Unidades':
				self.conversion_unidades()
			elif seleccion == 'Trigonometría':
				self.operaciones_trigonometricas()
			elif seleccion == 'Cambio de Bases':
				self.cambio_bases()
			elif seleccion == 'Geometría':
				self.operaciones_geometricas()
			elif seleccion == 'Química':
				self.operaciones_quimica()
			elif seleccion == 'estadística':
				self.operaciones_estadistica()
		dlg.Destroy()

	def operaciones_aritmeticas(self):
		"""Despliega las operaciones aritméticas disponibles."""
		operaciones = ['Suma', 'Resta', 'Multiplicación', 'División', 'Raíz Cuadrada', 'Logaritmo', 'Porcentaje', 'Potencia', 'Expresión Matemática']
		dlg = wx.SingleChoiceDialog(self, 'Seleccione una operación:', 'Aritmética', operaciones)
		if dlg.ShowModal() == wx.ID_OK:
			operacion = dlg.GetStringSelection()
			self.realizar_operacion_aritmetica(operacion)
		dlg.Destroy()

	def realizar_operacion_aritmetica(self, operacion):
		"""Inicia el diálogo para la operación aritmética seleccionada."""
		dialogo = DialogoAritmetica(self, operacion)
		dialogo.ShowModal()
		dialogo.Destroy()

	def conversion_unidades(self):
		"""Despliega las categorías de conversión de unidades."""
		categorias = ['Ángulo', 'Capacidad', 'Frecuencia', 'Información', 'Longitud/Superficie', 'Temperatura', 'Tiempo', 'Velocidad']
		dlg = wx.SingleChoiceDialog(self, 'Seleccione una categoría de conversión:', 'Conversión de Unidades', categorias)
		if dlg.ShowModal() == wx.ID_OK:
			categoria = dlg.GetStringSelection()
			dialogo = DialogoConversion(self, categoria)
			dialogo.ShowModal()
			dialogo.Destroy()
		dlg.Destroy()

	def operaciones_trigonometricas(self):
		"""Despliega las funciones trigonométricas disponibles."""
		funciones = ['Seno', 'Coseno', 'Tangente', 'Arco Seno', 'Arco Coseno', 'Arco Tangente']
		dlg = wx.SingleChoiceDialog(self, 'Seleccione una función trigonométrica:', 'Trigonometría', funciones)
		if dlg.ShowModal() == wx.ID_OK:
			funcion = dlg.GetStringSelection()
			dialogo = DialogoTrigonometria(self, funcion)
			dialogo.ShowModal()
			dialogo.Destroy()
		dlg.Destroy()

	def cambio_bases(self):
		"""Inicia el diálogo para cambio de bases numéricas."""
		dialogo = DialogoCambioBases(self)
		dialogo.ShowModal()
		dialogo.Destroy()

	def operaciones_geometricas(self):
		"""Despliega las operaciones geométricas disponibles."""
		figuras = ['Área de un Círculo', 'Perímetro de un Círculo', 'Área de un Triángulo', 'Perímetro de un Triángulo']
		dlg = wx.SingleChoiceDialog(self, 'Seleccione una operación geométrica:', 'Geometría', figuras)
		if dlg.ShowModal() == wx.ID_OK:
			figura = dlg.GetStringSelection()
			dialogo = DialogoGeometria(self, figura)
			dialogo.ShowModal()
			dialogo.Destroy()
		dlg.Destroy()

	def operaciones_quimica(self):
		"""Despliega las operaciones químicas disponibles."""
		operaciones = [
			'Calcular Masa Molar',
			'Convertir Masa a Moles',
			'Calcular Número de Partículas',
			'Energía de Enlace',
			'Calcular Concentración Molar',
			'Calcular pH',
			'Ley de Gases Ideales',
			'Calcular Constante de Equilibrio',
			'Calcular Rendimiento Porcentual'
		]
		dlg = wx.SingleChoiceDialog(self, 'Seleccione una operación química:', 'Química', operaciones)
		if dlg.ShowModal() == wx.ID_OK:
			operacion = dlg.GetStringSelection()
			self.realizar_operacion_quimica(operacion)
		dlg.Destroy()

	def realizar_operacion_quimica(self, operacion):
		"""Inicia el diálogo para la operación química seleccionada."""
		dialogo = DialogoQuimica(self, operacion)
		dialogo.ShowModal()
		dialogo.Destroy()

	def operaciones_estadistica(self):
		"""Despliega las operaciones estadísticas disponibles."""
		operaciones = [
			'Media',
			'Mediana',
			'Moda',
			'Varianza',
			'Desviación Estándar',
			'Percentil',
			'Cuartiles',
			'Rango',
			'Rango Intercuartil',
			'Coeficiente de Asimetría',
			'Curtosis',
			'Covarianza',
			'Coeficiente de Correlación',
			'Regresión Lineal',
			'Valor Z',
			'Probabilidad Normal Estándar'
		]
		dlg = wx.SingleChoiceDialog(self, 'Seleccione una operación estadística:', 'Estadística', operaciones)
		if dlg.ShowModal() == wx.ID_OK:
			operacion = dlg.GetStringSelection()
			self.realizar_operacion_estadistica(operacion)
		dlg.Destroy()
	
	def realizar_operacion_estadistica(self, operacion):
		"""Inicia el diálogo para la operación estadística seleccionada."""
		dialogo = DialogoEstadistica(self, operacion)
		dialogo.ShowModal()
		dialogo.Destroy()

class DialogoAritmetica(wx.Dialog):
	"""Diálogo para operaciones aritméticas."""
	def __init__(self, parent, operacion):
		super().__init__(parent, title=operacion, size=(350, 350))
		self.operacion = operacion

		vbox = wx.BoxSizer(wx.VERTICAL)

		# Ajustar los campos de entrada según la operación seleccionada
		if self.operacion in ['Suma', 'Resta', 'Multiplicación', 'División']:
			lbl_num1 = wx.StaticText(self, label="Primer número:")
			self.txt_entrada1 = wx.TextCtrl(self)
			lbl_num2 = wx.StaticText(self, label="Segundo número:")
			self.txt_entrada2 = wx.TextCtrl(self)
			vbox.Add(lbl_num1, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_entrada1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
			vbox.Add(lbl_num2, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_entrada2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
		elif self.operacion == 'Raíz Cuadrada':
			lbl_num = wx.StaticText(self, label="Ingrese el número:")
			self.txt_num = wx.TextCtrl(self)
			vbox.Add(lbl_num, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_num, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
		elif self.operacion == 'Logaritmo':
			lbl_num = wx.StaticText(self, label="Ingrese el número:")
			self.txt_num = wx.TextCtrl(self)
			lbl_base = wx.StaticText(self, label="Base (opcional, por defecto es e):")
			self.txt_base = wx.TextCtrl(self)
			vbox.Add(lbl_num, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_num, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
			vbox.Add(lbl_base, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_base, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
		elif self.operacion == 'Porcentaje':
			lbl_total = wx.StaticText(self, label="Valor total:")
			self.txt_total = wx.TextCtrl(self)
			lbl_porcentaje = wx.StaticText(self, label="Porcentaje a calcular:")
			self.txt_porcentaje = wx.TextCtrl(self)
			vbox.Add(lbl_total, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_total, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
			vbox.Add(lbl_porcentaje, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_porcentaje, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
		elif self.operacion == 'Potencia':
			lbl_base = wx.StaticText(self, label="Base:")
			self.txt_base = wx.TextCtrl(self)
			lbl_exponente = wx.StaticText(self, label="Exponente:")
			self.txt_exponente = wx.TextCtrl(self)
			vbox.Add(lbl_base, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_base, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
			vbox.Add(lbl_exponente, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_exponente, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
		elif self.operacion == 'Expresión Matemática':
			lbl_expresion = wx.StaticText(self, label="Ingrese la expresión matemática (puede usar variables):")
			self.txt_expresion = wx.TextCtrl(self)
			lbl_variables = wx.StaticText(self, label="Defina los valores de las variables (ejemplo: x=2, y=3):")
			self.txt_variables = wx.TextCtrl(self)
			vbox.Add(lbl_expresion, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_expresion, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
			vbox.Add(lbl_variables, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_variables, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

		lbl_resultado = wx.StaticText(self, label="Resultado:")
		self.txt_resultado = wx.TextCtrl(self, style=wx.TE_READONLY)
		vbox.Add(lbl_resultado, flag=wx.LEFT | wx.TOP, border=10)
		vbox.Add(self.txt_resultado, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		btn_calcular = wx.Button(self, label="&Calcular")
		btn_calcular.Bind(wx.EVT_BUTTON, self.calcular)
		btn_ayuda = wx.Button(self, label="&Ayuda")
		btn_ayuda.Bind(wx.EVT_BUTTON, self.mostrar_ayuda)
		btn_salir = wx.Button(self, label="&Salir")
		btn_salir.Bind(wx.EVT_BUTTON, self.salir)
		hbox.Add(btn_calcular, flag=wx.RIGHT, border=5)
		hbox.Add(btn_ayuda, flag=wx.RIGHT, border=5)
		hbox.Add(btn_salir)

		vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

		self.SetSizer(vbox)

	def calcular(self, event):
		"""Realiza el cálculo de la operación seleccionada."""
		try:
			if self.operacion == 'Suma':
				num1 = float(self.txt_entrada1.GetValue())
				num2 = float(self.txt_entrada2.GetValue())
				resultado = Aritmetica.suma(num1, num2)
			elif self.operacion == 'Resta':
				num1 = float(self.txt_entrada1.GetValue())
				num2 = float(self.txt_entrada2.GetValue())
				resultado = Aritmetica.resta(num1, num2)
			elif self.operacion == 'Multiplicación':
				num1 = float(self.txt_entrada1.GetValue())
				num2 = float(self.txt_entrada2.GetValue())
				resultado = Aritmetica.multiplicacion(num1, num2)
			elif self.operacion == 'División':
				num1 = float(self.txt_entrada1.GetValue())
				num2 = float(self.txt_entrada2.GetValue())
				resultado = Aritmetica.division(num1, num2)
			elif self.operacion == 'Raíz Cuadrada':
				num = float(self.txt_num.GetValue())
				resultado = Aritmetica.raiz_cuadrada(num)
			elif self.operacion == 'Logaritmo':
				num = float(self.txt_num.GetValue())
				base_str = self.txt_base.GetValue()
				if base_str:
					base = float(base_str)
					resultado = Aritmetica.logaritmo(num, base)
				else:
					resultado = Aritmetica.logaritmo(num)
			elif self.operacion == 'Porcentaje':
				total = float(self.txt_total.GetValue())
				porcentaje = float(self.txt_porcentaje.GetValue())
				resultado = Aritmetica.porcentaje(total, porcentaje)
			elif self.operacion == 'Potencia':
				base = float(self.txt_base.GetValue())
				exponente = float(self.txt_exponente.GetValue())
				resultado = Aritmetica.potencia(base, exponente)
			elif self.operacion == 'Expresión Matemática':
				expresion = self.txt_expresion.GetValue()
				variables_str = self.txt_variables.GetValue()
				variables = {}
				if variables_str:
					for var in variables_str.split(','):
						key, value = var.strip().split('=')
						variables[key.strip()] = float(value.strip())
				resultado = Aritmetica.expresion_matematica(expresion, variables)
			else:
				raise ValueError("Operación no soportada.")

			self.txt_resultado.SetValue(str(resultado))
			self.txt_resultado.SetFocus()

			if self.operacion in ['Suma', 'Resta', 'Multiplicación', 'División']:
				self.txt_entrada1.SetValue("")
				self.txt_entrada2.SetValue("")
			elif self.operacion == 'Raíz Cuadrada':
				self.txt_num.SetValue("")
			elif self.operacion == 'Logaritmo':
				self.txt_num.SetValue("")
				self.txt_base.SetValue("")
			elif self.operacion == 'Porcentaje':
				self.txt_total.SetValue("")
				self.txt_porcentaje.SetValue("")
			elif self.operacion == 'Potencia':
				self.txt_base.SetValue("")
				self.txt_exponente.SetValue("")
			elif self.operacion == 'Expresión Matemática':
				self.txt_expresion.SetValue("")
				self.txt_variables.SetValue("")

		except Exception as e:
			wx.MessageBox(f"Error: {e}", "Error", wx.OK | wx.ICON_ERROR)

	def mostrar_ayuda(self, event):
		"""Muestra la ayuda específica para la operación seleccionada."""
		if self.operacion in ['Suma', 'Resta', 'Multiplicación', 'División']:
			mensaje = f"Ingrese los dos números para realizar la operación de {self.operacion.lower()}."
		elif self.operacion == 'Raíz Cuadrada':
			mensaje = "Ingrese un número no negativo para calcular su raíz cuadrada."
		elif self.operacion == 'Logaritmo':
			mensaje = ("Ingrese el número para calcular su logaritmo.\n"
					   "Puede especificar la base; si no se proporciona, se calculará el logaritmo natural (base e).\n"
					   "La base debe ser un número positivo diferente de 1.")
		elif self.operacion == 'Porcentaje':
			mensaje = ("Ingrese el valor total y el porcentaje que desea calcular.\n"
					   "Por ejemplo, para calcular el 15% de 200, ingrese 'Valor total' = 200 y 'Porcentaje a calcular' = 15.")
		elif self.operacion == 'Potencia':
			mensaje = "Ingrese la base y el exponente para calcular la potencia."
		elif self.operacion == 'Expresión Matemática':
			mensaje = ("Ingrese una expresión matemática válida que puede incluir variables.\n"
					   "Ejemplos:\n- x**2 + 5*x + 6\n- sin(x) + cos(y)\n"
					   "Defina los valores de las variables en el formato: x=2, y=3")
		else:
			mensaje = "Operación no soportada."
		wx.MessageBox(mensaje, "Ayuda", wx.OK | wx.ICON_INFORMATION)

	def salir(self, event):
		"""Cierra el diálogo actual."""
		self.Destroy()

class DialogoConversion(wx.Dialog):
	"""Diálogo para conversión de unidades."""
	def __init__(self, parent, categoria):
		super().__init__(parent, title=f"Conversión de {categoria}", size=(350, 400))
		self.categoria = categoria

		vbox = wx.BoxSizer(wx.VERTICAL)

		lbl_valor = wx.StaticText(self, label="Valor a convertir:")
		self.txt_valor = wx.TextCtrl(self)
		lbl_unidad_origen = wx.StaticText(self, label="Unidad de origen:")
		self.cmb_origen = wx.ComboBox(self, choices=self.obtener_unidades(), style=wx.CB_READONLY)
		lbl_unidad_destino = wx.StaticText(self, label="Unidad de destino:")
		self.cmb_destino = wx.ComboBox(self, choices=self.obtener_unidades(), style=wx.CB_READONLY)
		lbl_resultado = wx.StaticText(self, label="Resultado:")
		self.txt_resultado = wx.TextCtrl(self, style=wx.TE_READONLY)

		vbox.Add(lbl_valor, flag=wx.LEFT|wx.TOP, border=10)
		vbox.Add(self.txt_valor, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
		vbox.Add(lbl_unidad_origen, flag=wx.LEFT|wx.TOP, border=10)
		vbox.Add(self.cmb_origen, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
		vbox.Add(lbl_unidad_destino, flag=wx.LEFT|wx.TOP, border=10)
		vbox.Add(self.cmb_destino, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
		vbox.Add(lbl_resultado, flag=wx.LEFT|wx.TOP, border=10)
		vbox.Add(self.txt_resultado, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		btn_calcular = wx.Button(self, label="&Calcular")
		btn_calcular.Bind(wx.EVT_BUTTON, self.calcular)
		btn_ayuda = wx.Button(self, label="&Ayuda")
		btn_ayuda.Bind(wx.EVT_BUTTON, self.mostrar_ayuda)
		btn_salir = wx.Button(self, label="&Salir")
		btn_salir.Bind(wx.EVT_BUTTON, self.salir)
		hbox.Add(btn_calcular, flag=wx.RIGHT, border=5)
		hbox.Add(btn_ayuda, flag=wx.RIGHT, border=5)
		hbox.Add(btn_salir)

		vbox.Add(hbox, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

		self.SetSizer(vbox)

	def obtener_unidades(self):
		"""Retorna las unidades disponibles para la categoría seleccionada."""
		unidades = {
			'Ángulo': ['Grados', 'Radianes'],
			'Capacidad': ['Litros', 'Mililitros', 'Galones'],
			'Frecuencia': ['Hertz', 'Kilohertz', 'Megahertz', 'Gigahertz'],
			'Información': ['Bytes', 'Kilobytes', 'Megabytes', 'Gigabytes', 'Terabytes'],
			'Longitud/Superficie': ['Metros', 'Centímetros', 'Pulgadas', 'Pies', 'Kilómetros', 'Millas'],
			'Temperatura': ['Celsius', 'Fahrenheit', 'Kelvin'],
			'Tiempo': ['Segundos', 'Minutos', 'Horas', 'Días'],
			'Velocidad': ['m/s', 'km/h', 'mph']
		}
		return unidades.get(self.categoria, [])

	def calcular(self, event):
		"""Realiza la conversión de unidades."""
		try:
			valor = float(self.txt_valor.GetValue())
			origen = self.cmb_origen.GetValue()
			destino = self.cmb_destino.GetValue()
			if not origen or not destino:
				raise ValueError("Debe seleccionar las unidades de origen y destino.")
			resultado = Conversion.convertir(valor, origen, destino, self.categoria)
			self.txt_resultado.SetValue(str(resultado))
			self.txt_resultado.SetFocus()
			self.txt_valor.SetValue("")
		except Exception as e:
			wx.MessageBox(f"Error: {e}", "Error", wx.OK | wx.ICON_ERROR)

	def mostrar_ayuda(self, event):
		"""Muestra la ayuda para la conversión de unidades."""
		mensaje = (f"Ingrese el valor y seleccione las unidades de origen y destino para convertir en la categoría {self.categoria}.\n"
				   "Por ejemplo, para convertir 100 centímetros a metros, seleccione 'Centímetros' como unidad de origen, 'Metros' como unidad de destino, y el valor 100.")
		wx.MessageBox(mensaje, "Ayuda", wx.OK | wx.ICON_INFORMATION)

	def salir(self, event):
		"""Cierra el diálogo actual."""
		self.Destroy()

class DialogoTrigonometria(wx.Dialog):
	"""Diálogo para operaciones trigonométricas."""
	def __init__(self, parent, funcion):
		super().__init__(parent, title=f"Función {funcion}", size=(350, 300))
		self.funcion = funcion

		vbox = wx.BoxSizer(wx.VERTICAL)

		if self.funcion in ['Seno', 'Coseno', 'Tangente']:
			lbl_angulo = wx.StaticText(self, label="Ingrese el ángulo en grados:")
			self.txt_angulo = wx.TextCtrl(self)
			vbox.Add(lbl_angulo, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_angulo, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
		elif self.funcion in ['Arco Seno', 'Arco Coseno', 'Arco Tangente']:
			lbl_valor = wx.StaticText(self, label="Ingrese el valor:")
			self.txt_valor = wx.TextCtrl(self)
			vbox.Add(lbl_valor, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_valor, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

		lbl_resultado = wx.StaticText(self, label="Resultado:")
		self.txt_resultado = wx.TextCtrl(self, style=wx.TE_READONLY)
		vbox.Add(lbl_resultado, flag=wx.LEFT | wx.TOP, border=10)
		vbox.Add(self.txt_resultado, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		btn_calcular = wx.Button(self, label="&Calcular")
		btn_calcular.Bind(wx.EVT_BUTTON, self.calcular)
		btn_ayuda = wx.Button(self, label="&Ayuda")
		btn_ayuda.Bind(wx.EVT_BUTTON, self.mostrar_ayuda)
		btn_salir = wx.Button(self, label="&Salir")
		btn_salir.Bind(wx.EVT_BUTTON, self.salir)
		hbox.Add(btn_calcular, flag=wx.RIGHT, border=5)
		hbox.Add(btn_ayuda, flag=wx.RIGHT, border=5)
		hbox.Add(btn_salir)

		vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

		self.SetSizer(vbox)

	def calcular(self, event):
		"""Realiza el cálculo de la función trigonométrica seleccionada."""
		try:
			if self.funcion in ['Seno', 'Coseno', 'Tangente']:
				angulo_grados = float(self.txt_angulo.GetValue())
				if self.funcion == 'Seno':
					resultado = Trigonometria.seno(angulo_grados)
				elif self.funcion == 'Coseno':
					resultado = Trigonometria.coseno(angulo_grados)
				elif self.funcion == 'Tangente':
					resultado = Trigonometria.tangente(angulo_grados)
				self.txt_resultado.SetValue(str(resultado))
				self.txt_angulo.SetValue("")
			elif self.funcion in ['Arco Seno', 'Arco Coseno', 'Arco Tangente']:
				valor = float(self.txt_valor.GetValue())
				if self.funcion == 'Arco Seno':
					resultado = Trigonometria.arco_seno(valor)
				elif self.funcion == 'Arco Coseno':
					resultado = Trigonometria.arco_coseno(valor)
				elif self.funcion == 'Arco Tangente':
					resultado = Trigonometria.arco_tangente(valor)
				self.txt_resultado.SetValue(str(resultado))
				self.txt_valor.SetValue("")
			self.txt_resultado.SetFocus()
		except Exception as e:
			wx.MessageBox(f"Error: {e}", "Error", wx.OK | wx.ICON_ERROR)

	def mostrar_ayuda(self, event):
		"""Muestra la ayuda específica para la función seleccionada."""
		if self.funcion in ['Seno', 'Coseno', 'Tangente']:
			mensaje = f"Ingrese el ángulo en grados para calcular el {self.funcion.lower()}.\nEjemplo: Para calcular el seno de 30 grados, ingrese 30."
		elif self.funcion in ['Arco Seno', 'Arco Coseno', 'Arco Tangente']:
			mensaje = f"Ingrese el valor para calcular el {self.funcion.lower()}.\nEjemplo: Para calcular el arco seno de 0.5, ingrese 0.5."
		else:
			mensaje = "Función no soportada."
		wx.MessageBox(mensaje, "Ayuda", wx.OK | wx.ICON_INFORMATION)

	def salir(self, event):
		"""Cierra el diálogo actual."""
		self.Destroy()

class DialogoCambioBases(wx.Dialog):
	"""Diálogo para cambio de bases numéricas."""
	def __init__(self, parent):
		super().__init__(parent, title="Cambio de Bases", size=(350, 300))

		vbox = wx.BoxSizer(wx.VERTICAL)

		lbl_numero = wx.StaticText(self, label="Ingrese el número:")
		self.txt_numero = wx.TextCtrl(self)
		lbl_base_origen = wx.StaticText(self, label="Base de origen:")
		self.cmb_origen = wx.ComboBox(self, choices=['2', '8', '10', '16'], style=wx.CB_READONLY)
		lbl_base_destino = wx.StaticText(self, label="Base de destino:")
		self.cmb_destino = wx.ComboBox(self, choices=['2', '8', '10', '16'], style=wx.CB_READONLY)
		lbl_resultado = wx.StaticText(self, label="Resultado:")
		self.txt_resultado = wx.TextCtrl(self, style=wx.TE_READONLY)

		vbox.Add(lbl_numero, flag=wx.LEFT|wx.TOP, border=10)
		vbox.Add(self.txt_numero, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
		vbox.Add(lbl_base_origen, flag=wx.LEFT|wx.TOP, border=10)
		vbox.Add(self.cmb_origen, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
		vbox.Add(lbl_base_destino, flag=wx.LEFT|wx.TOP, border=10)
		vbox.Add(self.cmb_destino, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
		vbox.Add(lbl_resultado, flag=wx.LEFT|wx.TOP, border=10)
		vbox.Add(self.txt_resultado, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		btn_calcular = wx.Button(self, label="&Calcular")
		btn_calcular.Bind(wx.EVT_BUTTON, self.calcular)
		btn_ayuda = wx.Button(self, label="&Ayuda")
		btn_ayuda.Bind(wx.EVT_BUTTON, self.mostrar_ayuda)
		btn_salir = wx.Button(self, label="&Salir")
		btn_salir.Bind(wx.EVT_BUTTON, self.salir)
		hbox.Add(btn_calcular, flag=wx.RIGHT, border=5)
		hbox.Add(btn_ayuda, flag=wx.RIGHT, border=5)
		hbox.Add(btn_salir)

		vbox.Add(hbox, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

		self.SetSizer(vbox)

	def calcular(self, event):
		"""Realiza la conversión de bases numéricas."""
		try:
			numero = self.txt_numero.GetValue()
			base_origen = int(self.cmb_origen.GetValue())
			base_destino = int(self.cmb_destino.GetValue())
			if not numero or not self.cmb_origen.GetValue() or not self.cmb_destino.GetValue():
				raise ValueError("Debe ingresar el número y seleccionar las bases de origen y destino.")
			resultado = CambioBases.convertir_base(numero, base_origen, base_destino)
			self.txt_resultado.SetValue(resultado)
			self.txt_resultado.SetFocus()
			self.txt_numero.SetValue("")
		except Exception as e:
			wx.MessageBox(f"Error: {e}", "Error", wx.OK | wx.ICON_ERROR)

	def mostrar_ayuda(self, event):
		"""Muestra la ayuda para el cambio de bases numéricas."""
		mensaje = ("Ingrese el número y seleccione las bases de origen y destino para convertir.\n"
				   "Ejemplo: Convertir el número '1010' de base 2 (binario) a base 10 (decimal).")
		wx.MessageBox(mensaje, "Ayuda", wx.OK | wx.ICON_INFORMATION)

	def salir(self, event):
		"""Cierra el diálogo actual."""
		self.Destroy()

class DialogoGeometria(wx.Dialog):
	"""Diálogo para operaciones geométricas."""
	def __init__(self, parent, figura):
		super().__init__(parent, title=figura, size=(350, 300))
		self.figura = figura

		vbox = wx.BoxSizer(wx.VERTICAL)

		if 'Círculo' in figura:
			lbl_radio = wx.StaticText(self, label="Ingrese el radio:")
			self.txt_radio = wx.TextCtrl(self)
			vbox.Add(lbl_radio, flag=wx.LEFT|wx.TOP, border=10)
			vbox.Add(self.txt_radio, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
		elif 'Triángulo' in figura:
			lbl_base = wx.StaticText(self, label="Ingrese la base:")
			self.txt_base = wx.TextCtrl(self)
			lbl_altura = wx.StaticText(self, label="Ingrese la altura:")
			self.txt_altura = wx.TextCtrl(self)
			vbox.Add(lbl_base, flag=wx.LEFT|wx.TOP, border=10)
			vbox.Add(self.txt_base, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
			vbox.Add(lbl_altura, flag=wx.LEFT|wx.TOP, border=10)
			vbox.Add(self.txt_altura, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)

		lbl_resultado = wx.StaticText(self, label="Resultado:")
		self.txt_resultado = wx.TextCtrl(self, style=wx.TE_READONLY)
		vbox.Add(lbl_resultado, flag=wx.LEFT | wx.TOP, border=10)
		vbox.Add(self.txt_resultado, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		btn_calcular = wx.Button(self, label="&Calcular")
		btn_calcular.Bind(wx.EVT_BUTTON, self.calcular)
		btn_ayuda = wx.Button(self, label="&Ayuda")
		btn_ayuda.Bind(wx.EVT_BUTTON, self.mostrar_ayuda)
		btn_salir = wx.Button(self, label="&Salir")
		btn_salir.Bind(wx.EVT_BUTTON, self.salir)
		hbox.Add(btn_calcular, flag=wx.RIGHT, border=5)
		hbox.Add(btn_ayuda, flag=wx.RIGHT, border=5)
		hbox.Add(btn_salir)

		vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

		self.SetSizer(vbox)

	def calcular(self, event):
		"""Realiza el cálculo geométrico seleccionado."""
		try:
			if 'Círculo' in self.figura:
				radio = float(self.txt_radio.GetValue())
				if 'Área' in self.figura:
					resultado = Geometria.area_circulo(radio)
				elif 'Perímetro' in self.figura:
					resultado = Geometria.perimetro_circulo(radio)
				self.txt_radio.SetValue("")
			elif 'Triángulo' in self.figura:
				base = float(self.txt_base.GetValue())
				altura = float(self.txt_altura.GetValue())
				if 'Área' in self.figura:
					resultado = Geometria.area_triangulo(base, altura)
				elif 'Perímetro' in self.figura:
					resultado = Geometria.perimetro_triangulo(base, base, base)  # Triángulo equilátero
				self.txt_base.SetValue("")
				self.txt_altura.SetValue("")
			else:
				raise ValueError("Figura no soportada.")
			self.txt_resultado.SetValue(str(resultado))
			self.txt_resultado.SetFocus()
		except Exception as e:
			wx.MessageBox(f"Error: {e}", "Error", wx.OK | wx.ICON_ERROR)

	def mostrar_ayuda(self, event):
		"""Muestra la ayuda específica para la figura seleccionada."""
		if 'Círculo' in self.figura:
			mensaje = f"Ingrese el radio del círculo para calcular el {self.figura.lower()}.\nEjemplo: Para un radio de 5 unidades."
		elif 'Triángulo' in self.figura:
			mensaje = f"Ingrese la base y la altura del triángulo para calcular el {self.figura.lower()}.\nEjemplo: Base = 4, Altura = 3."
		else:
			mensaje = "Figura no soportada."
		wx.MessageBox(mensaje, "Ayuda", wx.OK | wx.ICON_INFORMATION)

	def salir(self, event):
		"""Cierra el diálogo actual."""
		self.Destroy()

class DialogoQuimica(wx.Dialog):
	"""Diálogo para operaciones químicas."""
	def __init__(self, parent, operacion):
		super().__init__(parent, title=operacion, size=(450, 500))
		self.operacion = operacion

		vbox = wx.BoxSizer(wx.VERTICAL)

		# Crear los controles de entrada según la operación seleccionada
		if self.operacion == 'Calcular Masa Molar':
			lbl_compuesto = wx.StaticText(self, label="Ingrese la fórmula química del compuesto:")
			self.txt_compuesto = wx.TextCtrl(self)
			vbox.Add(lbl_compuesto, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_compuesto, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

		elif self.operacion == 'Convertir Masa a Moles':
			lbl_masa = wx.StaticText(self, label="Ingrese la masa en gramos:")
			self.txt_masa = wx.TextCtrl(self)
			lbl_masa_molar = wx.StaticText(self, label="Ingrese la masa molar (g/mol):")
			self.txt_masa_molar = wx.TextCtrl(self)
			vbox.Add(lbl_masa, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_masa, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
			vbox.Add(lbl_masa_molar, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_masa_molar, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

		elif self.operacion == 'Calcular Número de Partículas':
			lbl_moles = wx.StaticText(self, label="Ingrese la cantidad de moles:")
			self.txt_moles = wx.TextCtrl(self)
			vbox.Add(lbl_moles, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_moles, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

		elif self.operacion == 'Calcular Concentración Molar':
			lbl_moles = wx.StaticText(self, label="Ingrese el número de moles del soluto:")
			self.txt_moles = wx.TextCtrl(self)
			lbl_volumen = wx.StaticText(self, label="Ingrese el volumen de la solución en litros:")
			self.txt_volumen = wx.TextCtrl(self)
			vbox.Add(lbl_moles, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_moles, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
			vbox.Add(lbl_volumen, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_volumen, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

		elif self.operacion == 'Calcular pH':
			lbl_concentracion = wx.StaticText(self, label="Ingrese la concentración de H+ (mol/L):")
			self.txt_concentracion = wx.TextCtrl(self)
			vbox.Add(lbl_concentracion, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_concentracion, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

		elif self.operacion == 'Calcular Rendimiento Porcentual':
			lbl_real = wx.StaticText(self, label="Ingrese el rendimiento real (g):")
			self.txt_real = wx.TextCtrl(self)
			lbl_teorico = wx.StaticText(self, label="Ingrese el rendimiento teórico (g):")
			self.txt_teorico = wx.TextCtrl(self)
			vbox.Add(lbl_real, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_real, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
			vbox.Add(lbl_teorico, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_teorico, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

		elif self.operacion == 'Ley de Gases Ideales':
			lbl_desconocida = wx.StaticText(self, label="Seleccione la variable a calcular:")
			self.cmb_desconocida = wx.ComboBox(self, choices=['Presión (P)', 'Volumen (V)', 'Número de moles (n)', 'Temperatura (T)'], style=wx.CB_READONLY)
			vbox.Add(lbl_desconocida, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.cmb_desconocida, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

			lbl_presion = wx.StaticText(self, label="Ingrese la presión (atm):")
			self.txt_presion = wx.TextCtrl(self)
			lbl_volumen = wx.StaticText(self, label="Ingrese el volumen (L):")
			self.txt_volumen = wx.TextCtrl(self)
			lbl_moles = wx.StaticText(self, label="Ingrese el número de moles (mol):")
			self.txt_moles = wx.TextCtrl(self)
			lbl_temperatura = wx.StaticText(self, label="Ingrese la temperatura (K):")
			self.txt_temperatura = wx.TextCtrl(self)

			vbox.Add(lbl_presion, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_presion, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
			vbox.Add(lbl_volumen, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_volumen, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
			vbox.Add(lbl_moles, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_moles, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
			vbox.Add(lbl_temperatura, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_temperatura, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

		elif self.operacion == 'Calcular Constante de Equilibrio':
			lbl_productos = wx.StaticText(self, label="Ingrese las concentraciones de productos (ejemplo: H2=0.5, O2=0.2):")
			self.txt_productos = wx.TextCtrl(self)
			lbl_reactivos = wx.StaticText(self, label="Ingrese las concentraciones de reactivos (ejemplo: H2O=1.0):")
			self.txt_reactivos = wx.TextCtrl(self)
			vbox.Add(lbl_productos, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_productos, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
			vbox.Add(lbl_reactivos, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_reactivos, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

		elif self.operacion == 'Energía de Enlace':
			lbl_enlaces = wx.StaticText(self, label="Ingrese los enlaces y cantidades (ejemplo: C-H=4, C=C=1):")
			self.txt_enlaces = wx.TextCtrl(self)
			lbl_energias = wx.StaticText(self, label="Ingrese las energías de enlace (ejemplo: C-H=413, C=C=614):")
			self.txt_energias = wx.TextCtrl(self)
			vbox.Add(lbl_enlaces, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_enlaces, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
			vbox.Add(lbl_energias, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_energias, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

		else:
			mensaje = "Operación no soportada."
			wx.MessageBox(mensaje, "Error", wx.OK | wx.ICON_ERROR)
			self.Destroy()
			return

		# Campo para mostrar el resultado
		lbl_resultado = wx.StaticText(self, label="Resultado:")
		self.txt_resultado = wx.TextCtrl(self, style=wx.TE_READONLY)
		vbox.Add(lbl_resultado, flag=wx.LEFT | wx.TOP, border=10)
		vbox.Add(self.txt_resultado, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

		# Botones de acción
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		btn_calcular = wx.Button(self, label="&Calcular")
		btn_calcular.Bind(wx.EVT_BUTTON, self.calcular)
		btn_ayuda = wx.Button(self, label="&Ayuda")
		btn_ayuda.Bind(wx.EVT_BUTTON, self.mostrar_ayuda)
		btn_salir = wx.Button(self, label="&Salir")
		btn_salir.Bind(wx.EVT_BUTTON, self.salir)
		hbox.Add(btn_calcular, flag=wx.RIGHT, border=5)
		hbox.Add(btn_ayuda, flag=wx.RIGHT, border=5)
		hbox.Add(btn_salir)

		vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

		self.SetSizer(vbox)

	def calcular(self, event):
		"""Realiza el cálculo de la operación química seleccionada."""
		try:
			if self.operacion == 'Calcular Masa Molar':
				compuesto = self.txt_compuesto.GetValue()
				resultado = Quimica.calcular_masa_molar(compuesto)
				self.txt_resultado.SetValue(f"{resultado:.3f} g/mol")
				self.txt_compuesto.SetValue("")

			elif self.operacion == 'Convertir Masa a Moles':
				masa = float(self.txt_masa.GetValue())
				masa_molar = float(self.txt_masa_molar.GetValue())
				resultado = Quimica.convertir_masa_a_moles(masa, masa_molar)
				self.txt_resultado.SetValue(f"{resultado:.5f} moles")
				self.txt_masa.SetValue("")
				self.txt_masa_molar.SetValue("")

			elif self.operacion == 'Calcular Número de Partículas':
				moles = float(self.txt_moles.GetValue())
				resultado = Quimica.calcular_numero_particulas(moles)
				self.txt_resultado.SetValue(f"{resultado:.3e} partículas")
				self.txt_moles.SetValue("")

			elif self.operacion == 'Calcular Concentración Molar':
				n_moles = float(self.txt_moles.GetValue())
				volumen = float(self.txt_volumen.GetValue())
				resultado = Quimica.calcular_concentracion_molar(n_moles, volumen)
				self.txt_resultado.SetValue(f"{resultado:.5f} mol/L")
				self.txt_moles.SetValue("")
				self.txt_volumen.SetValue("")

			elif self.operacion == 'Calcular pH':
				concentracion = float(self.txt_concentracion.GetValue())
				resultado = Quimica.calcular_pH(concentracion)
				self.txt_resultado.SetValue(f"pH = {resultado:.2f}")
				self.txt_concentracion.SetValue("")

			elif self.operacion == 'Calcular Rendimiento Porcentual':
				rendimiento_real = float(self.txt_real.GetValue())
				rendimiento_teorico = float(self.txt_teorico.GetValue())
				resultado = Quimica.calcular_rendimiento_porcentual(rendimiento_real, rendimiento_teorico)
				self.txt_resultado.SetValue(f"Rendimiento: {resultado:.2f}%")
				self.txt_real.SetValue("")
				self.txt_teorico.SetValue("")

			elif self.operacion == 'Ley de Gases Ideales':
				desconocida = self.cmb_desconocida.GetValue()
				P = float(self.txt_presion.GetValue()) if self.txt_presion.GetValue() else None
				V = float(self.txt_volumen.GetValue()) if self.txt_volumen.GetValue() else None
				n = float(self.txt_moles.GetValue()) if self.txt_moles.GetValue() else None
				T = float(self.txt_temperatura.GetValue()) if self.txt_temperatura.GetValue() else None

				variables = {'P': P, 'V': V, 'n': n, 'T': T}

				# Establecer la variable desconocida a None
				if 'Presión' in desconocida:
					variables['P'] = None
				elif 'Volumen' in desconocida:
					variables['V'] = None
				elif 'Número de moles' in desconocida:
					variables['n'] = None
				elif 'Temperatura' in desconocida:
					variables['T'] = None
				else:
					raise ValueError("Variable desconocida no reconocida.")

				resultado = Quimica.ley_gases_ideales(P=variables['P'], V=variables['V'], n=variables['n'], T=variables['T'])
				variable_calculada = desconocida.split(' ')[0]
				self.txt_resultado.SetValue(f"{variable_calculada} = {resultado:.5f}")
				# Limpiar campos
				self.txt_presion.SetValue("")
				self.txt_volumen.SetValue("")
				self.txt_moles.SetValue("")
				self.txt_temperatura.SetValue("")

			elif self.operacion == 'Calcular Constante de Equilibrio':
				productos_str = self.txt_productos.GetValue()
				reactivos_str = self.txt_reactivos.GetValue()
				productos = self.parsear_concentraciones(productos_str)
				reactivos = self.parsear_concentraciones(reactivos_str)
				resultado = Quimica.calcular_constante_equilibrio(productos, reactivos)
				self.txt_resultado.SetValue(f"Kc = {resultado:.5f}")
				self.txt_productos.SetValue("")
				self.txt_reactivos.SetValue("")

			elif self.operacion == 'Energía de Enlace':
				enlaces_str = self.txt_enlaces.GetValue()
				energias_str = self.txt_energias.GetValue()
				enlaces = self.parsear_diccionario(enlaces_str)
				energias_enlace = self.parsear_diccionario(energias_str)
				resultado = Quimica.energia_enlace(enlaces, energias_enlace)
				self.txt_resultado.SetValue(f"Energía total: {resultado:.2f} kJ/mol")
				self.txt_enlaces.SetValue("")
				self.txt_energias.SetValue("")

			else:
				raise ValueError("Operación no soportada.")

			self.txt_resultado.SetFocus()

		except Exception as e:
			wx.MessageBox(f"Error: {e}", "Error", wx.OK | wx.ICON_ERROR)

	def mostrar_ayuda(self, event):
		"""Muestra la ayuda específica para la operación química seleccionada."""
		if self.operacion == 'Calcular Masa Molar':
			mensaje = "Ingrese la fórmula química del compuesto. Ejemplo: H2O, C6H12O6."
		elif self.operacion == 'Convertir Masa a Moles':
			mensaje = "Ingrese la masa en gramos y la masa molar del compuesto en g/mol."
		elif self.operacion == 'Calcular Número de Partículas':
			mensaje = "Ingrese la cantidad de moles para calcular el número de partículas usando el número de Avogadro."
		elif self.operacion == 'Calcular Concentración Molar':
			mensaje = "Ingrese el número de moles del soluto y el volumen de la solución en litros."
		elif self.operacion == 'Calcular pH':
			mensaje = "Ingrese la concentración de iones H+ en mol/L para calcular el pH de la solución."
		elif self.operacion == 'Calcular Rendimiento Porcentual':
			mensaje = "Ingrese el rendimiento real y el rendimiento teórico para calcular el rendimiento porcentual."
		elif self.operacion == 'Ley de Gases Ideales':
			mensaje = ("Seleccione la variable que desea calcular y proporcione los valores de las otras tres.\n"
					   "La ley de los gases ideales es PV = nRT.\n"
					   "Ingrese los valores en las unidades indicadas:\n"
					   "- Presión (P) en atmósferas (atm)\n"
					   "- Volumen (V) en litros (L)\n"
					   "- Número de moles (n) en moles (mol)\n"
					   "- Temperatura (T) en Kelvin (K)")
		elif self.operacion == 'Calcular Constante de Equilibrio':
			mensaje = ("Ingrese las concentraciones molares de productos y reactivos en el formato:\n"
					   "compuesto=concentración, separado por comas.\n"
					   "Ejemplo de productos: CO2=0.5, H2O=1.0\n"
					   "Ejemplo de reactivos: C6H12O6=0.1, O2=0.8")
		elif self.operacion == 'Energía de Enlace':
			mensaje = ("Ingrese los enlaces y sus cantidades en el formato:\n"
					   "enlace=cantidad, separado por comas.\n"
					   "Ejemplo de enlaces: C-H=4, C=C=1\n"
					   "Ingrese las energías de enlace en kJ/mol en el mismo formato:\n"
					   "Ejemplo de energías: C-H=413, C=C=614")
		else:
			mensaje = "Operación no soportada."
		wx.MessageBox(mensaje, "Ayuda", wx.OK | wx.ICON_INFORMATION)

	def salir(self, event):
		"""Cierra el diálogo actual."""
		self.Destroy()

	def parsear_concentraciones(self, cadena):
		"""Convierte una cadena de texto en un diccionario de concentraciones."""
		try:
			resultado = {}
			pares = cadena.split(',')
			for par in pares:
				compuesto, valor = par.strip().split('=')
				resultado[compuesto.strip()] = float(valor.strip())
			return resultado
		except Exception:
			raise ValueError("Formato incorrecto. Use el formato compuesto=concentración, separado por comas.")

	def parsear_diccionario(self, cadena):
		"""Convierte una cadena de texto en un diccionario."""
		try:
			resultado = {}
			pares = cadena.split(',')
			for par in pares:
				clave, valor = par.strip().split('=')
				resultado[clave.strip()] = float(valor.strip())
			return resultado
		except Exception:
			raise ValueError("Formato incorrecto. Use el formato clave=valor, separado por comas.")

class DialogoEstadistica(wx.Dialog):
	"""Diálogo para operaciones estadísticas."""
	def __init__(self, parent, operacion):
		super().__init__(parent, title=operacion, size=(500, 600))
		self.operacion = operacion

		vbox = wx.BoxSizer(wx.VERTICAL)

		# Crear los controles de entrada según la operación seleccionada
		if self.operacion in ['Media', 'Mediana', 'Moda', 'Varianza', 'Desviación Estándar', 'Cuartiles', 'Rango', 'Rango Intercuartil', 'Coeficiente de Asimetría', 'Curtosis']:
			lbl_datos = wx.StaticText(self, label="Ingrese los datos separados por comas:")
			self.txt_datos = wx.TextCtrl(self, style=wx.TE_MULTILINE)
			vbox.Add(lbl_datos, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_datos, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
		elif self.operacion == 'Percentil':
			lbl_datos = wx.StaticText(self, label="Ingrese los datos separados por comas:")
			self.txt_datos = wx.TextCtrl(self, style=wx.TE_MULTILINE)
			lbl_percentil = wx.StaticText(self, label="Ingrese el percentil (0-100):")
			self.txt_percentil = wx.TextCtrl(self)
			vbox.Add(lbl_datos, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_datos, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
			vbox.Add(lbl_percentil, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_percentil, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
		elif self.operacion in ['Covarianza', 'Coeficiente de Correlación', 'Regresión Lineal']:
			lbl_datos_x = wx.StaticText(self, label="Ingrese los datos de X separados por comas:")
			self.txt_datos_x = wx.TextCtrl(self, style=wx.TE_MULTILINE)
			lbl_datos_y = wx.StaticText(self, label="Ingrese los datos de Y separados por comas:")
			self.txt_datos_y = wx.TextCtrl(self, style=wx.TE_MULTILINE)
			vbox.Add(lbl_datos_x, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_datos_x, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
			vbox.Add(lbl_datos_y, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_datos_y, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
		elif self.operacion == 'Valor Z':
			lbl_x = wx.StaticText(self, label="Ingrese el valor X:")
			self.txt_x = wx.TextCtrl(self)
			lbl_media = wx.StaticText(self, label="Ingrese la media:")
			self.txt_media = wx.TextCtrl(self)
			lbl_desviacion = wx.StaticText(self, label="Ingrese la desviación estándar:")
			self.txt_desviacion = wx.TextCtrl(self)
			vbox.Add(lbl_x, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_x, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
			vbox.Add(lbl_media, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_media, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
			vbox.Add(lbl_desviacion, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_desviacion, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
		elif self.operacion == 'Probabilidad Normal Estándar':
			lbl_z = wx.StaticText(self, label="Ingrese el valor Z:")
			self.txt_z = wx.TextCtrl(self)
			vbox.Add(lbl_z, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_z, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
		else:
			mensaje = "Operación no soportada."
			wx.MessageBox(mensaje, "Error", wx.OK | wx.ICON_ERROR)
			self.Destroy()
			return

		# Campo para mostrar el resultado
		lbl_resultado = wx.StaticText(self, label="Resultado:")
		self.txt_resultado = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_MULTILINE)
		vbox.Add(lbl_resultado, flag=wx.LEFT | wx.TOP, border=10)
		vbox.Add(self.txt_resultado, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

		# Botones de acción
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		btn_calcular = wx.Button(self, label="&Calcular")
		btn_calcular.Bind(wx.EVT_BUTTON, self.calcular)
		btn_ayuda = wx.Button(self, label="&Ayuda")
		btn_ayuda.Bind(wx.EVT_BUTTON, self.mostrar_ayuda)
		btn_salir = wx.Button(self, label="&Salir")
		btn_salir.Bind(wx.EVT_BUTTON, self.salir)
		hbox.Add(btn_calcular, flag=wx.RIGHT, border=5)
		hbox.Add(btn_ayuda, flag=wx.RIGHT, border=5)
		hbox.Add(btn_salir)

		vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

		self.SetSizer(vbox)

	def calcular(self, event):
		"""Realiza el cálculo de la operación estadística seleccionada."""
		try:
			if self.operacion in ['Media', 'Mediana', 'Moda', 'Varianza', 'Desviación Estándar', 'Cuartiles', 'Rango', 'Rango Intercuartil', 'Coeficiente de Asimetría', 'Curtosis']:
				datos_str = self.txt_datos.GetValue()
				lista_datos = self.parsear_lista(datos_str)
				if self.operacion == 'Media':
					resultado = Estadistica.media(lista_datos)
				elif self.operacion == 'Mediana':
					resultado = Estadistica.mediana(lista_datos)
				elif self.operacion == 'Moda':
					resultado = Estadistica.moda(lista_datos)
				elif self.operacion == 'Varianza':
					resultado = Estadistica.varianza(lista_datos)
				elif self.operacion == 'Desviación Estándar':
					resultado = Estadistica.desviacion_estandar(lista_datos)
				elif self.operacion == 'Cuartiles':
					Q1, Q2, Q3 = Estadistica.cuartiles(lista_datos)
					resultado = f"Q1 = {Q1}\nQ2 (Mediana) = {Q2}\nQ3 = {Q3}"
				elif self.operacion == 'Rango':
					resultado = Estadistica.rango(lista_datos)
				elif self.operacion == 'Rango Intercuartil':
					resultado = Estadistica.rango_intercuartil(lista_datos)
				elif self.operacion == 'Coeficiente de Asimetría':
					resultado = Estadistica.coeficiente_asimetria(lista_datos)
				elif self.operacion == 'Curtosis':
					resultado = Estadistica.curtosis(lista_datos)
				self.txt_resultado.SetValue(str(resultado))
				self.txt_datos.SetValue("")
			elif self.operacion == 'Percentil':
				datos_str = self.txt_datos.GetValue()
				lista_datos = self.parsear_lista(datos_str)
				percentil = float(self.txt_percentil.GetValue())
				resultado = Estadistica.percentil(lista_datos, percentil)
				self.txt_resultado.SetValue(f"Percentil {percentil} = {resultado}")
				self.txt_datos.SetValue("")
				self.txt_percentil.SetValue("")
			elif self.operacion in ['Covarianza', 'Coeficiente de Correlación', 'Regresión Lineal']:
				datos_x_str = self.txt_datos_x.GetValue()
				datos_y_str = self.txt_datos_y.GetValue()
				lista_x = self.parsear_lista(datos_x_str)
				lista_y = self.parsear_lista(datos_y_str)
				if self.operacion == 'Covarianza':
					resultado = Estadistica.covarianza(lista_x, lista_y)
				elif self.operacion == 'Coeficiente de Correlación':
					resultado = Estadistica.coeficiente_correlacion(lista_x, lista_y)
				elif self.operacion == 'Regresión Lineal':
					pendiente, intercepto = Estadistica.regresion_lineal(lista_x, lista_y)
					resultado = f"Pendiente (m) = {pendiente}\nIntercepto (b) = {intercepto}"
				self.txt_resultado.SetValue(str(resultado))
				self.txt_datos_x.SetValue("")
				self.txt_datos_y.SetValue("")
			elif self.operacion == 'Valor Z':
				x = float(self.txt_x.GetValue())
				media = float(self.txt_media.GetValue())
				desviacion = float(self.txt_desviacion.GetValue())
				resultado = Estadistica.valor_z(x, media, desviacion)
				self.txt_resultado.SetValue(f"Valor Z = {resultado}")
				self.txt_x.SetValue("")
				self.txt_media.SetValue("")
				self.txt_desviacion.SetValue("")
			elif self.operacion == 'Probabilidad Normal Estándar':
				z = float(self.txt_z.GetValue())
				resultado = Estadistica.probabilidad_normal_estandar(z)
				self.txt_resultado.SetValue(f"Probabilidad acumulada hasta Z = {z} es {resultado}")
				self.txt_z.SetValue("")
			else:
				raise ValueError("Operación no soportada.")

			self.txt_resultado.SetFocus()

		except Exception as e:
			wx.MessageBox(f"Error: {e}", "Error", wx.OK | wx.ICON_ERROR)

	def parsear_lista(self, cadena):
		"""Convierte una cadena de texto en una lista de números."""
		try:
			return [float(item.strip()) for item in cadena.strip().split(',') if item.strip()]
		except Exception:
			raise ValueError("Formato incorrecto. Ingrese los datos separados por comas.")

	def mostrar_ayuda(self, event):
		"""Muestra la ayuda específica para la operación estadística seleccionada."""
		if self.operacion in ['Media', 'Mediana', 'Moda', 'Varianza', 'Desviación Estándar', 'Cuartiles', 'Rango', 'Rango Intercuartil', 'Coeficiente de Asimetría', 'Curtosis']:
			mensaje = "Ingrese una lista de números separados por comas para calcular la operación seleccionada."
		elif self.operacion == 'Percentil':
			mensaje = "Ingrese una lista de números separados por comas y el percentil que desea calcular (entre 0 y 100)."
		elif self.operacion in ['Covarianza', 'Coeficiente de Correlación', 'Regresión Lineal']:
			mensaje = "Ingrese dos listas de números separados por comas para X e Y, respectivamente."
		elif self.operacion == 'Valor Z':
			mensaje = "Ingrese el valor X, la media y la desviación estándar para calcular el valor Z."
		elif self.operacion == 'Probabilidad Normal Estándar':
			mensaje = "Ingrese el valor Z para calcular la probabilidad acumulada hasta ese punto en la distribución normal estándar."
		else:
			mensaje = "Operación no soportada."
		wx.MessageBox(mensaje, "Ayuda", wx.OK | wx.ICON_INFORMATION)

	def salir(self, event):
		"""Cierra el diálogo actual."""
		self.Destroy()


if __name__ == '__main__':
	app = wx.App()
	Calculadora()
	app.MainLoop()
