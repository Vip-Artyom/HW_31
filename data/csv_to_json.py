import csv
import json

DATA_AD = "data/source/ad.csv"
JSON_AD = "data/source/ad.json"
DATA_CATEGORY = "data/source/category.csv"
JSON_CATEGORY = "data/source/category.json"
DATA_LOCATION = "data/source/location.csv"
JSON_LOCATION = "data/source/location.json"
DATA_USER = "data/source/user.csv"
JSON_USER = "data/source/user.json"


def convert_to_json(csv_file, model_name, json_file):
    with open(csv_file, encoding='utf-8') as csv_f:
        result = []
        for row in csv.DictReader(csv_f):
            to_add = {'model': model_name, 'pk': int(row['Id'] if 'Id' in row else row['id'])}
            if 'Id' in row:
                del row['Id']
            else:
                del row['id']
            if 'is_published' in row:
                if row['is_published'] == 'TRUE':
                    row['is_published'] = True
                else:
                    row['is_published'] = False
            if 'price' in row:
                row['price'] = int(row['price'])
            to_add['fields'] = row
            result.append(to_add)

    with open(json_file, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(result, ensure_ascii=False))


convert_to_json(DATA_AD, "ads.ad", JSON_AD)
convert_to_json(DATA_CATEGORY, "ads.category", JSON_CATEGORY)
convert_to_json(DATA_LOCATION, "users.location", JSON_LOCATION)
convert_to_json(DATA_USER, "users.user", JSON_USER)
