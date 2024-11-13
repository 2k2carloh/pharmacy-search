import requests
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster

url = 'https://midas.minsal.cl/farmacia_v2/WS/getLocalesTurnos.php'
fetch = requests.get(url)

regiones = [
    "1. Arica y Parinacota",
    "2. Tarapacá",
    "3. Antofagasta",
    "4. Atacama",
    "5. Coquimbo",
    "6. Valparaíso",
    "7. Metropolitana de Santiago",
    "8. O'Higgins",
    "9. Maule",
    "10. Ñuble",
    "11. Biobío",
    "12. La Araucanía",
    "13. Los Ríos",
    "14. Los Lagos",
    "15. Aysén del General Carlos Ibáñez del Campo",
    "16. Magallanes y de la Antártica Chilena"
]

comunas_por_region = {
    "1. Arica y Parinacota": ["Arica", "Camarones", "Putre", "General Lagos"],
    "2. Tarapacá": ["Iquique", "Alto Hospicio", "Huara", "Pica", "Pozo Almonte", "Camiña", "Colchane"],
    "3. Antofagasta": ["Antofagasta", "Mejillones", "Sierra Gorda", "Taltal", "Calama", "Ollagüe", "San Pedro de Atacama", "María Elena", "Tocopilla"],
    "4. Atacama": ["Copiapó", "Caldera", "Tierra Amarilla", "Chañaral", "Diego de Almagro", "Vallenar", "Alto del Carmen", "Freirina", "Huasco"],
    "5. Coquimbo": ["La Serena", "Coquimbo", "Andacollo", "La Higuera", "Paihuano", "Vicuña", "Illapel", "Canela", "Los Vilos", "Salamanca", "Ovalle", "Combarbalá", "Monte Patria", "Punitaqui", "Río Hurtado"],
    "6. Valparaíso": ["Valparaíso", "Viña del Mar", "Concón", "Quilpué", "Villa Alemana", "Limache", "Quillota", "Calera", "Hijuelas", "La Cruz", "Nogales", "San Antonio", "Cartagena", "El Quisco", "El Tabo", "Algarrobo", "Santo Domingo", "Los Andes", "San Esteban", "Calle Larga", "Rinconada", "San Felipe", "Putaendo", "Santa María", "Llaillay", "Catemu", "Panquehue", "Casablanca", "Juan Fernández", "Zapallar", "Papudo", "Petorca", "La Ligua"],
    "7. Metropolitana de Santiago": ["Santiago", "Cerrillos", "Cerro Navia", "Conchalí", "El Bosque", "Estación Central", "Huechuraba", "Independencia", "La Cisterna", "La Florida", "La Granja", "La Pintana", "La Reina", "Las Condes", "Lo Barnechea", "Lo Espejo", "Lo Prado", "Macul", "Maipú", "Ñuñoa", "Pedro Aguirre Cerda", "Peñalolén", "Providencia", "Pudahuel", "Quilicura", "Quinta Normal", "Recoleta", "Renca", "San Joaquín", "San Miguel", "San Ramón", "Vitacura", "Puente Alto", "San Bernardo", "Colina", "Lampa", "Tiltil", "Pirque", "San José de Maipo", "Buin", "Paine", "Calera de Tango"],
    "8. O'Higgins": ["Rancagua", "Machalí", "Graneros", "Codegua", "Doñihue", "Coinco", "Coltauco", "Las Cabras", "Peumo", "Pichidegua", "San Vicente", "Requínoa", "Rengo", "Malloa", "San Fernando", "Chépica", "Chimbarongo", "Lolol", "Nancagua", "Palmilla", "Peralillo", "Placilla", "Pumanque", "Santa Cruz", "Pichilemu", "Marchigüe", "La Estrella", "Litueche", "Navidad", "Paredones"],
    "9. Maule": ["Talca", "Constitución", "Curepto", "Empedrado", "Maule", "Pelarco", "Pencahue", "Río Claro", "San Clemente", "San Rafael", "Curicó", "Hualañé", "Licantén", "Molina", "Rauco", "Romeral", "Sagrada Familia", "Teno", "Vichuquén", "Linares", "Colbún", "Longaví", "Parral", "Retiro", "San Javier", "Villa Alegre", "Yerbas Buenas", "Cauquenes", "Chanco", "Pelluhue"],
    "10. Ñuble": ["Chillán", "Chillán Viejo", "Quirihue", "Cobquecura", "Coelemu", "Ninhue", "Portezuelo", "Ránquil", "Treguaco", "Bulnes", "Quillón", "San Ignacio", "El Carmen", "Pemuco", "Yungay", "San Carlos", "San Nicolás"],
    "11. Biobío": ["Concepción", "Coronel", "Chiguayante", "Florida", "Hualqui", "Lota", "Penco", "San Pedro de la Paz", "Santa Juana", "Talcahuano", "Tomé", "Hualpén", "Los Ángeles", "Cabrero", "Laja", "Mulchén", "Nacimiento", "Negrete", "San Rosendo", "Santa Bárbara", "Tucapel", "Yumbel", "Alto Biobío", "Arauco", "Cañete", "Contulmo", "Curanilahue", "Lebu", "Los Álamos", "Tirúa"],
    "12. La Araucanía": ["Temuco", "Carahue", "Cunco", "Curarrehue", "Freire", "Galvarino", "Gorbea", "Lautaro", "Loncoche", "Melipeuco", "Nueva Imperial", "Padre Las Casas", "Perquenco", "Pitrufquén", "Pucón", "Saavedra", "Teodoro Schmidt", "Toltén", "Vilcún", "Villarrica", "Cholchol", "Angol", "Collipulli", "Curacautín", "Ercilla", "Lonquimay", "Los Sauces", "Lumaco", "Purén", "Renaico", "Traiguén", "Victoria"],
    "13. Los Ríos": ["Valdivia", "Corral", "Lanco", "Los Lagos", "Máfil", "Mariquina", "Paillaco", "Panguipulli", "La Unión", "Futrono", "Lago Ranco", "Río Bueno"],
    "14. Los Lagos": ["Puerto Montt", "Calbuco", "Cochamó", "Fresia", "Frutillar", "Los Muermos", "Llanquihue", "Maullín", "Puerto Varas", "Castro", "Ancud", "Chonchi", "Curaco de Vélez", "Dalcahue", "Puqueldón", "Queilén", "Quellón", "Quemchi", "Quinchao", "Osorno", "Puerto Octay", "Purranque", "Puyehue", "Río Negro", "San Juan de la Costa", "San Pablo", "Palena", "Chaitén", "Futaleufú", "Hualaihué"],
    "15. Aysén del General Carlos Ibáñez del Campo": ["Coyhaique", "Lago Verde", "Aysén", "Cisnes", "Guaitecas", "Chile Chico", "Río Ibáñez", "Cochrane", "O'Higgins", "Tortel"],
    "16. Magallanes y de la Antártica Chilena": ["Punta Arenas", "Laguna Blanca", "Río Verde", "San Gregorio", "Cabo de Hornos", "Antártica", "Porvenir", "Primavera", "Timaukel", "Puerto Natales", "Torres del Paine"]
}

if fetch.status_code == 200:
    print(f'{fetch.status_code}: conectado correctamente.')
    st.title("Consulta de Farmacias")
    
    if 'comunas_disponibles' not in st.session_state:
        st.session_state.comunas_disponibles = []

    region_seleccionada = st.selectbox("Selecciona una Región", regiones, key="region")
    
    st.session_state.comunas_disponibles = comunas_por_region.get(region_seleccionada, [])

    comuna_seleccionada = st.selectbox("Selecciona una Comuna", st.session_state.comunas_disponibles, key="comuna")
    
    def obtener_farmacias(region_id, comuna_id):
        params = {
            'fk_region': region_id,
            'fk_comuna': comuna_id
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error al obtener las farmacias: {response.status_code}")
            return []

    if st.button("Buscar Farmacias"):
        farmacias = obtener_farmacias(region_seleccionada.split(".")[0], comuna_seleccionada)

        comuna_seleccionada_upper = comuna_seleccionada.upper()
        farmacias_filtradas = [farmacia for farmacia in farmacias if farmacia['comuna_nombre'].upper() == comuna_seleccionada_upper]

        if farmacias_filtradas:
            farmacias_data = [{
                'Nombre': farmacia['local_nombre'],
                'Dirección': farmacia['local_direccion'],
                'Comuna': farmacia['comuna_nombre'],
                'Teléfono': farmacia['local_telefono'],
                'Hora Apertura': farmacia['funcionamiento_hora_apertura'],
                'Hora Cierre': farmacia['funcionamiento_hora_cierre'],
                'Lat': farmacia.get('local_lat', None),
                'Lon': farmacia.get('local_lng', None)
            } for farmacia in farmacias_filtradas]

            df_farmacias = pd.DataFrame(farmacias_data)

            st.dataframe(df_farmacias)

            mapa = folium.Map(location=[-33.4489, -70.6693], zoom_start=6)

            marker_cluster = MarkerCluster().add_to(mapa)
            for farmacia in farmacias_data:
                if farmacia['Lat'] and farmacia['Lon']:
                    folium.Marker(
                        location=[farmacia['Lat'], farmacia['Lon']],
                        popup=f"{farmacia['Nombre']}<br>{farmacia['Dirección']}<br>Tel: {farmacia['Teléfono']}",
                        icon=folium.Icon(color='blue')
                    ).add_to(marker_cluster)

            st.markdown("### Mapa de Farmacias")
            st.components.v1.html(mapa._repr_html_(), width=700, height=500)
        else:
            st.write("No se encontraron farmacias para esta región y comuna.")
    
else:
    print(f'No se pudo conectar al servidor. error: {fetch.status_code} ')
