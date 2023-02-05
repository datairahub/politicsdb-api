#!/bin/bash
echo "Restarting..."

echo "Remove sqlite"
rm -f backend/db.sqlite3

echo "Execute migrations"
python backend/manage.py migrate

echo "Update Spain parties from file"
python backend/manage.py update_parties

echo "Update Spain legislators from www.congreso.es"
python backend/manage.py update_spain_legislators
python backend/manage.py update_birth_dates_from_congresoes

echo "Get spain senators from senado.es"
python backend/manage.py update_spain_senators

echo "Fix duplicated persons"
python backend/manage.py fix_duplicated_persons

echo "Fix genres"
python backend/manage.py update_genres

echo "Get birth dates"
python backend/manage.py update_birth_dates_from_congresoes_historical
python backend/manage.py update_birth_dates_from_file
python backend/manage.py update_birth_dates_from_wikidata
python backend/manage.py update_birth_dates_from_wikipedia

# echo "Enrich data"
# python manage.py enrich_data_from_paresmcues
# python manage.py enrich_data_from_fpabloiglesias
