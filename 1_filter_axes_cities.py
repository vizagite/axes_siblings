import csv
import geopandas as gpd
import json

def load_csv_data(csv_filename):
    cities = []
    with open(csv_filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            city = {
                'ascii_name': row['ASCII Name'],
                'population': int(row['Population']) if row['Population'] else 0,
                'coords': (float(row['Coordinates'].split(',')[0]), float(row['Coordinates'].split(',')[1])),
            }
            cities.append(city)
    return cities

def load_geojson_area(geojson_filename):
    return gpd.read_file(geojson_filename)

def find_bounding_box_with_buffer(geojson_area, buffer_one=0.10, buffer_two=0.25):
    minx, miny, maxx, maxy = geojson_area.total_bounds
    buffer_one_x = (maxx - minx) * buffer_one
    buffer_one_y = (maxy - miny) * buffer_one
    buffer_two_x = (maxx - minx) * buffer_two
    buffer_two_y = (maxy - miny) * buffer_two
    main_bounds = (minx, miny, maxx, maxy)
    buffer_one_bounds = (minx - buffer_one_x, miny - buffer_one_y, maxx + buffer_one_x, maxy + buffer_one_y)
    buffer_two_bounds = (minx - buffer_two_x, miny - buffer_two_y, maxx + buffer_two_x, maxy + buffer_two_y)
    return main_bounds, buffer_one_bounds, buffer_two_bounds

def find_cities_in_bounds(cities, main_bounds, buffer_one_bounds, buffer_two_bounds, max_population=100000):
    minx_buffer_one, miny_buffer_one, maxx_buffer_one, maxy_buffer_one = buffer_one_bounds
    minx_buffer_two, miny_buffer_two, maxx_buffer_two, maxy_buffer_two = buffer_two_bounds
    minx, miny, maxx, maxy = main_bounds
    filtered_cities = []
    filtered_cities_one = []
    filtered_cities_two = []
    
    for city in cities:
        if city['population'] < max_population:
            continue
        lat, lon = city['coords']
        if minx <= lon <= maxx or miny <= lat <= maxy:
            filtered_cities.append((city['ascii_name'], city['coords'], city['population']))
        elif minx_buffer_one <= lon <= maxx_buffer_one or miny_buffer_one <= lat <= maxy_buffer_one:
            filtered_cities_one.append((city['ascii_name'], city['coords'], city['population']))
        elif minx_buffer_two <= lon <= maxx_buffer_two or miny_buffer_two <= lat <= maxy_buffer_two:
            filtered_cities_two.append((city['ascii_name'], city['coords'], city['population']))
    
    return filtered_cities, filtered_cities_one, filtered_cities_two


def convert_to_serializable(data):
    if isinstance(data, set):
        return list(data)
    if isinstance(data, dict):
        return {k: convert_to_serializable(v) for k, v in data.items()}
    if isinstance(data, list):
        return [convert_to_serializable(i) for i in data]
    return data

def main(csv_filename, geojson_filename):
    cities = load_csv_data(csv_filename)
    geojson_area = load_geojson_area(geojson_filename)
    main_bounds, buffer_one_bounds, buffer_two_bounds = find_bounding_box_with_buffer(geojson_area)
    filtered_cities, filtered_cities_one, filtered_cities_two = find_cities_in_bounds(
        cities, main_bounds, buffer_one_bounds, buffer_two_bounds)
    
    with open("vizag_axes_siblings.json", 'w') as f:
        json.dump(convert_to_serializable({
            'filtered_cities': filtered_cities,
            'filtered_cities_one': filtered_cities_one,
            'filtered_cities_two': filtered_cities_two,
            'main_bounds': main_bounds,
            'buffer_one_bounds': buffer_one_bounds,
            'buffer_two_bounds': buffer_two_bounds
        }), f, indent=4)
csv_filename = "geonames-all-cities-with-a-population-1000.csv"
geojson_filename = "vizag.geojson"
main(csv_filename, geojson_filename)