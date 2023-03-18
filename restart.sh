#!/bin/bash
echo "Restarting..."

echo "Remove sqlite"
rm -f backend/db.sqlite3

echo "Execute migrations"
python backend/manage.py migrate -v 0

echo "Update Spain parties from file"
python backend/manage.py update_parties -v 2

echo "Update Spain legislators from www.congreso.es"
python backend/manage.py update_spain_legislators -v 2
python backend/manage.py enrich_data_from_congresoes -v 2

echo "Get spain senators from senado.es"
python backend/manage.py update_spain_senators -v 2

echo "Fix duplicated persons"
python backend/manage.py fix_duplicated_persons -v 2

echo "Fix genres"
python backend/manage.py update_genres -v 2

echo "Get birth dates"
python backend/manage.py update_birth_dates_from_congresoes_historical -v 2
python backend/manage.py update_birth_dates_from_file -v 2
python backend/manage.py update_birth_dates_from_wikidata -v 2
python backend/manage.py update_birth_dates_from_wikipedia -v 2

echo "Enrich data"
python backend/manage.py enrich_data_from_paresmcues -v 2
python backend/manage.py enrich_data_from_fpabloiglesias -v 2
