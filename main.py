"""
Este programa contiene la interfaz gráfica del analizador de línea
del sistema de distribución de energía eléctrica de 4 nodos


Programa: Ingeniería Eléctrica
Asignatura: Análisis de señales
Universidad Tecnológica de Pereira
"""

# Librería y módulos necesarios
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox as mb  # Mensajes en la interfaz gráfica
from tkinter import Entry, ttk, Tk, Frame, Button, Text, INSERT  # Crear interfaz con widgets
import numpy as np
import time  # Para generar el temporizador (reloj)
from analizador import Analizador  # Módulo analizador
import requests
from tabulate import tabulate
import os


# Se define la función principal que contiene la interfaz gráfica:
def main():
    """
    Esta función ejecuta a la interfaz grpafica del analizador.
    :return: Interfaz del analizador.
    """
    root = Tk()  # Crea la ventana de la interfaz
    root.title("ANALIZADOR DE LÍNEA")  # Nombre de la ventana
    frame = Frame(highlightbackground="black", highlightthickness=22)  # Contorno de la ventana
    frame.pack(fill="both", expand=True)  # Posición del contorno
    frame.config(bg="orange", relief="flat", bd=22, cursor="spider")  # Personalización del contono
    gui = Interfaz(root)  # Clase Interfaz
    gui.root.mainloop()  # Mantiene la ejecución continua de la interfaz


def restart():
    """
    Este método reinicia los valores del analizador con su interfaz.
    :return:
    """
    os.execl(sys.executable, sys.executable, *sys.argv)


# Creando la clase interfaz
class Interfaz:
    """
    Esta es la clase Interfaz, la cual se encarga de presentar en pantalla
    las gráficas de las señales y algunos valores importantes de las mismas.
    """

    def __init__(self, root):
        """
        Inicializador de la clase Interfaz
        :param root: Ventana de la interfaz gráfica de usuario (GUI)
        """

        # Atributos de la clase:
        self.root = root
        self.root.geometry('1350x800')  # Dimensiones de la ventana
        self.root.resizable(0, 0)  # No deja modificar las dimensiones de la pantalla
        self.plot_empty()  # Muestra en pantalla el espacio donde van las gráficas
        self.message_data()  # Muestra en pantalla el espacio donde van los datos

        # Se extraen los datos de las señales a analizar:
        self.url = 'https://raw.githubusercontent.com/JulianDPastrana/signal_analysis/main/seniales_sep.py'
        self.r = requests.get(self.url)

        with open('seniales_sep.py', 'w') as f:
            f.write(self.r.text)
        from seniales_sep import signal_generation

        self.data = signal_generation()

        # Señales extraídas:
        self.V1, self.I1 = self.data["Node 1"]
        self.V2, self.I2 = self.data["Node 2"]
        self.V3, self.I3 = self.data["Node 3"]
        self.V = [self.V1, self.V2, self.V3]
        self.I = [self.I1, self.I2, self.I3]

        # Usamos la clase Analizador:
        self.analizador = Analizador(self.V, self.I)

        # Corrientes en el nodo 4:
        self.I_n4 = self.I[0] + self.I[1] + self.I[2]

        self.pinst = self.analizador.pot_instantanea()
        self.tabla_rms = self.analizador.tabla_rms()
        self.tabla_inpedancia = self.analizador.impedancias()
        self.P = self.analizador.pot_activa()
        self.Q = self.analizador.pot_reactiva()
        self.tabla_pot = self.analizador.tabla_potencias()

        # Se crean los widgets de la GUI

        # ------------  Selector de Señales --------------------

        style = ttk.Style()  # Define el estilo
        style.configure("BW.TLabel", foreground="black", background="orange", font=("Helvetica", 10, "bold"))
        self.select_label = ttk.Label(self.root, text="SELECTOR DE SEÑALES", style="BW.TLabel").place(x=23, y=100)
        self.select_graph = ttk.Combobox(self.root,
                                         values=['  ', 'Voltajes 3Ø', "Corrientes 3Ø", "Corrientes N4", "Lissajous",
                                                 "Lissajous nodo 4", "Triangulos Potencia", 'Potencias Instantaneas',
                                                 "Diagrama V_fasorial", "Diagrama I_fasorial"])

        self.select_graph.place(x=23, y=120)  # Posiciona al selector de señales
        self.select_graph.current(0)
        self.select_graph.bind("<Key>", lambda a: "break")  # Bloquea edición por parte del usuario

        # ----------- Selector de Datos-----------------------

        style = ttk.Style()
        style.configure("BW.TLabel", foreground="black", background="orange", font=("Helvetica", 10, "bold"))
        self.select_label = ttk.Label(self.root, text="SELECTOR DE DATOS", style="BW.TLabel").place(x=23, y=440)
        self.select_data = ttk.Combobox(self.root,
                                        values=['  ', 'Valores RMS', "Datos de Potencia", "Valores de Impedancias",
                                                "Energía"])

        self.select_data.place(x=23, y=460)
        self.select_data.current(0)
        self.select_data.bind("<Key>", lambda a: "break")

        # -------------- Botones ---------------------------

        # Botón generador de señales y de datos
        self.generate = Button(self.root, text="GENERAR", command=self.update, foreground="black", bg="green",
                               font=("Helvetica", 10, "bold"))
        self.generate.place(x=23, y=600)  # command=self.update,

        # Botón que apaga al analizador.
        self.turnoff = Button(self.root, text="APAGAR", command=root.destroy, foreground="black", bg="red",
                              font=("Helvetica", 10, "bold"))
        self.turnoff.place(x=230, y=600)

        # Botón de reinicio del analizador
        self.reset = Button(self.root, text="REINICIAR", command=restart, foreground="black", bg="gray",
                            font=("Helvetica", 10, "bold"))
        self.reset.place(x=128, y=600)

        # Temporizador
        self.label = ttk.Label(text="", font=('Times New Roman', 20))
        self.label.place(x=675, y=600)
        self.actualizar_tiempo()
        self.tiempo_actual = time.strftime("%H:%M:%S")  # Inicializar el tiempo
        # Extrae los valores de hora, minutos y segundos
        self.hora = int(self.tiempo_actual[:2])
        self.minutos = int(self.tiempo_actual[3:5])
        self.segundos = int(self.tiempo_actual[6:])

    def actualizar_tiempo(self):
        """
        Este método actualiza el tiempo del reloj
        :return: Tiempo
        """
        self.tiempo_actual = time.strftime("%H:%M:%S")
        self.label.configure(text=self.tiempo_actual)
        self.root.after(1000, self.actualizar_tiempo)  # Actualiza el tiempo constantemente

    # ----------- Gráficas de las señales -------------------------------

    def plot_empty(self):
        """
        Crea un gráfico vacío que se pondrá cuando se ejecute la función main.
        :return: Contorno de gráfica.
        """
        Emptyfig = plt.figure(figsize=(6.5, 6.5), dpi=80)
        plt.grid()
        chart = FigureCanvasTkAgg(Emptyfig, master=self.root)
        chart.get_tk_widget().place(x=210, y=60)

    def plot_voltages(self):
        """
        Método que contiene las gráficas de las señales de los voltajes trifásicos en los nodos.
        :return: Gráficas de voltajes.
        """
        fig, axs = plt.subplots(3, 1, figsize=(6.5, 6.5), dpi=80)  # Se crea la figura
        axs[0].plot(self.V[0].T)  # Grafica las señales de voltaje en el nodo 1
        axs[0].set_title("Tensiones en los nodos 1, 2 y 3")
        axs[0].legend(["Fase A", "Fase B", "Fase C"])

        axs[1].plot(self.V[1].T)  # Grafica las señales de voltaje en el nodo 2
        axs[1].legend(["Fase A", "Fase B", "Fase C"])
        axs[2].plot(self.V[2].T)  # Grafica las señales de voltaje en el nodo 3
        axs[2].legend(["Fase A", "Fase B", "Fase C"])
        axs[0].set_ylabel('Amplitud [V]')
        axs[1].set_ylabel('Amplitud [V]')
        axs[2].set_ylabel('Amplitud [V]')
        axs[0].grid()
        axs[1].grid()
        axs[2].grid()

        # Poner las gráficas en la GUI
        chart = FigureCanvasTkAgg(fig, master=self.root)
        chart.get_tk_widget().place(x=210, y=60)

    def plot_currents(self):
        """
        Método que contiene las gráficas de las señales de las corrientes trifásicas en los nodos.
        :return: Gráficas de corrientes.
        """
        fig, axs = plt.subplots(3, 1, figsize=(6.5, 6.5), dpi=80)  # Se crea la figura
        axs[0].plot(self.I[0].T)  # Grafica las señales de corrientes en el nodo 1
        axs[0].set_title("Corrientes en los nodos 1, 2 y 3")
        axs[0].legend(["Fase A", "Fase B", "Fase C"])
        axs[0].set_ylabel('Amplitud [A]')
        axs[0].grid()
        axs[1].plot(self.I[1].T)  # Grafica las señales de corriente en el nodo 2

        axs[1].legend(["Fase A", "Fase B", "Fase C"])
        axs[1].set_ylabel('Amplitud [A]')
        axs[1].grid()
        axs[2].plot(self.I[2].T)  # Grafica las señales de corriente en el nodo 3

        axs[2].legend(["Fase A", "Fase B", "Fase C"])
        axs[2].set_ylabel('Amplitud [A]')
        axs[2].grid()
        chart = FigureCanvasTkAgg(fig, master=self.root)
        chart.get_tk_widget().place(x=210, y=60)

    def plot_node4(self):
        """
        Este método contiene las señales de corrientes en el nodo 4
        :return: Gráfica de corrientes en el nodo 4.
        """
        fig, axs = plt.subplots(1, 1, figsize=(6.5, 6.5), dpi=80)  # Se crea la figura
        axs.plot(self.I_n4.T)  # Grafica las señales de corriente en el nodo 4
        axs.set_title("Corrientes en el Nodo 4")
        axs.legend(["Fase A", "Fase B", "Fase C"])
        axs.set_ylabel('Amplitud [A]')
        plt.grid()
        chart = FigureCanvasTkAgg(fig, master=self.root)
        chart.get_tk_widget().place(x=210, y=60)

    def plot_lissajous(self):
        """
        Este método contiene las gráficas de Lissajous en los nodos 1, 2 y 3.
        :return: Gráficas de Lissajous.
        """
        fig, axs = plt.subplots(3, 1, figsize=(6.5, 6.5), dpi=80)  # Se crea la figura
        axs[0].plot(self.V[0].T, self.I[0].T)  # Grafica las señales de Lissajous en el nodo 1
        axs[0].set_title("Diagramas de Lissajous en los nodos 1, 2 y 3")
        axs[0].legend(["Fase A", "Fase B", "Fase C"])
        axs[0].grid()

        axs[1].plot(self.V[1].T, self.I[1].T)  # Grafica las señales de Lissajous en el nodo 2

        axs[1].legend(["Fase A", "Fase B", "Fase C"])
        axs[1].grid()

        axs[2].plot(self.V[2].T, self.I[2].T)  # Grafica las señales de Lissajous en el nodo 3

        axs[2].legend(["Fase A", "Fase B", "Fase C"])
        axs[2].set_xlabel('$V$ [V]')
        axs[2].grid()
        axs[0].set_ylabel('$I$ [A]')
        axs[1].set_ylabel('$I$ [A]')
        axs[2].set_ylabel('$I$ [A]')

        chart = FigureCanvasTkAgg(fig, master=self.root)
        chart.get_tk_widget().place(x=210, y=60)

    def plot_lissajous_nodo4(self):
        """
        Este método contiene las gráficas de Lissajous del nodo 4.
        :return: Gráficas de Lissajous.
        """

        Y = (1 / self.analizador.Zl1) + (1 / self.analizador.Zl2) + (1 / self.analizador.Zl3)
        V4 = (self.I_n4 + (self.V[0] / self.analizador.Zl1) + (self.V[1] / self.analizador.Zl2) + (
                self.V[2] / self.analizador.Zl3)) / Y

        fig, axs = plt.subplots(1, 1, figsize=(6.5, 6.5), dpi=80)  # Se crea la figura
        axs.plot(abs(V4).T, self.I_n4.T)  # Gráfica de Lissajous en el nodo 4
        axs.set_title("Diagramas de Lissajous en el nodo 4")
        axs.legend(["Fase A", "Fase B", "Fase C"])
        axs.grid()
        chart = FigureCanvasTkAgg(fig, master=self.root)
        chart.get_tk_widget().place(x=210, y=60)

    def plot_phasor_voltage(self):
        """
        Este método contiene los diagramas fasoriales de las tensiones.
        :return: Diagramas fasoriales de tensiones.
        """
        fig = self.analizador.voltajes_fasorial()
        chart = FigureCanvasTkAgg(fig, master=self.root)
        chart.get_tk_widget().place(x=210, y=60)

    def plot_powertriangles(self):
        """
        Este método contiene los triángulos de potencia
        :return: Gráfica de triángulos de potencia.
        """
        # Potencias:
        P = self.P
        Q = self.Q

        fig, ax = plt.subplots(3, 1, figsize=(6.5, 6.5), dpi=80)
        ax[0].quiver(0, 0, P[0], 0, angles='xy', color=['green'], scale_units='xy', scale=1, label='P')
        ax[0].quiver(P[0], 0, 0, Q[0], angles='xy', color=['purple'], scale_units='xy', scale=1, label='Q')
        ax[0].quiver(0, 0, P[0], Q[0], angles='xy', color=['red'], scale_units='xy', scale=1, label='S')
        ax[0].set_ylim(-Q[0] * 0.1, Q[0] * 1.1)
        plt.axis([0, P[0] + 10, -10, Q[0] + 10])
        ax[0].set_xlim(-P[0] * 0.1, P[0] * 1.1)
        ax[0].set_title("Triángulos de potencia en los nodos 1, 2 y 3")

        ax[1].quiver(0, 0, P[1], 0, angles='xy', color=['green'], scale_units='xy', scale=1, label='P')
        ax[1].quiver(P[1], 0, 0, Q[1], angles='xy', color=['purple'], scale_units='xy', scale=1, label='Q')
        ax[1].quiver(0, 0, P[1], Q[1], angles='xy', color=['red'], scale_units='xy', scale=1, label='S')
        ax[1].set_ylim(-Q[1] * 0.1, Q[1] * 1.1)
        plt.axis([0, P[1] + 10, -10, Q[1] + 10])
        ax[1].set_xlim(-P[1] * 0.1, P[1] * 1.1)

        ax[2].quiver(0, 0, P[2], 0, angles='xy', color=['green'], scale_units='xy', scale=1, label='P')
        ax[2].quiver(P[2], 0, 0, Q[2], angles='xy', color=['purple'], scale_units='xy', scale=1, label='Q')
        ax[2].quiver(0, 0, P[2], Q[2], angles='xy', color=['red'], scale_units='xy', scale=1, label='S')
        ax[2].set_ylim(-Q[2] * 0.1, Q[2] * 1.1)
        plt.axis([0, P[2] + 10, -10, Q[2] + 10])
        ax[2].set_xlim(-P[2] * 0.1, P[2] * 1.1)

        ax[0].legend(loc='upper left')
        ax[0].grid()
        ax[1].legend(loc='upper left')
        ax[1].grid()
        ax[2].legend(loc='upper left')
        ax[2].grid()
        chart = FigureCanvasTkAgg(fig, master=self.root)
        chart.get_tk_widget().place(x=210, y=60)

    def plot_powerInstant(self):
        """
        Este método contiene las señales de potencias instantáneas.
        :return: Gráfico de potencias instantáneas.
        """
        fig, axs = plt.subplots(3, 1, figsize=(6.5, 6.5), dpi=80)  # Se crea la figura
        axs[0].plot(self.pinst[0].T)  # Grafica las señales de potencias instantáneas nodo 1

        axs[0].set_title("Potencias instantaneas en los nodos 1, 2 y 3")
        axs[0].legend(["Fase A", "Fase B", "Fase C"])
        axs[0].set_ylabel('Amplitud')
        axs[0].grid()

        axs[1].plot(self.pinst[1].T)  # Grafica las señales de potencias instantáneas nodo 2
        axs[1].legend(["Fase A", "Fase B", "Fase C"])
        axs[1].set_ylabel('Amplitud')
        axs[1].grid()

        axs[2].plot(self.pinst[2].T)  # Grafica las señales de potencias instantáneas nodo 3
        axs[2].legend(["Fase A", "Fase B", "Fase C"])
        axs[2].grid()
        axs[2].set_ylabel('Amplitud')

        chart = FigureCanvasTkAgg(fig, master=self.root)
        chart.get_tk_widget().place(x=210, y=60)

    def plot_phasor_current(self):
        """
        Este método contiene los diagramas fasoriales de la corrientes.
        :return: Gráfica de diagramas fasoriales de corrientes.
        """
        fig = self.analizador.corrientes_fasorial()
        chart = FigureCanvasTkAgg(fig, master=self.root)
        chart.get_tk_widget().place(x=210, y=60)

        # -------- Seleccionando la señal -----------------------

    def change_signal(self):
        """
        Este método grafica la señal seleccionada en el selector de señales.
        :return: Gráfico del selector.
        """
        if self.select_graph.get() == '  ':
            self.plot_empty()

        elif self.select_graph.get() == 'Voltajes 3Ø':
            self.plot_voltages()

        elif self.select_graph.get() == 'Corrientes 3Ø':
            self.plot_currents()

        elif self.select_graph.get() == 'Corrientes N4':
            self.plot_node4()

        elif self.select_graph.get() == 'Lissajous':
            self.plot_lissajous()

        elif self.select_graph.get() == "Diagrama V_fasorial":
            self.plot_phasor_voltage()

        elif self.select_graph.get() == "Diagrama I_fasorial":
            self.plot_phasor_current()

        elif self.select_graph.get() == 'Triangulos Potencia':
            self.plot_powertriangles()

        elif self.select_graph.get() == 'Potencias Instantaneas':
            self.plot_powerInstant()

        elif self.select_graph.get() == 'Lissajous nodo 4':
            self.plot_lissajous_nodo4()

    # -------- Generación de los datos de las señales -------
    def Table_rms(self):
        """
        Método que contiene la tabla de datos RMS de las señales (V e I).
        :return: Tabla con voltajes y corrientes RMS.
        """
        Data1 = Text(self.root, background="white", width=71, height=10, cursor='none')
        Data1.config(state="normal")
        Data1.place(x=740, y=60)
        Data1.edit_modified(arg=False)
        Data1.bind("<Key>", lambda a: "break")
        Data1.insert(INSERT, self.tabla_rms)

    def Table_power(self):
        """
        Este método contiene la tabla de valores de potencias del sistema.
        :return: Tabla con los valores de potencias.
        """
        Data2 = Text(self.root, background="white", width=71, height=10, cursor='none')
        Data2.config(state="normal")
        Data2.place(x=740, y=60)
        Data2.edit_modified(arg=False)
        Data2.bind("<Key>", lambda a: "break")
        Data2.insert(INSERT, self.tabla_pot)

    def table_energy(self):
        """
        Este método contiene la tabla con los valores de energía en las cargas con su costo total.
        :return: Tabla con valores de energía en las cargas y su costo total.
        """

        P_inst = []
        P = []

        for i in range(len(self.I)):
            p_inst1 = self.V[0][i] * self.I[0][i]
            p_inst2 = self.V[1][i] * self.I[1][i]
            p_inst3 = self.V[2][i] * self.I[2][i]
            p = [p_inst1, p_inst2, p_inst3]

            P_inst.append(p)

        for i in P_inst:
            act_power1 = abs(np.mean(i[0])) / 1000
            act_power2 = abs(np.mean(i[1])) / 1000
            act_power3 = abs(np.mean(i[2])) / 1000
            act_power = [act_power1, act_power2, act_power3]
            P.append(act_power)

        E = []  # Lista que contiene los valores de energía.
        for i in range(len(P)):
            e1 = P[0][i] * self.hora + P[0][i] * self.minutos / 60 + P[0][i] * self.segundos / 3600
            e2 = P[1][i] * self.hora + P[1][i] * self.minutos / 60 + P[1][i] * self.segundos / 3600
            e3 = P[2][i] * self.hora + P[2][i] * self.minutos / 60 + P[2][i] * self.segundos / 3600
            e = [e1, e2, e3]  # energía total
            E.append(e)
        e1a, e1b, e1c = np.round(E[0][0], 2), np.round(E[0][1], 2), np.round(E[0][2], 2)
        e2a, e2b, e2c = np.round(E[1][0], 2), np.round(E[1][1], 2), np.round(E[1][2], 2)
        e3a, e3b, e3c = np.round(E[2][0], 2), np.round(E[2][1], 2), np.round(E[2][2], 2)
        e1t = np.round(e1a + e1b + e1c, 2)
        e2t = np.round(e2a + e2b + e2c, 2)
        e3t = np.round(e3a + e3b + e3c, 2)
        et = np.round(e1t + e2t + e3t, 2)
        ct1 = np.round(800 * e1t, 2)
        ct2 = np.round(800 * e2t, 2)
        ct3 = np.round(800 * e3t, 2)
        ct = ct1 + ct2 + ct3
        tabla = tabulate([
            ['Ea [kWh]', e1a, e2a, e3a, '-'],
            ['Eb [kWh]', e1b, e2b, e3b, '-'],
            ['Ec [kWh]', e1c, e2c, e3c, '-'],
            ['Etotal [kWh]', e1t, e2t, e3t, et],
            ['Costo $800/kWh', '  ', ' ', ' ', ' '],
            ['Costo total', '$' + str(ct1), '$' + str(ct2), '$' + str(ct3), '$' + str(ct)]],
            headers=["Energía", "Nodo 1 ", "Nodo 2 ", "Nodo 3 ", "Total"], tablefmt="fancy_outline")
        datos = Text(self.root, background="white", width=71, height=10, cursor='none')
        datos.config(state="normal")
        datos.place(x=740, y=60)
        datos.edit_modified(arg=False)
        datos.bind("<Key>", lambda a: "break")
        datos.insert(INSERT, tabla)

    def Table_impedance(self):
        """
        Este método contiene la tabla con los valores de impedancia en las cargas.
        :return: Tabla con valores de impedancias de carga.
        """
        Data3 = Text(self.root, background="white", width=71, height=10, cursor='none')
        Data3.config(state="normal")
        Data3.place(x=740, y=60)
        Data3.edit_modified(arg=False)
        Data3.bind("<Key>", lambda a: "break")
        Data3.insert(INSERT, self.tabla_inpedancia)

    def message_data(self):
        """
        Este método contiene un mensaje inicial donde aparecerán los datos seleccionados
        del selector de datos.
        :return: Mensaje inicial en pantalla.
        """
        message = "\n\n   -------------------------------------------- \n\n" \
                  "   Aquí aparecen las tablas con los datos del\n      " \
                  "   Selector de datos  \n\n" \
                  "   --------------------------------------------"
        Data = Text(self.root, background="white", width=71, height=10, cursor='none')
        Data.config(state="normal")
        Data.place(x=740, y=60)
        Data.edit_modified(arg=False)
        Data.bind("<Key>", lambda a: "break")
        Data.insert(INSERT, message)

        ## ----------- Selección de los datos -----------------------------

    def change_data(self):
        """
        Este método muestra en pantalla los datos seleccionados del selector de datos.
        :return: Datos seleccionados del Selector de datos.
        """
        if self.select_data.get() == '  ':
            self.message_data()
        if self.select_data.get() == 'Valores RMS':
            self.Table_rms()
        elif self.select_data.get() == "Datos de Potencia":
            self.Table_power()

        elif self.select_data.get() == "Valores de Impedancias":
            self.Table_impedance()

        elif self.select_data.get() == "Energía":
            self.table_energy()
        ## ---------- Updating Values and Graphics -------------------

    def update(self, event=None):
        """
        Este método es usado por el Botón Generar, para mostrar las señales y los datos seleccionados.
        :param event: Evento que se presenta (inicialmente no hay evento).
        :return: Actualización de los selectores.
        """
        self.change_signal()
        self.change_data()


# Salvaguarda:
if __name__ == '__main__':
    # Prueba de la Interfaz:
    main()  # Ejecutando la interfaz del analizador
