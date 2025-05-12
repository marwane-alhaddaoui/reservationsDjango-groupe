import json
from pathlib import Path

# Chemins des fichiers
base_path = Path(__file__).resolve().parent.parent

artist_fixtures_path = base_path / 'fixtures' / 'ArtistFixtures.json'
artist_type_path = base_path / 'fixtures' / 'artist_type.json'

# Charger les artistes depuis ArtistFixtures.json
with open(artist_fixtures_path, 'r', encoding='utf-8') as artist_file:
    artist_data = json.load(artist_file)

# Créer un mapping {id: id}
artist_mapping = {
    artist['pk']: artist['pk']  # Associer directement l'ID à lui-même
    for artist in artist_data
}

# Charger les types existants depuis artist_type.json
with open(artist_type_path, 'r', encoding='utf-8') as artist_type_file:
    artist_type_data = json.load(artist_type_file)

# Mettre à jour les références dans artist_type.json
for entry in artist_type_data:
    if 'fields' in entry and 'artist' in entry['fields']:
        artist_id = entry['fields']['artist']  # Récupérer l'ID directement
        if artist_id in artist_mapping:
            entry['fields']['artist'] = artist_mapping[artist_id]
        else:
            print(f"Artiste non trouvé avec l'ID : {artist_id}")

# Sauvegarder les données mises à jour dans artist_type.json
with open(artist_type_path, 'w', encoding='utf-8') as artist_type_file:
    json.dump(artist_type_data, artist_type_file, indent=2, ensure_ascii=False)

print("artist_type.json a été mis à jour avec les IDs des artistes.")