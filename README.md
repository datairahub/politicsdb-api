# PoliticsDB API

## Update commands

### Update spain deputies (congress)

Get or update spanish congress members from the index of the congress page. The following data are obtained:

```
Person:
- first_name, last_name, full_name and id_name
- genre
- metadata    # Updated always

Position:
- person
- institution
- start       # Updated always
- end         # Updated always
- metadata    # Updated always
```

```sh
python backend/manage.py update_spain_legislators [--period <int>] [-v <int>]
# Example: update_spain_legislators --period 14 -v 2
```

### Update spain senators (senate)

Get or update spanish senators from the index of the senate page. The following data are obtained:

```
Person:
- first_name, last_name, full_name and id_name
- metadata    # Updated always

Position:
- person
- institution
- metadata    # Updated always
```

```sh
python backend/manage.py update_spain_senators [--period <int>] [-v <int>]
# Example: update_spain_senators --period 14 -v 2
```

## Fix commands

### Fix duplicated people

Remove duplicated people (they have different full names but are the same person) and move their data to the original one.

```sh
python backend/manage.py fix_duplicated_people [-v <int>]
# Example: fix_duplicated_people -v 2
```

### Fix genres

Update people's genre based on their counttry and first name

```sh
python backend/manage.py fix_genres [-v <int>]
# Example: fix_genres -v 2
```

## Enrich commands

### Enrich data using local files

Enrich people data using local files. The following data are obtained:

```
Person:
- birth_date # Updated always
```

```sh
python backend/manage.py enrich_from_local_files [-v <int>]
# Example: enrich_from_local_files -v 2
```

### Enrich deputies data using profile detail page

Enrich spanish deputies data using the detail page of each deputy. The following data are obtained:

```
Person:
- birth_date  # Updated
- biography   # Updated
- image       # Updated with --override
```

```sh
python backend/manage.py enrich_from_congresoes [--period <int>] [--override] [-v <int>]
# Example: enrich_from_congresoes --period 14 --override -v 2
```

### Enrich deputies data using congreso history

Enrich deputies data from congreso.es historical archive. The following data are obtained:

```
Person:
- birth_date
```

```sh
python backend/manage.py enrich_from_congresoes_historical [-v <int>]
# Example: enrich_from_congresoes_historical -v 2
```

### Enrich senators data using profile detail page

Enrich spanish senators data using the detail page of each senator. The following data are obtained:

```
Person:
- image      # Updated always
- biography  # Updated always

Position:
- start      # Updated always
- end        # Updated always
```

```sh
python backend/manage.py enrich_from_senadoes [--period <int>] [-v <int>]
# Example: enrich_from_senadoes --period 14 -v 2
```

### Enrich senators data using profile open data xml files

Enrich spanish senators data using each senator open data xml file (only a few have it). The following data are obtained:

```
Person
- metadata     # Updated with --override
- birth_date   # Updated with --override
- death_date   # Updated with --override
- biography    # Updated with --override
```

```sh
python backend/manage.py enrich_from_senadoes_opendata [--period <int>] [--override] [-v <int>]
# Example: enrich_from_senadoes_opendata --period 14 -v 2
```

### Enrich using wikidata

Enrich people's data using wikidata project "WikiProject every politician". The following data are obtained:

```
Person:
- birth_date  # Updated always
- metadata    # Updated always
```

```sh
python backend/manage.py enrich_from_wikidata [-v <int>]
# Example: enrich_from_wikidata -v 2
```

### Enrich using wikipedia

Enrich people's data using its own wikipedia page. **Only searchs for people without birth date**. The following data are obtained:

```
Person:
- birth_date  # Updated always
- metadata    # Updated always
```

```sh
python backend/manage.py enrich_from_wikipedia [-v <int>]
# Example: enrich_from_wikipedia -v 2
```

### Enrich using pares.mcu.es

Enrich people's data using using pares.mcu.es

```
Person:
- biography   # Updated always
- birth_date  # Updated always
- metadata    # Updated always
```

```sh
python backend/manage.py enrich_from_paresmcues [-v <int>]
# Example: enrich_from_paresmcues -v 2
```

### Enrich using fpabloiglesias.es

Enrich people's data using using fpabloiglesias.es

```
Person:
- biography   # Updated always
- birth_date  # Updated always
- metadata    # Updated always
```

```sh
python backend/manage.py enrich_from_fpabloiglesias [-v <int>]
# Example: enrich_from_fpabloiglesias -v 2
```
