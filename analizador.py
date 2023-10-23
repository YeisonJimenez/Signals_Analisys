"""
Este programa es un analizador de línea de un sistema de distribución de
energía de 4 nodos.


Programa: Ingeniería Eléctrica
Asignatura: Análisis de señales
Universidad Tecnológica de Pereira
"""

# Importación de las librerías y módulos necesarios
import requests  # Para importar las señales de Github
import matplotlib.pyplot as plt  # Para las gráficas
import numpy as np  # Cálculos matemáticos
from matplotlib.figure import Figure  # Personalizar figuras
from tabulate import tabulate  # Crear tablas


# Creando el objeto Analizador
class Analizador:
    """
    Esta es la clase Analizador, la cual se encarga de analizar un sistema de distribución de energía
    de 4 nodos.
    """

    def __init__(self, V, I):
        """
        Método que inicializa la clase. También conocido como Constructor.
        :param V: Voltajes en los nodos
        :param I: Corrientes en los nodos
        """
        # Atributos de la clase
        # Voltajes y corrientes en los nodos:
        self.V = V  # Vector de voltajes
        self.I = I  # Vector de corrientes
        self.Zl1 = 0.009  # Impedancia en la línea 1
        self.Zl2 = 0.01  # Impedancia en la línea 2
        self.Zl3 = 0.01 + 0.001j  # Impedancia en la línea 3

    # -------------------------------------------------------
    # Métodos de la clase Analizador:
    # Cálculo de los voltajes RMS
    def v_rms(self):
        """
        Este método calcula los valores RMS de voltajes en los nodos.
        :param V: Arreglo de voltajes en los nodos
        :return: El valor RMS de las tensiones
        """
        V_rms = []  # Lista que contiene los valores RMS
        for i in range(len(self.V)):  # Ciclo que calcula los valores RMS
            quad_array = self.V[i] ** 2  # Eleva al cuadrado el arreglo de Voltajes
            rms_value = np.sqrt(np.mean(quad_array))
            V_rms.append(np.round(rms_value, 4))  # Agrega los valores a la lista V_rms

        return np.round(V_rms, 4)

    def i_rms(self):
        """
        Este método calcula los valores RMS de corrientes en los nodos.
        :return: El valor RMS de las corrientes
        """

        I_rms = []
        for i in range(len(self.I)):
            quad_array = self.I[i] ** 2
            rms_value = np.sqrt(np.mean(quad_array[i]))
            I_rms.append(rms_value)
        return np.round(I_rms, 4)

    def __rms(self, v):
        """
        Este método cálcula el verdadero valor RMS de una señal
        :param v: señal para determinar su RMS
        :return: El valor RMS de v
        """
        quad = v ** 2
        rmsval = np.sqrt(np.mean(quad))
        return rmsval

    def tabla_rms(self):
        """
        Este método retorna la tabla con los valores RMS de las corrientes y tensiones
        de fase en cada uno de los nodos.
        :return: Tabla con verdaderos valores RMS.
        """
        v = self.V / np.sqrt(3)
        i = self.I / np.sqrt(3)
        V1a, I1a = Analizador.__rms(self, v[0][0]), Analizador.__rms(self, i[0][0])
        V1b, I1b = Analizador.__rms(self, v[0][1]), Analizador.__rms(self, i[0][1])
        V1c, I1c = Analizador.__rms(self, v[0][2]), Analizador.__rms(self, i[0][2])
        V2a, I2a = Analizador.__rms(self, v[1][0]), Analizador.__rms(self, i[1][0])
        V2b, I2b = Analizador.__rms(self, v[1][1]), Analizador.__rms(self, i[1][1])
        V2c, I2c = Analizador.__rms(self, v[1][2]), Analizador.__rms(self, i[1][2])
        V3a, I3a = Analizador.__rms(self, v[2][0]), Analizador.__rms(self, i[2][0])
        V3b, I3b = Analizador.__rms(self, v[2][1]), Analizador.__rms(self, i[2][1])
        V3c, I3c = Analizador.__rms(self, v[2][2]), Analizador.__rms(self, i[2][2])
        I_n4 = self.I[0] + self.I[1] + self.I[2]  # Corrientes en el nodo 4
        Y = (1 / self.Zl1) + (1 / self.Zl2) + (1 / self.Zl3)
        V4 = (I_n4 + (self.V[0] / self.Zl1) + (self.V[1] / self.Zl2) + (self.V[2] / self.Zl3)) / Y
        V4a, I4a = Analizador.__rms(self, abs(V4[0])), Analizador.__rms(self, I_n4[0])
        V4b, I4b = Analizador.__rms(self, abs(V4[1])), Analizador.__rms(self, I_n4[1])
        V4c, I4c = Analizador.__rms(self, abs(V4[2])), Analizador.__rms(self, I_n4[2])
        tabla = tabulate([
            ['Va [V]', V1a, V2a, V3a, V4a],
            ['Vb [V]', V1b, V2b, V3b, V4b],
            ['Vc [V]', V1c, V2c, V3c, V4c],
            ['Ia [A]', I1a, I2a, I3a, I4a],
            ['Ib [A]', I1b, I2b, I3b, I4b],
            ['Ic [A]', I1c, I2c, I3c, I4c]],
            headers=["Fase", "Nodo 1", "Nodo 2", "Nodo 3", "Nodo 4"], tablefmt="fancy_outline")
        return tabla

    def tabla_rms_nodo(self):
        vrms = Analizador.v_rms(self)
        irms = Analizador.i_rms(self)
        N1v = vrms[0]
        N2v = vrms[1]
        N3v = vrms[2]
        N1i = irms[0]
        N2i = irms[1]
        N3i = irms[2]

        tabla = tabulate([
            ['1', N1v, N1i],
            ['2', N2v, N2i],
            ['3', N3v, N3i]],
            headers=["Nodo ", "Voltajes [V]", "Corrientes [A]"], tablefmt="fancy_outline")
        return tabla

    def pot_instantanea(self):
        """
        Este método calcula las potencias instantáneas en los nodos.
        :return: Potencias instantáneas
        """
        P_inst = []  # Vector que va a contener las potencias instantáneas
        for i in self.V:  # Ciclo que calcula las potencias instantáneas
            for j in self.I:
                p_inst = i * j
                P_inst.append(p_inst)
        return P_inst

    def pot_activa(self):
        """
        Este método calcula las potencias activas en los nodos.
        :return: Potencias activas en los nodos
        """

        P = []  # Lista que contiene las potencias activas en los nodos
        for i in range(len(self.I)):  # ciclo que calcula las potencias activas
            # Valor medio de la potencia instantánea
            act_power = abs(np.mean(Analizador.pot_instantanea(self)[i]))
            P.append(act_power)
        return np.round(P, 4)

    def pot_reactiva(self):
        """
        Este método calcula la potencia reactiva en los nodos.
        :return: Los valores de potencias reactivas.
        """
        P = abs(self.pot_activa())  # Potencias activas
        Irms = self.i_rms()  # Corrientes RMS
        Vrms = self.v_rms()  # Voltajes RMS
        S = []  # Lista que contiene las potencias aparentes en los nodos
        Q = []  # Lista que contiene las potencias reactivas en llos nodos
        for i in range(len(self.I)):  # Ciclo principal
            s = Irms[i] * Vrms[i]  # potencias aparentes
            S.append(s)
            q = np.sqrt(abs(S[i] ** 2 - P[i] ** 2))  # potencias reactivas
            Q.append(q)

        return np.round(Q, 4)

    def pot_aparente(self):
        P = self.pot_activa()  # Potencias activas en los nodos
        Q = self.pot_reactiva()  # Potencias reactivas en los nodos
        S = []  # Lista de potencias aparentes en los nodos
        for i in range(len(P)):  # Ciclo que calcula las potencias aparentes
            s = np.sqrt(P[i] ** 2 + Q[i] ** 2)  # Potencias aparentes
            S.append(s)
        return np.round(S, 4)

    def factor_potencia(self):
        """
        Este método calcula el factor de potencia del sistema.
        :return: Los factores de potencia en los nodos.
        """
        P = self.pot_activa()  # Potencias activas
        S = self.pot_aparente()  # Potencias aparentes
        PF = []  # Lista factotres de potencia en los nodos
        for i in range(len(P)):  # Ciclo que calcula los factores de potencia
            pf = P[i] / S[i]  # Factor de potencia
            PF.append(pf)
        return np.round(PF, 4)

    def impedancias(self):
        v = self.V / np.sqrt(3)  # Voltajes de fase
        i = self.I / np.sqrt(3)  # Corrientes de fase

        # Cálculo de las impedancias con los valores rms de Vfase e Ifase
        Z1a = Analizador.__rms(self, v[0][0]) / Analizador.__rms(self, i[0][0])
        Z1b = Analizador.__rms(self, v[0][1]) / Analizador.__rms(self, i[0][1])
        Z1c = Analizador.__rms(self, v[0][2]) / Analizador.__rms(self, i[0][2])
        Z2a = Analizador.__rms(self, v[1][0]) / Analizador.__rms(self, i[1][0])
        Z2b = Analizador.__rms(self, v[1][1]) / Analizador.__rms(self, i[1][1])
        Z2c = Analizador.__rms(self, v[1][2]) / Analizador.__rms(self, i[1][2])
        Z3a = Analizador.__rms(self, v[2][0]) / Analizador.__rms(self, i[2][0])
        Z3b = Analizador.__rms(self, v[2][1]) / Analizador.__rms(self, i[2][1])
        Z3c = Analizador.__rms(self, v[2][2]) / Analizador.__rms(self, i[2][2])

        # Cálculo de los ángulos de las impedancias
        ang_1a, ang_1b, ang_1c = np.angle(np.argmax(v[0][0]) - np.argmax(i[0][0])) * 180 / np.pi, np.angle(
            np.argmax(v[0][1]) - np.argmax(i[0][1])) * 180 / np.pi, np.angle(
            np.argmax(v[0][2]) - np.argmax(i[0][2])) * 180 / np.pi
        ang_2a, ang_2b, ang_2c = np.angle(np.argmax(v[1][0]) - np.argmax(i[1][0])) * 180 / np.pi, np.angle(
            np.argmax(v[1][1]) - np.argmax(i[1][1])) * 180 / np.pi, np.angle(
            np.argmax(v[1][2]) - np.argmax(i[1][2])) * 180 / np.pi
        ang_3a, ang_3b, ang_3c = np.angle(np.argmax(v[2][0]) - np.argmax(i[2][0])) * 180 / np.pi, np.angle(
            np.argmax(v[2][1]) - np.argmax(i[2][1])) * 180 / np.pi, np.angle(
            np.argmax(v[2][2]) - np.argmax(i[2][2])) * 180 / np.pi
        # Se crea la tabla de impedancias como cadena de caracteres (strings)
        tabla = tabulate([
            ['A', str(np.round(Z1a, 3)) + '<' + str(np.round(ang_1a, 3)) + '°',
             str(np.round(Z2a, 3)) + '<' + str(np.round(ang_2a, 3)) + '°',
             str(np.round(Z3a, 3)) + '<' + str(np.round(ang_3a, 3)) + '°'],
            ['B', str(np.round(Z1b, 3)) + '<' + str(np.round(ang_1b, 3)) + '°',
             str(np.round(Z2b, 3)) + '<' + str(np.round(ang_2b, 3)) + '°',
             str(np.round(Z3b, 3)) + '<' + str(np.round(ang_3b, 3)) + '°'],
            ['C', str(np.round(Z1c, 3)) + '<' + str(np.round(ang_1c, 3)) + '°',
             str(np.round(Z2c, 3)) + '<' + str(np.round(ang_2c, 3)) + '°',
             str(np.round(Z3c, 3)) + '<' + str(np.round(ang_3c, 3)) + '°']],
            headers=["Fase", "Nodo 1 [Ω]", "Nodo 2 [Ω]", "Nodo 3 [Ω]"], tablefmt="fancy_outline")
        return tabla

    def tabla_potencias(self):
        P = self.pot_activa()  # Potencias activas
        Q = self.pot_reactiva()  # Potencias reactivas
        S = self.pot_aparente()  # Potencias aparentes
        PF = self.factor_potencia()  # Factores de potencia
        Pt = P[0].sum() + P[1].sum() + P[2].sum()  # Potencia activa total
        Qt = Q[0].sum() + Q[1].sum() + Q[2].sum()  # Potencia reactiva total
        St = S[0].sum() + S[1].sum() + S[2].sum()  # Potencia aparente total
        PFt = np.round(Pt / St, 3)  # Factor de potencia del sistema
        tabla = tabulate([
            ['P [W]', P[0], P[1], P[2], Pt],
            ['Q [VAr]', Q[0], Q[1], Q[2], Qt],
            ['S [VA]', S[0], S[1], S[2], St],
            ['cos(ϴ)', PF[0], PF[1], PF[2], PFt]],
            headers=["Potencia", "Nodo 1 ", "Nodo 2 ", "Nodo 3 ", "Total "], tablefmt="fancy_outline")
        return tabla

    def voltajes_fasorial(self):
        # Fases de los voltajes
        F = 60  # frecuencia del sistema
        V1phi_a = (np.argmax(self.V[0][0]) - np.argmax(self.V[0][0])) * (1 / (100 * F)) * 2 * np.pi * F
        V1phi_b = (np.argmax(self.V[0][0]) - np.argmax(self.V[0][1])) * (1 / (100 * F)) * 2 * np.pi * F
        V1phi_c = (np.argmax(self.V[0][0]) - np.argmax(self.V[0][2])) * (1 / (100 * F)) * 2 * np.pi * F
        V2phi_a = (np.argmax(self.V[0][0]) - np.argmax(self.V[1][0])) * (1 / (100 * F)) * 2 * np.pi * F
        V2phi_b = (np.argmax(self.V[0][0]) - np.argmax(self.V[1][1])) * (1 / (100 * F)) * 2 * np.pi * F
        V2phi_c = (np.argmax(self.V[0][0]) - np.argmax(self.V[1][2])) * (1 / (100 * F)) * 2 * np.pi * F
        V3phi_a = (np.argmax(self.V[0][0]) - np.argmax(self.V[2][0])) * (1 / (100 * F)) * 2 * np.pi * F
        V3phi_b = (np.argmax(self.V[0][0]) - np.argmax(self.V[2][1])) * (1 / (100 * F)) * 2 * np.pi * F
        V3phi_c = (np.argmax(self.V[0][0]) - np.argmax(self.V[2][2])) * (1 / (100 * F)) * 2 * np.pi * F

        # Nodo 4
        I_n4 = self.I[0] + self.I[1] + self.I[2]  # Corrientes en el nodo 4
        Y = (1 / self.Zl1) + (1 / self.Zl2) + (1 / self.Zl3)
        V4 = (I_n4 + (self.V[0] / self.Zl1) + (self.V[1] / self.Zl2) + (
                self.V[2] / self.Zl3)) / Y  # Voltaje en el nodo 4
        V4a, I4a = Analizador.__rms(self, abs(V4[0])), Analizador.__rms(self, I_n4[0])
        V4b, I4b = Analizador.__rms(self, abs(V4[1])), Analizador.__rms(self, I_n4[1])
        V4c, I4c = Analizador.__rms(self, abs(V4[2])), Analizador.__rms(self, I_n4[2])

        V4phi_a = (np.argmax(abs(V4[0])) - np.argmax(abs(abs(V4[0])))) * (1 / (100 * F)) * 2 * np.pi * F
        V4phi_b = (np.argmax(abs(V4[0])) - np.argmax(abs(V4[1]))) * (1 / (100 * F)) * 2 * np.pi * F
        V4phi_c = (np.argmax(abs(V4[0])) - np.argmax(abs(V4[2]))) * (1 / (100 * F)) * 2 * np.pi * F

        # Se crea la figura con los diagramas fasoriales
        fig, ax = plt.subplots(2, 2, subplot_kw={'projection': 'polar'}, figsize=(6.5, 6.5), dpi=80)

        # Diagrama de voltajes en nodo 1
        ax[0][0].set_title('Voltajes en los nodos 1, 2, 3 y 4')
        ax[0][0].quiver(V1phi_a, np.max(self.V[0][0]), angles='xy', scale_units='xy', scale=1, color='green', label='A')
        ax[0][0].quiver(V1phi_b, np.max(self.V[0][1]), angles='xy', scale_units='xy', scale=1, color='blue', label='B')
        ax[0][0].quiver(V1phi_c, np.max(self.V[0][2]), angles='xy', scale_units='xy', scale=1, color='red', label='C')
        ax[0][0].set_rmax(np.max(self.V[0]))
        ax[0][0].legend(loc="best")

        # Diagrama de voltajes en nodo 2
        ax[0][1].quiver(V2phi_a, np.max(self.V[1][0]), angles='xy', scale_units='xy', scale=1, color='green', label='A')
        ax[0][1].quiver(V2phi_b, np.max(self.V[1][1]), angles='xy', scale_units='xy', scale=1, color='blue', label='B')
        ax[0][1].quiver(V2phi_c, np.max(self.V[1][2]), angles='xy', scale_units='xy', scale=1, color='red', label='C')
        ax[0][1].set_rmax(np.max(self.V[1]))
        ax[0][1].legend(loc="best")
        # Diagrama de voltajes en nodo 3
        ax[1][0].quiver(V3phi_a, np.max(self.V[2][0]), angles='xy', scale_units='xy', scale=1, color='green', label='A')
        ax[1][0].quiver(V3phi_b, np.max(self.V[2][1]), angles='xy', scale_units='xy', scale=1, color='blue', label='B')
        ax[1][0].quiver(V3phi_c, np.max(self.V[2][2]), angles='xy', scale_units='xy', scale=1, color='red', label='C')
        ax[1][0].set_rmax(np.max(self.V[2]))
        ax[1][0].legend(loc="best")

        # Diagrama de voltajes en nodo 4
        ax[1][1].quiver(V4phi_a, np.max(abs(V4[0])), angles='xy', scale_units='xy', scale=1, color='green', label='A')
        ax[1][1].quiver(V4phi_b, np.max(abs(V4[1])), angles='xy', scale_units='xy', scale=1, color='blue', label='B')
        ax[1][1].quiver(V4phi_c, np.max(abs(V4[2])), angles='xy', scale_units='xy', scale=1, color='red', label='C')
        ax[1][1].set_rmax(np.max(abs(V4[2])))
        ax[1][1].legend(loc="best")

        return fig

    def corrientes_fasorial(self):
        # Fases de las corrientes
        F = 60  # Frecuencia del sistema
        I1phi_a = (np.argmax(self.V[0][0]) - np.argmax(self.I[0][0])) * (1 / (100 * F)) * 2 * np.pi * F
        I1phi_b = (np.argmax(self.V[0][0]) - np.argmax(self.I[0][1])) * (1 / (100 * F)) * 2 * np.pi * F
        I1phi_c = (np.argmax(self.V[0][0]) - np.argmax(self.I[0][2])) * (1 / (100 * F)) * 2 * np.pi * F
        I2phi_a = (np.argmax(self.V[0][0]) - np.argmax(self.I[1][0])) * (1 / (100 * F)) * 2 * np.pi * F
        I2phi_b = (np.argmax(self.V[0][0]) - np.argmax(self.I[1][1])) * (1 / (100 * F)) * 2 * np.pi * F
        I2phi_c = (np.argmax(self.V[0][0]) - np.argmax(self.I[1][2])) * (1 / (100 * F)) * 2 * np.pi * F
        I3phi_a = (np.argmax(self.V[0][0]) - np.argmax(self.I[2][0])) * (1 / (100 * F)) * 2 * np.pi * F
        I3phi_b = (np.argmax(self.V[0][0]) - np.argmax(self.I[2][1])) * (1 / (100 * F)) * 2 * np.pi * F
        I3phi_c = (np.argmax(self.V[0][0]) - np.argmax(self.I[2][2])) * (1 / (100 * F)) * 2 * np.pi * F

        # Nodo 4
        I_n4 = self.I[0] + self.I[1] + self.I[2]
        Z = (1 / self.Zl1) + (1 / self.Zl2) + (1 / self.Zl3)
        V4 = (I_n4 + (self.V[0] / self.Zl1) + (self.V[1] / self.Zl2) + (self.V[2] / self.Zl3)) / Z
        V4a, I4a = Analizador.__rms(self, abs(V4[0])), Analizador.__rms(self, I_n4[0])
        V4b, I4b = Analizador.__rms(self, abs(V4[1])), Analizador.__rms(self, I_n4[1])
        V4c, I4c = Analizador.__rms(self, abs(V4[2])), Analizador.__rms(self, I_n4[2])

        I4phi_a = (np.argmax(abs(V4[0])) - np.argmax(I_n4[0])) * (1 / (100 * F)) * 2 * np.pi * F
        I4phi_b = (np.argmax(abs(V4[0])) - np.argmax(I_n4[1])) * (1 / (100 * F)) * 2 * np.pi * F
        I4phi_c = (np.argmax(abs(V4[0])) - np.argmax(I_n4[2])) * (1 / (100 * F)) * 2 * np.pi * F

        # Se crea la figura con los diagramas fasoriales de las corrientes
        fig, ax = plt.subplots(2, 2, subplot_kw={'projection': 'polar'}, figsize=(6.5, 6.5), dpi=80)

        # Diagrama de corrientes en el nodo 1
        ax[0][0].set_title('Corrientes en los nodos 1, 2, 3 y 4')
        ax[0][0].quiver(I1phi_a, np.max(self.I[0][0]), angles='xy', scale_units='xy', scale=1, color='green', label='A')
        ax[0][0].quiver(I1phi_b, np.max(self.I[0][1]), angles='xy', scale_units='xy', scale=1, color='blue', label='B')
        ax[0][0].quiver(I1phi_c, np.max(self.I[0][2]), angles='xy', scale_units='xy', scale=1, color='red', label='C')
        ax[0][0].set_rmax(np.max(self.I[0]))
        ax[0][0].legend(loc="best")

        # Diagrama de corrientes en el nodo 2
        ax[0][1].quiver(I2phi_a, np.max(self.I[1][0]), angles='xy', scale_units='xy', scale=1, color='green', label='A')
        ax[0][1].quiver(I2phi_b, np.max(self.I[1][1]), angles='xy', scale_units='xy', scale=1, color='blue', label='B')
        ax[0][1].quiver(I2phi_c, np.max(self.I[1][2]), angles='xy', scale_units='xy', scale=1, color='red', label='C')
        ax[0][1].set_rmax(np.max(self.I[1]))
        ax[0][1].legend(loc="best")

        # Diagrama dee corrientes en el nodo 3
        ax[1][0].quiver(I3phi_a, np.max(self.I[2][0]), angles='xy', scale_units='xy', scale=1, color='green', label='A')
        ax[1][0].quiver(I3phi_b, np.max(self.I[2][1]), angles='xy', scale_units='xy', scale=1, color='blue', label='B')
        ax[1][0].quiver(I3phi_c, np.max(self.I[2][2]), angles='xy', scale_units='xy', scale=1, color='red', label='C')
        ax[1][0].set_rmax(np.max(self.I[2]))
        ax[1][0].legend(loc="best")

        # Diagrama de corrientes en el nodo 4
        ax[1][1].quiver(I4phi_a, np.max(I_n4[0]), angles='xy', scale_units='xy', scale=1, color='green', label='A')
        ax[1][1].quiver(I4phi_b, np.max(I_n4[1]), angles='xy', scale_units='xy', scale=1, color='blue', label='B')
        ax[1][1].quiver(I4phi_c, np.max(I_n4[2]), angles='xy', scale_units='xy', scale=1, color='red', label='C')
        ax[1][1].set_rmax(np.max(I_n4[2]))
        ax[1][1].legend(loc="best")

        return fig


# Salvaguarda
if __name__ == '__main__':
    # Pruebas unitarias:
    url = 'https://raw.githubusercontent.com/JulianDPastrana/signal_analysis/main/seniales_sep.py'
    # with httpimport.remote_repo(url):

    r = requests.get(url)

    with open('seniales_sep.py', 'w') as f:
        f.write(r.text)
    from seniales_sep import signal_generation

    data = signal_generation()

    V1, I1 = data["Node 1"]
    V2, I2 = data["Node 2"]
    V3, I3 = data["Node 3"]
    V = [V1, V2, V3]
    I = [I1, I2, I3]

    # Defino el analizador:
    analizador = Analizador(V, I)
    V_rms = analizador.v_rms()

    I_rms = analizador.i_rms()

    pinst = analizador.pot_instantanea()
    Val_rms = analizador.tabla_rms()
    P = analizador.pot_activa()
    Q = analizador.pot_reactiva()
    S = analizador.pot_aparente()
    fp = analizador.factor_potencia()
    Z = analizador.impedancias()
    potencias = analizador.tabla_potencias()
    analizador.voltajes_fasorial()
    print('Tensiones rms en los nodos:\n', V_rms)

    print('Corrientes rms en los nodos:\n', I_rms)

    print('Valores rms\n', Val_rms)
    print('Potencias activas: ', P)
    print('Potencias reactivas: ', Q)
    print('Potencias aparentes en los nodos: ', S)
    print('Factores de potencia en los nodos: ', fp)
    print('Impendacias: \n', Z)
    print('Tabla de potencias:\n', potencias)
