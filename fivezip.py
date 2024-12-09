import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import zipfile
import os
import shutil
import subprocess

# Carpeta temporal donde se extraen los archivos
TEMP_FOLDER = "temp"

# Función para limpiar la carpeta temporal al cerrar el programa
def clear_temp_folder():
    if os.path.exists(TEMP_FOLDER):
        shutil.rmtree(TEMP_FOLDER)
    root.quit()  # Cierra la ventana

# Función para cargar un archivo ZIP
def load_zip():
    global zip_file
    zip_path = filedialog.askopenfilename(filetypes=[("Archivo ZIP", "*.zip")], title="Selecciona un archivo ZIP")
    if not zip_path:
        return

    try:
        zip_file = zipfile.ZipFile(zip_path, 'r')
        files_list.delete(0, tk.END)  # Limpia la lista
        for file in zip_file.namelist():
            files_list.insert(tk.END, file)  # Agrega los archivos al explorador
        lbl_status.config(text=f"Cargado: {os.path.basename(zip_path)}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el archivo ZIP: {e}")
        zip_file = None

# Función para extraer un archivo seleccionado a la carpeta temporal y abrirlo
def open_selected():
    if not zip_file:
        messagebox.showinfo("Información", "Carga un archivo ZIP primero.")
        return

    selected_items = files_list.curselection()
    if not selected_items:
        messagebox.showinfo("Información", "Selecciona un archivo para abrir.")
        return

    # Crear la carpeta temporal si no existe
    if not os.path.exists(TEMP_FOLDER):
        os.makedirs(TEMP_FOLDER)

    try:
        for index in selected_items:
            file_name = files_list.get(index)
            extracted_path = zip_file.extract(file_name, TEMP_FOLDER)
            # Abre el archivo con la aplicación predeterminada
            subprocess.run(["xdg-open", extracted_path], check=True)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")

# Función para extraer todo el contenido
def extract_all():
    if not zip_file:
        messagebox.showinfo("Información", "Carga un archivo ZIP primero.")
        return

    extract_path = filedialog.askdirectory(title="Selecciona la carpeta de destino")
    if not extract_path:
        return

    try:
        zip_file.extractall(extract_path)
        messagebox.showinfo("Éxito", f"Todos los archivos extraídos en: {extract_path}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo extraer todo el contenido: {e}")

# Función para crear un nuevo archivo ZIP
def create_zip():
    # Mensaje de alerta antes de seleccionar archivos
    messagebox.showinfo("Seleccionar Archivos", "Para seleccionar varios archivos a la vez, mantén presionada la tecla Ctrl.")
    
    files_to_zip = filedialog.askopenfilenames(title="Selecciona los archivos a comprimir", filetypes=[("Todos los Archivos", "*.*")])
    if not files_to_zip:
        messagebox.showinfo("Información", "No se seleccionaron archivos para comprimir.")
        return

    # Seleccionar la ubicación para guardar el archivo ZIP
    zip_save_path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("Archivo ZIP", "*.zip")], title="Guardar como")
    if not zip_save_path:
        return

    try:
        with zipfile.ZipFile(zip_save_path, 'w', zipfile.ZIP_DEFLATED) as new_zip:
            for file in files_to_zip:
                new_zip.write(file, os.path.basename(file))  # Comprime cada archivo
        messagebox.showinfo("Éxito", f"Archivo ZIP creado exitosamente en: {zip_save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo crear el archivo ZIP: {e}")

# Ventana principal
root = tk.Tk()
root.title("FiveZIP 1.0 - By Ghosty")
root.geometry("800x600")
root.resizable(False, False)

# Llamar a clear_temp_folder cuando se cierre la ventana
root.protocol("WM_DELETE_WINDOW", clear_temp_folder)

# Zona superior (botones y estado)
frame_top = tk.Frame(root)
frame_top.pack(fill=tk.X, padx=10, pady=10)

btn_load = tk.Button(frame_top, text="Cargar ZIP", command=load_zip, width=15)
btn_load.pack(side=tk.LEFT, padx=5)

btn_open_selected = tk.Button(frame_top, text="Abrir Seleccionados", command=open_selected, width=20)
btn_open_selected.pack(side=tk.LEFT, padx=5)

btn_extract_all = tk.Button(frame_top, text="Extraer Todo", command=extract_all, width=15)
btn_extract_all.pack(side=tk.LEFT, padx=5)

btn_create_zip = tk.Button(frame_top, text="Crear ZIP", command=create_zip, width=15)
btn_create_zip.pack(side=tk.LEFT, padx=5)

lbl_status = tk.Label(frame_top, text="Cargado: Ninguno", fg="gray")
lbl_status.pack(side=tk.RIGHT, padx=5)

# Zona central (explorador de archivos)
frame_center = tk.Frame(root)
frame_center.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

files_list = tk.Listbox(frame_center, selectmode=tk.MULTIPLE, font=("Arial", 12))
files_list.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=5)

scrollbar = tk.Scrollbar(frame_center, orient=tk.VERTICAL, command=files_list.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
files_list.config(yscrollcommand=scrollbar.set)

# Pie de página
tk.Label(root, text="FiveZIP - Desarrollado por Ghosty", font=("Arial", 10), fg="gray").pack(side=tk.BOTTOM, pady=5)

root.mainloop()

