# calc.py
import wx
import webbrowser
import sys
import requests
import sympy as sp
from packaging import version

import os
import threading
import math

from operaciones import Aritmetica, Conversion, Trigonometria, CambioBases, Geometria

VERSION = '0.3' 

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
					
					# Comparar versiones utilizando packaging.version
					if version.parse(ultima_version) > version.parse(VERSION):
						# Obtener la URL del primer asset de la release
						assets = data.get('assets', [])
						if assets:
							url_asset = assets[0]['browser_download_url']
							asset_name = assets[0]['name']
							wx.CallAfter(self.notificar_nueva_version, ultima_version, url_asset, asset_name)
						else:
							print("No hay assets disponibles para descargar en la última release.")
					else:
						# La versión disponible no es más reciente
						pass
				else:
					print("No se pudo comprobar si hay actualizaciones.")
			except Exception as e:
				print(f"Error al comprobar actualizaciones: {e}")
		threading.Thread(target=check_update).start()

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
		def download():
			try:
				respuesta = requests.get(url_asset, stream=True)
				if respuesta.status_code == 200:
					# Guardar el archivo descargado con su nombre original
					nombre_archivo = asset_name
					with open(nombre_archivo, 'wb') as archivo:
						for chunk in respuesta.iter_content(chunk_size=1024):
							if chunk:
								archivo.write(chunk)
					wx.CallAfter(self.informar_descarga_exitosa, nombre_archivo)
				else:
					wx.CallAfter(self.mostrar_error_descarga, "No se pudo descargar la actualización.")
			except Exception as e:
				wx.CallAfter(self.mostrar_error_descarga, f"Error al descargar la actualización: {e}")
		threading.Thread(target=download).start()

	def informar_descarga_exitosa(self, nombre_archivo):
		"""Informa al usuario que la descarga fue exitosa y cómo actualizar."""
		mensaje = (f"La nueva versión se ha descargado como '{nombre_archivo}'.\n\n"
				   "Para actualizar:\n"
				   "1. Cierre la aplicación actual.\n"
				   "2. Descomprima o ejecute el archivo descargado, según corresponda.\n"
				   "3. Siga las instrucciones de instalación proporcionadas.\n\n"
				   "Si está utilizando el ejecutable, extraiga el archivo y reemplace el archivo '.exe' con el nuevo.")
		wx.MessageBox(mensaje, "Descarga completada", wx.OK | wx.ICON_INFORMATION)
	
	def mostrar_error_descarga(self, mensaje_error):
		"""Muestra un mensaje de error si la descarga falla."""
		wx.MessageBox(mensaje_error, "Error de descarga", wx.OK | wx.ICON_ERROR)

	def crear_menu(self):
		"""Crea el menú de opciones."""
		menubar = wx.MenuBar()
		menu_opciones = wx.Menu()
		menu_acerca_de = menu_opciones.Append(wx.ID_ABOUT, "&Acerca de\tCtrl+A", "Información del desarrollador")
		self.Bind(wx.EVT_MENU, self.mostrar_acerca_de, menu_acerca_de)
		menubar.Append(menu_opciones, "&Opciones")
		self.SetMenuBar(menubar)

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
		info = ("programa simple para realizar una calculadora accesible con lector de pantalla. Nombre del desarrollador: Ángel Alcántar.\n"
				"Email: rayoalcantar@gmail.com.\nTodos los derechos reservados.")
		wx.MessageBox(info, "Acerca de", wx.OK | wx.ICON_INFORMATION)

	def mostrar_categorias(self, event):
		"""Muestra las categorías de operaciones disponibles."""
		categorias = ['Aritmética', 'Conversión de Unidades', 'Trigonometría', 'Cambio de Bases', 'Geometría']
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

if __name__ == '__main__':
	app = wx.App()
	Calculadora()
	app.MainLoop()
