# DATOS INFORMATIVOS:

#Proyecto Final
#Integrantes:
# Shanem Cedeño
# Jessica Cuchipe
# Andrés Altamirano
# Mateo Beltrán
# SEGUNDO A
# -------------------------------------------------------------------------------------------------------------------------------------- #

# Librerías importadas
from PyQt6 import QtWidgets, uic # Importa los módulos relacionados con la interfaz gráfica de PyQt6
import sqlite3 # Importa el módulo relacionado con la base de datos de SQLite
from PyQt6.QtWidgets import QFileDialog  #libreria para subir archivos 
from PyQt6.QtCore import QUrl, Qt   # Libreria para ver archivos
from PyQt6.QtGui import QDesktopServices # Libreria para ver archivos y enlaces
from PyQt6.QtGui import QStandardItem, QStandardItemModel # Libreria para ver archivos
from PyQt6.QtWidgets import QTableWidgetItem # Importa el módulo relacionado con los widgets y la base de datos de PyQt6
import os # Libreria para interactuar con el sistema operativo (para subir archivos, ver enlaces)
import shutil # Libreria para interactuar con el sistema operativo (para subir archivos, ver enlaces)

# Inicar la aplicación
app = QtWidgets.QApplication([])

# Cargar todos los archivos .ui de las interfaces gráficas (creadas con Qt Designer)
principal = uic.loadUi("principal.ui")
login = uic.loadUi("login.ui")
login_correcto = uic.loadUi("login_correcto.ui")
login_error = uic.loadUi("login_error.ui")
registro = uic.loadUi("registro.ui")
base = uic.loadUi("base.ui")
Menu = uic.loadUi("Menu.ui")
CursoAsignatura1 = uic.loadUi("CursoAsignatura1.ui")
bienvenidaEstudiante = uic.loadUi("bienvenidaEstudiante.ui")
contenido = uic.loadUi("contenido.ui")
Pestañas = uic.loadUi("Pestañas.ui") 
CursosEst = uic.loadUi("CursosEst.ui")     
mtricMate = uic.loadUi("mtricMate.ui")
mtricLengua = uic.loadUi("mtricLengua.ui")
mtricHisto = uic.loadUi("mtricHisto.ui")
mensajeArchivo =uic.loadUi("mensajeArchivo.ui")
ventanaVisualizacionArchivo = uic.loadUi("ventanaVisualizacionArchivo.ui")
ventanaPreguntasAbiertas2 = uic.loadUi("ventanaPreguntasAbiertas2.ui")
ventanaPreguntasVF2 = uic.loadUi("ventanaPreguntasVF2.ui")
ventanaPreguntasOM = uic.loadUi("ventanaPreguntasOM.ui")
preguntas = uic.loadUi("preguntas.ui")
examenRecopilado = uic.loadUi("examenRecopilado.ui")
informeEstu = uic.loadUi("informeEstu.ui")
mensajeContenidoSubido = uic.loadUi("mensajeContenidoSubido.ui")
mensajeEnlaceSubido = uic.loadUi("mensajeEnlaceSubido.ui")

# Funciones de la interfaz gráfica del login
def gui_login():
    login.show()
    principal.hide()

# Función para validar el registro de un usuario 
def agregar_usuario():
    # Recuperar los valores de los campos
    Nombre = registro.Nombre.toPlainText()
    Apellido = registro.Apellido.toPlainText() #.toPlainText--> cuando usamos un textedit en pyqt6
    NombreUsuario = registro.NombreUsuario.toPlainText()
    Cedula = registro.CorreoInstitucional.toPlainText()
    Clave = registro.Clave.text()   #.text --> cuando usamos un line edit en pyqt6
    VerificarClave = registro.VerificarClave.text()
    
    # Validar que todos los campos estén llenos
    if not Nombre or not Apellido or not NombreUsuario or not Cedula or not Clave or not VerificarClave:
        registro.Aviso.setText("Todos los campos son obligatorios")

    # Validar que el número de cédula tenga 10 dígitos y que solo contenga números
    elif len(Cedula) != 10 or not Cedula.isdigit():
        registro.Aviso.setText("La cédula debe tener 10 dígitos y contener solo números")

    # Validar que la contraseña tenga al menos 8 caracteres
    elif len(Clave) < 8:
        registro.Aviso.setText("La contraseña debe tener al menos 8 caracteres")

    # Validar que se haya escogido un radio button (Docente o Estudiante)
    elif not registro.rbuttonDocente.isChecked() and not registro.rbuttonEstudiante.isChecked():
        registro.Aviso.setText("Debe seleccionar una opción")

    # Muestra un aviso que las contraseñas no coinciden
    elif Clave != VerificarClave:            
        registro.Aviso.setText("La contraseña no coincide")  # .setText --> Cuando usamos un label
    
    # Validar que el nombre y apellido solo contengan letras e iniciales en mayúscula
    elif not Nombre.isalpha() or not Apellido.isalpha():
        registro.Aviso.setText("El nombre y apellido solo pueden contener letras")

    elif not Nombre[0].isupper() or not Apellido[0].isupper():
        registro.Aviso.setText("El nombre y apellido deben iniciar con mayúscula")

    # Valida la existencia de un nombre de usuario y cédula idénticas en la base de datos
    else:
        # Valida que el usuario no exista en la base de datos de docentes
        if registro.rbuttonDocente.isChecked():
            conexion = sqlite3.connect("database.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM RegistroDocente WHERE Cedula = ? OR NombreUsuario = ?", (Cedula, NombreUsuario))
            if cursor.fetchall():
                registro.Aviso.setText("El usuario ya existe")
            else:
                # Agrega el usuario a la base de datos de docentes
                cursor.execute("INSERT INTO RegistroDocente (Nombre, Apellido, NombreUsuario, Cedula , Clave, VerificarClave) VALUES (?, ?, ?, ?, ?,?)", (Nombre, Apellido, NombreUsuario,Cedula , Clave,VerificarClave))
                conexion.commit()
                conexion.close()
                borrarCampos()
                gui_base()

        # Valida que el usuario no exista en la base de datos de estudiantes
        elif registro.rbuttonEstudiante.isChecked():
            conexion = sqlite3.connect("database.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM RegistroEstudiante WHERE Cedula = ? OR NombreUsuario = ?", (Cedula, NombreUsuario))
            if cursor.fetchall():
                registro.Aviso.setText("El usuario ya existe")
            else:
                # Agregar el usuario a la base de datos de estudiantes
                cursor.execute("INSERT INTO RegistroEstudiante (Nombre, Apellido, NombreUsuario, Cedula , Clave, VerificarClave) VALUES (?, ?, ?, ?, ?,?)", (Nombre, Apellido, NombreUsuario, Cedula, Clave,VerificarClave))
                conexion.commit()
                conexion.close()
                borrarCampos()
                gui_base()
        
#Función para borrar los campos de texto del registro una vez que se haya registrado un usuario
def borrarCampos():
    registro.Nombre.clear()
    registro.Apellido.clear()
    registro.NombreUsuario.clear()
    registro.CorreoInstitucional.clear()
    registro.Clave.clear()
    registro.VerificarClave.clear()
    registro.Aviso.clear()

# Función para validar el inicio de sesión de un usuario
def validacion_login():
    # Validar que el usuario y la contraseña no estén vacíos
    if not login.usuario_IS.toPlainText() or not login.clave_IS.text():
        # Mostrar un aviso
        login.avisoIS.setText("Debe ingresar un usuario y una contraseña")
    # Validar que se haya escogido un radio button (Docente o Estudiante)
    elif not login.rbuttonDocente.isChecked() and not login.rbuttonEstudiante.isChecked():
        login.avisoIS.setText("Debe seleccionar una opción")
    # Validar que el usuario y la contraseña sean correctos en funcion del tipo de usuario y cotejar con la base de datos
    else:
        # Conexión a la base de datos
        conexion = sqlite3.connect("database.db")
        cursor = conexion.cursor()

        # Recuperar los valores de los campos
        NombreUsuario = login.usuario_IS.toPlainText()  # Accede al contenido del widget de usuario
        Clave = login.clave_IS.text()  # Accede al contenido del widget de contraseña

        # Validar que el usuario y la contraseña sean correctos en funcion del tipo de usuario
        if login.rbuttonDocente.isChecked():
            cursor.execute("SELECT * FROM RegistroDocente WHERE NombreUsuario = ? AND Clave = ?", (NombreUsuario, Clave))
            if cursor.fetchall():
                gui_Menu()
                borrarCamposLogin()
                login.hide()
            else:
                login.avisoIS.setText("Usuario o contraseña incorrectos")
        elif login.rbuttonEstudiante.isChecked():
            cursor.execute("SELECT * FROM RegistroEstudiante WHERE NombreUsuario = ? AND Clave = ?", (NombreUsuario, Clave))
            if cursor.fetchall():
                gui_bienvenidaEstudiante()
                borrarCamposLogin()
                login.hide()
            else:
                login.avisoIS.setText("Usuario o contraseña incorrectos")
        
        # Cerrar la conexión
        conexion.close()

#Función para borrar los campos del inicio de sesión una vez que se haya ingresado un usuario
def borrarCamposLogin():
    login.usuario_IS.clear()
    login.clave_IS.clear()
    login.avisoIS.clear()

#Funciones para mostrar/ocultar las ventanas  ***GUI indica las funciones relacionadas con las ventanas***
def gui_login_correcto():
    login.hide() #.hide sirve para ocultar una ventana
    login_correcto.show()  #.show sirve para mostrar una ventana 

def gui_login_error():
    login.hide()
    login_error.show()

def gui_registro():
    registro.show()
    principal.hide()

def gui_principal():
    principal.show()
    registro.hide()
    base.hide()

def gui_rloginprincipal():
    login.hide()
    principal.show()

def gui_base():
    base.show()

def gui_Menu():
    Menu.show()
    login_correcto.hide()
    CursoAsignatura1.hide()

def gui_CursoAsignatura():
    CursoAsignatura1.show()
    Menu.hide()
            
def gui_bienvenidaEstudiante():
    bienvenidaEstudiante.show()

def gui_contenido():
    contenido.show()

def gui_Pestañas():
    Pestañas.show()

def gui_CursosEst():
    CursosEst.show()
    login.hide()
    bienvenidaEstudiante.hide()

def gui_mtricMate():
    mtricMate.show()

def gui_mtricLengua():
    mtricLengua.show()

def gui_mtricHisto():
    mtricHisto.show()

def gui_preguntas():
   preguntas.show()

def gui_ventanaPreguntasAbiertas2():
    ventanaPreguntasAbiertas2.show()

def gui_ventanaPreguntasVF2():
    ventanaPreguntasVF2.show()

def gui_ventanaPreguntasOM():
    ventanaPreguntasOM.show()

def gui_examenRecopilado():
    examenRecopilado.show()

def gui_mensajeContenidoSubido():
    mensajeContenidoSubido.show()
    contenido.hide()

def gui_mesajeEnlaceSubido():
    mensajeEnlaceSubido.show()
    
# Administración de estudiantes
def cargar_informe_estudiantes():
    # Conexión a la base de datos
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    # Consulta a la base de datos para obtener los datos
    cursor.execute("SELECT Cedula, Nombre, Apellido, NombreUsuario, Clave FROM RegistroEstudiante")
    data = cursor.fetchall()

    # Cerrar la conexión
    conexion.close()

    # Limpiar la tabla antes de cargar nuevos datos
    informeEstu.tablaRegistroEstudiantes.clearContents()
    informeEstu.tablaRegistroEstudiantes.setRowCount(0)

    # Cargar los datos en la tabla
    for row_idx, row_data in enumerate(data):  # row_idx es el índice de la fila y row_data es una lista con los datos de la fila
        informeEstu.tablaRegistroEstudiantes.insertRow(row_idx) # Insertar una fila en la tabla
        for col_idx, cell_data in enumerate(row_data): # col_idx es el índice de la columna y cell_data es el dato de la celda
            item = QTableWidgetItem(str(cell_data)) # Crear un QTableWidgetItem con el dato de la celda
            informeEstu.tablaRegistroEstudiantes.setItem(row_idx, col_idx, item) # Insertar el QTableWidgetItem en la tabla

# Función que permite actualizar la tabla de estudiantes con los nuevos datos ingresados (Sección de administración de estudiantes)
def actualizar_registro_estudiante():

    # Conexión a la base de datos
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    # Obtener los datos de la tabla de la interfaz
    data = []
    for row_idx in range(informeEstu.tablaRegistroEstudiantes.rowCount()):
        row = []
        for col_idx in range(informeEstu.tablaRegistroEstudiantes.columnCount()):
            item = informeEstu.tablaRegistroEstudiantes.item(row_idx, col_idx)
            if item is not None:
                row.append(item.text())
            else:
                row.append("")
        data.append(row)

    # Actualizar los datos en la base de datos
    for row_data in data:
        cedula = row_data[0]    # Cedula
        nombre = row_data[1]    # Nombre
        apellido = row_data[2]  # Apellido
        usuario = row_data[3]   # Nombre de usuario
        clave = row_data[4]     # Clave
        cursor.execute("UPDATE RegistroEstudiante SET Nombre = ?, Apellido = ?, NombreUsuario = ?, Clave = ? WHERE Cedula = ?",(nombre, apellido, usuario, clave, cedula))

    # Guardar los cambios
    conexion.commit()

    # Cerrar la conexión
    conexion.close()

# Función para eliminar un registro seleccionado de la tabla (Sección de administración de estudiantes)
def eliminar_registro_estudiante():
    # Obtener el índice de la fila seleccionada
    row_idx = informeEstu.tablaRegistroEstudiantes.currentRow()

    # Obtener la cédula de la fila seleccionada
    cedula = informeEstu.tablaRegistroEstudiantes.item(row_idx, 0).text()

    # Conexión a la base de datos
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    # Eliminar el registro de la base de datos
    cursor.execute("DELETE FROM RegistroEstudiante WHERE Cedula = ?", (cedula,))

    # Guardar los cambios
    conexion.commit()

    # Cerrar la conexión
    conexion.close()

    # Eliminar la fila de la tabla
    informeEstu.tablaRegistroEstudiantes.removeRow(row_idx)

# Función de búsqueda en tiempo real (Sección de administración de estudiantes)
def buscar_en_tiempo_real(texto_busqueda):

    # Conexión a la base de datos
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    # Consulta a la base de datos para obtener los datos
    cursor.execute("SELECT Cedula, Nombre, Apellido, NombreUsuario, Clave FROM RegistroEstudiante WHERE Cedula LIKE ? OR Nombre LIKE ? OR Apellido LIKE ? OR NombreUsuario LIKE ? OR Clave LIKE ?",('%' + texto_busqueda + '%', '%' + texto_busqueda + '%', '%' + texto_busqueda + '%', '%' + texto_busqueda + '%', '%' + texto_busqueda + '%'))
    data = cursor.fetchall()

    # Cerrar la conexión
    conexion.close()

    # Limpiar la tabla antes de cargar nuevos datos
    informeEstu.tablaRegistroEstudiantes.clearContents()
    informeEstu.tablaRegistroEstudiantes.setRowCount(0)

    # Cargar los datos en la tabla
    for row_idx, row_data in enumerate(data):
        informeEstu.tablaRegistroEstudiantes.insertRow(row_idx)
        for col_idx, cell_data in enumerate(row_data):
            item = QTableWidgetItem(str(cell_data))
            informeEstu.tablaRegistroEstudiantes.setItem(row_idx, col_idx, item)

# Conexión de la señal textChanged a la función de búsqueda (Para que se actualice la tabla de estudiantes en tiempo real mientras se busca)
informeEstu.busqueda.textChanged.connect(lambda texto: buscar_en_tiempo_real(texto))

# Función para mostrar la ventana de administración de estudiantes
def gui_informeEstu():
    informeEstu.show()

# Funión que muestra los archivos subidos en la ventana del aula virtual (Estudiante)
def gui_ventanaVisualizacionArchivo():
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    # Capturar la opción seleccionada en el comboBox de asignatura	
    asignatura_seleccionada = ventanaVisualizacionArchivo.asignatura.currentText()

    # Consulta a la base de datos para obtener los archivos de la asignatura seleccionada
    cursor.execute("SELECT nombre_archivo FROM archivos WHERE asignatura = ?", (asignatura_seleccionada,))
    data = cursor.fetchall()

    # Cerrar la conexión
    conexion.close()

    # Crear un modelo de datos
    model = QStandardItemModel()

    # Cargar los datos en el modelo
    for row_data in data:
        item = QStandardItem(str(row_data[0]))
        model.appendRow(item)

    # Asignar el modelo al QListView
    ventanaVisualizacionArchivo.comboBoxArchivos.setModel(model)

    # Permite actualizar la lista de archivos cuando se cambia la asignatura
    ventanaVisualizacionArchivo.asignatura.currentIndexChanged.connect(gui_ventanaVisualizacionArchivo)
    
    # Si se hace click en un elemento de la lista, se muestra el contenido del archivo
    ventanaVisualizacionArchivo.show()

# Función para seleccionar el archivo a abrir
def ver_contenido_archivo_seleccionado():
    nombre_archivo_seleccionado = ventanaVisualizacionArchivo.comboBoxArchivos.currentText()
    mostrar_contenido_archivo(nombre_archivo_seleccionado)

# Función para abrir el archivo
def abrir_archivo():
    nombre_archivo_seleccionado = ventanaVisualizacionArchivo.comboBoxArchivos.currentText()

    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    # Obtener la ruta del archivo desde la base de datos
    cursor.execute("SELECT ruta_archivo FROM archivos WHERE nombre_archivo = ?", (nombre_archivo_seleccionado,))
    resultado = cursor.fetchone()
    
    if resultado:
        archivo_path = resultado[0]
        url = QUrl.fromLocalFile(archivo_path) 
        QDesktopServices.openUrl(url)       

    conexion.close()

# Indica el directorio donde se guardan los archivos subidos
carpeta_destino = "files"

# Guarda un enlace en la base de datos
def guardar_enlace_en_db():
    enlace = Pestañas.ingresarEnlace.toPlainText()

    # Captura el texto de la opción seleccionada en el comboBox de asignatura
    asignatura_seleccionada = Pestañas.asignaturaArchivosEnlaces.currentText()

    # Conectar a la base de datos
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    # Insertar el enlace en la columna "enlace" de la tabla "enlace"
    cursor.execute("INSERT INTO enlace (enlace, asignatura) VALUES (?, ?)", (enlace, asignatura_seleccionada))

    # Guardar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()
    mensajeEnlaceSubido.show()

# Función para ver los archivos subidos
def mostrar_contenido_archivo(nombre_archivo):
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    # Obtener la ruta del archivo desde la base de datos
    cursor.execute("SELECT ruta_archivo FROM archivos WHERE nombre_archivo = ?", (nombre_archivo,))
    resultado = cursor.fetchone()
    
    if resultado:
        archivo_path = resultado[0]
        with open(archivo_path, 'r') as archivo:
            contenido = archivo.read()
            ventanaVisualizacionArchivo.archivoSubido.setText(contenido)  # Asignar el contenido al widget QTextEdit
            ventanaVisualizacionArchivo.show()

    conexion.close()

# *** "r" al inicio en el nombre de las funciones indica que es una función para un boton de regresar y su estructura es así: r_ventanaOrigen_ventanaDestino ***

# Funciones para el comportamiento de las ventanas que interactúan con los botones de regresar
def r_loginIncorrecto_login():
    login_error.hide()
    login.show()

def r_guiContenido_guiCursoAsignatura():
    contenido.hide()
    CursoAsignatura1.show()

def r_Pestañas_CursoAsignatura():
    Pestañas.hide()
    CursoAsignatura1.show()

def r_informeEstu_CursoAsignatura():
    informeEstu.hide()

def r_CursoAsignatura_Menu():
    CursoAsignatura1.hide()

def r_Menu_login():
    Menu.hide()
    login.show()

def r_cursosEst_bienvenidaestudiante():
    CursosEst.hide()
    bienvenidaEstudiante.show()

def r_bienvenidaEstudiantes_principal():
    bienvenidaEstudiante.hide()
    principal.show()

def r_mtricMate_CursosEst():
    mtricMate.hide()
    # Limpiar el campo de código de aula (Docente)
    mtricMate.codigoAula.clear()

def r_mtricLengua_CursosEst():
    mtricLengua.hide()

def r_mtricHisto_CursosEst():
    mtricHisto.hide()

def r_mensajeArchivo_Pestañas():
    mensajeArchivo.hide()

def r_ventanaVisualizacionArchivo_Menu():
    ventanaVisualizacionArchivo.hide()

def r_pestañas_CursoAsignatura():
    Pestañas.hide()

def r_examenRecopilado_Menu():
    Menu.show()
    examenRecopilado.hide()

def r_preguntas_CursoAsignatura():
    CursoAsignatura1.show()
    preguntas.hide()

def r_mensajeContenidoSubido_cursoAsignatura1():
    mensajeContenidoSubido.hide()

def r_mensajeEnlaceSubido():
    mensajeEnlaceSubido.hide()

# Función para agegar preguntas abiertas al examen
def agregar_pregunta_abierta():
    pregunta_abierta = ventanaPreguntasAbiertas2.textEditPreguntaAbierta.toPlainText()
    
    # Conectar a la base de datos
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()
    
    # Insertar la pregunta en la tabla del examen
    cursor.execute("INSERT INTO preguntasExamen (tipo, pregunta) VALUES (?, ?)", ("Pregunta Abierta", pregunta_abierta))
    
    # Guardar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()
    
    # Ocultar la ventana
    ventanaPreguntasAbiertas2.hide()

# Función para agregar preguntas de verdadero o falso al examen
def agregar_pregunta_vf():
    pregunta_vf = ventanaPreguntasVF2.textEditPreguntaVF.toPlainText()
    respuesta_correcta = "Verdadero" if ventanaPreguntasVF2.radioButtonVerdadero.isChecked() else "Falso"
    
    # Conectar a la base de datos
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()
    
    # Insertar la pregunta en la tabla del examen
    cursor.execute("INSERT INTO preguntasExamen (tipo, pregunta, opciones, respuesta_correcta) VALUES (?, ?, ?, ?)", ("Pregunta Cerrada", pregunta_vf, "Verdadero,Falso", respuesta_correcta))
    
    # Guardar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()
    
    # Ocultar la ventana
    ventanaPreguntasVF2.hide()

# Función para agregar preguntas de opción múltiple al examen
def agregar_pregunta_om():
    pregunta_om = ventanaPreguntasOM.textEditPreguntaOM.toPlainText()
    opciones_texto = ventanaPreguntasOM.textEditOpciones.toPlainText()
    opciones = opciones_texto.split(',')
    respuesta_correcta = ventanaPreguntasOM.textEditRespuestaCorrecta.toPlainText()  # Obtener la respuesta correcta del textEdit
    
    # Conectar a la base de datos
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()
    
    # Insertar la pregunta en la tabla del examen
    cursor.execute("INSERT INTO preguntasExamen (tipo, pregunta, opciones, respuesta_correcta) VALUES (?, ?, ?, ?)", ("Pregunta de Opción Múltiple", pregunta_om, opciones_texto, respuesta_correcta))
    
    # Guardar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()
    
    # Ocultar la ventana
    ventanaPreguntasOM.hide()

# Función para agregar las preguntas anteriores de forma recopilada al examen
def gui_examenRecopilado():
    # Conexión a la base de datos
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    # Recuperar las preguntas de la base de datos (por ejemplo, las preguntas de tipo "Pregunta Abierta")
    cursor.execute("SELECT pregunta FROM preguntasExamen WHERE tipo = 'Pregunta Abierta'")
    preguntas_abiertas = cursor.fetchall()

    # Recuperar las preguntas de tipo "Pregunta Cerrada"
    cursor.execute("SELECT pregunta FROM preguntasExamen WHERE tipo = 'Pregunta Cerrada'")
    preguntas_cerradas = cursor.fetchall()

    # Recuperar las preguntas de tipo "Pregunta Opción Múltiple"
    cursor.execute("SELECT pregunta, opciones FROM preguntasExamen WHERE tipo = 'Pregunta de Opción Múltiple'")
    preguntas_opcion_multiple = cursor.fetchall()

    # Cerrar la conexión
    conexion.close()

    # Mostrar las preguntas en la ventana examenRecopilado
    examenRecopilado.label_3.setText("\n".join([pregunta[0] for pregunta in preguntas_abiertas]))
    examenRecopilado.label_4.setText("\n".join([pregunta[0] for pregunta in preguntas_cerradas]))
    examenRecopilado.label_5.setText("\n".join([pregunta[0] for pregunta in preguntas_opcion_multiple]))

    # Mostrar las preguntas de opción múltiple en el label_5 y las opciones en el comboBoxRespuesta
    preguntas_y_opciones = [pregunta[0] for pregunta in preguntas_opcion_multiple]
    examenRecopilado.label_5.setText("\n".join(preguntas_y_opciones))

    examenRecopilado.comboBoxRespuesta.clear()  # Limpiar comboBoxRespuesta antes de agregar nuevas opciones
    # Agregar las opciones al comboBoxRespuesta
    for opciones in [pregunta[1].split(',') for pregunta in preguntas_opcion_multiple]:
        examenRecopilado.comboBoxRespuesta.addItems(opciones)

    # Mostrar la ventana examenRecopilado
    examenRecopilado.show()

# Función para guardar el contenido (Temas y descripción) en la base de datos
def guardar_contenido_en_db():
    titulo = contenido.titulo.toPlainText()
    descripcion = contenido.descripcion.toPlainText()

    # Conectar a la base de datos
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    # Capturar el texto de la opción seleccionada en el comboBox de asignaturaContenido
    asignatura_seleccionada = contenido.asignaturaContenido.currentText()

    # Insertar los valores en la tabla "contenido"
    cursor.execute("INSERT INTO contenido (titulo, descripcion, asignatura) VALUES (?, ?, ?)", (titulo, descripcion, asignatura_seleccionada))

    # Guardar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()

# Función para abrir los enlaces adjuntos en el navegador
def abrir_enlace(enlace):
    # Si enlace no comienza con "http://" o "https://", agregarlo
    if not enlace.startswith("http://") and not enlace.startswith("https://"):
        enlace = "http://" + enlace
    url = QUrl(enlace)
    QDesktopServices.openUrl(url)
    
    # Al abrir el enlace, ya no se abriran mas pestañas
    ventanaVisualizacionArchivo.listaEnlaces.clicked.disconnect()
    # Reiniciar la conexión para evitar que se abran múltiples pestañas en bucle
    ventanaVisualizacionArchivo.listaEnlaces.clicked.connect(lambda: abrir_enlace(ventanaVisualizacionArchivo.listaEnlaces.currentIndex().data()))

#Cargar enlaces en pantalla estudiantes
def cargar_enlaces_estudiantes():
    # Conexión a la base de datos
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    # Capturar la opción seleccionada en el comboBox de asignatura	
    asignatura_seleccionada = ventanaVisualizacionArchivo.asignatura.currentText()

    # Consulta a la base de datos para obtener los archivos de la asignatura seleccionada
    cursor.execute("SELECT enlace FROM enlace WHERE asignatura = ?", (asignatura_seleccionada,))
    data = cursor.fetchall()

    # Cerrar la conexión
    conexion.close()

    # Crear un modelo de datos
    model = QStandardItemModel()

    # Cargar los datos en el modelo
    for row_data in data:
        item = QStandardItem(str(row_data[0]))
        model.appendRow(item)

    # Asignar el modelo al QListView
    ventanaVisualizacionArchivo.listaEnlaces.setModel(model)

    # Permite actualizar la lista de archivos cuando se cambia la asignatura
    ventanaVisualizacionArchivo.asignatura.currentIndexChanged.connect(cargar_enlaces_estudiantes)

    # Si se hace click en un elemento de la lista, se abre el enlace en el navegador
    ventanaVisualizacionArchivo.listaEnlaces.clicked.connect(lambda: abrir_enlace(ventanaVisualizacionArchivo.listaEnlaces.currentIndex().data()))
    
#Cargar titulos del contenido en la pantalla de estudiantes
def cargarTitulos():
    # Operaciones para cargar los títulos en la lista del combobox
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    # Consulta a la base de datos para obtener los datos
    cursor.execute("SELECT titulo FROM contenido")
    data = cursor.fetchall()

    # Cerrar la conexión
    conexion.close()

    # Crear un modelo de datos
    model = QStandardItemModel()

    # Cargar los datos en el modelo
    for row_data in data:
        item = QStandardItem(str(row_data[0]))
        model.appendRow(item)

    # Asignar el modelo al QListView
    ventanaVisualizacionArchivo.tituloRelleno.setModel(model)

# Cargar descripción del contenido en la pantalla de estudiantes en base al título seleccionado
def cargarDescripcion():
    # Obtener el título seleccionado
    titulo_seleccionado = ventanaVisualizacionArchivo.tituloRelleno.currentText()

    # Conexión a la base de datos
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    # Consulta a la base de datos para obtener la descripción del contenido
    cursor.execute("SELECT descripcion FROM contenido WHERE titulo = ?", (titulo_seleccionado,))
    resultado = cursor.fetchone()

    if resultado:
        descripcion = resultado[0]
        ventanaVisualizacionArchivo.descripcionRelleno.setPlainText(descripcion)  # Asignar la descripción al QTextEdit

    conexion.close()

# Conectar la función cargarDescripcion al evento de cambio de selección del QComboBox
ventanaVisualizacionArchivo.tituloRelleno.currentIndexChanged.connect(cargarDescripcion)

# Función para validar el código de acceso al aula (Para estudiantes)
def validar_codigo_aula():
    # Obtener el código ingresado
    codigo_aula = mtricMate.codigoAula.toPlainText()

    # Conexión a la base de datos
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    # Consulta a la base de datos para obtener el código del aula
    cursor.execute("SELECT codigo FROM codigoAula WHERE codigo = ?", (codigo_aula,))

    # Si el código es correcto, mostrar la ventana de visualización de archivos
    if cursor.fetchone():
        gui_ventanaVisualizacionArchivo()
    else:
        mtricLengua.show()

    # Cerrar la conexión
    conexion.close()

    # Limpiar el campo de texto al hacer click acceder y cancelar
    mtricMate.codigoAula.clear()

# Función para cargar las asignaturas en el comboBox de la pantalla del aula virtual (Estudiante)
def cargarAsignaturas_cursoEstudiante():
    # Conexión a la base de datos
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    # Consulta a la base de datos para obtener las asignaturas únicas
    cursor.execute("SELECT DISTINCT asignatura FROM asignaturas")
    asignaturas_data = cursor.fetchall()

    # Cerrar la conexión
    conexion.close()

    # Crear un modelo de datos para las asignaturas
    asignaturas_model = QStandardItemModel()

    # Cargar las asignaturas en el modelo
    for asignatura_data in asignaturas_data:
        item = QStandardItem(str(asignatura_data[0]))
        asignaturas_model.appendRow(item)

    # Asignar el modelo al ComboBox de asignaturas
    ventanaVisualizacionArchivo.asignatura.setModel(asignaturas_model)

    # Conectar la señal de cambio en la selección de asignatura a la función cargarTitulos_asignatura
    ventanaVisualizacionArchivo.asignatura.currentIndexChanged.connect(cargarTitulos_asignatura)

# Cargar títulos en el comboBox de la pantalla del aula virtual (Estudiante) en base a la asignatura seleccionada
def cargarTitulos_asignatura():
    # Obtener la asignatura seleccionada
    asignatura_seleccionada = ventanaVisualizacionArchivo.asignatura.currentText()

    # Conexión a la base de datos
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    # Consulta a la base de datos para obtener los títulos del contenido
    cursor.execute("SELECT titulo FROM contenido WHERE asignatura = ?", (asignatura_seleccionada,))
    titulos_data = cursor.fetchall()

    # Cerrar la conexión
    conexion.close()

    # Crear un modelo de datos para los títulos
    titulos_model = QStandardItemModel()

    # Cargar los títulos en el modelo
    for titulo_data in titulos_data:
        item = QStandardItem(str(titulo_data[0]))
        titulos_model.appendRow(item)

    # Asignar el modelo al QListView de títulos
    ventanaVisualizacionArchivo.tituloRelleno.setModel(titulos_model)

# Consultar las asignaturas desde la tabla asignaturas en la base de datos
def cargarAsignaturas_contenido():
    # Conexión a la base de datos
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    # Consulta a la base de datos para obtener las asignaturas únicas
    cursor.execute("SELECT DISTINCT asignatura FROM asignaturas")
    asignaturas_data = cursor.fetchall()

    # Cerrar la conexión
    conexion.close()

    # Crear un modelo de datos para las asignaturas
    asignaturas_model = QStandardItemModel()

    # Cargar las asignaturas en el modelo
    for asignatura_data in asignaturas_data:
        item = QStandardItem(str(asignatura_data[0]))
        asignaturas_model.appendRow(item)

    # Asignar el modelo al ComboBox de asignaturas
    contenido.asignaturaContenido.setModel(asignaturas_model)

# Función de actualización de toda la información del aula virtual (Estudiante)
def actualizarContenido():
    cargarAsignaturas_contenido()

# Conectar el botón actualizar contenido a la función de actualización
contenido.actualizarContenido.clicked.connect(actualizarContenido)

# Cargar asignaturas en el comboBox de la pantalla de subida de archivos y enlaces (Docente)
def cargarAsignaturas_pestanas():
    # Conexión a la base de datos
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    # Consulta a la base de datos para obtener las asignaturas únicas
    cursor.execute("SELECT DISTINCT asignatura FROM asignaturas")
    asignaturas_data = cursor.fetchall()

    # Cerrar la conexión
    conexion.close()

    # Crear un modelo de datos para las asignaturas
    asignaturas_model = QStandardItemModel()

    # Cargar las asignaturas en el modelo
    for asignatura_data in asignaturas_data:
        item = QStandardItem(str(asignatura_data[0]))
        asignaturas_model.appendRow(item)

    # Asignar el modelo al ComboBox de asignaturas
    Pestañas.asignaturaArchivosEnlaces.setModel(asignaturas_model)

# Función de actualización de toda la información de la pantalla de subida de archivos y enlaces (Docente)
def actualizarPestañas():
    cargarAsignaturas_pestanas()

# Conectar el botón actualizar archivos y enlaces a la función de actualización
Pestañas.actualizarArchivos.clicked.connect(actualizarPestañas)

# Cargar los archivos y su ruta en la abse de datos, también abre la ventana de abrir archivos del sistema operativo
def cargar_archivo():
    archivo, _ = QFileDialog.getOpenFileName(None, "Seleccionar archivo", "", "Archivos de texto (*.txt);;Documentos de Word (*.docx);;Archivos PDF (*.pdf);;Todos los archivos (*)")

    if archivo:
        # Obtener solo el nombre del archivo de la ruta completa
        nombre_archivo = archivo.split("/")[-1]

        # Copiar el archivo a la carpeta de destino
        ruta_destino = os.path.join(carpeta_destino, nombre_archivo)
        shutil.copy(archivo, ruta_destino)

        # Capturar el texto de la opción seleccionada en el comboBox de asignaturaArchivosEnlaces
        asignatura_seleccionada = Pestañas.asignaturaArchivosEnlaces.currentText()

        # Guardar la nueva ruta en la base de datos
        nueva_ruta = ruta_destino  # Usar la ruta de destino como la nueva ubicación
        conexion = sqlite3.connect("database.db")
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO archivos (nombre_archivo, ruta_archivo, tipo_archivo, asignatura) VALUES (?, ?, ?, ?)", (nombre_archivo, nueva_ruta, "Tipo del archivo", asignatura_seleccionada))

        # Guardar los cambios y cerrar la conexión
        conexion.commit()
        conexion.close()

        # Mostrar el mensaje de archivo subido
        mensajeArchivo.show()

# Dar funcionalidad a la tabla de asignaturas (Docente)
def tablaAsignaturas():
    # Conexión a la base de datos
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    # Consulta a la base de datos para obtener los datos
    cursor.execute("SELECT asignatura FROM asignaturas")
    data = cursor.fetchall()

    # Cerrar la conexión
    conexion.close()

    # Limpiar la tabla antes de cargar nuevos datos
    Menu.tablaAsignaturas.clearContents()
    Menu.tablaAsignaturas.setRowCount(0)

    # Cargar los datos en la tabla
    for row_idx, row_data in enumerate(data):
        Menu.tablaAsignaturas.insertRow(row_idx)
        for col_idx, cell_data in enumerate(row_data):
            item = QTableWidgetItem(str(cell_data))
            Menu.tablaAsignaturas.setItem(row_idx, col_idx, item)

#Acción del botón para actualizar la tabla de asignaturas
Menu.actualizarAsignatura.clicked.connect(tablaAsignaturas)

# Acción del botón para agregar una nueva asignatura a la tabla de asignaturas
def agregar_tablaAsignaturas():
    # Conexión a la base de datos
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    # Obtener el texto ingresado en el textEdit
    asignatura = mtricHisto.nuevaAsignatura.toPlainText()
    
    # Insertar la asignatura en la tabla de la base de datos
    cursor.execute("INSERT INTO asignaturas (asignatura) VALUES (?)", (asignatura,))

    # Guardar los cambios
    conexion.commit()

    # Cerrar la conexión
    conexion.close()

    # Limpiar el textEdit
    mtricHisto.nuevaAsignatura.clear()

    # Actualizar la tabla de asignaturas
    tablaAsignaturas()

    # Esconder la ventana mtricHisto
    mtricHisto.hide()

# Acción del botón para eliminar una asignatura de la tabla de asignaturas
def eliminar_tablaAsignaturas():
    # Obtener el índice de la fila seleccionada
    row_idx = Menu.tablaAsignaturas.currentRow()

    # Obtener la asignatura de la fila seleccionada
    asignatura = Menu.tablaAsignaturas.item(row_idx, 0).text()

    # Conexión a la base de datos
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    # Eliminar la asignatura de la base de datos
    cursor.execute("DELETE FROM asignaturas WHERE asignatura = ?", (asignatura,))

    # Guardar los cambios
    conexion.commit()

    # Cerrar la conexión
    conexion.close()

    # Eliminar la fila de la tabla
    Menu.tablaAsignaturas.removeRow(row_idx)

# Botón para eliminar una asignatura de la tabla de asignaturas
Menu.eliminarAsignatura.clicked.connect(eliminar_tablaAsignaturas)

# Funcionalidad del QTextEdit para ver el código del aula actual 
def ver_codigo_aula(event):
    # Conexión a la base de datos
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    # Consulta a la base de datos para obtener el código del aula
    cursor.execute("SELECT codigo FROM codigoAula")
    codigo_aula = cursor.fetchone()[0]

    # Cerrar la conexión
    conexion.close()

    # Mostrar el código del aula en el QTextEdit
    CursoAsignatura1.codigoAulaDocente.setPlainText(codigo_aula)

    # Cargar la solicitud anterior en el QTextEdit automáticamente al abrir la ventana CursoAsignatura1.ui
    CursoAsignatura1.codigoAulaDocente.setPlainText(codigo_aula)

# Conectar la señal de carga de la ventana CursoAsignatura1.ui a la función ver_codigo_aula
CursoAsignatura1.showEvent = ver_codigo_aula

# Funcionalidad del botón Cambiar Código para cambiar el código del aula por el que se haya ingresado en el campo de texto
def cambiar_codigo_aula():
    # Obtener el código ingresado
    codigo_aula = CursoAsignatura1.codigoAulaDocente.toPlainText()

    # Conexión a la base de datos
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    # Actualizar el código del aula en la tabla de la base de datos
    cursor.execute("UPDATE codigoAula SET codigo = ?", (codigo_aula,))

    # Guardar los cambios
    conexion.commit()

    # Cerrar la conexión
    conexion.close()

# Conectar el botón "cambiarCodigoAula" a la función cambiar_codigo_aula
CursoAsignatura1.cambiarCodigoAula.clicked.connect(cambiar_codigo_aula)

# Recopilación de los botones de las ventanas y sus llamadas al resto de funciones del programa (Funciones de comportamiento de ventanas, validación, conexiones a las base de datos, etc.) *** Estructura:ventana.nombredelboton.clicked(al hacer click).connect(se conecta a una funcion) (función a donde se dirige) ***
mtricMate.botonMatricularse.clicked.connect(validar_codigo_aula)
principal.botonInicioSesion.clicked.connect(gui_login)
login.botonIngresar_IS.clicked.connect(validacion_login)
login_error.botonRegresar.clicked.connect(r_loginIncorrecto_login) #boton regresar
principal.botonRegistro.clicked.connect(gui_registro)
registro.botonRegresar1.clicked.connect(gui_principal)
registro.botonRegresar1.clicked.connect(borrarCampos)
login.botonRegresar_IS.clicked.connect(gui_rloginprincipal)
login.botonRegresar_IS.clicked.connect(borrarCamposLogin)
registro.botonRegistrarse.clicked.connect(agregar_usuario)
base.botonEntendido.clicked.connect(gui_principal)
login_correcto.botonEntendido.clicked.connect(gui_Menu)
Menu.botonEditar.clicked.connect(gui_CursoAsignatura)
CursoAsignatura1.botonContenido.clicked.connect(gui_contenido)
CursoAsignatura1.botonDoc.clicked.connect(gui_Pestañas)
contenido.botonCancelar.clicked.connect(r_guiContenido_guiCursoAsignatura)
CursoAsignatura1.botoRegresarCurso.clicked.connect(gui_Menu)
Menu.botonRegresarMenu.clicked.connect(r_Menu_login) #boton regresar
bienvenidaEstudiante.botonIrCurso.clicked.connect(gui_mtricMate)
Menu.agregarAsignatura.clicked.connect(gui_mtricHisto)
CursosEst.botonRegresarCursos.clicked.connect(r_cursosEst_bienvenidaestudiante) #boton regresar
bienvenidaEstudiante.botonSalirBienvenida.clicked.connect(r_bienvenidaEstudiantes_principal) #boton regresar
mtricMate.botonCancelarMate.clicked.connect(r_mtricMate_CursosEst) #boton regresar
mtricLengua.botonCancelarLengua.clicked.connect(r_mtricLengua_CursosEst) #boton regresar
mtricHisto.botonCancelarHisto.clicked.connect(r_mtricHisto_CursosEst)  #boton regresar
mtricHisto.agregar.clicked.connect(agregar_tablaAsignaturas)
mtricHisto.botonCancelarHisto.clicked.connect(gui_Menu)
Pestañas.botonSubirDoc.clicked.connect(cargar_archivo)
mensajeArchivo.botonEntendidoArchivo.clicked.connect(r_mensajeArchivo_Pestañas)
Menu.botonVer.clicked.connect(gui_ventanaVisualizacionArchivo)
ventanaVisualizacionArchivo.botonAbrirArchivo.clicked.connect(abrir_archivo) #abre los archivos 
ventanaVisualizacionArchivo.botonEntendidoArchivo.clicked.connect(r_ventanaVisualizacionArchivo_Menu)
Pestañas.botonRegresarPes.clicked.connect(r_pestañas_CursoAsignatura) #boton regresar
CursoAsignatura1.botonEvaluacion.clicked.connect(gui_preguntas)
preguntas.botonPreguntasAbiertas.clicked.connect(gui_ventanaPreguntasAbiertas2)
preguntas.botonPreguntasCerradas.clicked.connect(gui_ventanaPreguntasVF2)
preguntas.botonPreguntasOpcionMultiple.clicked.connect(gui_ventanaPreguntasOM)
Menu.botonExamenRecopilado.clicked.connect(gui_examenRecopilado)
CursoAsignatura1.botonInforme.clicked.connect(gui_informeEstu)
informeEstu.botonRegresarcurso.clicked.connect(r_informeEstu_CursoAsignatura) #boton regresar
examenRecopilado.botonRegresarExamenRecopilado.clicked.connect(r_examenRecopilado_Menu) 
ventanaPreguntasAbiertas2.botonAgregarPreguntaAbierta.clicked.connect(agregar_pregunta_abierta)
ventanaPreguntasVF2.botonAgregarPreguntaVF.clicked.connect(agregar_pregunta_vf)  # Agregar pregunta cerrada
ventanaPreguntasOM.botonAgregarPreguntaOM.clicked.connect(agregar_pregunta_om)
preguntas.botonRegresarPreguntas.clicked.connect(r_preguntas_CursoAsignatura)
informeEstu.verLista.clicked.connect(cargar_informe_estudiantes)
informeEstu.botonActualizar.clicked.connect(actualizar_registro_estudiante)
informeEstu.botonEliminar.clicked.connect(eliminar_registro_estudiante)
contenido.botonAddContenido.clicked.connect(guardar_contenido_en_db)
contenido.botonAddContenido.clicked.connect(gui_mensajeContenidoSubido)
mensajeContenidoSubido.botonEntendidoContenido.clicked.connect(r_mensajeContenidoSubido_cursoAsignatura1)
Pestañas.botonGuardarEnlace.clicked.connect(guardar_enlace_en_db)
mensajeEnlaceSubido.botonEntendidoEnlace.clicked.connect(r_mensajeEnlaceSubido)
ventanaVisualizacionArchivo.cargarEnlaces.clicked.connect(cargar_enlaces_estudiantes)
ventanaVisualizacionArchivo.cargarEnlaces.clicked.connect(cargarTitulos)
ventanaVisualizacionArchivo.cargarEnlaces.clicked.connect(cargarDescripcion)
ventanaVisualizacionArchivo.cargarEnlaces.clicked.connect(cargarAsignaturas_cursoEstudiante)
ventanaVisualizacionArchivo.cargarEnlaces.clicked.connect(gui_ventanaVisualizacionArchivo)
ventanaVisualizacionArchivo.intentarEvaluacion.clicked.connect(gui_examenRecopilado)

# Mostrar la ventana principal y ejecutarla
principal.show()
app.exec()