# operaciones.py
import math
import re
from collections import Counter

class Aritmetica:
	"""Clase para operaciones aritméticas básicas."""
	@staticmethod
	def suma(num1, num2):
		return num1 + num2

	@staticmethod
	def resta(num1, num2):
		return num1 - num2

	@staticmethod
	def multiplicacion(num1, num2):
		return num1 * num2

	@staticmethod
	def division(num1, num2):
		if num2 == 0:
			raise ZeroDivisionError("No se puede dividir entre cero.")
		return num1 / num2

	@staticmethod
	def raiz_cuadrada(num):
		if num < 0:
			raise ValueError("No se puede calcular la raíz cuadrada de un número negativo.")
		return math.sqrt(num)

	@staticmethod
	def logaritmo(num, base=None):
		if num <= 0:
			raise ValueError("El número debe ser positivo para calcular el logaritmo.")
		if base is not None:
			if base <= 0 or base == 1:
				raise ValueError("La base del logaritmo debe ser un número positivo diferente de 1.")
			return math.log(num, base)
		else:
			return math.log(num)  # Logaritmo natural

	@staticmethod
	def porcentaje(total, porcentaje):
		return (total * porcentaje) / 100

	@staticmethod
	def potencia(base, exponente):
		return math.pow(base, exponente)

	@staticmethod
	def expresion_matematica(expresion, variables):
		# Evaluación de la expresión matemática utilizando eval en un entorno controlado.
		allowed_names = {}
		allowed_names.update(math.__dict__)
		allowed_names.update(variables)
		try:
			result = eval(expresion, {"__builtins__": None}, allowed_names)
		except Exception as e:
			raise ValueError("Expresión inválida: " + str(e))
		return result

class Conversion:
	"""Clase para conversiones de unidades."""
	@staticmethod
	def convertir(valor, origen, destino, categoria):
		if origen == destino:
			return valor
		if categoria == 'Temperatura':
			return Conversion._convertir_temperatura(valor, origen, destino)
		elif categoria == 'Longitud/Superficie':
			return Conversion._convertir_longitud(valor, origen, destino)
		elif categoria == 'Capacidad':
			return Conversion._convertir_capacidad(valor, origen, destino)
		elif categoria == 'Información':
			return Conversion._convertir_informacion(valor, origen, destino)
		elif categoria == 'Tiempo':
			return Conversion._convertir_tiempo(valor, origen, destino)
		elif categoria == 'Velocidad':
			return Conversion._convertir_velocidad(valor, origen, destino)
		elif categoria == 'Ángulo':
			return Conversion._convertir_angulo(valor, origen, destino)
		elif categoria == 'Frecuencia':
			return Conversion._convertir_frecuencia(valor, origen, destino)
		else:
			raise ValueError("Conversión no implementada para esta categoría.")

	@staticmethod
	def _convertir_temperatura(valor, origen, destino):
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

	@staticmethod
	def _convertir_longitud(valor, origen, destino):
		factor_conversion = {
			'Metros': 1,
			'Centímetros': 0.01,
			'Pulgadas': 0.0254,
			'Pies': 0.3048,
			'Kilómetros': 1000,
			'Millas': 1609.34
		}
		if origen not in factor_conversion or destino not in factor_conversion:
			raise ValueError("Unidad de origen o destino no soportada.")
		valor_metros = valor * factor_conversion[origen]
		return valor_metros / factor_conversion[destino]

	@staticmethod
	def _convertir_capacidad(valor, origen, destino):
		factor_conversion = {
			'Litros': 1,
			'Mililitros': 0.001,
			'Galones': 3.78541
		}
		if origen not in factor_conversion or destino not in factor_conversion:
			raise ValueError("Unidad de origen o destino no soportada.")
		valor_litros = valor * factor_conversion[origen]
		return valor_litros / factor_conversion[destino]

	@staticmethod
	def _convertir_informacion(valor, origen, destino):
		factor_conversion = {
			'Bytes': 1,
			'Kilobytes': 1024,
			'Megabytes': 1024**2,
			'Gigabytes': 1024**3,
			'Terabytes': 1024**4
		}
		if origen not in factor_conversion or destino not in factor_conversion:
			raise ValueError("Unidad de origen o destino no soportada.")
		valor_bytes = valor * factor_conversion[origen]
		return valor_bytes / factor_conversion[destino]

	@staticmethod
	def _convertir_tiempo(valor, origen, destino):
		factor_conversion = {
			'Segundos': 1,
			'Minutos': 60,
			'Horas': 3600,
			'Días': 86400
		}
		if origen not in factor_conversion or destino not in factor_conversion:
			raise ValueError("Unidad de origen o destino no soportada.")
		valor_segundos = valor * factor_conversion[origen]
		return valor_segundos / factor_conversion[destino]

	@staticmethod
	def _convertir_velocidad(valor, origen, destino):
		factor_conversion = {
			'm/s': 1,
			'km/h': 0.277778,
			'mph': 0.44704
		}
		if origen not in factor_conversion or destino not in factor_conversion:
			raise ValueError("Unidad de origen o destino no soportada.")
		valor_ms = valor * factor_conversion[origen]
		return valor_ms / factor_conversion[destino]

	@staticmethod
	def _convertir_angulo(valor, origen, destino):
		if origen == 'Grados' and destino == 'Radianes':
			return math.radians(valor)
		elif origen == 'Radianes' and destino == 'Grados':
			return math.degrees(valor)
		else:
			raise ValueError("Conversión no soportada.")

	@staticmethod
	def _convertir_frecuencia(valor, origen, destino):
		factor_conversion = {
			'Hertz': 1,
			'Kilohertz': 1000,
			'Megahertz': 1e6,
			'Gigahertz': 1e9
		}
		if origen not in factor_conversion or destino not in factor_conversion:
			raise ValueError("Unidad de origen o destino no soportada.")
		valor_hz = valor * factor_conversion[origen]
		return valor_hz / factor_conversion[destino]

class Trigonometria:
	"""Clase para operaciones trigonométricas."""
	@staticmethod
	def seno(angulo_grados):
		angulo_radianes = math.radians(angulo_grados)
		return math.sin(angulo_radianes)

	@staticmethod
	def coseno(angulo_grados):
		angulo_radianes = math.radians(angulo_grados)
		return math.cos(angulo_radianes)

	@staticmethod
	def tangente(angulo_grados):
		angulo_radianes = math.radians(angulo_grados)
		return math.tan(angulo_radianes)

	@staticmethod
	def arco_seno(valor):
		if -1 <= valor <= 1:
			return math.degrees(math.asin(valor))
		else:
			raise ValueError("El valor debe estar entre -1 y 1.")

	@staticmethod
	def arco_coseno(valor):
		if -1 <= valor <= 1:
			return math.degrees(math.acos(valor))
		else:
			raise ValueError("El valor debe estar entre -1 y 1.")

	@staticmethod
	def arco_tangente(valor):
		return math.degrees(math.atan(valor))

	@staticmethod
	def decimal_a_dms(grados_decimales):
		"""
		Convierte grados decimales a formato sexagesimal (grados, minutos, segundos).
		
		Ejemplo: 45.5125° → 45° 30' 45"
		
		Parámetros:
			grados_decimales (float): El ángulo en grados decimales.
		
		Retorna:
			tuple: (grados, minutos, segundos) como enteros/float
			str: Representación legible "G° M' S\""
		"""
		negativo = grados_decimales < 0
		grados_decimales = abs(grados_decimales)
		
		grados = int(grados_decimales)
		resto_minutos = (grados_decimales - grados) * 60
		minutos = int(resto_minutos)
		segundos = (resto_minutos - minutos) * 60
		
		if negativo:
			grados = -grados
		
		# Retornar tanto la tupla como el string formateado
		return (grados, minutos, round(segundos, 2), f"{grados}° {minutos}' {round(segundos, 2)}\"")

	@staticmethod
	def dms_a_decimal(grados, minutos, segundos):
		"""
		Convierte formato sexagesimal (grados, minutos, segundos) a grados decimales.
		
		Ejemplo: 45° 30' 45" → 45.5125°
		
		Parámetros:
			grados (int): Los grados.
			minutos (int): Los minutos (0-59).
			segundos (float): Los segundos (0-59.99).
		
		Retorna:
			float: El ángulo en grados decimales.
		"""
		if minutos < 0 or minutos >= 60:
			raise ValueError("Los minutos deben estar entre 0 y 59.")
		if segundos < 0 or segundos >= 60:
			raise ValueError("Los segundos deben estar entre 0 y 59.99.")
		
		negativo = grados < 0
		grados = abs(grados)
		
		decimal = grados + (minutos / 60) + (segundos / 3600)
		
		if negativo:
			decimal = -decimal
		
		return decimal

class CambioBases:
	"""Clase para cambio de bases numéricas."""
	@staticmethod
	def convertir_base(numero, base_origen, base_destino):
		numero_decimal = int(numero, base_origen)
		if base_destino == 2:
			return bin(numero_decimal)[2:]
		elif base_destino == 8:
			return oct(numero_decimal)[2:]
		elif base_destino == 10:
			return str(numero_decimal)
		elif base_destino == 16:
			return hex(numero_decimal)[2:].upper()
		else:
			raise ValueError("Base de destino no soportada.")

class Geometria:
	"""Clase para cálculos geométricos."""
	@staticmethod
	def area_circulo(radio):
		return math.pi * radio ** 2

	@staticmethod
	def perimetro_circulo(radio):
		return 2 * math.pi * radio

	@staticmethod
	def area_triangulo(base, altura):
		return (base * altura) / 2

	@staticmethod
	def perimetro_triangulo(lado1, lado2, lado3):
		return lado1 + lado2 + lado3

class Quimica:
	"""Clase para operaciones químicas, enfocada en química orgánica y enlaces covalentes."""

	@staticmethod
	def calcular_masa_molar(compuesto):
		"""
		Calcula la masa molar de un compuesto dado su fórmula química.

		Parámetros:
			compuesto (str): Fórmula química del compuesto (por ejemplo, 'H2O', 'C6H12O6')

		Retorna:
			float: Masa molar en gramos/mol

		Nota:
			Se utiliza una expresión regular para identificar correctamente elementos de una o dos letras.
		"""
		# Diccionario ampliado de masas atómicas (g/mol) para elementos comunes
		masas_atomicas = {
			'H': 1.008,
			'He': 4.0026,
			'Li': 6.94,
			'Be': 9.0122,
			'B': 10.81,
			'C': 12.011,
			'N': 14.007,
			'O': 15.999,
			'F': 18.998,
			'Ne': 20.180,
			'Na': 22.990,
			'Mg': 24.305,
			'Al': 26.982,
			'Si': 28.085,
			'P': 30.974,
			'S': 32.06,
			'Cl': 35.45,
			'Ar': 39.948,
			'K': 39.098,
			'Ca': 40.078,
			'Fe': 55.845,
			# Se pueden agregar más elementos según se requiera
		}
		
		# Expresión regular para analizar la fórmula química: un elemento comienza con letra mayúscula, 
		# puede ir seguido de una minúscula opcional, y un número opcional que indica la cantidad.
		patron = r'([A-Z][a-z]?)(\d*)'
		componentes = re.findall(patron, compuesto)
		masa_molar = 0.0
		
		for (elemento, cantidad) in componentes:
			if elemento not in masas_atomicas:
				raise ValueError(f"Elemento '{elemento}' no reconocido.")
			cantidad_valor = int(cantidad) if cantidad else 1
			masa_molar += masas_atomicas[elemento] * cantidad_valor
		
		return masa_molar

	@staticmethod
	def convertir_masa_a_moles(masa, masa_molar):
		"""
		Convierte una masa en gramos a moles utilizando la masa molar.

		Parámetros:
			masa (float): Masa en gramos.
			masa_molar (float): Masa molar del compuesto en gramos/mol.

		Retorna:
			float: Cantidad de moles.
		"""
		if masa_molar <= 0:
			raise ValueError("La masa molar debe ser positiva.")
		return masa / masa_molar

	@staticmethod
	def calcular_numero_particulas(moles):
		"""
		Calcula el número de partículas a partir de moles usando el número de Avogadro.

		Parámetros:
			moles (float): Cantidad de moles.

		Retorna:
			float: Número de partículas.
		"""
		NA = 6.02214076e23  # Número de Avogadro
		return moles * NA

	@staticmethod
	def energia_enlace(enlaces, energias_enlace):
		"""
		Calcula la energía total de enlaces en una molécula.

		Parámetros:
			enlaces (dict): Diccionario con tipos de enlace y cantidad 
							(por ejemplo, {'C-H': 4, 'C=C': 1})
			energias_enlace (dict): Energías de enlace para cada tipo en kJ/mol

		Retorna:
			float: Energía total en kJ/mol
		"""
		energia_total = 0.0
		for enlace, cantidad in enlaces.items():
			if enlace not in energias_enlace:
				raise ValueError(f"Energía de enlace para '{enlace}' no disponible.")
			energia_total += energias_enlace[enlace] * cantidad
		return energia_total

	@staticmethod
	def calcular_concentracion_molar(n_moles, volumen_litros):
		"""
		Calcula la concentración molar de una solución.

		Parámetros:
			n_moles (float): Número de moles del soluto.
			volumen_litros (float): Volumen de la solución en litros.

		Retorna:
			float: Concentración en mol/L.
		"""
		if volumen_litros <= 0:
			raise ValueError("El volumen debe ser positivo.")
		return n_moles / volumen_litros

	@staticmethod
	def calcular_pH(concentracion_hidrogeniones):
		"""
		Calcula el pH de una solución dada la concentración de iones H+.

		Parámetros:
			concentracion_hidrogeniones (float): Concentración de H+ en mol/L.

		Retorna:
			float: Valor de pH.
		"""
		if concentracion_hidrogeniones <= 0:
			raise ValueError("La concentración debe ser positiva.")
		pH = -math.log10(concentracion_hidrogeniones)
		return pH

	@staticmethod
	def ley_gases_ideales(P=None, V=None, n=None, T=None):
		"""
		Calcula una variable desconocida usando la ley de los gases ideales PV = nRT.
		Proporcione tres de las cuatro variables; la cuarta será calculada.

		Parámetros:
			P (float): Presión en atmósferas.
			V (float): Volumen en litros.
			n (float): Número de moles.
			T (float): Temperatura en Kelvin.

		Retorna:
			float: Valor de la variable desconocida.
		"""
		R = 0.082057  # Constante de los gases ideales en L·atm/(mol·K)
		variables = {'P': P, 'V': V, 'n': n, 'T': T}
		variables_proporcionadas = {k: v for k, v in variables.items() if v is not None}
		
		if len(variables_proporcionadas) != 3:
			raise ValueError("Proporcione exactamente tres variables.")
		
		if P is None:
			return (n * R * T) / V
		elif V is None:
			return (n * R * T) / P
		elif n is None:
			return (P * V) / (R * T)
		elif T is None:
			return (P * V) / (n * R)
		else:
			raise ValueError("Una variable debe ser desconocida (None).")

	@staticmethod
	def calcular_constante_equilibrio(productos, reactivos):
		"""
		Calcula la constante de equilibrio Kc para una reacción química.

		Parámetros:
			productos (dict): Concentraciones molares de los productos {compuesto: concentración}.
			reactivos (dict): Concentraciones molares de los reactivos {compuesto: concentración}.

		Retorna:
			float: Constante de equilibrio Kc.
		"""
		Kc_productos = 1.0
		Kc_reactivos = 1.0
		for conc in productos.values():
			Kc_productos *= conc
		for conc in reactivos.values():
			Kc_reactivos *= conc
		
		if Kc_reactivos == 0:
			raise ValueError("La concentración de reactivos no puede ser cero.")
		
		return Kc_productos / Kc_reactivos

	@staticmethod
	def calcular_rendimiento_porcentual(rendimiento_real, rendimiento_teorico):
		"""
		Calcula el rendimiento porcentual de una reacción química.

		Parámetros:
			rendimiento_real (float): Cantidad obtenida experimentalmente.
			rendimiento_teorico (float): Cantidad teórica esperada.

		Retorna:
			float: Rendimiento porcentual.
		"""
		if rendimiento_teorico == 0:
			raise ValueError("El rendimiento teórico no puede ser cero.")
		return (rendimiento_real / rendimiento_teorico) * 100

class Estadistica:
	"""Clase para operaciones estadísticas básicas y avanzadas."""

	@staticmethod
	def media(lista):
		"""Calcula la media aritmética de una lista de números."""
		if not lista:
			raise ValueError("La lista no puede estar vacía.")
		return sum(lista) / len(lista)

	@staticmethod
	def mediana(lista):
		"""Calcula la mediana de una lista de números."""
		if not lista:
			raise ValueError("La lista no puede estar vacía.")
		n = len(lista)
		lista_ordenada = sorted(lista)
		mitad = n // 2
		if n % 2 == 0:
			mediana = (lista_ordenada[mitad - 1] + lista_ordenada[mitad]) / 2.0
		else:
			mediana = lista_ordenada[mitad]
		return mediana

	@staticmethod
	def moda(lista):
		"""Calcula la moda de una lista de números."""
		if not lista:
			raise ValueError("La lista no puede estar vacía.")
		frecuencias = Counter(lista)
		max_freq = max(frecuencias.values())
		modas = [key for key, freq in frecuencias.items() if freq == max_freq]
		return modas

	@staticmethod
	def varianza(lista, poblacional=False):
		"""Calcula la varianza de una lista de números."""
		if not lista:
			raise ValueError("La lista no puede estar vacía.")
		n = len(lista)
		if n < 2 and not poblacional:
			raise ValueError("La varianza muestral requiere al menos dos datos.")
		media_val = Estadistica.media(lista)
		suma_cuadrados = sum((x - media_val) ** 2 for x in lista)
		if poblacional:
			return suma_cuadrados / n
		else:
			return suma_cuadrados / (n - 1)

	@staticmethod
	def desviacion_estandar(lista, poblacional=False):
		"""Calcula la desviación estándar de una lista de números."""
		var = Estadistica.varianza(lista, poblacional)
		return math.sqrt(var)

	@staticmethod
	def percentil(lista, percentil):
		"""Calcula el percentil de una lista de números."""
		if not lista:
			raise ValueError("La lista no puede estar vacía.")
		if not 0 <= percentil <= 100:
			raise ValueError("El percentil debe estar entre 0 y 100.")
		lista_ordenada = sorted(lista)
		k = (len(lista) - 1) * (percentil / 100.0)
		f = math.floor(k)
		c = math.ceil(k)
		if f == c:
			return lista_ordenada[int(k)]
		d0 = lista_ordenada[int(f)] * (c - k)
		d1 = lista_ordenada[int(c)] * (k - f)
		return d0 + d1

	@staticmethod
	def cuartiles(lista):
		"""Calcula los cuartiles de una lista de números."""
		Q1 = Estadistica.percentil(lista, 25)
		Q2 = Estadistica.percentil(lista, 50)  # Mediana
		Q3 = Estadistica.percentil(lista, 75)
		return (Q1, Q2, Q3)

	@staticmethod
	def rango(lista):
		"""Calcula el rango de una lista de números."""
		if not lista:
			raise ValueError("La lista no puede estar vacía.")
		return max(lista) - min(lista)

	@staticmethod
	def rango_intercuartil(lista):
		"""Calcula el rango intercuartil (IQR) de una lista de números."""
		Q1, _, Q3 = Estadistica.cuartiles(lista)
		return Q3 - Q1

	@staticmethod
	def coeficiente_asimetria(lista):
		"""Calcula el coeficiente de asimetría (skewness) de una lista de números."""
		if not lista:
			raise ValueError("La lista no puede estar vacía.")
		n = len(lista)
		if n < 3:
			raise ValueError("Se requieren al menos tres datos para calcular el coeficiente de asimetría.")
		media_val = Estadistica.media(lista)
		desviacion = Estadistica.desviacion_estandar(lista, poblacional=True)
		suma_cubos = sum((x - media_val) ** 3 for x in lista)
		skewness = (n / ((n - 1) * (n - 2))) * (suma_cubos / (desviacion ** 3))
		return skewness

	@staticmethod
	def curtosis(lista):
		"""Calcula la curtosis (kurtosis) de una lista de números."""
		if not lista:
			raise ValueError("La lista no puede estar vacía.")
		n = len(lista)
		if n < 4:
			raise ValueError("Se requieren al menos cuatro datos para calcular la curtosis.")
		media_val = Estadistica.media(lista)
		desviacion = Estadistica.desviacion_estandar(lista, poblacional=True)
		suma_cuartos = sum((x - media_val) ** 4 for x in lista)
		kurtosis = ((n * (n + 1)) / ((n - 1) * (n - 2) * (n - 3))) * (suma_cuartos / (desviacion ** 4))
		kurtosis -= (3 * (n - 1) ** 2) / ((n - 2) * (n - 3))
		return kurtosis

	@staticmethod
	def covarianza(lista_x, lista_y):
		"""Calcula la covarianza entre dos listas de números."""
		if not lista_x or not lista_y:
			raise ValueError("Las listas no pueden estar vacías.")
		if len(lista_x) != len(lista_y):
			raise ValueError("Las listas deben tener la misma longitud.")
		n = len(lista_x)
		media_x = Estadistica.media(lista_x)
		media_y = Estadistica.media(lista_y)
		suma_producto = sum((x - media_x) * (y - media_y) for x, y in zip(lista_x, lista_y))
		return suma_producto / (n - 1)

	@staticmethod
	def coeficiente_correlacion(lista_x, lista_y):
		"""Calcula el coeficiente de correlación de Pearson entre dos listas de números."""
		cov = Estadistica.covarianza(lista_x, lista_y)
		desviacion_x = Estadistica.desviacion_estandar(lista_x)
		desviacion_y = Estadistica.desviacion_estandar(lista_y)
		if desviacion_x == 0 or desviacion_y == 0:
			raise ValueError("La desviación estándar no puede ser cero.")
		return cov / (desviacion_x * desviacion_y)

	@staticmethod
	def regresion_lineal(lista_x, lista_y):
		"""Calcula los coeficientes de la regresión lineal (pendiente y ordenada al origen)."""
		if not lista_x or not lista_y:
			raise ValueError("Las listas no pueden estar vacías.")
		if len(lista_x) != len(lista_y):
			raise ValueError("Las listas deben tener la misma longitud.")
		n = len(lista_x)
		media_x = Estadistica.media(lista_x)
		media_y = Estadistica.media(lista_y)
		sum_xy = sum(x * y for x, y in zip(lista_x, lista_y))
		sum_xx = sum(x ** 2 for x in lista_x)
		pendiente = (sum_xy - n * media_x * media_y) / (sum_xx - n * media_x ** 2)
		intercepto = media_y - pendiente * media_x
		return pendiente, intercepto

	@staticmethod
	def valor_z(x, media, desviacion_estandar):
		"""Calcula el valor Z (estandarización) de un valor X."""
		if desviacion_estandar == 0:
			raise ValueError("La desviación estándar no puede ser cero.")
		return (x - media) / desviacion_estandar

	@staticmethod
	def probabilidad_normal_estandar(z):
		"""Calcula la probabilidad acumulada hasta un valor Z en la distribución normal estándar."""
		return 0.5 * (1 + math.erf(z / math.sqrt(2)))
