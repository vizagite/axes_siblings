from shapely.geometry import Polygon
import folium
import json

def plot_map(filtered_cities, filtered_cities_one, filtered_cities_two, bounds, buffer_one_bounds, buffer_two_bounds):
    center_lat = (bounds[1] + bounds[3]) / 2
    center_lon = (bounds[0] + bounds[2]) / 2
    
    m = folium.Map(
        location=[center_lat, center_lon], 
        zoom_start=6, 
        control_scale=True, 
        tiles="Cartodb Positron", 
        max_bounds=True,
        max_bounds_visible=True, 
        attr = 'OpenStreetMap contributors, CARTO, <a href="https://github.com/vizagite">github.com/vizagite</a>'
    )

    vertical_band = Polygon([(bounds[0], -90), (bounds[0], 90), (bounds[2], 90), (bounds[2], -90)])    
    horizontal_band = Polygon([(-180, bounds[1]), (180, bounds[1]), (180, bounds[3]), (-180, bounds[3])])    
    vertical_band_one = Polygon([(buffer_one_bounds[0], -90), (buffer_one_bounds[0], 90), (buffer_one_bounds[2], 90), (buffer_one_bounds[2], -90)])
    horizontal_band_one = Polygon([(-180, buffer_one_bounds[1]), (180, buffer_one_bounds[1]), (180, buffer_one_bounds[3]), (-180, buffer_one_bounds[3])])
    vertical_band_two = Polygon([(buffer_two_bounds[0], -90), (buffer_two_bounds[0], 90), (buffer_two_bounds[2], 90), (buffer_two_bounds[2], -90)])
    horizontal_band_two = Polygon([(-180, buffer_two_bounds[1]), (180, buffer_two_bounds[1]), (180, buffer_two_bounds[3]), (-180, buffer_two_bounds[3])])

    folium.GeoJson(vertical_band, style_function=lambda x: {'fillColor': 'lightgray', 'color': 'gray', 'fillOpacity': 0.2}).add_to(m)
    folium.GeoJson(horizontal_band, style_function=lambda x: {'fillColor': 'lightgray', 'color': 'gray', 'fillOpacity': 0.2}).add_to(m)

    folium.GeoJson(vertical_band_one, style_function=lambda x: {'fillColor': 'orange', 'color': 'orange', 'fillOpacity': 0.1}).add_to(m)
    folium.GeoJson(horizontal_band_one, style_function=lambda x: {'fillColor': 'orange', 'color': 'orange', 'fillOpacity': 0.1}).add_to(m)

    folium.GeoJson(vertical_band_two, style_function=lambda x: {'fillColor': 'yellow', 'color': 'yellow', 'fillOpacity': 0.05}).add_to(m)
    folium.GeoJson(horizontal_band_two, style_function=lambda x: {'fillColor': 'yellow', 'color': 'yellow', 'fillOpacity': 0.05}).add_to(m)

    def get_marker_size(population):
        base_size = min(10, population / 100000)
        return base_size
    from collections import defaultdict
    
    # def add_text_label(map_obj, lat, lon, text, label_positions):
    #     grid_size = 1
    #     grid_x = int(lon / grid_size)
    #     grid_y = int(lat / grid_size)
    #     if 74< lon < 84 and lat < 40:
    #         # skipping india for screenshot
    #         return 
    #     position_key = (grid_x, grid_y)
    #     if position_key not in label_positions:
    #         label_positions[position_key] = 1
    #     label_offset = label_positions[position_key] * 4
    #     label_positions[position_key] += 1
        
    #     # india
    #     # label_lat = lat + label_offset * 0.5
    #     # label_lon = lon + label_offset * 0.8
          
    #     # world     
    #     label_lat = lat + label_offset * 2
    #     label_lon = lon + label_offset * 1.4
        
    #     folium.PolyLine([(lat, lon), (label_lat, label_lon - 0.2)], color='teal', weight=1).add_to(map_obj)
        
    #     folium.Marker(
    #         location=[label_lat, label_lon],
    #         icon=folium.DivIcon(html=f'<div style="font-size: 10pt">{text}</div>')
    #     ).add_to(map_obj)

    def plot_city_set(cities, color):
        for city in cities:
            city_name, (lat, lon), population = city
            marker_size = get_marker_size(population)
            description = city_descriptions.get(city_name, 'No description available')

            folium.CircleMarker(
                location=[lat, lon],
                radius=marker_size,
                color="red",
                fill=True,
                fill_color=color,
                fill_opacity=1.0,
                popup=folium.Popup(f'<b>{city_name}</b>: {population:,} (~people in 2024)<br><br>{description}', max_width=200)
            ).add_to(m)
            # label_positions = defaultdict(int)
            # if marker_size > 2: #for screenshot
                # add_text_label(m, lat, lon, city_name, label_positions)
    plot_city_set(filtered_cities, 'lightgray')
    plot_city_set(filtered_cities_one, 'orange')
    plot_city_set(filtered_cities_two, 'yellow')
    m.save('index.html')

# chatgpt
city_descriptions = {
    'Spanish Town': 'Historic capital of Jamaica, known for its colonial architecture and rich history.',
    'Xinyuan': 'A county-level city in Xinjiang, China, famous for its stunning natural landscapes and ethnic diversity.',
    'Satara': 'A city in Maharashtra, India, renowned for its historical forts and proximity to the scenic Western Ghats.',
    'Villahermosa': 'Capital of Tabasco, Mexico, known for its archaeological sites and vibrant cultural scene.',
    'Visakhapatnam': 'Major port city in India, recognized for its beaches, shipbuilding industry, and scenic hills.',
    'Bidar': 'A city in Karnataka, India, famous for its historical monuments and Bidriware handicrafts.',
    'Raigarh': 'A city in Chhattisgarh, India, known for its rich cultural heritage and natural resources.',
    'Ponce': 'A city in Puerto Rico, celebrated for its unique architecture and vibrant arts scene.',
    'Atbara': 'A city in Sudan, known for its railway history and as a hub for agricultural trade.',
    'Vizianagaram': 'A city in Andhra Pradesh, India, known for its historical significance and cultural heritage.',
    'Hinthada': 'A town in Myanmar, recognized for its agricultural production and local markets.',
    'Portmore': 'A coastal town in Jamaica, known for its residential communities and proximity to Kingston.',
    'Solapur': 'A city in Maharashtra, India, famous for its textile industry and historical temples.',
    'Warangal': 'A city in Telangana, India, known for its rich history and UNESCO World Heritage Sites.',
    'Gorakhpur': 'A city in Uttar Pradesh, India, known for its religious significance and as a major railway hub.',
    'Chilpancingo': 'Capital of Guerrero, Mexico, known for its political history and cultural festivals.',
    'Ad Damir': 'A city in Sudan, recognized for its agricultural activities and local markets.',
    'Minatitlan': 'A city in Veracruz, Mexico, known for its oil industry and strategic port location.',
    'Kingston': 'Capital of Jamaica, known for its vibrant music scene and cultural landmarks.',
    'Vientiane': 'Capital of Laos, known for its French colonial architecture and Buddhist temples.',
    'Tuguegarao': 'Capital of Cagayan, Philippines, known for its historical sites and as a gateway to natural attractions.',
    'Azamgarh': 'A city in Uttar Pradesh, India, known for its cultural heritage and historical significance.',
    'Mau': 'A city in Uttar Pradesh, India, recognized for its agricultural production and local industries.',
    'Nouakchott': 'Capital of Mauritania, known for its coastal location and vibrant markets.',
    'Tuxtepec': 'A city in Oaxaca, Mexico, known for its agricultural production and cultural festivals.',
    'Hyderabad': 'Capital of Telangana, India, renowned for its historical landmarks and IT industry.',
    'Najran': 'A city in Saudi Arabia, known for its archaeological sites and rich cultural heritage.',
    'Dong Hoi': 'A city in Vietnam, recognized for its coastal beauty and proximity to Phong Nha-Ke Bang National Park.',
    'Ghazipur': 'A city in Uttar Pradesh, India, known for its historical significance and local handicrafts.',
    'Mulugu': 'A town in Telangana, India, known for its natural beauty and cultural heritage.',
    'Les Cayes': 'A coastal city in Haiti, known for its beautiful beaches and agricultural production.',
    'Varanasi': 'One of the oldest cities in the world, known for its spiritual significance and ghats along the Ganges.',
    'Coatzacoalcos': 'A city in Veracruz, Mexico, known for its oil industry and strategic port.',
    'Dharashiv': 'A city in Maharashtra, India, known for its historical caves and cultural significance.'
}


def load_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data
data = load_json("vizag_axes_siblings_sanitised.json")
filtered_cities = data['filtered_cities']
filtered_cities_one = data['filtered_cities_one']
filtered_cities_two = data['filtered_cities_two']
main_bounds = data['main_bounds']
buffer_one_bounds = data['buffer_one_bounds']
buffer_two_bounds = data['buffer_two_bounds']
plot_map(filtered_cities, filtered_cities_one, filtered_cities_two, main_bounds, buffer_one_bounds, buffer_two_bounds)
