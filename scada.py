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
    "titulo": {
        "Español": "PLIM- CONTROL DE PRODUCCION",
        "English": "PLIM- PRODUCTION CONTROL"
    },
    "agregar": {
        "Español": "Agregar Orden",
        "English": "Add Order"
    },
    "editar": {
        "Español": "Editar Orden",
        "English": "Edit Order"
    },
    "eliminar": {
        "Español": "Eliminar Orden",
        "English": "Delete Order"
    },
    "estado": {
        "Español": "Estado",
        "English": "Status"
    },
    "reporte": {
        "Español": "Reporte PDF",
        "English": "PDF Report"
    },
    "filtro": {
        "Español": "Filtro",
        "English": "Filter"
    },
    "mes": {
        "Español": "Seleccionar Mes",
        "English": "Select Month"
    },
    "fecha_liberacion": {
        "Español": "Fecha de Liberación",
        "English": "Release Date"
    
    },
    "btn_eliminar": {
        "Español": "Eliminar Orden",
        "English": "Delete Order"
    },
    "servicio": {
        "Español": "Servicio al Cliente",
        "English": "Customer Service"
    },
    "cumplimiento": {
    "Español": "Cumplimiento",
    "English": "Performance"
    },
    "ventas": {
    "Español": "Ventas del Mes",
    "English": "Monthly Sales"
    },
    "generar_pdf": {
    "Español": "Generar Reporte PDF",
    "English": "Generate PDF Report"
    },
    "descargar": {
    "Español": "Descargar PDF",
    "English": "Download PDF"
    },
    "ordenes": {
    "Español": "Órdenes",
    "English": "Orders"
    },
    "carga": {
    "Español": "Carga de Trabajo por Día",
    "English": "Daily Workload"
    },
    "actualizar": {
    "Español": "Actualizar Orden",
    "English": "Update Order"
    },
    "seleccionar": {
    "Español": "Selecciona la orden",
    "English": "Select Order"
    },
    "ventas": {
    "Español": "Ventas del Mes",
    "English": "Monthly Sales"
    },
    "millones": {
    "Español": "Millones USD",
    "English": "Millions USD"
    },
    "orden": {
    "Español": "Orden",
    "English": "Order"
    },
    "estado_label": {
    "Español": "Estado",
    "English": "Status"
    },
    "eliminar_titulo": {
    "Español": "Eliminar Orden",
    "English": "Delete Order"
    },
    "carga_trabajo": {
    "Español": "Carga de Trabajo por Día",
    "English": "Daily Workload"
    },
    "secciones": {
    "Español": "Secciones",
    "English": "Sections"
    },
    "error_orden": {
    "Español": "Debes ingresar una orden",
    "English": "You must enter an order"
    },
    "orden_agregada": {
        "Español": "Orden agregada",
        "English": "Order added"
    },
    "orden_existe": {
        "Español": "La orden ya existe",
        "English": "Order already exists"
    },
    "eliminada": {
        "Español": "Eliminada",
        "English": "Deleted"
    },
    "sin_ordenes": {
        "Español": "No hay órdenes para este mes",
        "English": "No orders for this month"
    },
    "titulo_pdf": {
        "Español": "Reporte Pre-Embarque",
        "English": "Pre-shipping Report"
    },
    "actualizada": {
        "Español": "Orden actualizada",
        "English": "Order updated"
    },
    "agregada": {
        "Español": "Orden agregada",
        "English": "Order added"
    },
    "eliminada": {
        "Español": "Orden eliminada",
        "English": "Order deleted"
    },
    "error_orden": {
        "Español": "La orden ya existe",
        "English": "Order already exists"
    },
    "error_vacio": {
        "Español": "Debes ingresar una orden",
        "English": "You must enter an order"
},
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

# ---------------------------------
# TITULOS 
# ---------------------------------
st.title(textos["titulo"][st.session_state.idioma])

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
    KUSD REAL
)
""")
conn.commit()
try:
    conn.execute("ALTER TABLE ordenes ADD COLUMN Fecha_Liberado DATE")
    conn.commit()
except:
    pass

df_total = pd.read_sql_query("SELECT * FROM ordenes", conn)

# -------------------------------------------------
# FILTRO
# -------------------------------------------------
st.sidebar.title(textos["filtro"][st.session_state.idioma])

mes = st.sidebar.selectbox(
    textos["mes"][st.session_state.idioma],
    ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
     "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"],
    key="filtro_mes"
)

# -------------------------------------------------
# AGREGAR
# -------------------------------------------------
st.subheader(textos["agregar"][st.session_state.idioma])

orden = st.text_input(textos["orden"][idioma], key="add_orden")
secciones = st.number_input(textos["secciones"][idioma], min_value=1, key="add_sec")
lgi = st.date_input("LGI", key="add_lgi")
fecha_embarque = None

estado = st.selectbox(
    textos["estado_label"][idioma],
    ["Pre-embarque","Pruebas","Línea","Liberado"],
    key="add_estado"
)

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
                "INSERT INTO ordenes VALUES (?, ?, ?, ?, ?, ?, ?)",
                (orden, secciones, lgi, fecha_embarque, None, estado, kusd)
            )
            conn.commit()
            st.success("Orden agregada")
            st.rerun()
        except:
            st.error("La orden ya existe")
# -------------------------------------------------
# EDITAR
# -------------------------------------------------
st.subheader(textos["editar"][st.session_state.idioma])

if not df_total.empty:

    orden_editar = st.selectbox(
        textos["seleccionar"][st.session_state.idioma],
        df_total["Orden"],
        key="edit_select"
    )

    fila = df_total[df_total["Orden"] == orden_editar].iloc[0]

    nuevo_lgi = st.date_input(
        "LGI",
        value=pd.to_datetime(fila["LGI"]) if pd.notnull(fila["LGI"]) else datetime.today(),
        key="edit_lgi"
    )

    nuevo_estado = st.selectbox(textos["estado_label"][idioma],
        ["Pre-embarque","Pruebas","Línea","Liberado"],
        index=["Pre-embarque","Pruebas","Línea","Liberado"].index(fila["Estado"]),
        key="edit_estado"
    )

    # SOLO SI ES LIBERADO
    if nuevo_estado == "Liberado":
        nuevo_fecha_liberado = st.date_input(
            textos["fecha_liberacion"][st.session_state.idioma],
            value=pd.to_datetime(fila["Fecha_Liberado"]) if pd.notnull(fila["Fecha_Liberado"]) else datetime.today(),
            key="edit_liberado"
        )
    else:
        nuevo_fecha_liberado = None

    if st.button(textos["actualizar"][st.session_state.idioma], key="btn_update"):

        conn.execute("""
        UPDATE ordenes
        SET LGI=?, Fecha_Embarque=?, Fecha_Liberado=?, Estado=?
        WHERE Orden=?
        """, (
            nuevo_lgi,
            fila["Fecha_Embarque"],
            nuevo_fecha_liberado if nuevo_estado == "Liberado" else None,
            nuevo_estado,
            orden_editar
        ))

        conn.commit()
        st.success(textos["actualizada"][idioma])
        st.rerun()

# -------------------------------------------------
# ELIMINAR
# -------------------------------------------------
st.subheader(textos["eliminar_titulo"][idioma])

if not df_total.empty:

    orden_eliminar = st.selectbox(
        textos["seleccionar"][st.session_state.idioma],
        df_total["Orden"],
        key="del_select"
    )

    if st.button(textos["eliminar"][st.session_state.idioma], key="btn_delete"):

        conn.execute("DELETE FROM ordenes WHERE Orden=?", (orden_eliminar,))
        conn.commit()
        st.success("Eliminada")
        st.rerun()

# -------------------------------------------------
# LIMPIEZA
# -------------------------------------------------
hoy = datetime.today()
limite = (hoy - pd.DateOffset(months=3)).strftime("%Y-%m-%d")

conn.execute("DELETE FROM ordenes WHERE DATE(LGI) < DATE(?)", (limite,))
conn.commit()

# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------
df = pd.read_sql_query("SELECT * FROM ordenes", conn)

if not df.empty:

    df["LGI"] = pd.to_datetime(df["LGI"])
    df["KUSD"] = pd.to_numeric(df["KUSD"])

    meses = {
        "Enero":1,"Febrero":2,"Marzo":3,"Abril":4,
        "Mayo":5,"Junio":6,"Julio":7,"Agosto":8,
        "Septiembre":9,"Octubre":10,"Noviembre":11,"Diciembre":12
    }

    mes_num = meses[mes]

    df_filtrado = df[df["LGI"].dt.month == mes_num]

    df = df_filtrado

    if df_filtrado.empty:
        st.warning("No hay órdenes para este mes")
    

    # Convertir fechas
    df["LGI"] = pd.to_datetime(df["LGI"], errors="coerce")
    df["Fecha_Liberado"] = pd.to_datetime(df["Fecha_Liberado"], errors="coerce")

#  REGLA REAL
    df.loc[
        (df["Estado"] == "Liberado") & (df["Fecha_Liberado"] > df["LGI"]),
        "Estado"
    ] = "Vencido"

# -------------------------------------------------
# KPIs
# -------------------------------------------------
if not df.empty:

    total = len(df)
    vencidos = len(df[df["Estado"] == "Vencido"])
    servicio = ((total - vencidos) / total) * 100

    ventas = df[df["Estado"] == "Liberado"]["KUSD"].sum() / 1000

    st.subheader(textos["servicio"][idioma])
    st.metric(textos["cumplimiento"][idioma], f"{servicio:.2f}%")

    st.subheader(textos["ventas"][idioma])
    st.metric(textos["millones"][idioma], f"${ventas:.2f} M")

# -------------------------------------------------
# PDF 
# -------------------------------------------------
st.subheader(textos["reporte"][st.session_state.idioma])

if not df.empty:

    if st.button("Generar Reporte PDF", key="btn_pdf"):

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        elementos = []
        elementos.append(Paragraph("Reporte Pre-Embarque", styles["Title"]))

        # LIMPIEZA
        df_reporte = df.drop(columns=["Fecha_Embarque"], errors="ignore").copy()

        # FORMATO DE FECHAS 
        for col in ["LGI", "Fecha_Liberado"]:
            if col in df_reporte.columns:
                df_reporte[col] = pd.to_datetime(df_reporte[col], errors="coerce").dt.strftime("%d-%m-%Y")

        #CONVERTIR TODO A TEXTO
        df_reporte = df_reporte.astype(str)

        # TABLA
        data = [df_reporte.columns.tolist()] + df_reporte.values.tolist()

        tabla = Table(data)
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.black),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey)
        ]))

        elementos.append(tabla)
        doc.build(elementos)

        buffer.seek(0)

        st.download_button(
            "Descargar PDF",
            buffer,
            file_name="reporte_preembarque.pdf",
            mime="application/pdf"
        )

# -------------------------------------------------
# TABLA
# -------------------------------------------------
st.subheader(textos["ordenes"][st.session_state.idioma])
def colorear(row):
    colores = {
        "Pre-embarque": "#D3D3D3",  
        "Pruebas": "#0B3D91",
        "Línea": "orange",
        "Liberado": "green",
        "Vencido": "red"
    }
    
    estado_real = row.get("Estado", "")
    
    # IMPORTANTE: traducir de regreso si está en inglés
    estados_reverse = {
        "Pre-shipping": "Pre-embarque",
        "Testing": "Pruebas",
        "Production": "Línea",
        "Released": "Liberado",
        "Late": "Vencido"
    }

    estado_real = estados_reverse.get(estado_real, estado_real)

    color = colores.get(estado_real, "white")
    return [f"background-color: {color}; color: white"] * len(row)

if not df.empty:

    df_mostrar = df.copy()
    df_mostrar = df_mostrar.drop(columns=["Fecha_Embarque"], errors="ignore")
    # FORMATO DE FECHAS
    df_mostrar["LGI"] = pd.to_datetime(df_mostrar["LGI"], errors="coerce").dt.strftime("%d-%m-%Y")
    df_mostrar["Fecha_Liberado"] = pd.to_datetime(df_mostrar["Fecha_Liberado"], errors="coerce").dt.strftime("%d-%m-%Y")
    # FORMATO KUSD 
    df_mostrar["KUSD"] = df_mostrar["KUSD"].apply(lambda x: f"{x:,.2f}")
    #  CREAR COLUMNA TRADUCIDA (SIN TOCAR LA ORIGINAL)
    df_mostrar["Estado"] = df_mostrar["Estado"].map(
        lambda x: estados.get(x, {}).get(st.session_state.idioma, x)
    )
   

    # MOSTRAR
    st.dataframe(df_mostrar.style.apply(colorear, axis=1))

else:
    st.warning("No hay órdenes para mostrar")
# -------------------------------------------------
# GRAFICA
# -------------------------------------------------
st.subheader(textos["carga_trabajo"][idioma])

if not df.empty:

    df_graf = df.copy()

    df_graf = df_graf[df_graf["Estado"] != "Liberado"]

    carga = df_graf.groupby("LGI")["Secciones"].sum()

    st.bar_chart(carga)