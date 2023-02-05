# PoliticsDB API

## Commands

All commands admits verbosity level with `-v` or `--verbosity` flags:

```
0 - ERROR -> Only ERROR level
1 - WARN  -> WARN and ERROR levels
2 - INFO  -> INFO, WARN and ERROR levels
3 - DEBUG -> DEBUG, INFO, WARN and ERROR levels
```

### Update spain parties

Update Spain parties from file `data_input/parties/adm0_parties.csv`

```sh
python backend/manage.py update_parties
```

### Update spain legislators (congreso y senado)

Update Spain legislators from `www.congreso.es`

```sh
python backend/manage.py update_spain_legislators
python backend/manage.py update_birth_dates_from_congresoes
```

Update Spain senators from `www.senado.es`

```sh
python backend/manage.py update_spain_senators
```

### Update birth dates from indirect resources

Update people's birth date using www.congreso.es historial archive

```sh
python backend/manage.py update_birth_dates_from_congresoes_historical
```

Update people's birth date using local file

```sh
python backend/manage.py update_birth_dates_from_file
```

Update people's birth date using wikidata (project "WikiProject every politician")

```sh
python backend/manage.py update_birth_dates_from_wikidata
```

Update people's birth date using wikipedia (search for each people)

```sh
python backend/manage.py update_birth_dates_from_wikipedia
```

## Fix commands

### Fix duplicated people

Remove duplicate people (they are collected in different sources with different full names)

```sh
python backend/manage.py fix_duplicated_persons
```

### Fix genres

Update people's genre based on their names

```sh
python backend/manage.py update_genres
```
