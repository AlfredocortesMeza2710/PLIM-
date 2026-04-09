# VERSION FINAL DE PROYECTO PARA SCHNEIDER ELECTRIC PLANTA ROJO GOMEZ
#CODIGO HECHO POR: ALFREDO CORTES MEZA
#PROYECTO "PLIM" - PRODUCTION LINE INTEGRATION MANAGER 

import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# ---------------------------------
# IDIOMA GLOBAL
# ---------------------------------
if "idioma" not in st.session_state:
    st.session_state.idioma = "Español"

idioma = st.sidebar.selectbox(
    "Idioma / Language",
    ["Español", "English"],
    index=0 if st.session_state.idioma == "Español" else 1,
    key="selector_idioma"
)

st.session_state.idioma = idioma

# ---------------------------------
# TEXTOS
# ---------------------------------
textos = {
    "titulo": {"Español": "PLIM- CONTROL DE PRODUCCION","English": "PLIM- PRODUCTION CONTROL"},
    "agregar": {"Español": "Agregar Orden","English": "Add Order"},
    "editar": {"Español": "Editar Orden","English": "Edit Order"},
    "eliminar": {"Español": "Eliminar Orden","English": "Delete Order"},
    "estado": {"Español": "Estado","English": "Status"},
    "reporte": {"Español": "Reporte PDF","English": "PDF Report"},
    "filtro": {"Español": "Filtro","English": "Filter"},
    "mes": {"Español": "Seleccionar Mes","English": "Select Month"},
    "fecha_liberacion": {"Español": "Fecha de Liberación","English": "Release Date"},
    "servicio": {"Español": "Servicio al Cliente","English": "Customer Service"},
    "cumplimiento": {"Español": "Cumplimiento","English": "Performance"},
    "ventas": {"Español": "Ventas del Mes","English": "Monthly Sales"},
    "generar_pdf": {"Español": "Generar Reporte PDF","English": "Generate PDF Report"},
    "descargar": {"Español": "Descargar PDF","English": "Download PDF"},
    "ordenes": {"Español": "Órdenes","English": "Orders"},
    "carga": {"Español": "Carga de Trabajo por Día","English": "Daily Workload"},
    "actualizar": {"Español": "Actualizar Orden","English": "Update Order"},
    "seleccionar": {"Español": "Selecciona la orden","English": "Select Order"},
    "millones": {"Español": "Millones USD","English": "Millions USD"},
    "orden": {"Español": "Orden","English": "Order"},
    "estado_label": {"Español": "Estado","English": "Status"},
    "eliminar_titulo": {"Español": "Eliminar Orden","English": "Delete Order"},
    "carga_trabajo": {"Español": "Carga de Trabajo por Día","English": "Daily Workload"},
    "secciones": {"Español": "Secciones","English": "Sections"},
    "actualizada": {"Español": "Orden actualizada","English": "Order updated"},
}

# ---------------------------------
# ESTADOS TRADUCIDOS
# ---------------------------------
estados = {
    "Pre-embarque": {"Español": "Pre-embarque", "English": "Pre-shipping"},
    "Pruebas": {"Español": "Pruebas", "English": "Testing"},
    "Línea": {"Español": "Línea", "English": "Production"},
    "Liberado": {"Español": "Liberado", "English": "Released"},
    "Vencido": {"Español": "Vencido", "English": "Late"}
}

st.title(textos["titulo"][idioma])

# -------------------------------------------------
# DB
# -------------------------------------------------
conn = sqlite3.connect("ordenes_preembarque.db", check_same_thread=False)

conn.execute("""
CREATE TABLE IF NOT EXISTS ordenes (
    Orden TEXT PRIMARY KEY,
    Secciones INTEGER,
    LGI DATE,
    Fecha_Embarque DATE,
    Fecha_Liberado DATE,
    Estado TEXT,
    KUSD REAL,
    Comentarios TEXT
)
""")
conn.commit()

try:
    conn.execute("ALTER TABLE ordenes ADD COLUMN Fecha_Liberado DATE")
    conn.commit()
except:
    pass

try:
    conn.execute("ALTER TABLE ordenes ADD COLUMN Comentarios TEXT")
    conn.commit()
except:
    pass

df_total = pd.read_sql_query("SELECT * FROM ordenes", conn)

# -------------------------------------------------
# FILTRO
# -------------------------------------------------
st.sidebar.title(textos["filtro"][idioma])

mes = st.sidebar.selectbox(
    textos["mes"][idioma],
    ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
     "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"],
    key="filtro_mes"
)

# -------------------------------------------------
# AGREGAR
# -------------------------------------------------
st.subheader(textos["agregar"][idioma])

orden = st.text_input(textos["orden"][idioma], key="add_orden")
secciones = st.number_input(textos["secciones"][idioma], min_value=1, key="add_sec")
lgi = st.date_input("LGI", key="add_lgi")
fecha_embarque = None

estado = st.selectbox(
    textos["estado_label"][idioma],
    ["Pre-embarque","Pruebas","Línea","Liberado"],
    key="add_estado"
)

comentarios = ""
if estado == "Pre-embarque":
    comentarios = st.text_area("Comentarios Pre-embarque", key="add_comentarios")

kusd_input = st.text_input("KUSD", key="add_kusd")

try:
    kusd = float(kusd_input.replace(",", ""))
except:
    kusd = 0
    if kusd_input != "":
        st.warning("KUSD inválido, se asignó 0")

if st.button(textos["agregar"][idioma], key="btn_add"):

    if orden == "":
        st.error("Debes ingresar una orden")
    else:
        try:
            conn.execute(
                "INSERT INTO ordenes VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (orden, secciones, lgi, fecha_embarque, None, estado, kusd, comentarios)
            )
            conn.commit()
            st.success("Orden agregada")
            st.rerun()
        except:
            st.error("La orden ya existe")

# -------------------------------------------------
# EDITAR
# -------------------------------------------------
st.subheader(textos["editar"][idioma])

if not df_total.empty:

    orden_editar = st.selectbox(
        textos["seleccionar"][idioma],
        df_total["Orden"],
        key="edit_select"
    )

    fila = df_total[df_total["Orden"] == orden_editar].iloc[0]

    nuevo_lgi = st.date_input(
        "LGI",
        value=pd.to_datetime(fila["LGI"]) if pd.notnull(fila["LGI"]) else datetime.today(),
        key="edit_lgi"
    )

    nuevo_estado = st.selectbox(
        textos["estado_label"][idioma],
        ["Pre-embarque","Pruebas","Línea","Liberado"],
        index=["Pre-embarque","Pruebas","Línea","Liberado"].index(fila["Estado"]),
        key="edit_estado"
    )

    nuevo_comentario = fila["Comentarios"] if "Comentarios" in fila else ""

    if nuevo_estado == "Pre-embarque":
        nuevo_comentario = st.text_area(
            "Comentarios Pre-embarque",
            value=fila["Comentarios"] if pd.notnull(fila["Comentarios"]) else "",
            key="edit_comentarios"
        )
    else:
        nuevo_comentario = None

    if nuevo_estado == "Liberado":
        nuevo_fecha_liberado = st.date_input(
            textos["fecha_liberacion"][idioma],
            value=pd.to_datetime(fila["Fecha_Liberado"]) if pd.notnull(fila["Fecha_Liberado"]) else datetime.today(),
            key="edit_liberado"
        )
    else:
        nuevo_fecha_liberado = None

    if st.button(textos["actualizar"][idioma], key="btn_update"):

        conn.execute("""
        UPDATE ordenes
        SET LGI=?, Fecha_Embarque=?, Fecha_Liberado=?, Estado=?, Comentarios=?
        WHERE Orden=?
        """, (
            nuevo_lgi,
            fila["Fecha_Embarque"],
            nuevo_fecha_liberado if nuevo_estado == "Liberado" else None,
            nuevo_estado,
            nuevo_comentario if nuevo_estado == "Pre-embarque" else None,
            orden_editar
        ))

        conn.commit()
        st.success(textos["actualizada"][idioma])
        st.rerun()

# -------------------------------------------------
# PDF
# -------------------------------------------------
st.subheader(textos["reporte"][idioma])

if st.button("Generar Reporte PDF", key="btn_pdf"):

    df_pdf = pd.read_sql_query("SELECT * FROM ordenes", conn)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    elementos = []
    elementos.append(Paragraph("Reporte Pre-Embarque", styles["Title"]))

    data = [df_pdf.columns.tolist()] + df_pdf.astype(str).values.tolist()
    tabla = Table(data)

    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.black),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey)
    ]))

    elementos.append(tabla)

    # ✅ comentarios ANTES del build
    elementos.append(Paragraph("<b>Comentarios Pre-Embarque</b>", styles["Heading2"]))

    for _, row in df_pdf.iterrows():
        if row["Estado"] == "Pre-embarque" and pd.notnull(row["Comentarios"]):
            texto = f"Orden: {row['Orden']} - Comentarios: {row['Comentarios']}"
            elementos.append(Paragraph(texto, styles["Normal"]))

    doc.build(elementos)

    buffer.seek(0)

    st.download_button(
        "Descargar PDF",
        buffer,
        file_name="reporte_preembarque.pdf",
        mime="application/pdf"
    )