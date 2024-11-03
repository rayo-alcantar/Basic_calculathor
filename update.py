import argparse
import os
import subprocess
import sys
import shutil
import zipfile
import traceback
import time
import ctypes

def is_admin():
	"""Verifica si el script se está ejecutando con privilegios de administrador."""
	try:
		return ctypes.windll.shell32.IsUserAnAdmin()
	except:
		return False

def is_file_in_use(filepath):
	"""Verifica si un archivo está en uso."""
	try:
		os.rename(filepath, filepath)  # Intentar renombrar el archivo a sí mismo
		return False
	except:
		return True

def main():
	if not is_admin():
		# Si no tiene privilegios de administrador, se reinicia solicitándolos
		try:
			script = sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]
			params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
			ctypes.windll.shell32.ShellExecuteW(None, "runas", script, params, None, 1)
		except Exception as e:
			log_error(f'Error al solicitar privilegios de administrador: {e}')
		sys.exit(0)
	else:
		# Código principal del actualizador
		try:
			parser = argparse.ArgumentParser(description='Actualiza la aplicación Calculadora.')
			parser.add_argument('zip_filename', help='Nombre del archivo zip descargado')
			parser.add_argument('zip_path', help='Ruta donde se encuentra el archivo zip')
	
			args = parser.parse_args()
			zip_filename = args.zip_filename
			zip_path = args.zip_path
	
			# Ruta al directorio actual
			if getattr(sys, 'frozen', False):
				# Si la aplicación está empaquetada
				current_dir = os.path.dirname(sys.executable)
			else:
				# Si se ejecuta desde el script
				current_dir = os.path.dirname(os.path.abspath(__file__))
	
			log_message(f'current_dir: {current_dir}')
	
			# Ruta al archivo zip
			zip_full_path = os.path.join(zip_path, zip_filename)
			log_message(f'zip_full_path: {zip_full_path}')
	
			if not os.path.exists(zip_full_path):
				log_error(f'Error: El archivo zip {zip_full_path} no existe.')
				sys.exit(1)
	
			# Crear un directorio temporal para la extracción
			temp_extract_dir = os.path.join(current_dir, 'temp_update')
			log_message(f'temp_extract_dir: {temp_extract_dir}')
	
			if not os.path.exists(temp_extract_dir):
				os.makedirs(temp_extract_dir)
	
			# Esperar un momento para asegurarse de que los archivos no estén en uso
			time.sleep(2)
	
			# Extraer el archivo zip usando el módulo zipfile
			log_message('Extrayendo el archivo zip...')
			with zipfile.ZipFile(zip_full_path, 'r') as zip_ref:
				zip_ref.extractall(temp_extract_dir)
	
			# Esperar hasta que el ejecutable principal no esté en uso
			main_executable = os.path.join(current_dir, os.path.basename(sys.executable))
			wait_time = 0
			max_wait = 30  # Tiempo máximo de espera en segundos
			while is_file_in_use(main_executable):
				if wait_time >= max_wait:
					log_error(f'El archivo {main_executable} está en uso después de esperar {max_wait} segundos.')
					sys.exit(1)
				log_message(f'Esperando que {main_executable} esté disponible...')
				time.sleep(1)
				wait_time += 1
	
			# Copiar los archivos extraídos al directorio actual, reemplazando los existentes
			log_message('Actualizando archivos...')
			for item in os.listdir(temp_extract_dir):
				s = os.path.join(temp_extract_dir, item)
				d = os.path.join(current_dir, item)
				log_message(f'Copiando {s} a {d}')
				if os.path.isdir(s):
					# Copiar directorios recursivamente
					if os.path.exists(d):
						shutil.rmtree(d)
					shutil.copytree(s, d)
				else:
					# Copiar archivos individuales
					if os.path.exists(d):
						os.remove(d)
					shutil.copy2(s, d)
	
			# Limpiar archivos temporales
			shutil.rmtree(temp_extract_dir)
			os.remove(zip_full_path)
	
			# Reiniciar la aplicación
			log_message('Reiniciando la aplicación...')
			if getattr(sys, 'frozen', False):
				calc_exe = os.path.join(current_dir, os.path.basename(sys.executable))
			else:
				calc_exe = os.path.join(current_dir, 'calc.py')
	
			log_message(f'Ejecutando {calc_exe}')
			subprocess.Popen([calc_exe], shell=False)
	
			sys.exit(0)
		except Exception as e:
			log_error(f'Error durante la actualización: {e}')
			traceback_str = traceback.format_exc()
			log_error(traceback_str)
			sys.exit(1)

def log_message(message):
	with open('update.log', 'a', encoding='utf-8') as log_file:
		log_file.write(f'{message}\n')

def log_error(error_message):
	with open('update.log', 'a', encoding='utf-8') as log_file:
		log_file.write(f'ERROR: {error_message}\n')

if __name__ == '__main__':
	main()
# update.py
import argparse
import os
import subprocess
import sys
import shutil
import zipfile
import traceback
import time
import ctypes

def is_admin():
	"""Verifica si el script se está ejecutando con privilegios de administrador."""
	try:
		return ctypes.windll.shell32.IsUserAnAdmin()
	except:
		return False

def main():
	if not is_admin():
		# Si no tiene privilegios de administrador, se reinicia solicitándolos
		try:
			script = sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]
			params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
			ctypes.windll.shell32.ShellExecuteW(None, "runas", script, params, None, 1)
		except Exception as e:
			log_error(f'Error al solicitar privilegios de administrador: {e}')
		sys.exit(0)
	else:
		# Código principal del actualizador
		try:
			parser = argparse.ArgumentParser(description='Actualiza la aplicación Calculadora.')
			parser.add_argument('zip_filename', help='Nombre del archivo zip descargado')
			parser.add_argument('zip_path', help='Ruta donde se encuentra el archivo zip')
	
			args = parser.parse_args()
			zip_filename = args.zip_filename
			zip_path = args.zip_path
	
			# Ruta al directorio actual
			if getattr(sys, 'frozen', False):
				# Si la aplicación está empaquetada
				current_dir = os.path.dirname(sys.executable)
			else:
				# Si se ejecuta desde el script
				current_dir = os.path.dirname(os.path.abspath(__file__))
	
			log_message(f'current_dir: {current_dir}')
	
			# Ruta al archivo zip
			zip_full_path = os.path.join(zip_path, zip_filename)
			log_message(f'zip_full_path: {zip_full_path}')
	
			if not os.path.exists(zip_full_path):
				log_error(f'Error: El archivo zip {zip_full_path} no existe.')
				sys.exit(1)
	
			# Crear un directorio temporal para la extracción
			temp_extract_dir = os.path.join(current_dir, 'temp_update')
			log_message(f'temp_extract_dir: {temp_extract_dir}')
	
			if not os.path.exists(temp_extract_dir):
				os.makedirs(temp_extract_dir)
	
			# Esperar un momento para asegurarse de que los archivos no estén en uso
			time.sleep(2)
	
			# Extraer el archivo zip usando el módulo zipfile
			log_message('Extrayendo el archivo zip...')
			with zipfile.ZipFile(zip_full_path, 'r') as zip_ref:
				zip_ref.extractall(temp_extract_dir)
	
			# Copiar los archivos extraídos al directorio actual, reemplazando los existentes
			log_message('Actualizando archivos...')
			for item in os.listdir(temp_extract_dir):
				s = os.path.join(temp_extract_dir, item)
				d = os.path.join(current_dir, item)
				log_message(f'Copiando {s} a {d}')
				if os.path.isdir(s):
					# Copiar directorios recursivamente
					if os.path.exists(d):
						shutil.rmtree(d)
					shutil.copytree(s, d)
				else:
					# Copiar archivos individuales
					if os.path.exists(d):
						os.remove(d)
					shutil.copy2(s, d)
	
			# Limpiar archivos temporales
			shutil.rmtree(temp_extract_dir)
			os.remove(zip_full_path)
	
			# Reiniciar la aplicación
			log_message('Reiniciando la aplicación...')
			if getattr(sys, 'frozen', False):
				calc_exe = os.path.join(current_dir, os.path.basename(sys.executable))
			else:
				calc_exe = os.path.join(current_dir, 'calc.py')
	
			log_message(f'Ejecutando {calc_exe}')
			subprocess.Popen([calc_exe], shell=False)
	
			sys.exit(0)
		except Exception as e:
			log_error(f'Error durante la actualización: {e}')
			traceback_str = traceback.format_exc()
			log_error(traceback_str)
			sys.exit(1)

def log_message(message):
	with open('update.log', 'a', encoding='utf-8') as log_file:
		log_file.write(f'{message}\n')

def log_error(error_message):
	with open('update.log', 'a', encoding='utf-8') as log_file:
		log_file.write(f'ERROR: {error_message}\n')

if __name__ == '__main__':
	main()
