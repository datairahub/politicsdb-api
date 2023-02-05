# PoliticsDB API

## Update commands

### Update spain parties

Update Spain parties from file `data_input/parties/adm0_parties.csv`

```sh
python backend/manage.py update_parties
```

### Update spain legislators (congreso y senado)

Update Spain legislators from `www.congreso.es`

```sh
python backend/manage.py update_spain_legislators
```

Update Spain senators from `www.senado.es`

```sh
python backend/manage.py update_spain_senators
```

### Update genres

Update people's genre based on their names

```sh
python backend/manage.py update_genres
```

### Fix duplicated people

Remove duplicate persons (they are collected in different sources with different full names)

```sh
python backend/manage.py fix_duplicated_persons
```
