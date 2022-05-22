import requests, zipfile, io, json
from pathlib import Path

zip_file_url = "https://docs.unit.co/json-schemas.zip"
extract_dir = "./files"

# r = requests.get(zip_file_url)
# z = zipfile.ZipFile(io.BytesIO(r.content))
# z.extractall(extract_dir)

files = Path(extract_dir).glob('*')
for file in files:
    with open(file) as data_file:
        data = json.load(data_file)
        print(data)
        # for v in data.values():
        #     print(v['x'], v['y'], v['yr'])





