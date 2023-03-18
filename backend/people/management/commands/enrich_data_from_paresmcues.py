# -*- coding: utf-8 -*-
import sys
import time
import logging
from bs4 import BeautifulSoup
from unidecode import unidecode
from django.conf import settings
from django.core.management.base import BaseCommand
from core.services.requests import request_page

sys.path.append(str(settings.BASE_DIR.parent))
from parsers.paresmcu import ParesmcuParser
from people.services.biographies import register_biography_source
from people.services.birth_dates import register_birth_date_source
from people.models import Person

logger = logging.getLogger("commands")

CORRECT_PERSONS_MISMATCH = [
    # People who are marked as incorrect when comparing
    # person.last_name with a profile pares.mcu.es page title
    # but they are a correct match
    "adolfo_suarez_gonzalez",
    "josep_maria_obiols_germa",
    "telesforo_monzon_ortiz_urruela",
    "jose_maria_romero_calero",
    "felip_lorda_alaiz",
    "josefina_lopez_sanmartin",
    "jose_diosdado_prat_garcia",
    "alexandre_cirici_pellicer",
    "joan_casanelles_ibarz",
    "julio_jauregui_lasanta",
    "fernando_chueca_goitia",
    "gregorio_peces_barba_del_brio",
    "victor_serna_gutierrez_repide",
    "manuel_chaves_gonzalez",
    "enrique_martinez_martinez",
    "jaime_gaspar_auria",
    "jose_maria_areilza_martinez_rodas",
    "francisco_paula_burguera_escriva",
    "ana_palacio_vallelersundi",
    "gregorio_lopez_bravo_castro",
    "inigo_aguirre_kerexeta",
    "pilar_brabo_castells",
    "maria_belen_landaburu_gonzalez",
    "ricardo_cierva_hoces",
    "xabier_arzalluz_antia",
    "francisco_gari_mir",
    "joaquin_fuster_perez",
    "salvador_sanchez_teran_hernandez",
    "camilo_jose_cela_trulock",
    "sebastian_martin_retortillo_baquer",
    "maria_rubies_garrofe",
    "francisca_sauquillo_perez_del_arco",
    "jose_manuel_garcia_margallo_marfil",
    "juli_busquets_bragulat",
    "ramon_trias_fargas",
    "jose_miguel_alava_aguirre",
    "jose_pedro_perez_llorca_rodrigo",
    "inigo_cavero_lataillade",
    "luis_del_val_velilla",
    "micaela_navarro_garzon",
    "raul_morodo_leoncio",
    "ernest_lluch_martin",
    "ignacio_gallego_bezares",
    "ana_maria_ruiz_tagle_morales",
    "antoni_gutierrez_diaz",
    "fermin_solana_prellezo",
    "emilio_alonso_sarmiento",
    "leopoldo_calvo_sotelo_bustelo",
    "jordi_pujol_soley",
    "soledad_becerril_bustamante",
    "luis_apostua_palos",
    "josep_borrell_fontelles",
    "manuel_lucio_diaz_marta_pinilla",
    "alfonso_lazo_diaz",
    "perfecto_yebra_martul_ortega",
    "luis_solana_madariaga",
    "macia_alavedra_moner",
    "gabriel_urralburu_tainta",
    "juan_manuel_eguiagaray_ucelay",
    "heribert_barrera_costa",
    "gonzalo_fernandez_mora_mon",
    "enrique_baron_crespo",
    "carlota_bustelo_garcia_del_real",
    "loyola_palacio_del_valle_lersundi",
    "fernando_alvarez_miranda_torres",
    "modesto_fraile_poujade",
    "eugenio_triana_garcia",
    "gregorio_peces_barba_martinez",
    "angel_salas_larrazabal",
    "nicolas_redondo_urbieta",
    "emilio_attard_alonso",
    "virgilio_zapatero_gomez",
    "rodolf_guerra_fontana",
    "licinio_fuente_fuente",
    "joaquin_leguina_herran",
    "carmen_romero_lopez",
    "marta_mata_garriga",
    "gerardo_iglesias_arguelles",
    "fernando_benzo_mestre",
    "marcelino_camacho_abad",
    "pio_cabanillas_gallas",
    "oscar_alzaga_villaamil",
    "justo_las_cuevas_gonzalez",
    "matilde_fernandez_sanz",
    "alberto_carlos_oliart_saussol",
    "manuel_fernandez_montesinos_garcia",
    "jose_maria_benegas_haddad",
    "joaquin_fuster_perez",
    "wenceslao_roces_suarez",
    "maria_cristina_almeida_castro",
    "rafael_escuredo_rodriguez",
]


class Command(BaseCommand):
    """
    Enriquecer con datos de la página pares.mcu.es
    Datos a obtener:
        - Descripción
        - Fecha de nacimiento
        - Lugar de nacimiento
        - Fecha de defunción
        - Lugar de defunción
        - Género
    """

    help = "Update birth dates using pares.mcu.es"
    domain = "http://pares.mcu.es"
    sleep_time = 0

    def handle(self, *args, **options):
        self.update_birth_dates_from_paresmcues(*args, **options)
        if options["verbosity"] >= 2:
            logger.info("Done")

    def update_birth_dates_from_paresmcues(self, *args, **options):
        for person in Person.objects.filter(
            positions__period__institution__adm0__code="es"
        ).distinct():

            if not person.last_name:
                # last_name is used to verify that the match is correct
                continue

            if person.metadata.get("pares.mcu.es") and person.metadata[
                "pares.mcu.es"
            ].get("link"):
                # If person is already enriched, continue
                continue

            time.sleep(self.sleep_time)

            # Get search page
            name = unidecode(person.full_name).strip().replace(" ", "+")
            url = self.domain + (
                "/ParesBusquedas20/catalogo/autfind?nm=&texto=" f"{name}"
            )
            response = request_page(url).decode("utf-8")
            soup = BeautifulSoup(response, "html.parser")
            rows = soup.select("div#resultados table#resultados tbody tr")

            if not (rows and len(rows) == 1):
                # 0 or more than 1 result -> imprecise result
                continue

            if len(rows[0].select(".titulo a")) == 0:
                # No title with link -> imprecise result
                continue

            # Get profile page
            profile_url = self.domain + rows[0].select(".titulo a")[0]["href"]
            try:
                response = request_page(profile_url).decode("utf-8")
            except Exception:
                continue
            parser = ParesmcuParser(response)

            if not parser.is_persona_page:
                continue

            if (not person.last_name.lower() in parser.title.lower()) and (
                not person.id_name in CORRECT_PERSONS_MISMATCH
            ):
                # Person page title doesn't contain the person last name -> imprecise match
                continue

            # store common data in person metadata
            if not person.metadata.get("pares.mcu.es", None):
                person.metadata["pares.mcu.es"] = {}
            person.metadata["pares.mcu.es"]["link"] = profile_url
            person.metadata["pares.mcu.es"]["title"] = parser.title
            person.metadata["pares.mcu.es"]["birth_date"] = parser.birth_date_str
            person.metadata["pares.mcu.es"]["death_date"] = parser.death_date_str
            person.metadata["pares.mcu.es"]["birth_place"] = parser.birth_place
            person.metadata["pares.mcu.es"]["death_place"] = parser.death_place

            if parser.description:
                register_biography_source(
                    person=person,
                    url=profile_url,
                    value=parser.description,
                )

            if parser.birth_date:
                register_birth_date_source(
                    person=person,
                    url=profile_url,
                    value=parser.birth_date,
                )

            person.save(update_fields=["metadata"])

            if options["verbosity"] >= 2:
                logger.info(f"{person} saved")
