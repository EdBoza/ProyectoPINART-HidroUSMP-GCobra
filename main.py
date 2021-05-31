from random import randint
from PyQt5.QtGui import QIcon, QFont, QPalette, QImage, QPixmap
from PyQt5.QtCore import (Qt, QDir, QFile, QFileInfo, QPropertyAnimation, QRect,
                          QAbstractAnimation, QTranslator, QLocale, QLibraryInfo)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QMessageBox,
                             QFrame, QLabel, QFileDialog)

# ========================= CLASE Widgets ==========================
class hoverButton(QPushButton):
    def __init__(self, parent=None):
        QPushButton.__init__(self, parent)

        self.setMouseTracking(True)

        self.fuente = self.font()

        self.posicionX = int
        self.posicionY = int

    def enterEvent(self, event):
        self.posicionX = self.pos().x()
        self.posicionY = self.pos().y()

        self.animacionCursor = QPropertyAnimation(self, b"geometry")
        self.animacionCursor.setDuration(100)
        self.animacionCursor.setEndValue(QRect(self.posicionX - 15, self.posicionY - 6, 170, 38))
        self.animacionCursor.start(QAbstractAnimation.DeleteWhenStopped)

        self.fuente.setPointSize(11)
        self.setFont(self.fuente)

    def leaveEvent(self, event):
        self.fuente.setPointSize(10)
        self.setFont(self.fuente)

        self.animacionNoCursor = QPropertyAnimation(self, b"geometry")
        self.animacionNoCursor.setDuration(100)
        self.animacionNoCursor.setEndValue(QRect(self.posicionX, self.posicionY, 140, 28))
        self.animacionNoCursor.start(QAbstractAnimation.DeleteWhenStopped)

class Widgets(QWidget):
    def __init__(self, parent=None):
        super(Widgets, self).__init__(parent)
        self.parent = parent
        self.initUI()
    def initUI(self):
        # ======================== WIDGETS ===========================
        framePrincipal = QFrame(self)
        framePrincipal.setFrameShape(QFrame.Box)
        framePrincipal.setFrameShadow(QFrame.Sunken)
        framePrincipal.setAutoFillBackground(True)
        framePrincipal.setBackgroundRole(QPalette.Light)
        framePrincipal.setFixedSize(662, 503)
        framePrincipal.move(10, 10)

        frame = QFrame(framePrincipal)
        frame.setFixedSize(640, 480)
        frame.move(10, 10)

        self.labelImagen = QLabel(frame)
        self.labelImagen.setAlignment(Qt.AlignCenter)
        self.labelImagen.setGeometry(0, 0, 640, 480)

        self.labelImagenUno = QLabel(frame)
        self.labelImagenUno.setAlignment(Qt.AlignCenter)
        self.labelImagenUno.setGeometry(-650, 0, 640, 480)

        # =================== BOTONES (QPUSHBUTTON) ==================
        self.buttonCargar = hoverButton(self)
        self.buttonCargar.setText(("TUTORIAL"))
        self.buttonCargar.setCursor(Qt.PointingHandCursor)
        self.buttonCargar.setFixedSize(210, 30)
        self.buttonCargar.setAutoDefault(False)
        self.buttonCargar.move(10, 519)


        self.buttonEliminar = hoverButton(self)
        self.buttonEliminar.setText("EJECUTAR PINART")
        self.buttonEliminar.setCursor(Qt.PointingHandCursor)
        self.buttonEliminar.setFixedSize(210, 30)
        self.buttonCargar.setAutoDefault(False)
        self.buttonEliminar.move(220, 519)

        self.buttonExportar = hoverButton(self)
        self.buttonExportar.setText("EXPORT DATA")
        self.buttonExportar.setCursor(Qt.PointingHandCursor)
        self.buttonExportar.setFixedSize(175, 30)
        self.buttonCargar.setAutoDefault(False)
        self.buttonExportar.move(430, 519)

        self.buttonAnterior = QPushButton("<", self)
        self.buttonAnterior.setObjectName("Anterior")
        self.buttonAnterior.setToolTip("Imagen anterior")
        self.buttonAnterior.setCursor(Qt.PointingHandCursor)
        self.buttonAnterior.setFixedSize(30, 30)
        self.buttonAnterior.move(610, 519)

        self.buttonSiguiente = QPushButton(">", self)
        self.buttonSiguiente.setObjectName("Siguiente")
        self.buttonSiguiente.setToolTip("Imagen siguiente")
        self.buttonSiguiente.setCursor(Qt.PointingHandCursor)
        self.buttonSiguiente.setFixedSize(30, 30)
        self.buttonSiguiente.move(642, 519)

        # ===================== CONECTAR SEÑALES =====================

        self.buttonCargar.clicked.connect(self.Cargar)
        self.buttonEliminar.clicked.connect(self.Eliminar)
        self.buttonAnterior.clicked.connect(self.anteriorSiguiente)
        self.buttonSiguiente.clicked.connect(self.anteriorSiguiente)
        self.buttonExportar.clicked.connect(self.Exportar)

        # Establecer los valores predeterminados
        self.posicion = int
        self.estadoAnterior, self.estadoSiguiente = False, False
        self.carpetaActual = QDir()
        self.imagenesCarpeta = []

    # ======================= FUNCIONES ==============================

    def bloquearBotones(self, bool):
        self.buttonCargar.setEnabled(bool)
        self.buttonEliminar.setEnabled(bool)
        self.buttonExportar.setEnabled(bool)
        self.buttonAnterior.setEnabled(bool)
        self.buttonSiguiente.setEnabled(bool)


    def Mostrar(self, label, imagen, nombre, posicionX=650):
        imagen = QPixmap.fromImage(imagen)
        # Escalar imagen a 640x480 si el ancho es mayor a 640 o el alto mayor a 480
        if imagen.width() > 640 or imagen.height() > 480:
            imagen = imagen.scaled(640, 480, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # Mostrar imagen
        label.setPixmap(imagen)
        # Animación (al finalizar la animación se muestra en la barra de estado el nombre y la extensión de la imagen
        # y se desbloquean los botones).
        self.animacionMostar = QPropertyAnimation(label, b"geometry")
        self.animacionMostar.finished.connect(lambda: (self.parent.statusBar.showMessage(nombre),
                                                       self.bloquearBotones(True)))
        self.animacionMostar.setDuration(200)
        self.animacionMostar.setStartValue(QRect(posicionX, 0, 640, 480))
        self.animacionMostar.setEndValue(QRect(0, 0, 640, 480))
        self.animacionMostar.start(QAbstractAnimation.DeleteWhenStopped)

    def Limpiar(self, labelConImagen, labelMostrarImagen, imagen, nombre,
                posicionInternaX, posicionX=None):
        def Continuar(estado):
            if estado:
                if posicionX:
                    self.Mostrar(labelMostrarImagen, imagen, nombre, posicionX)
                else:
                    self.Mostrar(labelMostrarImagen, imagen, nombre)

        self.animacionLimpiar = QPropertyAnimation(labelConImagen, b"geometry")
        self.animacionLimpiar.finished.connect(lambda: labelConImagen.clear())
        self.animacionLimpiar.setDuration(200)
        # self.animacionLimpiar.valueChanged.connect(lambda x: print(x))
        self.animacionLimpiar.stateChanged.connect(Continuar)
        self.animacionLimpiar.setStartValue(QRect(0, 0, 640, 480))
        self.animacionLimpiar.setEndValue(QRect(posicionInternaX, 0, 640, 480))
        self.animacionLimpiar.start(QAbstractAnimation.DeleteWhenStopped)

    def Cargar(self):
        nombreImagen, _ = QFileDialog.getOpenFileName(self, "Seleccionar TUTORIAL",
                                                      QDir.currentPath(),
                                                      "Archivos de imagen (*.jpg *.png *.ico *.bmp)")
        if nombreImagen:
            # Verificar que QLabel tiene imagen
            labelConImagen = ""
            if self.labelImagen.pixmap():
                labelConImagen = self.labelImagen
            elif self.labelImagenUno.pixmap():
                labelConImagen = self.labelImagenUno
            imagen = QImage(nombreImagen)
            if imagen.isNull():
                if labelConImagen:
                    self.Eliminar()
                QMessageBox.information(self, "Visor de imágenes",
                                        "No se puede cargar %s." % nombreImagen)
                return
            # Obtener ruta de la carpeta que contiene la imagen seleccionada
            self.carpetaActual = QDir(QFileInfo(nombreImagen).absoluteDir().path())
            # Obtener la ruta y el nombre de las imagenes que se encuentren en la carpeta de
            # la imagen seleccionada
            imagenes = self.carpetaActual.entryInfoList(["*.jpg", "*.png", "*.ico", "*.bmp", '.gift'],
                                                        QDir.Files, QDir.Name)
            self.imagenesCarpeta = [imagen.absoluteFilePath() for imagen in imagenes]
            self.posicion = self.imagenesCarpeta.index(nombreImagen)
            self.estadoAnterior = True if self.posicion == 0 else False
            self.estadoSiguiente = True if self.posicion == len(self.imagenesCarpeta) - 1 else False
            # Función encargada de bloquear o desbloquear los botones
            self.bloquearBotones(False)
            # Nombre y extensión de la imagen
            nombre = QFileInfo(nombreImagen).fileName()
            if labelConImagen:
                posicionInternaX = -650
                labelMostrarImagen = self.labelImagen if self.labelImagenUno.pixmap() else self.labelImagenUno
                self.Limpiar(labelConImagen, labelMostrarImagen, imagen, nombre, posicionInternaX)
            else:
                self.Mostrar(self.labelImagen, imagen, nombre)

    def Eliminar(self):
        from string import ascii_letters
        import pandas as pd
        import numpy as np
        from matplotlib import pyplot as plt
        import seaborn as sns
        from sklearn.preprocessing import StandardScaler
        from keras.models import Sequential
        from keras.layers import Dense
        # ------------------------------------------------------------------------------------------------
        TodasEstaciones = r"C:\Program Files\Pinart\DatosPrecipitacionesPinart.xlsx"
        df = pd.read_excel(TodasEstaciones, index_col=0)
        # ------------------------------------------------------------------------------------------
        x_train = df.loc['2013-01-01':'2013-12-31', ['Est1', 'Est2', 'Est3', 'Est4', 'Est5']].astype(float).values
        y_train = df.loc['2013-01-01':'2013-12-31', ['Estx']].astype(float).values
        # ----------------------------------------------------------------------------------------------
        scaler = StandardScaler().fit(x_train)
        x_train = scaler.transform(x_train)
        # -----------------------------------------------------------------------------------------------
        model = Sequential()
        model.add(Dense(2, activation='linear', input_shape=(5,)))
        model.add(Dense(4, activation='linear'))
        model.add(Dense(8, activation='linear'))
        model.add(Dense(1, activation='linear'))
        model.summary()
        # -------------------------------------------------------------------------------
        y_pred = model.predict(x_train)
        x_missing = df.loc['2013-01-01':'2013-12-31', ['Est1', 'Est2', 'Est3', 'Est4', 'Est5']].astype(float).values

        scaler = StandardScaler().fit(x_missing)
        x_missing = scaler.transform(x_missing)
        y_missing = model.predict(x_missing)
        y_missing = y_missing.reshape(365).tolist()
        df['Estx_Completed'] = df['Estx']
        df['Estx_Completed'].loc['2013-01-01':'2013-12-31'] = y_missing
        df.plot(subplots=['Est1', 'Est2', 'Est3', 'Est4', 'Est5', 'Estx''Estx_Completed'], figsize=(12, 8));
        plt.legend(loc='best')
        plt.show()


    def Exportar(self):
        from fpdf import FPDF
        from string import ascii_letters
        import pandas as pd
        import numpy as np
        from matplotlib import pyplot as plt
        import seaborn as sns
        from sklearn.preprocessing import StandardScaler
        from keras.models import Sequential
        from keras.layers import Dense
        # ------------------------------------------------------------------------------------------------
        TodasEstaciones = r"C:\Program Files\Pinart\DatosPrecipitacionesPinart.xlsx"
        df = pd.read_excel(TodasEstaciones, index_col=0)
        x_train = df.loc['2013-01-01':'2013-12-31', ['Est1', 'Est2', 'Est3', 'Est4', 'Est5']].astype(float).values
        y_train = df.loc['2013-01-01':'2013-12-31', ['Estx']].astype(float).values
        # ----------------------------------------------------------------------------------------------
        scaler = StandardScaler().fit(x_train)
        x_train = scaler.transform(x_train)
        # -----------------------------------------------------------------------------------------------
        model = Sequential()
        model.add(Dense(2, activation='linear', input_shape=(5,)))
        model.add(Dense(4, activation='linear'))
        model.add(Dense(8, activation='linear'))
        model.add(Dense(1, activation='linear'))
        model.summary()
        # -------------------------------------------------------------------------------
        y_pred = model.predict(x_train)
        x_missing = df.loc['2013-01-01':'2013-12-31', ['Est1', 'Est2', 'Est3', 'Est4', 'Est5']].astype(float).values

        scaler = StandardScaler().fit(x_missing)
        x_missing = scaler.transform(x_missing)
        y_missing = model.predict(x_missing)
        y_missing = y_missing.reshape(365).tolist()
        df['Estx_Completed'] = df['Estx']
        df['Estx_Completed'].loc['2013-01-01':'2013-12-31'] = y_missing
        df.plot(subplots=['Est1', 'Est2', 'Est3', 'Est4', 'Est5', 'Estx''Estx_Completed'], figsize=(12, 8));
        plt.xlabel("Tiempo (Days)")
        plt.ylabel('                                                                                                                     Precipitación (mm)')
        plt.legend(loc='best')
        plt.savefig('grafico.png')
        pdf = FPDF('P', 'mm', 'A4')
        pdf.add_page()
        pdf.set_font('arial', 'BU', 20)
        pdf.cell(60)
        pdf.cell(75, 10, 'Estimación de Datos Faltantes', 0, 2, 'C')
        pdf.cell(75, 10, 'con uso de', 0, 2, 'C')
        pdf.cell(75, 10, 'Inteligencia Artificial', 0, 2, 'C')
        pdf.set_font('arial', 'B', 20)
        pdf.cell(75, 10, 'PINART', 0, 2, 'C')
        pdf.set_font('arial','I', 11)
        pdf.cell(75, 1, '(Precipitación - Inteligencia - Artificial)', 0, 2, 'C')
        pdf.cell(75, 20, 'UNIVERSIDAD SAN MARTIN DE PORRES', 0, 2, 'C')
        pdf.cell(75, 1, 'HIDROLOGÍA', 0, 2, 'C')
        pdf.cell(1, 10, 'Docente:', 0, 2, 'L')
        pdf.cell(1, 10, 'FERNANDO PAZ ZAGACETA', 0, 2, 'L')
        pdf.cell(1, 10, 'Integrantes:', 0, 2, 'L')
        pdf.cell(75, 5, 'MIRZA ELIZABETH APAZA VALDEZ', 0, 2, 'C')
        pdf.cell(75, 5, 'JHEAN PAUL ARIZACA SALDIVAR', 0, 2, 'C')
        pdf.cell(75, 5, 'JESUS SIMON BECERRA MIRANDA', 0, 2, 'C')
        pdf.cell(75, 5, 'JOAN MANUEL BEJAR DINOS', 0, 2, 'C')
        pdf.cell(75, 5, 'EDWIN HEBER BOZA SALAS', 0, 2, 'C')
        pdf.cell(75, 5, 'ANDRES AVELINO CACERES CHICLLASTO', 0, 2, 'C')
        pdf.cell(75, 5, 'ROGGER CELSO CACYA OVIEDO', 0, 2, 'C')
        pdf.cell(75, 10, '', 0, 2, 'C')
        pdf.set_font('arial', 'BU', 15)
        pdf.cell(75, 10, 'RESULTADOS EXPORTADOS DE PINART', 0, 2, 'C')
        pdf.cell(75, 10, '', 0, 2, 'C')
        pdf.cell(-55)
        pdf.set_font('arial', 'B', 11)

        columnNameList = list(df.columns)
        for header in columnNameList[:-1]:
            pdf.cell(25, 10, header, 1, 0, 'C')
        pdf.cell(25, 10, columnNameList[-1], 1, 1, 'C')
        pdf.cell(5)
        pdf.set_font('arial', '', 11)
        for row in range(0, len(df)):
            for col_num, col_name in enumerate(columnNameList):
                if col_num != len(columnNameList) - 1:
                    pdf.cell(25, 10, str(df['%s' % (col_name)].iloc[row]), 1, 0, 'C')

                else:
                    pdf.cell(25, 10, str(df['%s' % (col_name)].iloc[row]), 1, 1, 'C')
                    pdf.cell(5)
        pdf.add_page('l')

        pdf.set_font('arial', 'BU', 15)
        pdf.cell(75, 1, 'GRÁFICA PINART', 0, 2, 'C')
        pdf.image("grafico.png", 0,15, 300)
        pdf.output('tuto1.pdf', 'F')

    def anteriorSiguiente(self):
        if self.imagenesCarpeta:
            widget = self.sender().objectName()

            if widget == "Anterior":
                self.estadoAnterior = True if self.posicion == 0 else False
                self.estadoSiguiente = False

                self.posicion -= 1 if self.posicion > 0 else 0
                posicionInternaX, posicionX = 650, -650
            else:
                self.estadoSiguiente = True if self.posicion == len(self.imagenesCarpeta) - 1 else False
                self.estadoAnterior = False

                self.posicion += 1 if self.posicion < len(self.imagenesCarpeta) - 1 else 0
                posicionInternaX, posicionX = -650, 650

            if self.estadoAnterior or self.estadoSiguiente:
                return
            else:
                imagen = self.imagenesCarpeta[self.posicion]

                # Verificar que la carpeta que contiene la imagene exista
                if not QDir(self.carpetaActual).exists():
                    self.Eliminar()
                    return
                elif not QFile.exists(imagen):
                    # Obtener la ruta y el nombre de las imagenes que se encuentren en la
                    # carpeta de la imagen seleccionada
                    imagenes = self.carpetaActual.entryInfoList(["*.jpg", "*.png", "*.ico", "*.bmp"],
                                                                QDir.Files, QDir.Name)

                    if not imagenes:
                        self.Eliminar()
                        return

                    self.imagenesCarpeta = [imagen.absoluteFilePath() for imagen in imagenes]

                    self.posicion = randint(0, len(self.imagenesCarpeta) - 1)
                    self.estadoAnterior = True if self.posicion == 0 else False
                    self.estadoSiguiente = True if self.posicion == len(self.imagenesCarpeta) - 1 else False
                elif QImage(imagen).isNull():
                    del self.imagenesCarpeta[self.posicion]

                    if not self.imagenesCarpeta:
                        self.Eliminar()
                        return

                    self.posicion = randint(0, len(self.imagenesCarpeta) - 1)
                    self.estadoAnterior = True if self.posicion == 0 else False
                    self.estadoSiguiente = True if self.posicion == len(self.imagenesCarpeta) - 1 else False

                imagen = self.imagenesCarpeta[self.posicion]

                if self.labelImagen.pixmap():
                    labelConImagen = self.labelImagen
                elif self.labelImagenUno.pixmap():
                    labelConImagen = self.labelImagenUno

                # Función encargada de bloquear o desbloquear los botones
                self.bloquearBotones(False)

                # Nombre y extensión de la imagen
                nombre = QFileInfo(imagen).fileName()

                # Label en el que se va a mostrar la imagen
                labelMostrarImagen = self.labelImagen if self.labelImagenUno.pixmap() else self.labelImagenUno

                # Quitar la imagen actual y mostrar la siguiente
                self.Limpiar(labelConImagen, labelMostrarImagen, QImage(imagen),
                             nombre, posicionInternaX, posicionX)
# ====================== CLASE visorImagenes =======================
class visorImagenes(QMainWindow):
    def __init__(self, parent=None):
        super(visorImagenes, self).__init__(parent)

        self.setWindowIcon(QIcon(r"C:\Program Files\Pinart\icon\pinart.png"))
        self.setWindowTitle("PINART                                                            Universidad San Martin de Porres                  ")
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
        self.setFixedSize(682, 573)
        self.initUI()
    def initUI(self):
        # ===================== LLAMAR WIDGETS =======================

        widget = Widgets(self)
        self.setCentralWidget(widget)

        # =============== BARRA DE ESTADO (STATUSBAR) ================

        labelVersion = QLabel(self)
        labelVersion.setText("ING: Fernando Paz           G-COBRA: Mirza A. - Jhean A. - Jesus B. - Joan B. - Edwin B. - Andres A. - Rogger C.  ")


        self.statusBar = self.statusBar()
        self.statusBar.addPermanentWidget(labelVersion, 0)
# ==================================================================

if __name__ == '__main__':
    import sys
    aplicacion = QApplication(sys.argv)

    traductor = QTranslator(aplicacion)
    lugar = QLocale.system().name()
    path = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
    traductor.load("qtbase_%s" % lugar, path)
    aplicacion.installTranslator(traductor)

    fuente = QFont()
    fuente.setPointSize(10)
    aplicacion.setFont(fuente)

    ventana = visorImagenes()
    ventana.show()
    sys.exit(aplicacion.exec_())


