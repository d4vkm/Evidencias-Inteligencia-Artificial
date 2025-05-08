import tkinter as tk
from tkinter import ttk, messagebox


class SistemaExpertoCardiaco:
    def __init__(self):
        # Definición de los factores de riesgo
        self.factores = {
            'C': 'Tiene Anemia',
            'D': 'Tiene hipertensión',
            'E': 'Posee fracción de eyección Normal (55-70%)',
            'F': 'Creatinina sérica en rango aceptable',
            'G': 'Sodio sérico en rango aceptable'
        }

        # Base de conocimiento con probabilidades de supervivencia
        self.base_conocimiento = {
            0: {  # 0-1 factores de riesgo
                'C&D&E&F&¬G': (6, 6),
                'C&D&¬E&¬F&¬G': (2, 3),
                'C&D&E&¬F&¬G': (5, 5),
                'C&D&E&¬F&G': (6, 8),
                'C&¬D&E&¬F&¬G': (0, 1),
                '¬C&D&E&¬F&¬G': (48, 54),
                'default': (67, 77, 87.01)
            },
            1: {  # 0-1 factores de riesgo (continuación)
                'default': (67, 77, 87.01)
            },
            2: {  # 2 factores de riesgo
                'C&D&¬E&¬F&G': (0, 1),
                'C&¬D&E&¬F&G': (2, 2),
                '¬C&D&E&F&¬G': (19, 28),
                'C&D&E&F&G': (7, 7),
                'C&¬D&¬E&¬F&¬G': (1, 2),
                '¬C&D&E&¬F&G': (30, 41),
                '¬C&¬D&E&¬F&¬G': (11, 16),
                '¬C&D&¬E&¬F&¬G': (11, 17),
                'default': (81, 114, 71.05)
            },
            3: {  # 3 factores de riesgo
                'C&¬D&E&F&G': (1, 2),
                'C&¬D&¬E&¬F&G': (0, 1),
                '¬C&D&¬E&¬F&G': (5, 6),
                '¬C&D&¬E&F&¬G': (8, 9),
                '¬C&D&E&F&G': (14, 21),
                '¬C&¬D&¬E&¬F&¬G': (5, 15),
                '¬C&¬D&E&¬F&G': (9, 13),
                '¬C&¬D&E&F&¬G': (2, 6),
                'default': (44, 73, 60.27)
            },
            4: {  # 4 factores de riesgo
                '¬C&D&¬E&F&G': (5, 7),
                '¬C&¬D&¬E&¬F&G': (2, 9),
                '¬C&¬D&¬E&F&¬G': (1, 8),
                '¬C&¬D&E&F&G': (0, 4),
                'default': (8, 28, 28.57)
            },
            5: {  # 5 factores de riesgo
                '¬C&¬D&¬E&F&G': (2, 7),
                'default': (2, 7, 28.57)
            }
        }

        # Niveles de riesgo
        self.niveles_riesgo = {
            0: "Riesgo bajo",
            1: "Riesgo bajo",
            2: "Riesgo moderado",
            3: "Riesgo moderado-alto",
            4: "Riesgo alto",
            5: "Emergencia"
        }

    def evaluar_paciente(self, paciente):
        """
        Evalúa el riesgo cardíaco de un paciente basado en sus factores de riesgo

        Args:
            paciente: Diccionario con los factores del paciente (ej: {'C': True, 'D': False, ...})

        Returns:
            Diccionario con la evaluación del riesgo
        """
        # Contar factores de riesgo (True significa que el factor de riesgo está presente)
        # Nota: Para E, F y G, True significa que son NORMALES (no son factores de riesgo)
        factores_presentes = 0

        # Factor C: Anemia (presente = factor de riesgo)
        if paciente.get('C', False):
            factores_presentes += 1

        # Factor D: Hipertensión (presente = factor de riesgo)
        if paciente.get('D', False):
            factores_presentes += 1

        # Factor E: Fracción de eyección (NO normal = factor de riesgo)
        if not paciente.get('E', False):
            factores_presentes += 1

        # Factor F: Creatinina sérica (NO en rango = factor de riesgo)
        if not paciente.get('F', False):
            factores_presentes += 1

        # Factor G: Sodio sérico (NO en rango = factor de riesgo)
        if not paciente.get('G', False):
            factores_presentes += 1

        # Determinar nivel de riesgo
        nivel_riesgo = self.niveles_riesgo.get(factores_presentes, "Desconocido")

        # Generar expresión lógica para buscar en la base de conocimiento
        expr = []
        expr.append('C' if paciente.get('C', False) else '¬C')
        expr.append('D' if paciente.get('D', False) else '¬D')
        expr.append('E' if paciente.get('E', False) else '¬E')
        expr.append('F' if paciente.get('F', False) else '¬F')
        expr.append('G' if paciente.get('G', False) else '¬G')
        expr_logica = '&'.join(expr)

        # Buscar en la base de conocimiento
        datos = self.base_conocimiento.get(factores_presentes, {}).get(expr_logica)
        if datos is None:
            datos = self.base_conocimiento.get(factores_presentes, {}).get('default', (0, 0, 0.0))

        # Calcular tasa de supervivencia si no está en los datos
        if len(datos) == 2:
            tasa = (datos[0] / datos[1]) * 100 if datos[1] != 0 else 0.0
            datos = (datos[0], datos[1], tasa)

        # Preparar resultado
        resultado = {
            'factores_riesgo': factores_presentes,
            'nivel_riesgo': nivel_riesgo,
            'expresion_logica': expr_logica,
            'supervivencia': f"{datos[0]}/{datos[1]}",
            'tasa_supervivencia': datos[2],
            'interpretacion': self.interpretar_riesgo(factores_presentes)
        }

        return resultado

    def interpretar_riesgo(self, num_factores):
        """Proporciona una interpretación del nivel de riesgo"""
        interpretaciones = {
            0: "Paciente con riesgo muy bajo. Supervivencia esperada muy alta (>85%).",
            1: "Paciente con riesgo bajo. Supervivencia esperada alta (>85%).",
            2: "Paciente con riesgo moderado. Supervivencia esperada alrededor del 70%.",
            3: "Paciente con riesgo moderado-alto. Supervivencia esperada alrededor del 60%.",
            4: "Paciente con riesgo alto. Supervivencia esperada alrededor del 30%.",
            5: "Paciente en emergencia. Supervivencia esperada muy baja (<30%). Requiere atención inmediata."
        }
        return interpretaciones.get(num_factores, "Nivel de riesgo desconocido.")

    def mostrar_factores(self):
        """Muestra la descripción de los factores de riesgo"""
        print("Factores de riesgo considerados:")
        for key, desc in self.factores.items():
            print(f"{key}: {desc}")
        print("\nNota: Para E, F y G, True significa que son NORMALES (no son factores de riesgo)")


class InterfazSistemaExperto:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Experto de Evaluación Cardíaca")
        self.root.geometry("800x600")

        # Configurar el icono (opcional)
        try:
            self.root.iconbitmap('heart.ico')  # Puedes crear un icono heart.ico
        except:
            pass

        self.sistema = SistemaExpertoCardiaco()

        self.crear_interfaz()

    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        ttk.Label(main_frame, text="Evaluación de Riesgo Cardíaco",
                  font=('Helvetica', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        # Factores de riesgo
        ttk.Label(main_frame, text="Factores de Riesgo:",
                  font=('Helvetica', 12, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=5)

        # Variables para los checkboxes
        self.var_C = tk.BooleanVar()
        self.var_D = tk.BooleanVar()
        self.var_E = tk.BooleanVar()
        self.var_F = tk.BooleanVar()
        self.var_G = tk.BooleanVar()

        # Checkboxes para los factores
        self.chk_C = ttk.Checkbutton(main_frame, text="Tiene Anemia", variable=self.var_C)
        self.chk_C.grid(row=2, column=0, sticky=tk.W, padx=20)

        self.chk_D = ttk.Checkbutton(main_frame, text="Tiene Hipertensión", variable=self.var_D)
        self.chk_D.grid(row=3, column=0, sticky=tk.W, padx=20)

        self.chk_E = ttk.Checkbutton(main_frame, text="Fracción eyección NORMAL (55-70%)", variable=self.var_E)
        self.chk_E.grid(row=4, column=0, sticky=tk.W, padx=20)

        self.chk_F = ttk.Checkbutton(main_frame, text="Creatinina sérica en rango aceptable", variable=self.var_F)
        self.chk_F.grid(row=5, column=0, sticky=tk.W, padx=20)

        self.chk_G = ttk.Checkbutton(main_frame, text="Sodio sérico en rango aceptable", variable=self.var_G)
        self.chk_G.grid(row=6, column=0, sticky=tk.W, padx=20)

        # Botón de evaluación
        ttk.Button(main_frame, text="Evaluar Riesgo", command=self.evaluar_paciente).grid(row=7, column=0, pady=20)

        # Frame de resultados
        self.result_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        self.result_frame.grid(row=8, column=0, columnspan=2, sticky=tk.EW, pady=10)

        # Área de información
        self.info_text = tk.Text(self.result_frame, height=15, width=80, wrap=tk.WORD)
        self.info_text.pack(fill=tk.BOTH, expand=True)

        # Barra de desplazamiento


        # Configurar tags para colores
        self.info_text.tag_config('bajo', foreground='green')
        self.info_text.tag_config('moderado', foreground='orange')
        self.info_text.tag_config('alto', foreground='red')
        self.info_text.tag_config('emergencia', foreground='dark red', font=('Helvetica', 10, 'bold'))
        self.info_text.tag_config('titulo', font=('Helvetica', 10, 'bold'))

        # Botón de información
        ttk.Button(main_frame, text="Acerca de", command=self.mostrar_info).grid(row=9, column=0, pady=10)

    def evaluar_paciente(self):
        """Evalúa al paciente basado en los factores seleccionados"""
        # Obtener valores de los checkboxes
        paciente = {
            'C': self.var_C.get(),
            'D': self.var_D.get(),
            'E': self.var_E.get(),
            'F': self.var_F.get(),
            'G': self.var_G.get()
        }

        # Validar que al menos un factor esté marcado
        if not any(paciente.values()):
            messagebox.showwarning("Advertencia", "Por favor, seleccione al menos un factor para evaluar.")
            return

        # Evaluar con el sistema experto
        resultado = self.sistema.evaluar_paciente(paciente)

        # Mostrar resultados
        self.info_text.delete(1.0, tk.END)

        # Determinar tag para el color según el nivel de riesgo
        nivel = resultado['nivel_riesgo'].lower()
        tag = 'normal'
        if 'bajo' in nivel:
            tag = 'bajo'
        elif 'moderado' in nivel:
            tag = 'moderado'
        elif 'alto' in nivel:
            tag = 'alto'
        elif 'emergencia' in nivel:
            tag = 'emergencia'

        # Insertar resultados con formato
        self.info_text.insert(tk.END, "Resumen de Evaluación:\n", 'titulo')
        self.info_text.insert(tk.END, f"Factores de riesgo presentes: {resultado['factores_riesgo']}\n", tag)
        self.info_text.insert(tk.END, f"Nivel de riesgo: {resultado['nivel_riesgo']}\n\n", tag)

        self.info_text.insert(tk.END, "Detalles Técnicos:\n", 'titulo')
        self.info_text.insert(tk.END, "Expresión lógica evaluada:\n")
        self.info_text.insert(tk.END, f"{resultado['expresion_logica']}\n\n")

        self.info_text.insert(tk.END, "Datos históricos de supervivencia:\n")
        self.info_text.insert(tk.END, f"Casos similares: {resultado['supervivencia']}\n")
        self.info_text.insert(tk.END, f"Tasa de supervivencia: {resultado['tasa_supervivencia']:.2f}%\n\n")

        self.info_text.insert(tk.END, "Interpretación y Recomendaciones:\n", 'titulo')
        self.info_text.insert(tk.END, f"{resultado['interpretacion']}\n", tag)

        # Desplazar al inicio
        self.info_text.see(tk.END)

    def mostrar_info(self):
        """Muestra información sobre el sistema"""
        info = """
        Sistema Experto de Evaluación Cardíaca

        Este sistema evalúa el riesgo cardíaco de un paciente basado en 5 factores de riesgo
        Instrucciones:
        1. Marque las casillas correspondientes a los factores del paciente
        2. Haga clic en "Evaluar Riesgo"
        3. Revise los resultados en el área inferior

        Los resultados incluyen:
        - Número de factores de riesgo
        - Nivel de riesgo
        - Datos históricos de supervivencia
        - Interpretación y recomendaciones
        """
        messagebox.showinfo("Acerca del Sistema", info)


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazSistemaExperto(root)
    root.mainloop()