# -*- coding: utf-8 -*-
import logging
from django.core.management.base import BaseCommand
from positions.models import Position
from people.models import (
    Person,
    BirthDateSource,
)

logger = logging.getLogger("commands")

# fmt: off
DATA = [
    # to_remove, to_preserve, to_preserve new name
    ['elena_espinosa_mangana', 'maria_elena_espinosa_mangana'],
    ['jaime_lamo_espinosa_michel_champourcin', 'jaime_lamo_espinosa_michels_champourcin'],
    ['rosa_romero_sanchez', 'rosa_maria_romero_sanchez'],
    ['cristobal_montoro_romero', 'cristobal_ricardo_montoro_romero'],
    ['felipe_guardiola_selles', 'felipe_guillermo_guardiola_selles'],
    ['ofelia_reyes_miranda', 'ofelia_maria_del_cristo_reyes_miranda'],
    ['fernando_fernandez_troconiz', 'fernando_fernandez_troconiz_marcos'],
    ['marta_mata_garriga', 'marta_angela_mata_garriga'],
    ['julian_campo_sainz_rozas', 'julian_campo_sainz_las_rozas'],
    ['irene_montero_gil', 'irene_maria_montero_gil'],
    ['marisol_sanchez_jodar', 'maria_soledad_sanchez_jodar'],
    ['ildefonso_pastor_gonzalez', 'ildefonso_rafael_pastor_gonzalez'],
    ['pilar_alegria_continente', 'maria_pilar_alegria_continente'],
    ['pilar_llop_cuenca', 'maria_pilar_llop_cuenca'],
    ['javier_maroto_aranzabal', 'javier_ignacio_maroto_aranzabal', 'Javier Ignacio Maroto Aranzábal'],
    ['soraya_saenz_santamaria_anton', 'maria_soraya_saenz_santamaria_anton', 'María Soraya Sáenz de Santamaría Antón'],
    ['alvaro_nadal_belda', 'alvaro_maria_nadal_belda'],
    ['fernando_martinez_maillo', 'fernando_martinez_maillo_toribio'],
    ['beatriz_corredor_sierra', 'maria_beatriz_corredor_sierra'],
    ['fatima_banez_garcia', 'maria_fatima_banez_garcia'],
    ['maria_angeles_marra_dominguez', 'maria_los_angeles_marra_dominguez'],
    ['artemi_rallo_lombarte', 'artemi_vicent_rallo_lombarte', 'Artemi Vicent Rallo Lombarte'],
    ['ana_torme_pardo', 'ana_maria_torme_pardo'],
    ['miriam_blasco_soto', 'miriam_guadalupe_blasco_soto'],
    ['francisco_caamano_dominguez', 'francisco_manuel_caamano_dominguez'],
    ['encarnacion_naharro_mora', 'maria_encarnacion_naharro_mora'],
    ['mercedes_perez_merino', 'maria_mercedes_perez_merino'],
    ['immaculada_riera_rene', 'inmaculada_riera_rene'],
    ['elena_valenciano_martinez_orozco', 'maria_elena_valenciano_martinez_orozco'],
    ['pilar_rojo_noguera', 'pilar_milagros_rojo_noguera', 'Pilar Milagros Rojo Noguera'],
    ['angeles_munoz_uriol', 'maria_angeles_munoz_uriol', 'María Ángeles Muñoz Uriol'],
    ['vicente_ferrer_rosello', 'vicente_liliano_ferrer_rosello'],
    ['gonzalo_robles_orozco', 'gonzalo_jesus_robles_orozco', 'Gonzalo Jesús Robles Orozco'],
    ['octavio_granado_martinez', 'octavio_jose_granado_martinez'],
    ['mateu_isern_estela', 'mateo_isern_estela'],
    ['maria_del_mar_julios_reyes', 'maria_del_mar_del_pino_julios_reyes', 'María del Mar del Pino Julios Reyes'],
    ['ruben_moreno_palanques', 'ruben_fausto_moreno_palanques', 'Rubén Fausto Moreno Palanques'],
    ['angel_acebes_paniagua', 'angel_jesus_acebes_paniagua'],
    ['salvador_encina_ortega', 'salvador_antonio_encina_ortega'],
    ['javier_arenas_bocanegra', 'francisco_javier_arenas_bocanegra'],
    ['josep_suner_cuberta', 'josep_sunyer_cuberta'],
    ['felipe_lorda_alaiz', 'felip_lorda_alaiz'],
    ['ramon_sainz_varanda_jimenez', 'ramon_sainz_varanda_jimenez_iglesia'],
    ['adriano_marques_magallanes', 'adriano_antonio_marques_magallanes'],
    ['manuel_clavero_arevalo', 'manuel_francisco_clavero_arevalo'],
    ['alberto_oliart_saussol', 'alberto_carlos_oliart_saussol'],
    ['francisco_fernandez_ordonez', 'francisco_jose_fernandez_ordonez'],
    ['victor_carrascal_felgueroso', 'victor_manuel_carrascal_felgueroso'],
    ['juan_iglesias_marcelo', 'juan_angel_iglesias_marcelo'],
    ['jaime_garcia_anoveros', 'jaime_julian_garcia_anoveros'],
    ['pilar_salarrullana_verda', 'maria_pilar_salarrullana_verda'],
    ['luis_ramallo_garcia', 'luis_jacinto_ramallo_garcia'],
    ['ricardo_bueno_fernandez', 'ricardo_manuel_bueno_fernandez'],
    ['francisco_torre_prados', 'francisco_manuel_torre_prados'],
    ['tomas_rodriguez_bolanos', 'tomas_manuel_rodriguez_bolanos'],
    ['xabier_albistur_marin', 'francisco_xabier_albistur_marin'],
    ['juan_jose_lucas_jimenez', 'juan_jose_lucas_gimenez'],
    ['soledad_becerril_bustamante', 'maria_soledad_becerril_bustamante'],
    ['jesus_posada_moreno', 'jesus_maria_posada_moreno', 'Jesús María Posada Moreno'],
    ['amparo_rubiales_torrejon', 'maria_amparo_rubiales_torrejon', 'María Amparo Rubiales Torrejón'],
    ['angel_franco_gutiez', 'angel_antonio_franco_gutiez'],
    ['teofila_martinez_saiz', 'maria_teofila_martinez_saiz','María Teófila Martínez Saiz'],
    ['alberto_perez_ferre', 'alberto_javier_perez_ferre'],
    ['isabel_celaa_dieguez', 'maria_isabel_celaa_dieguez'],
    ['joseba_zubia_atxaerandio', 'joseba_mirena_zubia_atxaerandio', 'Joseba Mirena de Zubía Atxaerandio'],
    ['joan_lerma_blasco', 'juan_francisco_lerma_blasco'],
    ['cristina_narbona_ruiz', 'maria_cristina_narbona_ruiz'],
    ['gonzalo_pineiro_garcia_lago', 'gonzalo_javier_pineiro_garcia_lago'],
    ['eloisa_alvarez_otero', 'eloisa_alvarez_oteo'],
    ['eloisa_alvarez_oteo', 'maria_eloisa_alvarez_oteo', 'María Eloísa Álvarez Oteo'],
    ['carmen_calvo_poyato', 'maria_del_carmen_calvo_poyato'],
    ['valeriano_gomez_sanchez', 'tomas_valeriano_gomez_sanchez'],
]
# fmt: on


class Command(BaseCommand):
    """
    Remove duplicate persons (they are collected in
    different sources with different full names)
    """

    help = "Fix duplicated persons"

    def handle(self, *args, **options):
        for row in DATA:
            for to_remove in Person.objects.filter(id_name=row[0]):
                to_remove = Person.objects.filter(id_name=row[0]).first()
                to_preserve = Person.objects.filter(id_name=row[1]).first()

                if not to_remove or not to_preserve:
                    continue

                for key in to_remove.metadata:
                    if not key in to_preserve.metadata:
                        to_preserve.metadata[key] = to_remove.metadata[key]

                for key in ["birth_date", "genre", "first_name", "last_name"]:
                    self.update_new_field(to_preserve, to_remove, key)

                if len(row) == 3:
                    # if new name is provided, change it (and id_name)
                    to_preserve.full_name = row[2]

                to_preserve.save()
                self.update_positions(to_preserve, to_remove)
                self.update_birth_sources(to_preserve, to_remove)
                to_remove.delete()
                if options["verbosity"] >= 2:
                    logger.info(f"{to_remove} -> {to_preserve} fixed")

        if options["verbosity"] >= 2:
            logger.info("Done")

    def update_new_field(self, to_preserve: Person, to_remove: Person, field: str):
        """
        Update field from old person to new person if new person
        doesn't have it
        """
        if getattr(to_remove, field) and not getattr(to_preserve, field):
            setattr(to_preserve, field, getattr(to_remove, field))

    def update_positions(self, to_preserve: Person, to_remove: Person):
        """
        Update all positions from old person to new person
        """
        Position.objects.filter(person=to_remove).update(person=to_preserve)

    def update_birth_sources(self, to_preserve: Person, to_remove: Person):
        """
        Update all birth date sources from old person to new person
        """
        for old_birth_source in BirthDateSource.objects.filter(person=to_remove):
            if not BirthDateSource.objects.filter(
                person=to_preserve, url=old_birth_source.url
            ).exists():
                # birth source not registered yet
                old_birth_source.person = to_preserve
                old_birth_source.date = to_preserve.birth_date
                old_birth_source.save(update_fields=["person"])
