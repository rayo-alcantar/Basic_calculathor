import wx
import math
import sympy as sp

VERSION = 0.2
class Calculadora(wx.Frame):
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

		panel.SetSizer(vbox)
		self.Centre()
		self.Show()

	def crear_menu(self):
		menubar = wx.MenuBar()
		menu_opciones = wx.Menu()
		menu_acerca_de = menu_opciones.Append(wx.ID_ABOUT, "&Acerca de\tCtrl+A", "Información del desarrollador")
		self.Bind(wx.EVT_MENU, self.mostrar_acerca_de, menu_acerca_de)
		menubar.Append(menu_opciones, "&Opciones")
		self.SetMenuBar(menubar)

	def mostrar_acerca_de(self, event):
		info = ("Nombre del desarrollador: Ángel Alcántar\n"
				"Email: rayoalcantar@gmail.com")
		wx.MessageBox(info, "Acerca de", wx.OK | wx.ICON_INFORMATION)

	def mostrar_categorias(self, event):
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
		operaciones = ['Suma', 'Resta', 'Multiplicación', 'División', 'Raíz Cuadrada', 'Logaritmo', 'Porcentaje', 'Potencia', 'Expresión Matemática']
		dlg = wx.SingleChoiceDialog(self, 'Seleccione una operación:', 'Aritmética', operaciones)
		if dlg.ShowModal() == wx.ID_OK:
			operacion = dlg.GetStringSelection()
			self.realizar_operacion_aritmetica(operacion)
		dlg.Destroy()

	def realizar_operacion_aritmetica(self, operacion):
		dialogo = DialogoAritmetica(self, operacion)
		dialogo.ShowModal()
		dialogo.Destroy()

	def conversion_unidades(self):
		categorias = ['Ángulo', 'Capacidad', 'Frecuencia', 'Información', 'Longitud/Superficie', 'Temperatura', 'Tiempo', 'Velocidad']
		dlg = wx.SingleChoiceDialog(self, 'Seleccione una categoría de conversión:', 'Conversión de Unidades', categorias)
		if dlg.ShowModal() == wx.ID_OK:
			categoria = dlg.GetStringSelection()
			dialogo = DialogoConversion(self, categoria)
			dialogo.ShowModal()
			dialogo.Destroy()
		dlg.Destroy()

	def operaciones_trigonometricas(self):
		funciones = ['Seno', 'Coseno', 'Tangente', 'Arco Seno', 'Arco Coseno', 'Arco Tangente']
		dlg = wx.SingleChoiceDialog(self, 'Seleccione una función trigonométrica:', 'Trigonometría', funciones)
		if dlg.ShowModal() == wx.ID_OK:
			funcion = dlg.GetStringSelection()
			dialogo = DialogoTrigonometria(self, funcion)
			dialogo.ShowModal()
			dialogo.Destroy()
		dlg.Destroy()

	def cambio_bases(self):
		dialogo = DialogoCambioBases(self)
		dialogo.ShowModal()
		dialogo.Destroy()

	def operaciones_geometricas(self):
		figuras = ['Área de un Círculo', 'Perímetro de un Círculo', 'Área de un Triángulo', 'Perímetro de un Triángulo']
		dlg = wx.SingleChoiceDialog(self, 'Seleccione una operación geométrica:', 'Geometría', figuras)
		if dlg.ShowModal() == wx.ID_OK:
			figura = dlg.GetStringSelection()
			dialogo = DialogoGeometria(self, figura)
			dialogo.ShowModal()
			dialogo.Destroy()
		dlg.Destroy()
class DialogoAritmetica(wx.Dialog):
	def __init__(self, parent, operacion):
		super().__init__(parent, title=operacion, size=(350, 350))
		self.operacion = operacion

		vbox = wx.BoxSizer(wx.VERTICAL)

		# Ajustar los campos de entrada según la operación seleccionada
		if self.operacion in ['Suma', 'Resta', 'Multiplicación', 'División']:
			# Operaciones básicas que requieren dos números
			lbl_num1 = wx.StaticText(self, label="Primer número:")
			self.txt_entrada1 = wx.TextCtrl(self)
			lbl_num2 = wx.StaticText(self, label="Segundo número:")
			self.txt_entrada2 = wx.TextCtrl(self)
			vbox.Add(lbl_num1, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_entrada1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
			vbox.Add(lbl_num2, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_entrada2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

		elif self.operacion == 'Raíz Cuadrada':
			# Raíz cuadrada requiere un solo número
			lbl_num = wx.StaticText(self, label="Ingrese el número:")
			self.txt_num = wx.TextCtrl(self)
			vbox.Add(lbl_num, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_num, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

		elif self.operacion == 'Logaritmo':
			# Logaritmo requiere el número y opcionalmente la base
			lbl_num = wx.StaticText(self, label="Ingrese el número:")
			self.txt_num = wx.TextCtrl(self)
			lbl_base = wx.StaticText(self, label="Base (opcional, por defecto es e):")
			self.txt_base = wx.TextCtrl(self)
			vbox.Add(lbl_num, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_num, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
			vbox.Add(lbl_base, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_base, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

		elif self.operacion == 'Porcentaje':
			# Porcentaje requiere un valor total y el porcentaje a calcular
			lbl_total = wx.StaticText(self, label="Valor total:")
			self.txt_total = wx.TextCtrl(self)
			lbl_porcentaje = wx.StaticText(self, label="Porcentaje a calcular:")
			self.txt_porcentaje = wx.TextCtrl(self)
			vbox.Add(lbl_total, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_total, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
			vbox.Add(lbl_porcentaje, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_porcentaje, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

		elif self.operacion == 'Potencia':
			# Potencia requiere una base y un exponente
			lbl_base = wx.StaticText(self, label="Base:")
			self.txt_base = wx.TextCtrl(self)
			lbl_exponente = wx.StaticText(self, label="Exponente:")
			self.txt_exponente = wx.TextCtrl(self)
			vbox.Add(lbl_base, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_base, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
			vbox.Add(lbl_exponente, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_exponente, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

		elif self.operacion == 'Expresión Matemática':
			# Expresión matemática permite ingresar una expresión y definir variables
			lbl_expresion = wx.StaticText(self, label="Ingrese la expresión matemática (puede usar variables):")
			self.txt_expresion = wx.TextCtrl(self)
			lbl_variables = wx.StaticText(self, label="Defina los valores de las variables (ejemplo: x=2, y=3):")
			self.txt_variables = wx.TextCtrl(self)
			vbox.Add(lbl_expresion, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_expresion, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
			vbox.Add(lbl_variables, flag=wx.LEFT | wx.TOP, border=10)
			vbox.Add(self.txt_variables, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

		# Campo para mostrar el resultado
		lbl_resultado = wx.StaticText(self, label="Resultado:")
		self.txt_resultado = wx.TextCtrl(self, style=wx.TE_READONLY)
		vbox.Add(lbl_resultado, flag=wx.LEFT | wx.TOP, border=10)
		vbox.Add(self.txt_resultado, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

		# Botones de acción con atajos de teclado
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
		try:
			# Realizar la operación según la selección
			if self.operacion in ['Suma', 'Resta', 'Multiplicación', 'División']:
				num1 = float(self.txt_entrada1.GetValue())
				num2 = float(self.txt_entrada2.GetValue())
				if self.operacion == 'Suma':
					resultado = num1 + num2
				elif self.operacion == 'Resta':
					resultado = num1 - num2
				elif self.operacion == 'Multiplicación':
					resultado = num1 * num2
				elif self.operacion == 'División':
					if num2 != 0:
						resultado = num1 / num2
					else:
						raise ZeroDivisionError("No se puede dividir entre cero.")
			elif self.operacion == 'Raíz Cuadrada':
				num = float(self.txt_num.GetValue())
				if num >= 0:
					resultado = math.sqrt(num)
				else:
					raise ValueError("No se puede calcular la raíz cuadrada de un número negativo.")
			elif self.operacion == 'Logaritmo':
				num = float(self.txt_num.GetValue())
				base_str = self.txt_base.GetValue()
				if num > 0:
					if base_str:
						base = float(base_str)
						if base > 0 and base != 1:
							resultado = math.log(num, base)
						else:
							raise ValueError("La base del logaritmo debe ser un número positivo diferente de 1.")
					else:
						resultado = math.log(num)  # Logaritmo natural
				else:
					raise ValueError("El número debe ser positivo para calcular el logaritmo.")
			elif self.operacion == 'Porcentaje':
				total = float(self.txt_total.GetValue())
				porcentaje = float(self.txt_porcentaje.GetValue())
				resultado = (total * porcentaje) / 100
			elif self.operacion == 'Potencia':
				base = float(self.txt_base.GetValue())
				exponente = float(self.txt_exponente.GetValue())
				resultado = math.pow(base, exponente)
			elif self.operacion == 'Expresión Matemática':
				expresion = self.txt_expresion.GetValue()
				variables_str = self.txt_variables.GetValue()
				variables = {}
				if variables_str:
					for var in variables_str.split(','):
						key, value = var.strip().split('=')
						variables[key.strip()] = float(value.strip())
				resultado = sp.sympify(expresion).evalf(subs=variables)
			else:
				raise ValueError("Operación no soportada.")

			# Mostrar el resultado y enfocar el campo
			self.txt_resultado.SetValue(str(resultado))
			self.txt_resultado.SetFocus()

			# Limpiar los campos de entrada para nuevas operaciones
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
			# Manejo de excepciones y mostrar mensaje de error
			wx.MessageBox(f"Error: {e}", "Error", wx.OK | wx.ICON_ERROR)

	def mostrar_ayuda(self, event):
		# Mostrar ayuda específica para cada operación
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
		# Cerrar el diálogo
		self.Destroy()


class DialogoConversion(wx.Dialog):
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
		try:
			valor = float(self.txt_valor.GetValue())
			origen = self.cmb_origen.GetValue()
			destino = self.cmb_destino.GetValue()
			resultado = self.realizar_conversion(valor, origen, destino)
			self.txt_resultado.SetValue(str(resultado))
			self.txt_resultado.SetFocus()
			self.txt_valor.SetValue("")
		except Exception as e:
			wx.MessageBox(f"Error: {e}", "Error", wx.OK | wx.ICON_ERROR)

	def realizar_conversion(self, valor, origen, destino):
		if origen == destino:
			return valor
		if self.categoria == 'Temperatura':
			# Conversión de temperatura
			if origen == 'Celsius':
				if destino == 'Fahrenheit':
					return (valor * 9/5) + 32
				elif destino == 'Kelvin':
					return valor + 273.15
			elif origen == 'Fahrenheit':
				if destino == 'Celsius':
					return (valor - 32) * 5/9
				elif destino == 'Kelvin':
					return (valor - 32) * 5/9 + 273.15
			elif origen == 'Kelvin':
				if destino == 'Celsius':
					return valor - 273.15
				elif destino == 'Fahrenheit':
					return (valor - 273.15) * 9/5 + 32
			else:
				raise ValueError("Conversión no soportada.")
		elif self.categoria == 'Longitud/Superficie':
			# Conversión de longitud
			factor_conversion = {
				'Metros': 1,
				'Centímetros': 0.01,
				'Pulgadas': 0.0254,
				'Pies': 0.3048,
				'Kilómetros': 1000,
				'Millas': 1609.34
			}
			valor_metros = valor * factor_conversion[origen]
			return valor_metros / factor_conversion[destino]
		elif self.categoria == 'Capacidad':
			factor_conversion = {
				'Litros': 1,
				'Mililitros': 0.001,
				'Galones': 3.78541
			}
			valor_litros = valor * factor_conversion[origen]
			return valor_litros / factor_conversion[destino]
		elif self.categoria == 'Información':
			factor_conversion = {
				'Bytes': 1,
				'Kilobytes': 1024,
				'Megabytes': 1024**2,
				'Gigabytes': 1024**3,
				'Terabytes': 1024**4
			}
			valor_bytes = valor * factor_conversion[origen]
			return valor_bytes / factor_conversion[destino]
		elif self.categoria == 'Tiempo':
			factor_conversion = {
				'Segundos': 1,
				'Minutos': 60,
				'Horas': 3600,
				'Días': 86400
			}
			valor_segundos = valor * factor_conversion[origen]
			return valor_segundos / factor_conversion[destino]
		elif self.categoria == 'Velocidad':
			factor_conversion = {
				'm/s': 1,
				'km/h': 0.277778,
				'mph': 0.44704
			}
			valor_ms = valor * factor_conversion[origen]
			return valor_ms / factor_conversion[destino]
		elif self.categoria == 'Ángulo':
			if origen == 'Grados' and destino == 'Radianes':
				return math.radians(valor)
			elif origen == 'Radianes' and destino == 'Grados':
				return math.degrees(valor)
			else:
				raise ValueError("Conversión no soportada.")
		elif self.categoria == 'Frecuencia':
			factor_conversion = {
				'Hertz': 1,
				'Kilohertz': 1000,
				'Megahertz': 1e6,
				'Gigahertz': 1e9
			}
			valor_hz = valor * factor_conversion[origen]
			return valor_hz / factor_conversion[destino]
		else:
			raise ValueError("Conversión no implementada para esta categoría.")

	def mostrar_ayuda(self, event):
		mensaje = (f"Ingrese el valor y seleccione las unidades de origen y destino para convertir en la categoría {self.categoria}.\n"
				   "Por ejemplo, para convertir 100 centímetros a metros, seleccione 'Centímetros' como unidad de origen, 'Metros' como unidad de destino, y el valor 100.")
		wx.MessageBox(mensaje, "Ayuda", wx.OK | wx.ICON_INFORMATION)

	def salir(self, event):
		self.Destroy()

class DialogoTrigonometria(wx.Dialog):
	def __init__(self, parent, funcion):
		super().__init__(parent, title=f"Función {funcion}", size=(350, 250))
		self.funcion = funcion

		vbox = wx.BoxSizer(wx.VERTICAL)

		lbl_angulo = wx.StaticText(self, label="Ingrese el ángulo en grados:")
		self.txt_angulo = wx.TextCtrl(self)
		lbl_resultado = wx.StaticText(self, label="Resultado:")
		self.txt_resultado = wx.TextCtrl(self, style=wx.TE_READONLY)

		vbox.Add(lbl_angulo, flag=wx.LEFT|wx.TOP, border=10)
		vbox.Add(self.txt_angulo, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
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
		try:
			angulo_grados = float(self.txt_angulo.GetValue())
			angulo_radianes = math.radians(angulo_grados)
			if self.funcion == 'Seno':
				resultado = math.sin(angulo_radianes)
			elif self.funcion == 'Coseno':
				resultado = math.cos(angulo_radianes)
			elif self.funcion == 'Tangente':
				resultado = math.tan(angulo_radianes)
			elif self.funcion == 'Arco Seno':
				if -1 <= angulo_grados <= 1:
					resultado = math.degrees(math.asin(angulo_grados))
				else:
					raise ValueError("El valor debe estar entre -1 y 1.")
			elif self.funcion == 'Arco Coseno':
				if -1 <= angulo_grados <= 1:
					resultado = math.degrees(math.acos(angulo_grados))
				else:
					raise ValueError("El valor debe estar entre -1 y 1.")
			elif self.funcion == 'Arco Tangente':
				resultado = math.degrees(math.atan(angulo_grados))
			self.txt_resultado.SetValue(str(resultado))
			self.txt_resultado.SetFocus()
			self.txt_angulo.SetValue("")
		except Exception as e:
			wx.MessageBox(f"Error: {e}", "Error", wx.OK | wx.ICON_ERROR)

	def mostrar_ayuda(self, event):
		mensaje = f"Ingrese el ángulo en grados para calcular el {self.funcion.lower()}.\nPor ejemplo, para calcular el seno de 30 grados, ingrese 30."
		wx.MessageBox(mensaje, "Ayuda", wx.OK | wx.ICON_INFORMATION)

	def salir(self, event):
		self.Destroy()

class DialogoCambioBases(wx.Dialog):
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
		try:
			numero = self.txt_numero.GetValue()
			base_origen = int(self.cmb_origen.GetValue())
			base_destino = int(self.cmb_destino.GetValue())
			numero_decimal = int(numero, base_origen)
			if base_destino == 2:
				resultado = bin(numero_decimal)[2:]
			elif base_destino == 8:
				resultado = oct(numero_decimal)[2:]
			elif base_destino == 10:
				resultado = str(numero_decimal)
			elif base_destino == 16:
				resultado = hex(numero_decimal)[2:].upper()
			else:
				raise ValueError("Base de destino no soportada.")
			self.txt_resultado.SetValue(resultado)
			self.txt_resultado.SetFocus()
			self.txt_numero.SetValue("")
		except Exception as e:
			wx.MessageBox(f"Error: {e}", "Error", wx.OK | wx.ICON_ERROR)

	def mostrar_ayuda(self, event):
		mensaje = ("Ingrese el número y seleccione las bases de origen y destino para convertir.\n"
				   "Ejemplo: Convertir el número '1010' de base 2 (binario) a base 10 (decimal).")
		wx.MessageBox(mensaje, "Ayuda", wx.OK | wx.ICON_INFORMATION)

	def salir(self, event):
		self.Destroy()

class DialogoGeometria(wx.Dialog):
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
		try:
			if 'Círculo' in self.figura:
				radio = float(self.txt_radio.GetValue())
				if 'Área' in self.figura:
					resultado = math.pi * radio ** 2
				elif 'Perímetro' in self.figura:
					resultado = 2 * math.pi * radio
			elif 'Triángulo' in self.figura:
				base = float(self.txt_base.GetValue())
				altura = float(self.txt_altura.GetValue())
				if 'Área' in self.figura:
					resultado = (base * altura) / 2
				elif 'Perímetro' in self.figura:
					# Para un triángulo equilátero
					resultado = base * 3
			self.txt_resultado.SetValue(str(resultado))
			self.txt_resultado.SetFocus()
			if 'Círculo' in self.figura:
				self.txt_radio.SetValue("")
			elif 'Triángulo' in self.figura:
				self.txt_base.SetValue("")
				self.txt_altura.SetValue("")
		except Exception as e:
			wx.MessageBox(f"Error: {e}", "Error", wx.OK | wx.ICON_ERROR)

	def mostrar_ayuda(self, event):
		if 'Círculo' in self.figura:
			mensaje = f"Ingrese el radio del círculo para calcular el {self.figura.lower()}.\nEjemplo: Para un radio de 5 unidades."
		elif 'Triángulo' in self.figura:
			mensaje = f"Ingrese la base y la altura del triángulo para calcular el {self.figura.lower()}.\nEjemplo: Base = 4, Altura = 3."
		wx.MessageBox(mensaje, "Ayuda", wx.OK | wx.ICON_INFORMATION)

	def salir(self, event):
		self.Destroy()

if __name__ == '__main__':
	app = wx.App()
	Calculadora()
	app.MainLoop()
