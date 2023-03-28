# -*- coding: utf-8 -*-
import logging
from django.core.management.base import BaseCommand
from organizations.models import Party
from positions.models import Position

logger = logging.getLogger("commands")


class Command(BaseCommand):
    """ """

    help = "Update Parties"
    parties_cache = {}
    parties_group = {
        "0": {  # https://es.wikipedia.org/wiki/Elecciones_generales_de_Espa%C3%B1a_de_1977
            "PSOE": "es-46",
            "PSC-PSOE": "es-351",
            "PSE-PSOE": "es-90",
            "UCD": "es-282",
            "AP": "es-100042,es-100001,es-100039,es-100040,es-100010,es-100035",
            "PCE": "es-49",
            "PCE-PCPV": "es-787",
            "PNV": "es-170",
            "PDC": "es-71,es-100032,es-100016,es-2268",
            "EE": "es-100018,es-100017",
            "CIC": "es-100006",
            "PSUC": "es-60",
            "CAIC": "es-100005",
            "UCIDCC": "es-100038",
            "EC": "es-100031,es-166,es-234",
            "US-PSP": "es-100030,es-100028,es-2322,es-100027,es-100029,es-100033,es-100021,es-100034",  # Unidad Socialista-Partido Socialista Popular
            "US": "es-100030,es-100028,es-2322,es-100027,es-100029,es-100033,es-100021,es-100034",  # Unidad Socialista
        },
        "1": {  # https://es.wikipedia.org/wiki/Elecciones_generales_de_Espa%C3%B1a_de_1979
            "PSOE": "es-46",
            "PSC-PSOE": "es-351",
            "PSE-PSOE": "es-90",
            "UCD": "es-282",
            "CC-UCD": "es-282",
            "CD": "es-171,es-317,es-100024,es-100036,es-45,es-100025,es-100002,es-100004,es-100011,es-100008",
            "PCE": "es-49",
            "PCPV": "es-49",
            "PNV": "es-170",
            "CIU": "es-71,es-100041",
            "HB": "es-100020",
            "EE": "es-555",
            "ERC": "es-166",
            "PSA": "es-2322",
            "PAR": "es-315",
            "UPN": "es-372",
            "UPC": "es-603",
            "PSUC": "es-60",
            "UN": "es-1380,es-7,es-100009,es-2319,es-304",
        },
        "2": {  # https://es.wikipedia.org/wiki/Elecciones_generales_de_Espa%C3%B1a_de_1982
            "PSOE": "es-46",
            "UCD": "es-282",
            "CDS": "es-560",
            "CD": "es-171,es-317,es-100024,es-100036,es-45,es-100025,es-100002,es-100004,es-100011,es-100008",
            "PCE": "es-49",
            "PNV": "es-170",
            "CIU": "es-71,es-100041",
            "HB": "es-100020",
            "EE": "es-555",
            "ERC": "es-166",
            "PSUC": "es-60",
        },
        "3": {  # https://es.wikipedia.org/wiki/Elecciones_generales_de_Espa%C3%B1a_de_1986
            "PSOE": "es-46",
            "PSC-PSOE": "es-351",
            "PSC": "es-351",
            "CP": "es-171,es-100023,es-100026,es-552,es-372,es-315,es-100007",
            "IU": "es-49,es-60,es-617,es-625,es-558,es-294,es-709,es-686,es-50",
            "UEC": "es-60,es-437",
            "CDS": "es-560",
            "PNV": "es-170",
            "CIU": "es-71,es-100041",
            "HB": "es-100020",
            "CG": "es-676",
            "EE": "es-555",
            "UV": "es-552",
            "AIC": "es-778",
            "PAR": "es-315",
        },
        "4": {  # https://es.wikipedia.org/wiki/Elecciones_generales_de_Espa%C3%B1a_de_1989
            "PSOE": "es-46",
            "PSOE-A": "es-46",
            "PSC-PSOE": "es-351",
            "PSG-PSOE": "es-46",
            "PSE-PSOE": "es-90",
            "PP": "es-244",
            "UPN-PP": "es-244,es-372",  # http://www.juntaelectoralcentral.es/cs/jec/documentos/JEPNavarra_UPN-PP.pdf
            "PP-CG": "es-244,es-676",
            "CDS": "es-560",
            "IU": "es-1309",
            "IU-A": "es-1309",
            "IU-CA": "es-1309",
            "IU-EU": "es-1309",
            "IU-EUPV": "es-1309,es-1266",
            "PNV": "es-170",
            "EAJ-PNV": "es-170",
            "CIU": "es-71,es-100041",
            "HB": "es-100020",
            "IC": "es-876",
            "EE": "es-555",
            "EA": "es-807",
            "PA": "es-2322",
            "UV": "es-552",
            "PAR": "es-315",
            "AIC": "es-778",
        },
        "5": {  # https://es.wikipedia.org/wiki/Elecciones_generales_de_Espa%C3%B1a_de_1993
            "PSOE": "es-46",
            "PSOE-A": "es-46",
            "PSC-PSOE": "es-351",
            "PSG-PSOE": "es-46",
            "PSE-EE": "es-1356",
            "PP": "es-244",
            "UPN-PP": "es-244,es-372",  # http://www.juntaelectoralcentral.es/cs/jec/documentos/JEPNavarra_UPN-PP.pdf
            "IU": "es-1309",
            "IU-A": "es-1309",
            "IU-CA": "es-1309",
            "IU-EU": "es-1309",
            "IU-EUPV": "es-1309,es-1266",
            "CIU": "es-71,es-100041",
            "ERC": "es-166",
            "EAJ-PNV": "es-170",
            "EA-EE": "es-807,es-555",
            "IC": "es-876",
            "CC": "es-1807",
            "UV": "es-552",
            "HB": "es-100020",
            "PAR": "es-315",
        },
        "6": {  # https://es.wikipedia.org/wiki/Elecciones_generales_de_Espa%C3%B1a_de_1996
            "PSOE": "es-46",
            "PSOE-A": "es-46",
            "PSC-PSOE": "es-351",
            "PSG-PSOE": "es-46",
            "PSE-EE": "es-1356",
            "PP": "es-244",
            "UPN-PP": "es-244,es-372",  # http://www.juntaelectoralcentral.es/cs/jec/documentos/JEPNavarra_UPN-PP.pdf
            "PP-PAR": "es-244,es-315",
            "IU": "es-1309",
            "IU-LV": "es-1309",
            "IU-LV-CA": "es-1747",
            "IU-EUPV": "es-1309,es-1266",
            "IU-EB": "es-1309",
            "EUPV": "es-1266",
            "EAJ-PNV": "es-170",
            "EA": "es-807",
            "CIU": "es-71,es-100041",
            "ERC": "es-166",
            "BNG": "es-1765",
            "CC": "es-1807",
            "UV": "es-552",
            "IC-EV": "es-876",
        },
        "7": {  # https://es.wikipedia.org/wiki/Elecciones_generales_de_Espa%C3%B1a_de_2000
            "PSOE": "es-46",
            "PSOE-PROGRESISTAS": "es-46",
            "PSC(PSC-PSOE)": "es-351",
            "PSDEG-PSOE-PROGRESISTAS": "es-46",
            "PSE-EE (PSOE-PROGRESISTAS)": "es-1356",
            "PP": "es-244",
            "PP-UPN": "es-244,es-372",  # http://www.juntaelectoralcentral.es/cs/jec/documentos/JEPNavarra_UPN-PP.pdf
            "UPN-PP": "es-244,es-372",  # http://www.juntaelectoralcentral.es/cs/jec/documentos/JEPNavarra_UPN-PP.pdf
            "PP-UPM": "es-244,es-721",
            "IU": "es-1309",
            "IU-CM": "es-1756",
            "EUPV": "es-1266",
            "IU-LV-CA": "es-1747",
            "CIU": "es-71,es-100041",
            "ERC": "es-166",
            "IC-V": "es-876",
            "EAJ-PNV": "es-170",
            "EA": "es-807",
            "CC": "es-1807",
            "CHA": "es-810",
            "BNG": "es-1765",
            "PA": "es-2322",
        },
        "8": {  # https://es.wikipedia.org/wiki/Elecciones_generales_de_Espa%C3%B1a_de_2004
            "PSOE": "es-46",
            "PSC(PSC-PSOE)": "es-351",
            "PSOEDEANDALUCÍA": "es-46",
            "PSDEG-PSOE": "es-46",
            "PSE-EE(PSOE)": "es-1356",
            "PP": "es-244",
            "PPDEC": "es-244",
            "UPN-PP": "es-244,es-372",  # http://www.juntaelectoralcentral.es/cs/jec/documentos/JEPNavarra_UPN-PP.pdf
            "IU": "es-1309",
            "ICV-EUIA": "es-876,es-1875",
            "CIU": "es-71,es-100041",
            "ERC": "es-166",
            "EAJ-PNV": "es-170",
            "NA-BAI": "es-100003,es-807,es-1118,es-170",
            "EA": "es-807",
            "BNG": "es-1765",
            "CC": "es-1807",
            "NC": "es-1807",  # WTF
            "CHA": "es-810",
        },
        "9": {  # https://es.wikipedia.org/wiki/Elecciones_generales_de_Espa%C3%B1a_de_2008
            "PSOE": "es-46",
            "PSC(PSC-PSOE)": "es-351",
            "PSE-EE(PSOE)": "es-1356",
            "PSDEG-PSOE": "es-46",
            "PSOEDEANDALUCÍA": "es-46",
            "PP": "es-244",
            "IU-ALTERNATIVA": "es-1309",
            "CIU": "es-71,es-100041",
            "ERC": "es-166",
            "EAJ-PNV": "es-170",
            "UPN": "es-372",
            "NA-BAI": "es-100003,es-807,es-1118,es-170",
            "UPYD": "es-3779",
            "BNG": "es-1765",
            "ICV-EUIA": "es-876,es-1875",
            "CC": "es-1807",
            "CC-PNC": "es-1807,es-181",
        },
        "10": {  # https://es.wikipedia.org/wiki/Elecciones_generales_de_Espa%C3%B1a_de_2011
            "PSOE": "es-46",
            "PSC-PSOE": "es-351",
            "PP": "es-244",
            "PP-PAR": "es-244,es-315",
            "PP-EU": "es-244,es-489",
            "UPN-PP": "es-244,es-372",  # http://www.juntaelectoralcentral.es/cs/jec/documentos/JEPNavarra_UPN-PP.pdf
            "IZQ-PLU": "es-1309",
            "IU-IX": "es-3810",
            "EAJ-PNV": "es-170",
            "CIU": "es-71,es-100041",
            "ERC-RI.CAT": "es-166,es-4708",  # http://www.juntaelectoralcentral.es/cs/jec/documentos/C1.%20ERC-CATSI.pdf
            "BNG": "es-1765",
            "UPYD": "es-3779",
            "CC-NC-PNC": "es-1807,es-181,es-3021",
            "GB": "es-170,es-4487",
            "AMAIUR": "es-807,es-3881,es-100003",
            "FORO": "es-4321",
            "COMPROMÍS-Q": "es-1869,es-3771,es-2465,es-4338",
        },
        "11": {  # https://es.wikipedia.org/wiki/Elecciones_generales_de_Espa%C3%B1a_de_2015
            "PSOE": "es-46",
            "PSC-PSOE": "es-351",
            "PSOE-NCA": "es-46,es-3021",
            "PP": "es-244",
            "PP-PAR": "es-244,es-315",
            "PP-FORO": "es-244,es-4321",
            "UPN-PP": "es-244,es-372",  # http://www.juntaelectoralcentral.es/cs/jec/documentos/JEPNavarra_UPN-PP.pdf
            "PODEMOS": "es-4940",
            "PODEMOS-EN MAREA-ANOVA-EU": "es-4940,es-1821,es-4793",  # http://www.juntaelectoralcentral.es/cs/jec/doctrina/acuerdos?idacuerdoinstruccion=35480&idsesion=861&template=Doctrina/JEC_Detalle
            "PODEMOS-COMPROMÍS": "es-1869,es-3771,es-2997,es-4054,es-4940",  # http://www.juntaelectoralcentral.es/cs/jec/doctrina/acuerdos?idacuerdoinstruccion=35480&idsesion=861&template=Doctrina/JEC_Detalle
            "POD-AAA EN COMÚN": "es-4940,es-5967",
            "EN COMÚ": "es-5201,es-1875,es-876,es-4940",  # http://www.juntaelectoralcentral.es/cs/jec/doctrina/acuerdos?idacuerdoinstruccion=35480&idsesion=861&template=Doctrina/JEC_Detalle
            "IU-UPEC": "es-1309,es-5743,es-810,es-1285,es-1118,es-100012,es-1000053,es-100037,es-2273",  # http://www.juntaelectoralcentral.es/cs/jec/doctrina/acuerdos?idacuerdoinstruccion=35480&idsesion=861&template=Doctrina/JEC_Detalle
            "CS": "es-3184",
            "EAJ-PNV": "es-170",
            "EH BILDU": "es-4933",
            "ERC-CATSÍ": "es-166,es-4708",  # http://www.juntaelectoralcentral.es/cs/jec/documentos/C1.%20ERC-CATSI.pdf
            "DL": "es-71,es-5737,es-1000051",  # http://www.juntaelectoralcentral.es/cs/jec/doctrina/acuerdos?idacuerdoinstruccion=35480&idsesion=861&template=Doctrina/JEC_Detalle
            "CCA-PNC": "es-1807,es-181",
        },
        "12": {  # https://es.wikipedia.org/wiki/Elecciones_generales_de_Espa%C3%B1a_de_2016
            "PSOE": "es-46",
            "PSC-PSOE": "es-351",
            "PSDG-PSOE": "es-46",
            "PSE-EE-PSOE": "es-1356",
            "PSOE-NCA": "es-46,es-3021",  # http://www.juntaelectoralcentral.es/cs/jec/documentos/C3.%20PSOE-NCa.pdf
            "PP": "es-244",
            "PP-FORO": "es-244,es-4321",
            "PP-PAR": "es-244,es-315",  # http://www.juntaelectoralcentral.es/cs/jec/documentos/C4.%20PP-PAR.pdf
            "UPN-PP": "es-244,es-372",  # http://www.juntaelectoralcentral.es/cs/jec/documentos/JEPNavarra_UPN-PP.pdf
            "CS": "es-3184",
            "UP": "es-4940,es-1309,es-4338,es-1000043,es-1118,es-5743,es-1285,es-100012,es-100037,es-2273,es-4528",  # https://app.juntaelectoralcentral.es/svtjec/descargarFichero?tipo=tipoCoalicion&codigoCoalicion=1611
            "ECP": "es-5201,es-5759,es-1875,es-876,es-4940",  # http://www.juntaelectoralcentral.es/cs/jec/documentos/C9.%20ECP.pdf
            "EM-P-A-EU": "es-4940,es-1309,es-4793",  # http://www.juntaelectoralcentral.es/cs/jec/documentos/C8.%20PODEMOS%20-%20EN%20MAREA%20-%20ANOVA%20-%20EU.pdf
            "EAJ-PNV": "es-170",
            "EH BILDU": "es-4933",
            "CDC": "es-71",
            "ERC-CATSÍ": "es-166,es-4708",  # http://www.juntaelectoralcentral.es/cs/jec/documentos/C1.%20ERC-CATSI.pdf
            "CCA-PNC": "es-1807,es-181",
            "C-P-EUPV": "es-1869,es-3771,es-2997,es-4054,es-1266,es-4940",  # http://www.juntaelectoralcentral.es/cs/jec/documentos/C7.%20PODEMOS-Comprom%C3%ADs-EUPV.pdf
            "UPM": "es-4940,es-1775,es-4846",  # http://www.juntaelectoralcentral.es/cs/jec/documentos/JEPBalears_PODEMOS-EU-MAS.pdf
        },
        "13": {  # https://es.wikipedia.org/wiki/Elecciones_generales_de_Espa%C3%B1a_de_abril_de_2019
            "PSOE": "es-46",
            "PSC-PSOE": "es-351",
            "PSDEG-PSOE": "es-46",
            "PSE-EE-PSOE": "es-1356",
            "PP": "es-244",
            "PP-FORO": "es-244,es-4321",
            "UP": "es-4940,es-1309,es-4338,es-1118,es-5967",  # https://app.juntaelectoralcentral.es/svtjec/descargarFichero?tipo=tipoCoalicion&codigoCoalicion=2760
            "ECP": "es-5201,es-5759,es-876,es-1875,es-5756,es-4940",  # https://app.juntaelectoralcentral.es/svtjec/descargarFichero?tipo=tipoCoalicion&codigoCoalicion=2769
            "EC-UP": "es-4940,es-1821",
            "EAJ-PNV": "es-170",
            "EH BILDU": "es-4933",
            "JXCAT-JUNTS": "es-5819,es-71,es-6102",  # https://app.juntaelectoralcentral.es/svtjec/descargarFichero?tipo=tipoCoalicion&codigoCoalicion=2762
            "ERC-S": "es-166,es-6151",  # https://app.juntaelectoralcentral.es/svtjec/descargarFichero?tipo=tipoCoalicion&codigoCoalicion=2729
            "CS": "es-3184",
            "VOX": "es-4881",
            "CCA-PNC": "es-1807,es-181",
            "NA+": "es-3184,es-372",  # http://www.juntaelectoralcentral.es/cs/jec/documentos/Pacto%20de%20coalicion%20-%20Navarra%20-%20Navarra%20Suma.pdf
            "PRC": "es-362",
            "C:B-I-V": "es-1869,es-3771,es-2997,es-4054",
        },
        "14": {  # https://es.wikipedia.org/wiki/Elecciones_generales_de_Espa%C3%B1a_de_noviembre_de_2019
            "PSOE": "es-46",
            "PSC-PSOE": "es-351",
            "PSE-EE-PSOE": "es-1356",
            "PSDEG-PSOE": "es-46",
            "PP": "es-244",
            "PP-FORO": "es-244,es-4321",  # http://www.juntaelectoralcentral.es/cs/jec/documentos/JEPAsturias-COALICION%20PP-FORO.pdf
            "UP": "es-4940,es-1309,es-1118,es-5967",  # https://app.juntaelectoralcentral.es/svtjec/descargarFichero?tipo=tipoCoalicion&codigoCoalicion=32389
            "ECP-GUAYEM EL CANVI": "es-5759,es-5756,es-4940",  # https://app.juntaelectoralcentral.es/svtjec/descargarFichero?tipo=tipoCoalicion&codigoCoalicion=32440
            "EC-UP": "es-4940,es-1821",  # https://app.juntaelectoralcentral.es/svtjec/descargarFichero?tipo=tipoCoalicion&codigoCoalicion=32444
            "MÁS PAÍS-EQUO": "es-4338,es-6712",  # https://app.juntaelectoralcentral.es/svtjec/descargarFichero?tipo=tipoCoalicion&codigoCoalicion=32446
            "EAJ-PNV": "es-170",
            "EH BILDU": "es-4933",
            "JXCAT-JUNTS": "es-5819,es-6102",  # https://app.juntaelectoralcentral.es/svtjec/descargarFichero?tipo=tipoCoalicion&codigoCoalicion=32427
            "JXCAT-JUNTS (JUNTS)": "es-5819,es-6102",  # https://app.juntaelectoralcentral.es/svtjec/descargarFichero?tipo=tipoCoalicion&codigoCoalicion=32427
            "JXCAT-JUNTS (PDECAT)": "es-5819,es-6102",  # https://app.juntaelectoralcentral.es/svtjec/descargarFichero?tipo=tipoCoalicion&codigoCoalicion=32427
            "ERC-S": "es-166,es-6151",  # https://app.juntaelectoralcentral.es/svtjec/descargarFichero?tipo=tipoCoalicion&codigoCoalicion=32424
            "CUP-PR": "es-1107,es-5335",  # https://app.juntaelectoralcentral.es/svtjec/descargarFichero?tipo=tipoCoalicion&codigoCoalicion=32436
            "CCA-PNC-NC": "es-1807,es-3021",  # WTF https://app.juntaelectoralcentral.es/svtjec/descargarFichero?tipo=tipoCoalicion&codigoCoalicion=32442
            "NC-CCA-PNC": "es-1807,es-3021",  # WTF https://app.juntaelectoralcentral.es/svtjec/descargarFichero?tipo=tipoCoalicion&codigoCoalicion=32442
            "NA+": "es-3184,es-372",  # http://www.juntaelectoralcentral.es/cs/jec/documentos/JEPNavarra-COALICION%20NAVARRA%20SUMA.pdf
            "¡TERUEL EXISTE!": "es-6779",
            "MÉS COMPROMÍS": "es-1869,es-3771,es-2997,es-4054,es-6712",  # https://app.juntaelectoralcentral.es/svtjec/descargarFichero?tipo=tipoCoalicion&codigoCoalicion=32447
            "CS": "es-3184",
            "VOX": "es-4881",
            "PRC": "es-362",
            "BNG": "es-1765",
        },
    }

    def get_positions(self, institution_name):
        return Position.objects.filter(
            period__institution__name=institution_name,
            period__number__gte=0,
        )

    def get_party(self, short_name):
        short_name = short_name.strip().upper()
        short_name = self.parties_group.get(short_name, short_name)
        result = self.parties_cache.get(short_name)
        if result:
            return result
        result = Party.objects.filter(short_name__iexact=short_name).first()
        if result:
            self.parties_cache[short_name] = result
            return result
        return None

    def handle_special_cases(self, position):
        leg = position.metadata["www.congreso.es"]["idLegislatura"]
        code = position.metadata["www.congreso.es"]["codParlamentario"]

        if leg == 8 and code == 331:
            return "PARTIDO POPULAR"

        return None

    def handle(self, *args, **options):
        for position in self.get_positions("Parlamento de España"):
            name = position.metadata["www.congreso.es"]["formacion"].strip().upper()

            if self.handle_special_cases(position):
                continue

            if not self.parties_group[str(position.period.number)].get(name):
                print(name, "                 ->", position)

        # parties = set()

        # for leg in self.parties_group:
        #     for coa in self.parties_group[leg]:
        #         for party in self.parties_group[leg][coa].split(","):
        #             parties.add(party)

        # for party in sorted(parties):
        #     print(party)
