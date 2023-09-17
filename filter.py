import json

print('read...')
with open('buildings.json') as f:
    data = json.load(f)

full_geojson = {
    "type": "FeatureCollection",
    "features": [
    ]
}
print('filter...')

for feature in data['features']:
    if isinstance(feature['geometry']['coordinates'][0][0][0], float):
        full_geojson['features'].append(feature)

print('write...')
with open('buildings-filtered.json', 'w') as f:
    json.dump(full_geojson, f)