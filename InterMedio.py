import tkinter as tk
from tkinter import messagebox
import serial
import time
import threading

# Configuración del puerto serie
arduino_port = "COM3"  # ver en IDE de arduino a donde se conectó el micro.
baud_rate = 9600
gearReductionRadial = 40  # Relación de reducción del engranaje para el movimiento radial
gearReductionUlnar = 30   # Relación de reducción del engranaje para el movimiento ulnar
motorSpeed = 180.0  # Velocidad del motor en grados por segundo (ajusta según tu motor)
ser = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)

def read_serial():
    """Lee la salida del puerto serie para verificar si un motor ha finalizado su movimiento."""
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(f"Mensaje del Arduino: {line}")

# Ejecutar la función de lectura de serie en un hilo separado
threading.Thread(target=read_serial, daemon=True).start()

def send_command(command):
    """Envía un comando al Arduino."""
    if ser.is_open:
        ser.write(f"{command}\n".encode())
        print(f"Comando enviado al Arduino: {command}")
    else:
        print("El puerto serial no está abierto.")

# Funciones de calibración manual
def start_calibration_motor1():
    response = messagebox.askyesno("Calibración Motor 1", "¿Desea realizar la calibración manual del primer motor (Radial-Ulnar)?")
    if response:
        calibrate_window_motor1()

def calibrate_window_motor1():
    calibrate_win = tk.Toplevel(root)
    calibrate_win.title("Calibración Manual Motor 1 (Radial-Ulnar)")
    tk.Label(calibrate_win, text="Use los botones para ajustar la posición del primer motor:").pack(pady=10)

    tk.Button(calibrate_win, text="Sentido Horario", command=lambda: send_command('h')).pack(pady=5)
    tk.Button(calibrate_win, text="Sentido Antihorario", command=lambda: send_command('a')).pack(pady=5)
    tk.Button(calibrate_win, text="Pausar Movimiento", command=lambda: send_command('p')).pack(pady=5)
    tk.Button(calibrate_win, text="Establecer Posición 0°", command=lambda: [send_command('d'), calibrate_win.destroy()]).pack(pady=5)

def start_calibration_motor2():
    response = messagebox.askyesno("Calibración Motor 2", "¿Desea realizar la calibración manual del segundo motor (Flexión-Extensión)?")
    if response:
        calibrate_window_motor2()

def calibrate_window_motor2():
    calibrate_win = tk.Toplevel(root)
    calibrate_win.title("Calibración Manual Motor 2 (Flexión-Extensión)")
    tk.Label(calibrate_win, text="Use los botones para ajustar la posición del segundo motor:").pack(pady=10)

    tk.Button(calibrate_win, text="Sentido Horario", command=lambda: send_command('H')).pack(pady=5)
    tk.Button(calibrate_win, text="Sentido Antihorario", command=lambda: send_command('A')).pack(pady=5)
    tk.Button(calibrate_win, text="Pausar Movimiento", command=lambda: send_command('P')).pack(pady=5)
    tk.Button(calibrate_win, text="Establecer Posición 0°", command=lambda: [send_command('D'), calibrate_win.destroy()]).pack(pady=5)

# Funciones de movimiento
def set_radial_angle():
    try:
        angle = float(entry_radial.get())
        repetitions = int(entry_reps_radial.get())
        move_duration = (angle / motorSpeed) * 1000 * gearReductionRadial
        send_command(f"R1:{int(move_duration)},{repetitions}")
        messagebox.showinfo("Movimiento radial", f"Movimiento radial establecido: {angle} grados, {repetitions} repeticiones.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos para el ángulo y las repeticiones del movimiento radial.")

def set_ulnar_angle():
    try:
        angle = float(entry_ulnar.get())
        repetitions = int(entry_reps_ulnar.get())
        move_duration = (angle / motorSpeed) * 1000 * gearReductionUlnar
        send_command(f"U1:{int(move_duration)},{repetitions}")
        messagebox.showinfo("Movimiento ulnar", f"Movimiento ulnar establecido: {angle} grados, {repetitions} repeticiones.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos para el ángulo y las repeticiones del movimiento ulnar.")

def set_flexion_angle():
    try:
        angle = float(entry_flexion.get())
        repetitions = int(entry_reps_flexion.get())
        move_duration = (angle / motorSpeed) * 1000 * gearReductionRadial
        send_command(f"F2:{int(move_duration)},{repetitions}")
        messagebox.showinfo("Movimiento de flexión", f"Movimiento de flexión establecido: {angle} grados, {repetitions} repeticiones.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos para el ángulo y las repeticiones de flexión.")

def set_extension_angle():
    try:
        angle = float(entry_extension.get())
        repetitions = int(entry_reps_extension.get())
        move_duration = (angle / motorSpeed) * 1000 * gearReductionRadial
        send_command(f"E2:{int(move_duration)},{repetitions}")
        messagebox.showinfo("Movimiento de extensión", f"Movimiento de extensión establecido: {angle} grados, {repetitions} repeticiones.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos para el ángulo y las repeticiones de extensión.")

def emergency_stop():
    send_command('E')
    messagebox.showwarning("Paro de Emergencia", "Ambos motores han sido detenidos de inmediato.")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Control de Dispositivo de Rehabilitación Pasiva")

# Dividir la ventana en dos columnas
frame_motor1 = tk.Frame(root)
frame_motor1.grid(row=0, column=0, padx=20, pady=20, sticky="n")

frame_motor2 = tk.Frame(root)
frame_motor2.grid(row=0, column=1, padx=20, pady=20, sticky="n")

# Columna 1: Configuración y control del primer motor (Radial-Ulnar)
tk.Label(frame_motor1, text="Motor 1: Calibración de Rotación Radial-Ulnar", font=("Arial", 12, "bold")).pack(pady=5)
tk.Button(frame_motor1, text="Iniciar Calibración", command=start_calibration_motor1).pack(pady=10)

tk.Label(frame_motor1, text="Motor 1: Control de Rotación Radial-Ulnar", font=("Arial", 12, "bold")).pack(pady=10)

frame_radial = tk.Frame(frame_motor1)
frame_radial.pack(pady=5)
tk.Label(frame_radial, text="Ángulo Radial (sentido horario):").pack(side="left")
entry_radial = tk.Entry(frame_radial)
entry_radial.pack(side="left")
tk.Label(frame_radial, text="grados (°)").pack(side="left")
entry_reps_radial = tk.Entry(frame_radial, width=5)
entry_reps_radial.pack(side="left")
tk.Label(frame_radial, text="repeticiones").pack(side="left")
tk.Button(frame_motor1, text="Establecer Movimiento Radial", command=set_radial_angle).pack(pady=10)

frame_ulnar = tk.Frame(frame_motor1)
frame_ulnar.pack(pady=5)
tk.Label(frame_ulnar, text="Ángulo Ulnar (sentido antihorario):").pack(side="left")
entry_ulnar = tk.Entry(frame_ulnar)
entry_ulnar.pack(side="left")
tk.Label(frame_ulnar, text="grados (°)").pack(side="left")
entry_reps_ulnar = tk.Entry(frame_ulnar, width=5)
entry_reps_ulnar.pack(side="left")
tk.Label(frame_ulnar, text="repeticiones").pack(side="left")
tk.Button(frame_motor1, text="Establecer Movimiento Ulnar", command=set_ulnar_angle).pack(pady=10)

# Columna 2: Configuración y control del segundo motor (Flexión-Extensión)
tk.Label(frame_motor2, text="Motor 2: Calibración de Flexión-Extensión", font=("Arial", 12, "bold")).pack(pady=5)
tk.Button(frame_motor2, text="Iniciar Calibración", command=start_calibration_motor2).pack(pady=10)

tk.Label(frame_motor2, text="Motor 2: Control de Flexión-Extensión", font=("Arial", 12, "bold")).pack(pady=10)

frame_flexion = tk.Frame(frame_motor2)
frame_flexion.pack(pady=5)
tk.Label(frame_flexion, text="Ángulo de Flexión (sentido horario):").pack(side="left")
entry_flexion = tk.Entry(frame_flexion)
entry_flexion.pack(side="left")
tk.Label(frame_flexion, text="grados (°)").pack(side="left")
entry_reps_flexion = tk.Entry(frame_flexion, width=5)
entry_reps_flexion.pack(side="left")
tk.Label(frame_flexion, text="repeticiones").pack(side="left")
tk.Button(frame_motor2, text="Establecer Movimiento de Flexión", command=set_flexion_angle).pack(pady=10)

frame_extension = tk.Frame(frame_motor2)
frame_extension.pack(pady=5)
tk.Label(frame_extension, text="Ángulo de Extensión (sentido antihorario):").pack(side="left")
entry_extension = tk.Entry(frame_extension)
entry_extension.pack(side="left")
tk.Label(frame_extension, text="grados (°)").pack(side="left")
entry_reps_extension = tk.Entry(frame_extension, width=5)
entry_reps_extension.pack(side="left")
tk.Label(frame_extension, text="repeticiones").pack(side="left")
tk.Button(frame_motor2, text="Establecer Movimiento de Extensión", command=set_extension_angle).pack(pady=10)

# Botón de Paro de Emergencia (centrado debajo de ambas columnas)
emergency_button = tk.Button(root, text="Paro de Emergencia", command=emergency_stop, bg="red", fg="white", font=("Arial", 14, "bold"))
emergency_button.grid(row=1, column=0, columnspan=2, pady=20)

# Ajustar la ventana al contenido
root.update_idletasks()
root.minsize(root.winfo_width(), root.winfo_height())

# Iniciar la interfaz gráfica
root.mainloop()

# Cerrar la conexión serial al cerrar la interfaz
if ser.is_open:
    ser.close()