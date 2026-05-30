import os

# Definición de los 20 documentos corporativos de GOBS
knowledge_base = {
    "01_gobs_framework.txt": 
        "MANUAL GENERAL GOBS - SISTEMA GLOBAL DE OPERACIONES\n"
        "El Global Operation Business System (GOBS) es el marco de trabajo unificado que rige a la corporación.\n"
        "Su objetivo principal es estandarizar los procesos de manufactura, asegurar la excelencia operacional (OPEX)\n"
        "y garantizar que todas las plantas operen bajo los mismos estándares de costos, seguridad y calidad global.\n"
        "GOBS se sostiene sobre 4 pilares fundamentales: Seguridad Industrial, Calidad Total, Entrega a Tiempo y Eficiencia de Costos.",

    "02_lean_manufacturing_sps.txt":
        "SISTEMA DE PRODUCCIÓN ESPECÍFICO (SPS) Y LEAN MANUFACTURING\n"
        "El SPS (Specific Production System) es la adaptación interna de la metodología Lean Manufacturing.\n"
        "El enfoque principal del SPS es la eliminación absoluta de las 8 Mudas o desperdicios en el piso de producción:\n"
        "sobreproducción, tiempos de espera, transporte innecesario, sobreprocesamiento, exceso de inventario,\n"
        "movimientos innecesarios, defectos en el producto y talento humano no utilizado.",

    "03_5s_procedimiento_planta.txt":
        "ESTÁNDAR OPERATIVO PARA LA IMPLEMENTACIÓN DE LAS 5S\n"
        "El orden y la limpieza en las estaciones de trabajo se auditan bajo el estándar de las 5S de GOBS.\n"
        "Las fases obligatorias son: Seiri (Clasificar), Seiton (Ordenar), Seiso (Limpiar), Seiketsu (Estandarizar) y Shitsuke (Disciplina).\n"
        "Las auditorías de planta se ejecutan de forma mandatoria todos los viernes a las 15:00 horas.\n"
        "Cualquier estación de trabajo con un puntaje de auditoría inferior al 85% ingresará automáticamente\n"
        "en un estatus de desviación, requiriendo un plan de acción correctivo en un plazo máximo de 24 horas.",

    "04_six_sigma_dmaic.txt":
        "METODOLOGÍA SIX SIGMA Y CICLO DMAIC PARA PROYECTOS COMPLEJOS\n"
        "Para la reducción drástica de la variabilidad y defectos en los procesos de manufactura, GOBS exige el uso de Six Sigma.\n"
        "Todo proyecto de mejora debe seguir estrictamente las 5 fases del ciclo DMAIC:\n"
        "1. Definir (Define): Establecer el problema, el alcance y los objetivos del proyecto.\n"
        "2. Medir (Measure): Recolectar datos confiables del estado actual del proceso.\n"
        "3. Analizar (Analyze): Identificar las causas raíz de la variabilidad utilizando diagramas de Ishikawa y Pareto.\n"
        "4. Mejorar (Improve): Desarrollar, implementar y validar soluciones óptimas.\n"
        "5. Controlar (Control): Diseñar mecanismos de monitoreo estandarizados para sostener los ahorros económicos.",

    "05_calidad_alcoa_integrity.txt":
        "DIRECTRICES DE INTEGRIDAD DE DATOS BAJO EL ESTÁNDAR ALCOA+\n"
        "Todos los registros manuales, electrónicos y de laboratorio de control de calidad (QC) deben cumplir con ALCOA+.\n"
        "Los datos deben ser: Atribuibles (saber quién firmó), Legibles (claros y duraderos), Contemporáneos (registrados al momento),\n"
        "Originales (o copia certificada) y Precisos (Accurate, sin alteraciones).\n"
        "La extensión (+) exige que la información operativa sea Completa, Consistente, Duradera y Disponible en auditorías.",

    "06_metricas_kpis_globales.txt":
        "CATÁLOGO DE KPIS Y MÉTRICAS DE RENDIMIENTO OPERATIVO\n"
        "La eficiencia operativa de las líneas de producción en el sistema GOBS se mide a través de tres KPIs maestros:\n"
        "1. OEE (Overall Equipment Effectiveness): Mide la eficiencia global de la maquinaria (Disponibilidad x Rendimiento x Calidad).\n"
        "El target global corporativo para el OEE es del 85%.\n"
        "2. Takt Time: Ritmo de producción calculado como el Tiempo Disponible dividido para la Demanda del Cliente.\n"
        "3. DPMO (Defectos por Millón de Oportunidades): Estándar Six Sigma para medir la tasa de fallas en lotes masivos.",

    "07_indicadores_leading_lagging.txt":
        "POLÍTICA DE CONTROL MEDIANTE INDICADORES LEADING Y LAGGING\n"
        "El tablero de control gerencial de GOBS divide sus métricas en dos categorías críticas:\n"
        "- LEADING INDICATORS (Predictivos): Métricas proactivas que miden actividades preventivas (ej. Horas de capacitación,\n"
        "número de mantenimientos preventivos ejecutados a tiempo). Ayudan a predecir y evitar fallas.\n"
        "- LAGGING INDICATORS (De Resultado): Métricas reactivas que miden eventos históricos que ya ocurrieron\n"
        "y no se pueden cambiar (ej. Índice de accidentabilidad del mes anterior, toneladas totales de merma).",

    "08_calidad_rft_qc.txt":
        "ESTÁNDAR DE CONTROL DE CALIDAD (QC) Y PRODUCTO BIEN A LA PRIMERA (RFT)\n"
        "El departamento de Control de Calidad (QC) se encarga de la inspección física y detección de defectos en planta.\n"
        "La métrica clave del área es el RFT (Right First Time / Bien a la Primera), la cual calcula el porcentaje de unidades\n"
        "que cumplen al 100% con las especificaciones técnicas en el primer intento de producción.\n"
        "Un indicador RFT bajo es síntoma directo de fallas en el set-up de maquinaria o falta de estandarización.",

    "09_aseguramiento_calidad_qa.txt":
        "PROCESOS DE ASEGURAMIENTO DE CALIDAD (QA) Y AUDITORÍAS\n"
        "A diferencia de QC, Aseguramiento de Calidad (QA) tiene un enfoque 100% preventivo y de diseño de procesos.\n"
        "QA es el área responsable de diseñar los flujos de trabajo, validar los sistemas informáticos, certificar proveedores\n"
        "y coordinar las auditorías internas obligatorias de cumplimiento del sistema GOBS.",

    "10_educacion_entrenamiento_et.txt":
        "PILAR DE EDUCACIÓN Y ENTRENAMIENTO (E&T) - MATRIZ DE HABILIDADES\n"
        "El pilar de E&T busca elevar el nivel técnico y la autonomía de los operadores en el piso de manufactura.\n"
        "Es obligatorio que cada línea cuente con una Matriz de Habilidades (Skill Matrix) actualizada mensualmente.\n"
        "La escala de evaluación va del nivel 1 (Principiante bajo supervisión) al nivel 4 (Experto calificado para entrenar).\n"
        "El objetivo del pilar E&T es eliminar la dependencia de personal único en turnos críticos.",

    "11_logistica_inventario_rot.txt":
        "GESTIÓN DE MATERIALES INDISPENSABLES Y TIEMPO DE AGOTAMIENTO (ROT)\n"
        "El ROT (Run-Out Time) es el indicador logístico que determina el tiempo teórico en días o horas que durará el inventario\n"
        "actual de materia prima para abastecer las líneas antes de quedarse completamente en cero.\n"
        "Adicionalmente, en los almacenes técnicos se aplica el análisis ROT para identificar refacciones bajo tres criterios:\n"
        "Redundantes (R), Obsoletas (O) y Triviales (T), las cuales deben depurarse semestralmente.",

    "12_operaciones_confiables_ro.txt":
        "MARCO DE OPERACIONES CONFIABLES (RO - RELIABLE OPERATIONS)\n"
        "El programa RO (Reliable Operations) establece las bases técnicas para estabilizar los procesos industriales.\n"
        "Se enfoca en reducir drásticamente los paros no programados mediante la aplicación rigurosa de mantenimiento autónomo\n"
        "por parte de los operadores de planta, garantizando la predictibilidad y la continuidad del negocio.",

    "13_logistica_despacho_mdl.txt":
        "FLUJO DE ENTREGA Y MANUFACTURING DELIVERY LEAD (MDL)\n"
        "El rol del MDL (Manufacturing Delivery Lead) es coordinar el puente de comunicación entre producción y logística.\n"
        "El MDL rastrea que el producto terminado sea liberado por QA, empacado bajo las normas de estiba oficiales\n"
        "y transferido a los centros de distribución (CEDIS) dentro de las ventanas de tiempo acordadas,\n"
        "garantizando un indicador OTIF (On-Time In-Full) óptimo.",

    "14_mantenimiento_eficiencia_adh.txt":
        "GESTIÓN DE TIEMPOS MUERTOS Y HORAS DE PARO ACUMULADAS (ADH)\n"
        "El ADH (Accumulated Down Hours) registra el impacto financiero y operativo de los tiempos muertos mecánicos en planta.\n"
        "Cada vez que una máquina crítica se detiene por más de 5 minutos, el operador debe registrar la causa exacta en el sistema.\n"
        "Al final de cada semana, el área de Ingeniería de Mantenimiento analiza el ADH acumulado por línea\n"
        "para priorizar las órdenes de trabajo del mantenimiento preventivo del fin de semana.",

    "15_seguridad_ehs_framework.txt":
        "MANUAL DE MEDIO AMBIENTE, SEGURIDAD E HIGIENE INDUSTRIAL (EHS)\n"
        "La seguridad de las personas es la prioridad número uno en el sistema corporativo GOBS.\n"
        "El departamento de EHS (Environment, Health and Safety) es la autoridad máxima para detener cualquier operación\n"
        "si se detecta un riesgo inminente a la salud de los colaboradores o un impacto ecológico negativo.\n"
        "Es obligatorio el uso de Equipo de Protección Personal (EPP) completo: casco, gafas, botas de punta de acero y protección auditiva.",

    "16_seguridad_loto_protocol.txt":
        "PROCEDIMIENTO CRÍTICO DE SEGURIDAD: BLOQUEO Y ETIQUETADO (LOTO)\n"
        "Antes de realizar cualquier mantenimiento, limpieza profunda o intervención técnica dentro de una máquina,\n"
        "es obligatorio aplicar el protocolo LOTO (Lockout / Tagout).\n"
        "Este procedimiento exige: 1. Aislar las fuentes de energía (eléctrica, neumática, hidráulica).\n"
        "2. Colocar un candado físico personal en el interruptor principal. 3. Colocar una tarjeta de advertencia visible.\n"
        "Está estrictamente prohibido retirar un candado ajeno; la violación de esta norma conlleva sanción disciplinaria severa.",

    "17_desviaciones_sistema_capa.txt":
        "GESTIÓN DE NO CONFORMIDADES Y ACCIONES CORRECTIVAS Y PREVENTIVAS (CAPA)\n"
        "Cuando se detecta una falla grave de calidad, seguridad o un reclamo de cliente, se abre una investigación CAPA.\n"
        "El proceso exige conformar un equipo multidisciplinario para aplicar la técnica de los 5 Porqués para hallar la causa raíz.\n"
        "- Acción Correctiva: Detiene el problema de forma inmediata (mitiga el impacto actual).\n"
        "- Acción Preventiva: Modifica el diseño del proceso o máquina para asegurar que la falla no vuelva a ocurrir jamás.",

    "18_analisis_riesgos_fmea.txt":
        "ANÁLISIS DE MODO DE FALLA Y EFECTOS (FMEA / AMFE) EN PROCESOS\n"
        "El FMEA es la herramienta analítica obligatoria para evaluar riesgos potenciales en líneas de producción.\n"
        "Cada modo de falla identificado se evalúa calculando el NPR (Número de Prioridad de RIESGO), el cual multiplica:\n"
        "Severidad (Qué tan grave es el fallo) x Ocurrencia (Qué tan seguido pasa) x Detección (Qué tan fácil es verlo antes de que salga).\n"
        "Cualquier item con un NPR superior a 120 puntos exige el diseño obligatorio e inmediato de un mecanismo Poka-Yoke.",

    "19_estandarizacion_procesos_sop.txt":
        "CREACIÓN Y CONTROL DE PROCEDIMIENTOS OPERATIVOS ESTÁNDARES (SOP)\n"
        "En GOBS, si una tarea no está escrita, no existe. Todo proceso clave debe contar con un SOP (Standard Operating Procedure).\n"
        "Los SOPs deben ser documentos altamente visuales, ubicados físicamente en la estación de trabajo en tableros acrílicos.\n"
        "Deben detallar de forma inequívoca el paso a paso de la operación, los parámetros de control obligatorios\n"
        "y las acciones a tomar en caso de una emergencia operativa.",

    "20_mejora_continua_gemba_kaizen.txt":
        "FILOSOFÍA KAIZEN Y CAMINATAS GEMBA DE LIDERAZGO\n"
        "La mejora continua en la planta se ejecuta a través de dos herramientas del pilar de Liderazgo (Leading):\n"
        "- GEMBA WALK: Recorrido diario de los gerentes por el piso real de producción para observar operaciones y remover obstáculos.\n"
        "- KAIZEN: Sistema corporativo donde los operadores de primera línea envían ideas de micro-mejoras.\n"
        "Cada idea Kaizen aprobada e implementada con éxito genera un reconocimiento directo en el expediente del colaborador."
}

def build_knowledge_base():
    target_dir = "./data"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"Carpeta '{target_dir}' creada.")

    print("Generando los 20 documentos técnicos para la base de conocimiento GOBS...")
    for filename, content in knowledge_base.items():
        filepath = os.path.join(target_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f" -> Creado con éxito: {filename}")
    
    print("\n¡Listo! Tu carpeta './data' ya tiene los 20 documentos requeridos para la simulación.")

if __name__ == "__main__":
    build_knowledge_base()