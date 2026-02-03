"""
Tests unitarios para las operaciones matemáticas de la calculadora.
Ejecutar con: python -m pytest tests/ -v
O directamente: python tests/test_operaciones.py
"""

import sys
import os

# Añadir el directorio padre al path para importar operaciones
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from operaciones import Aritmetica, Conversion, Trigonometria, CambioBases, Geometria, Estadistica
import math


class TestAritmetica:
    """Tests para operaciones aritméticas básicas."""
    
    def test_suma(self):
        assert Aritmetica.suma(2, 3) == 5
        assert Aritmetica.suma(-1, 1) == 0
        assert Aritmetica.suma(0.5, 0.5) == 1.0
    
    def test_resta(self):
        assert Aritmetica.resta(5, 3) == 2
        assert Aritmetica.resta(0, 5) == -5
    
    def test_multiplicacion(self):
        assert Aritmetica.multiplicacion(3, 4) == 12
        assert Aritmetica.multiplicacion(-2, 3) == -6
        assert Aritmetica.multiplicacion(0, 100) == 0
    
    def test_division(self):
        assert Aritmetica.division(10, 2) == 5
        assert Aritmetica.division(7, 2) == 3.5
    
    def test_raiz_cuadrada(self):
        assert Aritmetica.raiz_cuadrada(4) == 2
        assert Aritmetica.raiz_cuadrada(9) == 3
        assert abs(Aritmetica.raiz_cuadrada(2) - 1.4142135623730951) < 0.0001
    
    def test_potencia(self):
        assert Aritmetica.potencia(2, 3) == 8
        assert Aritmetica.potencia(5, 0) == 1
        assert Aritmetica.potencia(2, -1) == 0.5
    
    def test_porcentaje(self):
        assert Aritmetica.porcentaje(100, 10) == 10
        assert Aritmetica.porcentaje(200, 50) == 100


class TestConversion:
    """Tests para conversión de unidades."""
    
    def test_convertir_temperatura_celsius_a_fahrenheit(self):
        resultado = Conversion.convertir(0, 'Celsius', 'Fahrenheit', 'Temperatura')
        assert resultado == 32
    
    def test_convertir_temperatura_fahrenheit_a_celsius(self):
        resultado = Conversion.convertir(32, 'Fahrenheit', 'Celsius', 'Temperatura')
        assert resultado == 0
    
    def test_convertir_longitud_metros_a_centimetros(self):
        resultado = Conversion.convertir(1, 'Metros', 'Centímetros', 'Longitud/Superficie')
        assert resultado == 100


class TestTrigonometria:
    """Tests para operaciones trigonométricas."""
    
    def test_seno(self):
        assert abs(Trigonometria.seno(30) - 0.5) < 0.0001
        assert abs(Trigonometria.seno(90) - 1) < 0.0001
        assert abs(Trigonometria.seno(0)) < 0.0001
    
    def test_coseno(self):
        assert abs(Trigonometria.coseno(0) - 1) < 0.0001
        assert abs(Trigonometria.coseno(60) - 0.5) < 0.0001
    
    def test_tangente(self):
        assert abs(Trigonometria.tangente(45) - 1) < 0.0001
    
    def test_decimal_a_dms(self):
        grados, minutos, segundos, texto = Trigonometria.decimal_a_dms(45.5125)
        assert grados == 45
        assert minutos == 30
        assert abs(segundos - 45) < 0.1
    
    def test_dms_a_decimal(self):
        resultado = Trigonometria.dms_a_decimal(45, 30, 45)
        assert abs(resultado - 45.5125) < 0.001


class TestCambioBases:
    """Tests para cambio de bases numéricas."""
    
    def test_binario_a_decimal(self):
        assert CambioBases.convertir_base('1010', 2, 10) == '10'
    
    def test_decimal_a_binario(self):
        assert CambioBases.convertir_base('10', 10, 2) == '1010'
    
    def test_decimal_a_hexadecimal(self):
        assert CambioBases.convertir_base('255', 10, 16).upper() == 'FF'


class TestGeometria:
    """Tests para cálculos geométricos."""
    
    def test_area_circulo(self):
        resultado = Geometria.area_circulo(1)
        assert abs(resultado - math.pi) < 0.0001
    
    def test_perimetro_circulo(self):
        resultado = Geometria.perimetro_circulo(1)
        assert abs(resultado - 2 * math.pi) < 0.0001
    
    def test_area_triangulo(self):
        assert Geometria.area_triangulo(4, 3) == 6


class TestEstadistica:
    """Tests para operaciones estadísticas."""
    
    def test_media(self):
        assert Estadistica.media([1, 2, 3, 4, 5]) == 3
    
    def test_mediana_impar(self):
        assert Estadistica.mediana([1, 2, 3, 4, 5]) == 3
    
    def test_mediana_par(self):
        assert Estadistica.mediana([1, 2, 3, 4]) == 2.5


def run_all_tests():
    """Ejecuta todos los tests y muestra resultados."""
    import traceback
    
    test_classes = [
        TestAritmetica,
        TestConversion,
        TestTrigonometria,
        TestCambioBases,
        TestGeometria,
        TestEstadistica
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    print("=" * 60)
    print("EJECUTANDO TESTS DE LA CALCULADORA BÁSICA v2.0.0")
    print("=" * 60)
    
    for test_class in test_classes:
        print(f"\n{test_class.__name__}:")
        instance = test_class()
        
        for method_name in dir(instance):
            if method_name.startswith('test_'):
                total_tests += 1
                try:
                    getattr(instance, method_name)()
                    print(f"  ✓ {method_name}")
                    passed_tests += 1
                except Exception as e:
                    print(f"  ✗ {method_name}: {e}")
                    failed_tests += 1
    
    print("\n" + "=" * 60)
    print(f"RESULTADOS: {passed_tests}/{total_tests} tests pasaron")
    if failed_tests > 0:
        print(f"FALLARON: {failed_tests} tests")
    else:
        print("¡TODOS LOS TESTS PASARON! ✓")
    print("=" * 60)
    
    return failed_tests == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
