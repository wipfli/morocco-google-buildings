import csv
import json
from shapely.wkt import loads
from shapely import to_geojson

# latitude,longitude,area_in_meters,confidence,geometry,full_plus_code,last_detection_date

with open('open_buildings_v3_morocco_epicenter.csv') as csv_file:

    csv_reader = csv.reader(csv_file, delimiter=',')
    first_line = True

    lines = []
    for row in csv_reader:
        if first_line:
            first_line = False
            continue

        line = {
            # 'latitude': row[0],
            # 'longitude': row[1],
            # 'area_in_meters': row[2],
            'confidence': float(row[3]),
            'geometry': row[4],
            # 'full_plus_code': row[5],
            'last_detection_date': row[6],
        }

        coordinates = json.loads(to_geojson(loads(line['geometry'])))['coordinates']

        del line['geometry']
        line['coordinates'] = coordinates
        lines.append(line)
        if len(lines) % 1000 == 0:
            print(len(lines))


    full_geojson = {
        "type": "FeatureCollection",
        "features": [
        ]
    }
    for line in lines:
        geojson = {
            "type": "Feature",
            "properties": {
                "confidence": line['confidence'],
                "last_detection_date": line['last_detection_date'],
            },
            "geometry": {
                "coordinates": line['coordinates'],
                "type": "Polygon"
            }
        }

        full_geojson['features'].append(geojson)


with open('buildings.json', 'w') as f:
    json.dump(full_geojson, f)
