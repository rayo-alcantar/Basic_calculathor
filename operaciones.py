﻿# operaciones.py
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
		"""
		# Diccionario de masas atómicas (g/mol) para elementos comunes
		masas_atomicas = {
			'H': 1.008,
			'C': 12.011,
			'N': 14.007,
			'O': 15.999,
			'P': 30.974,
			'S': 32.06,
			'Cl': 35.45,
			# Agrega más elementos según sea necesario
		}
		import re
		# Expresión regular para analizar la fórmula química
		patron = r'([A-Z][a-z]?)(\d*)'
		componentes = re.findall(patron, compuesto)
		masa_molar = 0.0
		for (elemento, cantidad) in componentes:
			if elemento not in masas_atomicas:
				raise ValueError(f"Elemento '{elemento}' no reconocido.")
			cantidad = int(cantidad) if cantidad else 1
			masa_molar += masas_atomicas[elemento] * cantidad
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
			enlaces (dict): Diccionario con tipos de enlace y cantidad (e.g., {'C-H': 4, 'C=C': 1})
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
		return -math.log10(concentracion_hidrogeniones)

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
		Kc_productos = 1
		Kc_reactivos = 1
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
