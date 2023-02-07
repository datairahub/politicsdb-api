#!/bin/bash
echo "Restarting..."

echo "Remove sqlite"
rm -f backend/db.sqlite3

echo "Execute migrations"
python backend/manage.py migrate -v 0

echo "Update Spain parties from file"
python backend/manage.py update_parties -v 1

echo "Update Spain legislators from www.congreso.es"
python backend/manage.py update_spain_legislators -v 1
python backend/manage.py update_birth_dates_from_congresoes -v 1

echo "Get spain senators from senado.es"
python backend/manage.py update_spain_senators -v 1

echo "Fix duplicated persons"
python backend/manage.py fix_duplicated_persons -v 1

echo "Fix genres"
python backend/manage.py update_genres -v 1

echo "Get birth dates"
python backend/manage.py update_birth_dates_from_congresoes_historical -v 1
python backend/manage.py update_birth_dates_from_file -v 1
python backend/manage.py update_birth_dates_from_wikidata -v 1
python backend/manage.py update_birth_dates_from_wikipedia -v 1

echo "Enrich data"
python manage.py enrich_data_from_paresmcues -v 1
# python manage.py enrich_data_from_fpabloiglesias
