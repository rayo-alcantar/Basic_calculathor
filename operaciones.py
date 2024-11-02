# operaciones.py
import math
import sympy as sp

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
		return sp.sympify(expresion).evalf(subs=variables)

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
