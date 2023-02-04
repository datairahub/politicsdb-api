# PoliticsDB API

## Update commands

### Update spain parties

Update Spain parties from file `data_input/parties/adm0_parties.csv`

```sh
python backend/manage.py update_parties
```

Update Spain legislators from `www.congreso.es`

```sh
python backend/manage.py update_spain_legislators
```

Update Spain senators from `www.senado.es`

```sh
python backend/manage.py update_spain_senators
```
