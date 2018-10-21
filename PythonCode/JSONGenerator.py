import json
import csv

output = { "type": "FeatureCollection",
           "features": []}
rowCount = 50
with open('top500.csv') as csv_file:
    for (i,row) in enumerate(csv.DictReader(csv_file)):
        if i < rowCount:
            print(i)
            output['features'].append({
                'type': 'Feature',
                'properties': {"Rank": row["Rank"],
                               "Name": row["Name"],
                               "City": row["City"],
                               "Country": row["Country"],
                               "Manufacturer": row["Manufacturer"],
                               "Cores":'{0:,}'.format(int(row["Cores"])),
                               "Rmax": '{0:,}'.format(float(row["Rmax"])),
                               "Rpeak": '{0:,}'.format(float(row["Rpeak"])),
                               "Power": row["Power"],
                               "icon": "Markers/" + row["Rank"]+".png"
                               },
                "geometry":{"type": "Point",
                            "coordinates":[float(row["Lng"]),float(row["Lat"])]}
            })
        else:
            break

output_json = json.dumps(output)

print(output_json)