# TesisExoesqueleto
Este repositorio contiene el código y la interfaz gráfica (desarrollada en Python con Tkinter) para controlar un exoesqueleto de muñeca diseñado para la rehabilitación pasiva de pacientes con lesiones como el codo de tenista y el codo de golfista. El dispositivo permite movimientos programables y ajustables de flexión, extensión, y rotación radial-ulnar, proporcionando una herramienta accesible y efectiva para la recuperación de movilidad en la muñeca. Además, cuenta con el código de Arduino que permite controlar los motores de un exoesqueleto diseñado para la rehabilitación pasiva de la muñeca. El dispositivo facilita la recuperación de la movilidad en pacientes con lesiones de muñeca, como el codo de tenista o el codo de golfista, mediante movimientos programados de flexión, extensión y rotación radial-ulnar.

# Características del Proyecto
# Interfaz Gráfica de Usuario (GUI): 
La interfaz, desarrollada en Python, permite a los usuarios configurar parámetros como el ángulo de movimiento y el número de repeticiones para cada motor.

# Control de Motores Radial-Ulnar y Flexión-Extensión: Cada motor se configura individualmente para ejecutar movimientos de acuerdo con las necesidades de rehabilitación.

  Parada de Emergencia: Un botón de emergencia detiene ambos motores inmediatamente en caso de que se necesite detener el dispositivo de forma rápida.
Retroalimentación en Tiempo Real: La interfaz muestra el ángulo actual del dispositivo, permitiendo al usuario monitorear los movimientos en tiempo real.
  Calibración Manual: Opciones para calibrar manualmente cada motor antes de iniciar las rutinas de rehabilitación, estableciendo posiciones de referencia.
Archivos en el Repositorio

  interfaz_control.py: Código Python para la interfaz gráfica de usuario, que incluye la configuración de los movimientos y la calibración de los motores.
  codigoMedio.ino: Código Arduino que recibe comandos desde la interfaz y controla los motores, ejecutando los movimientos programados.

  Documentación: Instrucciones detalladas para la instalación, configuración y uso del sistema.
Requisitos del Sistema

  Hardware: Arduino Nano, motores con encoders, sistema de transmisión mecánica para el exoesqueleto.
  Software: Python 3.x, Tkinter, Arduino IDE.
  
# Instalación
Conecta el Arduino y carga el archivo arduino_control.ino.
Instala las dependencias de Python y ejecuta interfaz_control.py para iniciar la interfaz gráfica.
Sigue las instrucciones en la interfaz para configurar los ángulos y las repeticiones de cada movimiento.
