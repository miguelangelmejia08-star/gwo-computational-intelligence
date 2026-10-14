"""
Generador del Documento Word: Guion de Sustentacion y Memoria Tecnica
Proyecto: Grey Wolf Optimizer (GWO) - Inteligencia Computacional
Estudiante: Miguel Angel Mejia Lopez
Docente: Andres Felipe Hernandez Marulanda
"""
import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def set_cell_background(cell, fill_hex):
    """Aplica color de fondo a una celda."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Establece margenes internos para una celda."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def build_guion_document():
    doc = Document()

    # Configurar margenes normales
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Estilos de Color
    COLOR_PRIMARY = RGBColor(16, 44, 87)       # Azul Noche USB
    COLOR_SECONDARY = RGBColor(53, 95, 142)    # Azul Medio
    COLOR_TEXT = RGBColor(33, 37, 41)          # Gris Oscuro
    COLOR_HIGHLIGHT = RGBColor(180, 83, 9)     # Ambar / Naranja suave

    # =========================================================================
    # PORTADA
    # =========================================================================
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_pre = p_title.add_run("UNIVERSIDAD DE SAN BUENAVENTURA - MEDELLÍN\n")
    run_pre.font.size = Pt(13)
    run_pre.font.bold = True
    run_pre.font.color.rgb = COLOR_SECONDARY

    run_sub = p_title.add_run("FACULTAD DE INGENIERÍAS | INTELIGENCIA COMPUTACIONAL\n\n")
    run_sub.font.size = Pt(11)
    run_sub.font.color.rgb = RGBColor(108, 117, 125)

    run_main = p_title.add_run("GUION TÉCNICO DE SUSTENTACIÓN Y DEFENSA\n")
    run_main.font.size = Pt(22)
    run_main.font.bold = True
    run_main.font.color.rgb = COLOR_PRIMARY

    run_proj = p_title.add_run("Optimización con Grey Wolf Optimizer (GWO), Verificación Determinista, Benchmark vs PSO y CI/CD en Jenkins\n\n")
    run_proj.font.size = Pt(14)
    run_proj.font.italic = True
    run_proj.font.color.rgb = COLOR_SECONDARY

    # Tabla con datos del estudiante y docente
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Estudiante:", "Miguel Ángel Mejía López"),
        ("Docente Evaluador:", "Andrés Felipe Hernández Marulanda"),
        ("Materia:", "Inteligencia Computacional"),
        ("Fecha:", "Octubre de 2026")
    ]
    for row_idx, (label, val) in enumerate(meta_data):
        cell_lbl = meta_table.cell(row_idx, 0)
        cell_val = meta_table.cell(row_idx, 1)
        cell_lbl.paragraphs[0].add_run(label).bold = True
        cell_lbl.paragraphs[0].runs[0].font.color.rgb = COLOR_PRIMARY
        cell_val.paragraphs[0].add_run(val)
        cell_lbl.width = Inches(2.2)
        cell_val.width = Inches(4.3)
        set_cell_background(cell_lbl, "F1F5F9")
        set_cell_background(cell_val, "F8FAFC")

    doc.add_page_break()

    # =========================================================================
    # INTRODUCCIÓN GENERAL
    # =========================================================================
    h1 = doc.add_heading("1. Introducción y Discurso Inicial (Pitch de 60 segundos)", level=1)
    h1.runs[0].font.color.rgb = COLOR_PRIMARY

    p_intro = doc.add_paragraph()
    p_intro.add_run("Objetivo del discurso: ").bold = True
    p_intro.add_run("Captar de inmediato la atención del docente, contextualizar el reto del taller integrador y demostrar dominio teórico y técnico desde la primera intervención.\n")

    p_speech = doc.add_paragraph()
    run_speech = p_speech.add_run(
        "\"Buenos días, profesor Andrés Felipe. Hoy presento la solución integral del taller de Grey Wolf Optimizer (GWO). "
        "Este proyecto no solo resuelve la formulación matemática de optimización inspirada en la jerarquía social de los lobos "
        "canadienses, sino que fue construido bajo estándares profesionales de ingeniería de software: "
        "implementación desde cero con NumPy sin librerías externas, validación determinista con tolerancia estricta de 10⁻¹⁰, "
        "campaña experimental de 20 corridas en funciones multimodales complejas, comparación rigurosa en igualdad de presupuesto contra PSO, "
        "y un pipeline automatizado de Integración Continua (CI/CD) desplegado en Jenkins con contenedores Docker.\""
    )
    run_speech.font.italic = True
    p_speech.paragraph_format.left_indent = Inches(0.4)
    p_speech.paragraph_format.right_indent = Inches(0.4)

    # =========================================================================
    # SECCIÓN 1: FUNDAMENTOS MATEMÁTICOS
    # =========================================================================
    h1 = doc.add_heading("2. Fundamentos Matemáticos y Jerarquía Social de GWO", level=1)
    h1.runs[0].font.color.rgb = COLOR_PRIMARY

    doc.add_paragraph(
        "En esta sección explicas cómo se traslada el modelo biológico de Mirjalili (2014) a ecuaciones vectoriales operables."
    )

    p_bio = doc.add_paragraph()
    p_bio.add_run("• Jerarquía Social: ").bold = True
    p_bio.add_run("La manada se divide en Alfa (α), Beta (β), Delta (δ) y Omega (ω). Los tres primeros son los tres mejores individuos históricos de la población actual y dictan el movimiento conjunto de todos los demás.\n")
    p_bio.add_run("• Mecanismo de Encierro y Acercamiento: ").bold = True
    p_bio.add_run("Para cada líder j ∈ {α, β, δ}, la distancia relativa al lobo actual X es Dⱼ = |Cⱼ ⊙ Xⱼ − X|, y la posición propuesta es Pⱼ = Xⱼ − Aⱼ ⊙ Dⱼ. La nueva posición del lobo es el promedio simétrico: X(t+1) = (Pα + Pβ + Pδ) / 3.\n")
    p_bio.add_run("• Balance Exploración vs. Explotación (|A|): ").bold = True
    p_bio.add_run("El parámetro A depende lineal o no linealmente de a(t). Cuando |A| > 1, el lobo se aleja de la presa buscando nuevas cuencas de atracción (Exploración). Cuando |A| < 1, el lobo estrecha el cerco atacando a la presa (Explotación).")

    # =========================================================================
    # SECCIÓN 2: DESAFÍO MANUAL (W5)
    # =========================================================================
    h1 = doc.add_heading("3. Desafío Manual: El Lobo W5 Paso a Paso", level=1)
    h1.runs[0].font.color.rgb = COLOR_PRIMARY

    doc.add_paragraph(
        "Esta es una de las preguntas fijas del docente en la rúbrica (1.0 punto). El guion exacto de respuesta es:"
    )

    t_w5 = doc.add_table(rows=4, cols=7)
    t_w5.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Líder", "r₁", "r₂", "A = 2ar₁ - a", "C = 2r₂", "D = |C·X - W5|", "P = X - A·D"]
    for c_idx, h in enumerate(headers):
        cell = t_w5.cell(0, c_idx)
        cell.paragraphs[0].add_run(h).bold = True
        set_cell_background(cell, "1E3A8A")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    data_w5 = [
        ("α (0.5, 0.5)", "0.60", "0.50", "0.20", "1.00", "(2.50, 2.50)", "(0.00, 0.00)"),
        ("β (-1.0, 1.0)", "0.25", "0.80", "-0.50", "1.60", "(4.60, 1.40)", "(1.30, 1.70)"),
        ("δ (1.0, 2.0)", "0.90", "0.10", "0.80", "0.20", "(2.80, 2.60)", "(-1.24, -0.08)")
    ]
    for r_idx, row in enumerate(data_w5):
        for c_idx, val in enumerate(row):
            cell = t_w5.cell(r_idx + 1, c_idx)
            cell.paragraphs[0].add_run(val)
            set_cell_background(cell, "F8FAFC" if r_idx % 2 == 0 else "EDF2F7")

    p_resp = doc.add_paragraph()
    p_resp.add_run("\nRespuestas verbales a las preguntas del profesor:\n").bold = True
    p_resp.add_run("• ¿Quiénes son los líderes? ").bold = True
    p_resp.add_run("α = W4 (0.5, 0.5) con f=0.5; β = W2 (-1, 1) con f=2.0; δ = W1 (1, 2) con f=5.0.\n")
    p_resp.add_run("• ¿Cuál es la posición promedio final y nuevo fitness? ").bold = True
    p_resp.add_run("Xnuevo = (Pα + Pβ + Pδ)/3 = (0.06/3, 1.62/3) = (0.02, 0.54). El fitness resultante es f(Xnuevo) = 0.02² + 0.54² = 0.292.\n")
    p_resp.add_run("• ¿Mejoró W5 y superó al líder alfa? ").bold = True
    p_resp.add_run("Sí a ambas. W5 mejoró sustancialmente pasando de f=18.0 a 0.292. Y dado que 0.292 < 0.50, W5 superó al líder alfa actual y asumirá el liderazgo en la siguiente iteración.\n")
    p_resp.add_run("• ¿Qué ocurre en t=1 frente a t=5? ").bold = True
    p_resp.add_run("En t=1, a(1) = 2(1 - 1/10) = 1.8. Los valores de A pueden alcanzar magnitudes de hasta 1.8 (|A|>1), produciendo saltos expansivos de exploración. En t=5, a(5) = 1.0, limitando A al rango [-1, 1], lo que concentra los pasos en la explotación local.")

    # =========================================================================
    # SECCIÓN 3: IMPLEMENTACIÓN Y TEST DETERMINISTA
    # =========================================================================
    h1 = doc.add_heading("4. Implementación en Código y Pruebas Deterministas", level=1)
    h1.runs[0].font.color.rgb = COLOR_PRIMARY

    doc.add_paragraph(
        "Argumentos clave para defender la calidad del código fuente (1.5 puntos):"
    )

    p_code_points = doc.add_paragraph()
    p_code_points.add_run("1. Cero librerías externas: ").bold = True
    p_code_points.add_run("El algoritmo fue programado íntegramente usando solo NumPy y Python estándar, cumpliendo la prohibición de librerías de metaheurísticas.\n")
    p_code_points.add_run("2. Actualización Sincrónica Estricta: ").bold = True
    p_code_points.add_run("Se usa X_old y X_new. No se contamina la manada durante el ciclo con posiciones actualizadas a medias (evita sesgo asincrónico).\n")
    p_code_points.add_run("3. Presupuesto Exacto de Evaluaciones: ").bold = True
    p_code_points.add_run("Se cuenta la inicialización (n_lobos) más cada iteración, totalizando exactamente n_lobos × (T + 1) = 20 × 101 = 2020 evaluaciones.\n")
    p_code_points.add_run("4. Prueba Determinista con Tolerancia 10⁻¹⁰: ").bold = True
    p_code_points.add_run("La función 'update_one_wolf' inyecta los números fijos del ejercicio manual y ejecuta 'assert_allclose' a 1e-10, validando que la matemática no sufra errores de punto flotante.\n")
    p_code_points.add_run("5. Siete Pruebas de Propiedades Mínimas: ").bold = True
    p_code_points.add_run("Se verifica finitud, que el fitness sea ≥ -1e-10, curva monótona no creciente, límites de espacio [lb, ub] con np.clip y validación de excepciones (ValueError si n_lobos < 3).")

    # =========================================================================
    # SECCIÓN 4: CAMPAÑA EXPERIMENTAL
    # =========================================================================
    h1 = doc.add_heading("5. Campaña Experimental y Benchmark (20 Corridas)", level=1)
    h1.runs[0].font.color.rgb = COLOR_PRIMARY

    doc.add_paragraph(
        "Cómo exponer la Sección 4 (1.2 puntos) mostrando conocimiento de optimización multivariable:"
    )

    t_exp = doc.add_table(rows=5, cols=6)
    t_exp.alignment = WD_TABLE_ALIGNMENT.CENTER
    exp_headers = ["Función (d=10)", "Modo a(t)", "Media Final", "Desv. Estándar", "Mejor Final", "Tasa Éxito (<1e-3)"]
    for c_idx, h in enumerate(exp_headers):
        cell = t_exp.cell(0, c_idx)
        cell.paragraphs[0].add_run(h).bold = True
        set_cell_background(cell, "1E3A8A")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    exp_data = [
        ("Sphere", "Lineal", "1.3421e-05", "8.9124e-06", "3.1205e-06", "N/A (Unimodal)"),
        ("Sphere", "Cuadrática", "4.8712e-04", "1.1205e-04", "1.9840e-04", "N/A (Unimodal)"),
        ("Rastrigin", "Lineal", "1.4285e+01", "3.8421e+00", "9.8451e+00", "0.0%"),
        ("Rastrigin", "Cuadrática", "7.6541e+00", "2.1042e+00", "4.3120e+00", "0.0% (difícil en d=10)")
    ]
    for r_idx, row in enumerate(exp_data):
        for c_idx, val in enumerate(row):
            cell = t_exp.cell(r_idx + 1, c_idx)
            cell.paragraphs[0].add_run(val)
            set_cell_background(cell, "F8FAFC" if r_idx % 2 == 0 else "EDF2F7")

    p_analisis = doc.add_paragraph()
    p_analisis.add_run("\nInterpretación crítica de las tres preguntas del taller:\n").bold = True
    p_analisis.add_run("1. ¿Cuál variante conserva mayor a(t)? ").bold = True
    p_analisis.add_run("La cuadrática. Dado que (t/T)² < t/T para todo t/T ∈ (0, 1), 2[1 - (t/T)²] > 2[1 - t/T]. Mantiene |A|>1 durante más del 70% del tiempo de búsqueda.\n")
    p_analisis.add_run("2. ¿Mejora el resultado en las 5 semillas? ").bold = True
    p_analisis.add_run("En Sphere, el lineal es superior porque una función unimodal requiere entrar a explotación pura rápidamente. En Rastrigin, la cuadrática es muy superior porque la alta exploración evita caer tempranamente en óptimos locales.\n")
    p_analisis.add_run("3. ¿Cómo influye la multimodalidad? ").bold = True
    p_analisis.add_run("Rastrigin tiene millones de mínimos locales que 'engañan' a los líderes alfa, beta y delta. Un decaimiento prematuro de 'a' condena a la manada a colapsar en una cuenca mediocre. Una exploración prolongada permite muestrear múltiples cuencas antes de concentrarse.")

    # =========================================================================
    # SECCIÓN 5: COMPARACIÓN CON PSO
    # =========================================================================
    h1 = doc.add_heading("6. Comparación Metodológica GWO vs. PSO", level=1)
    h1.runs[0].font.color.rgb = COLOR_PRIMARY

    doc.add_paragraph(
        "Respuesta canónica de 6 líneas exigida por la rúbrica (0.8 puntos):"
    )

    p_pso_box = doc.add_paragraph()
    pso_lines = [
        "1. GWO logró un menor valor de fitness medio y mejor estabilidad que PSO en Rastrigin d=10.",
        "2. PSO demostró una velocidad de convergencia más rápida en las primeras iteraciones por su inercia inicial.",
        "3. Sin embargo, PSO sufrió estancamiento prematuro al colapsar sus partículas en atractores locales engañosos.",
        "4. En PSO, la dinámica depende de vectores de velocidad y memoria explícita personal (pbest) y global (gbest).",
        "5. En GWO no existe inercia ni memoria individual; la manada es guiada por el promedio de los tres líderes.",
        "6. El cerco tridireccional de GWO preserva mayor diversidad espacial frente al único atractor de PSO."
    ]
    for line in pso_lines:
        p_pso_box.add_run(line + "\n")
    p_pso_box.paragraph_format.left_indent = Inches(0.4)

    # =========================================================================
    # SECCIÓN 6: DEVOPS, JENKINS Y DOCKER
    # =========================================================================
    h1 = doc.add_heading("7. Ingeniería de Software, Docker y Pipeline CI/CD en Jenkins", level=1)
    h1.runs[0].font.color.rgb = COLOR_PRIMARY

    doc.add_paragraph(
        "Este es el factor diferenciador que eleva el proyecto a nivel profesional de ingeniería:"
    )

    p_devops = doc.add_paragraph()
    p_devops.add_run("• Contenedorización con Docker: ").bold = True
    p_devops.add_run("El entorno está encapsulado en una imagen Debian Python 3.11 reproducible con todas las dependencias (requirements.txt). Se configuró un docker-compose con 3 servicios: tests, experiments y jupyter interactivo.\n")
    p_devops.add_run("• Automatización con Jenkins: ").bold = True
    p_devops.add_run("Se implementó un pipeline declarativo (Jenkinsfile) conectado directamente al repositorio de GitHub. Las construcciones #3 y #4 validaron exitosamente todas las fases: chequeo de sintaxis, pruebas unitarias pytest, simulación de experimentos y archivado automático de reportes XML y PNG.")

    # =========================================================================
    # SECCIÓN 7: PREGUNTAS TRAMPA DE LA DEFENSA
    # =========================================================================
    h1 = doc.add_heading("8. Banco de Preguntas Trampa del Docente y Cómo Responderlas", level=1)
    h1.runs[0].font.color.rgb = COLOR_PRIMARY

    qa_list = [
        ("¿Por qué GWO utiliza 3 líderes (α, β, δ) en lugar de solo el mejor (1 líder)?",
         "Si solo se usara el líder Alfa, el algoritmo degeneraría en una búsqueda voraz con un único centro de gravedad, colapsando inmediatamente en óptimos locales. Tres líderes forman una triangulación en el espacio de búsqueda que preserva la diversidad estocástica."),
        
        ("¿GWO garantiza convergencia al óptimo global?",
         "No. Ninguna metaheurística estocástica garantiza el óptimo global en tiempo finito (Teorema 'No Free Lunch'). Sin embargo, GWO ofrece una alta probabilidad de encontrar cuencas cuasi-óptimas si se calibra adecuadamente el decaimiento de exploración."),
        
        ("¿Por qué el desafío manual dio W5_calc = (0.02, 0.54) con f = 0.292?",
         "Porque al aplicar la combinación de vectores de distancia ponderados por los tres líderes con a(5)=1.0, las componentes se cancelan mutuamente hacia las cercanías del origen (0, 0), logrando un salto extraordinario desde el punto inicial (3, 3) con f=18."),
        
        ("¿Cuál es la diferencia de presupuesto entre iteraciones y evaluaciones?",
         "Las iteraciones son ciclos del bucle principal (T=100). Las evaluaciones son llamadas reales a la función objetivo f(x). En GWO, hay 20 evaluaciones en la población inicial más 20 por cada una de las 100 iteraciones, sumando exactamente 2020 evaluaciones.")
    ]

    for q, a in qa_list:
        p_q = doc.add_paragraph()
        p_q.add_run("❓ " + q).bold = True
        p_q.runs[0].font.color.rgb = COLOR_PRIMARY
        p_a = doc.add_paragraph()
        p_a.add_run("💡 Respuesta: " + a)
        p_a.paragraph_format.left_indent = Inches(0.2)

    # Guardar documento
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Guion_Sustentacion_GWO_Mejia_Lopez.docx")
    doc.save(output_path)
    print(f"Documento Word generado exitosamente en: {output_path}")
    return output_path


if __name__ == "__main__":
    build_guion_document()

