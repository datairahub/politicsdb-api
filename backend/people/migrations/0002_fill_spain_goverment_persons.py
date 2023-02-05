# -*- coding: utf-8 -*-
from urllib.parse import urlparse
from django.db import migrations
from people.services.people_id import people_id_from_name
from people.services.names import clean_spanish_name

# fmt: off
DATA = [
    ['Abel', 'Matutes Juan',                                   'M', '1941-10-31', 1, 'https://en.wikipedia.org/wiki/Abel_Matutes'],
    ['Abel Ramón', 'Caballero Álvarez',                        'M', '1946-09-02', 1, 'https://en.wikipedia.org/wiki/Abel_Caballero'],
    ['Adolfo', 'Suárez González',                              'M', '1932-09-25', 1, 'https://en.wikipedia.org/wiki/Adolfo_Su%C3%A1rez'],
    ['Agustín', 'Rodríguez Sahagún',                           'M', '1932-04-27', 1, 'https://en.wikipedia.org/wiki/Agust%C3%ADn_Rodr%C3%ADguez_Sahag%C3%BAn'],
    ['Alberto', 'Garzón Espinosa',                             'M', '1985-10-09', 1, 'https://en.wikipedia.org/wiki/Alberto_Garz%C3%B3n'],
    ['Alberto', 'Oliart Saussol',                              'M', '1928-07-29', 1, 'https://en.wikipedia.org/wiki/Alberto_Oliart'],
    ['Alberto', 'Ruiz-Gallardón Jiménez',                      'M', '1958-12-11', 1, 'https://en.wikipedia.org/wiki/Alberto_Ruiz-Gallard%C3%B3n'],
    ['Alfonso', 'Alonso Aranegui',                             'M', '1967-04-14', 1, 'https://en.wikipedia.org/wiki/Alfonso_Alonso'],
    ['Alfonso', 'Dastis Quecedo',                              'M', '1955-10-05', 1, 'https://en.wikipedia.org/wiki/Alfonso_Dastis'],
    ['Alfonso', 'Guerra González',                             'M', '1940-05-31', 1, 'https://en.wikipedia.org/wiki/Alfonso_Guerra'],
    ['Alfonso', 'Osorio García',                               'M', '1923-12-13', 1, 'https://en.wikipedia.org/wiki/Alfonso_Osorio'],
    ['Alfredo', 'Pérez Rubalcaba',                             'M', '1951-07-28', 1, 'https://en.wikipedia.org/wiki/Alfredo_P%C3%A9rez_Rubalcaba'],
    ['Álvaro', 'Nadal Belda',                                  'M', '1970-01-30', 1, 'https://en.wikipedia.org/wiki/%C3%81lvaro_Nadal'],
    ['Álvaro', 'Rengifo Calderón',                             'M', '1932-07-05', 1, 'https://es.wikipedia.org/wiki/%C3%81lvaro_Rengifo'],
    ['Ana María', 'Pastor Julián',                             'F', '1957-11-11', 1, 'https://en.wikipedia.org/wiki/Ana_Pastor_(politician)'],
    ['Ana', 'Mato Adrover',                                    'F', '1959-09-24', 1, 'https://en.wikipedia.org/wiki/Ana_Mato'],
    ['Ana', 'Palacio Vallelersundi',                           'F', '1948-07-22', 1, 'https://en.wikipedia.org/wiki/Ana_Palacio'],
    ['Andrés', 'Reguera Guajardo',                             'M', '1930-11-16', 1, 'https://es.wikipedia.org/wiki/Andr%C3%A9s_Reguera_Guajardo'],
    ['Ángel', 'Acebes Paniagua',                               'M', '1958-07-03', 1, 'https://en.wikipedia.org/wiki/%C3%81ngel_Acebes'],
    ['Ángel', 'Gabilondo Pujol',                               'M', '1949-03-01', 1, 'https://en.wikipedia.org/wiki/%C3%81ngel_Gabilondo'],
    ['Ángeles', 'González-Sinde Reig',                         'F', '1965-04-07', 1, 'https://en.wikipedia.org/wiki/%C3%81ngeles_Gonz%C3%A1lez-Sinde'],
    ['Anna María', 'Birulés Bertrán',                          'F', '1954-06-28', 1, 'https://en.wikipedia.org/wiki/Anna_Birul%C3%A9s'],
    ['Antoni', 'Asunción Hernández',                           'M', '1951-07-12', 1, 'https://en.wikipedia.org/wiki/Antoni_Asunci%C3%B3n'],
    ['Antonio', 'Camacho Vizcaíno',                            'M', '1964-02-11', 1, 'https://en.wikipedia.org/wiki/Antonio_Camacho_Vizca%C3%ADno'],
    ['Antonio', 'Fontán Pérez',                                'M', '1923-10-15', 1, 'https://en.wikipedia.org/wiki/Antonio_Font%C3%A1n'],
    ['Antonio', 'Ibáñez Freire',                               'M', '1913-09-25', 1, 'https://en.wikipedia.org/wiki/Antonio_Ib%C3%A1%C3%B1ez_Freire'],
    ['Arancha', 'González Laya',                               'F', '1969-05-22', 1, 'https://en.wikipedia.org/wiki/Arancha_Gonz%C3%A1lez_Laya'],
    ['Aurelio', 'Menéndez Menéndez',                           'M', '1927-05-01', 1, 'https://en.wikipedia.org/wiki/Aurelio_Men%C3%A9ndez'],
    ['Beatriz', 'Corredor Sierra',                             'F', '1968-07-01', 1, 'https://en.wikipedia.org/wiki/Beatriz_Corredor'],
    ['Bernat', 'Soria Escoms',                                 'M', '1951-05-07', 1, 'https://en.wikipedia.org/wiki/Bernat_Soria'],
    ['Bibiana', 'Aído Almagro',                                'F', '1977-02-02', 1, 'https://en.wikipedia.org/wiki/Bibiana_A%C3%ADdo'],
    ['Carlos', 'Bustelo García del Real',                      'M', '1936-10-21', 1, 'https://www.diariocordoba.com/opinion/2005/02/02/carlos-bustelo-38806511.html'],
    ['Carlos', 'Franco Iribarnegaray',                         'M', '1912-08-30', 1, 'https://en.wikipedia.org/wiki/Carlos_Franco_Iribarnegaray'],
    ['Carlos', 'Pérez de Bricio Olariaga',                     'M', '1927-12-31', 1, 'https://es.wikipedia.org/wiki/Carlos_P%C3%A9rez_de_Bricio'],
    ['Carlos', 'Romero Herrera',                               'M', '1941-12-12', 1, 'https://gee.mienciclo.com/articulo/jose-carlos-romero-herrera'],
    ['Carlos', 'Solchaga Catalán',                             'M', '1944-05-28', 1, 'https://es.wikipedia.org/wiki/Carlos_Solchaga'],
    ['Carlos', 'Westendorp Cabeza',                            'M', '1937-01-07', 1, 'https://es.wikipedia.org/wiki/Carlos_Westendorp'],
    ['Carme', 'Chacón Piqueras',                               'F', '1971-03-13', 1, 'https://es.wikipedia.org/wiki/Carme_Chac%C3%B3n'],
    ['Carmen', 'Alborch Bataller',                             'F', '1947-10-31', 1, 'https://es.wikipedia.org/wiki/Carmen_Alborch'],
    ['Carmen', 'Calvo Poyato',                                 'F', '1957-06-07', 1, 'https://es.wikipedia.org/wiki/Carmen_Calvo'],
    ['Carmen', 'Montón Giménez',                               'F', '1976-03-09', 1, 'https://es.wikipedia.org/wiki/Carmen_Mont%C3%B3n'],
    ['Carolina', 'Darias San Sebastián',                       'F', '1965-11-25', 1, 'https://es.wikipedia.org/wiki/Carolina_Darias'],
    ['Celestino', 'Corbacho Chaves',                           'M', '1949-11-14', 1, 'https://es.wikipedia.org/wiki/Celestino_Corbacho'],
    ['Celia', 'Villalobos Talero',                             'F', '1949-04-18', 1, 'https://es.wikipedia.org/wiki/Celia_Villalobos'],
    ['César Antonio', 'Molina Sánchez',                        'M', '1952-09-14', 1, 'https://es.wikipedia.org/wiki/C%C3%A9sar_Antonio_Molina'],
    ['Cristina', 'Alberdi Alonso',                             'F', '1946-02-22', 1, 'https://es.wikipedia.org/wiki/Cristina_Alberdi'],
    ['Cristina', 'Garmendia Mendizábal',                       'F', '1962-02-21', 1, 'https://es.wikipedia.org/wiki/Cristina_Garmendia'],
    ['Cristina', 'Narbona Ruiz',                               'F', '1951-07-29', 1, 'https://es.wikipedia.org/wiki/Cristina_Narbona'],
    ['Cristóbal Ricardo', 'Montoro Romero',                    'M', '1950-07-28', 1, 'https://es.wikipedia.org/wiki/Crist%C3%B3bal_Montoro'],
    ['Diana', 'Morant Ripoll',                                 'F', '1980-06-25', 1, 'https://es.wikipedia.org/wiki/Diana_Morant'],
    ['Dolores', 'Delgado García',                              'F', '1962-11-09', 1, 'https://es.wikipedia.org/wiki/Dolores_Delgado'],
    ['Dolors', 'Montserrat Montserrat',                        'F', '1973-09-18', 1, 'https://es.wikipedia.org/wiki/Dolors_Montserrat'],
    ['Eduard', 'Punset Casals',                                'M', '1936-11-09', 1, 'https://es.wikipedia.org/wiki/Eduardo_Punset'],
    ['Eduardo', 'Carriles Galarraga',                          'M', '1923-11-28', 1, 'https://es.wikipedia.org/wiki/Eduardo_Punset'],
    ['Eduardo', 'Serra Rexach',                                'M', '1946-12-19', 1, 'https://es.wikipedia.org/wiki/Eduardo_Serra_Rexach'],
    ['Eduardo Andrés', 'Zaplana Hernández-Soro',               'M', '1956-04-03', 1, 'https://es.wikipedia.org/wiki/Eduardo_Zaplana'],
    ['Elena', 'Espinosa Mangana',                              'F', '1960-03-21', 1, 'https://es.wikipedia.org/wiki/Elena_Espinosa'],
    ['Elena', 'Salgado Méndez',                                'F', '1949-05-12', 1, 'https://es.wikipedia.org/wiki/Elena_Salgado'],
    ['Enrique', 'Barón Crespo',                                'M', '1944-03-27', 1, 'https://es.wikipedia.org/wiki/Enrique_Bar%C3%B3n'],
    ['Enrique', 'de la Mata Gorostizaga',                      'M', '1933-09-20', 1, 'https://es.wikipedia.org/wiki/Enrique_de_la_Mata'],
    ['Enrique', 'Fuentes Quintana',                            'M', '1924-12-13', 1, 'https://es.wikipedia.org/wiki/Enrique_Fuentes_Quintana'],
    ['Enrique', 'Múgica Herzog',                               'M', '1932-02-20', 1, 'https://es.wikipedia.org/wiki/Enrique_M%C3%BAgica'],
    ['Enrique', 'Sánchez de León Pérez',                       'M', '1934-06-09', 1, 'https://es.wikipedia.org/wiki/Enrique_S%C3%A1nchez_de_Le%C3%B3n'],
    ['Ernest', 'Lluch Martín',                                 'M', '1937-01-21', 1, 'https://es.wikipedia.org/wiki/Ernest_Lluch'],
    ['Esperanza', 'Aguirre Gil de Biedma',                     'F', '1952-01-03', 1, 'https://es.wikipedia.org/wiki/Esperanza_Aguirre'],
    ['Fátima', 'Báñez García',                                 'F', '1967-01-06', 1, 'https://es.wikipedia.org/wiki/F%C3%A1tima_B%C3%A1%C3%B1ez'],
    ['Federico', 'Mayor Zaragoza',                             'M', '1934-01-27', 1, 'https://es.wikipedia.org/wiki/Federico_Mayor_Zaragoza'],
    ['Federico', 'Trillo-Figueroa Martínez-Conde',             'M', '1952-05-23', 1, 'https://es.wikipedia.org/wiki/Federico_Trillo'],
    ['Felipe', 'González Márquez',                             'M', '1942-03-05', 1, 'https://es.wikipedia.org/wiki/Felipe_Gonz%C3%A1lez'],
    ['Félix', 'Álvarez-Arenas Pacheco',                        'M', '1913-10-05', 1, 'https://es.wikipedia.org/wiki/F%C3%A9lix_%C3%81lvarez-Arenas_Pacheco'],
    ['Félix', 'Bolaños García',                                'M', '1975-12-17', 1, 'https://es.wikipedia.org/wiki/F%C3%A9lix_Bola%C3%B1os'],
    ['Félix Manuel', 'Pérez Miyares',                          'M', '1936-09-04', 1, 'https://www.march.es/es/coleccion/archivo-linz-transicion-espanola/ficha/biografias-nuevos-ministros--linz%3AR-67627'],
    ['Félix', 'Pons Irazazábal',                               'M', '1942-09-14', 1, 'https://es.wikipedia.org/wiki/F%C3%A9lix_Pons'],
    ['Fernando', 'Abril Martorell',                            'M', '1936-08-31', 1, 'https://es.wikipedia.org/wiki/Fernando_Abril_Martorell'],
    ['Fernando', 'de Santiago Díaz de Mendívil',               'M', '1910-07-23', 1, 'https://es.wikipedia.org/wiki/Fernando_de_Santiago'],
    ['Fernando', 'Grande-Marlaska Gómez',                      'M', '1962-07-26', 1, 'https://es.wikipedia.org/wiki/Fernando_Grande-Marlaska'],
    ['Fernando', 'Ledesma Bartret',                            'M', '1939-12-30', 1, 'https://es.wikipedia.org/wiki/Fernando_Ledesma'],
    ['Fernando', 'Morán López',                                'M', '1926-03-25', 1, 'https://es.wikipedia.org/wiki/Fernando_Mor%C3%A1n_L%C3%B3pez'],
    ['Francisco', 'Álvarez-Cascos Fernández',                  'M', '1947-10-01', 1, 'https://es.wikipedia.org/wiki/Francisco_%C3%81lvarez-Cascos'],
    ['Francisco', 'Caamaño Domínguez',                         'M', '1963-01-08', 1, 'https://es.wikipedia.org/wiki/Francisco_Caama%C3%B1o_Dom%C3%ADnguez'],
    ['Francisco', 'Fernández Ordóñez',                         'M', '1930-06-22', 1, 'https://es.wikipedia.org/wiki/Francisco_Fern%C3%A1ndez_Ord%C3%B3%C3%B1ez'],
    ['Francisco', 'Lozano Vicente',                            'M', '1922-10-04', 1, 'https://es.wikipedia.org/wiki/Francisco_Lozano_Vicente'],
    ['Gabriel', 'Pita da Veiga Sanz',                          'M', '1909-01-31', 1, 'https://es.wikipedia.org/wiki/Gabriel_Pita_da_Veiga'],
    ['Gustavo', 'Suárez Pertierra',                            'M', '1949-02-27', 1, 'https://humanidadesdigitales.uc3m.es/s/catedraticos/item/16990'],
    ['Ignacio', 'Bayón Mariné',                                'M', '1944-02-14', 1, 'https://es.wikipedia.org/wiki/Ignacio_Bay%C3%B3n'],
    ['Ignacio', 'Camuñas Solís',                               'M', '1940-09-01', 1, 'https://es.wikipedia.org/wiki/Ignacio_Camu%C3%B1as_Sol%C3%ADs'],
    ['Ignacio', 'García López',                                'M', '1924-09-05', 1, 'https://es.wikipedia.org/wiki/Ignacio_Garc%C3%ADa_L%C3%B3pez'],
    ['Íñigo', 'Cavero Lataillade',                             'M', '1929-08-01', 1, 'https://es.wikipedia.org/wiki/%C3%8D%C3%B1igo_Cavero'],
    ['Íñigo', 'de la Serna Hernáiz',                           'M', '1971-01-10', 1, 'https://es.wikipedia.org/wiki/%C3%8D%C3%B1igo_de_la_Serna'],
    ['Íñigo', 'Méndez de Vigo Montojo',                        'M', '1956-01-21', 1, 'https://es.wikipedia.org/wiki/%C3%8D%C3%B1igo_M%C3%A9ndez_de_Vigo'],
    ['Ione', 'Belarra Urteaga',                                'F', '1987-09-25', 1, 'https://es.wikipedia.org/wiki/Ione_Belarra'],
    ['Irene', 'Montero Gil',                                   'F', '1988-02-13', 1, 'https://es.wikipedia.org/wiki/Irene_Montero'],
    ['Isabel', 'García Tejerina',                              'F', '1968-10-09', 1, 'https://es.wikipedia.org/wiki/Isabel_Garc%C3%ADa_Tejerina'],
    ['Isabel', 'Rodríguez García',                             'F', '1981-06-05', 1, 'https://es.wikipedia.org/wiki/Isabel_Rodr%C3%ADguez_Garc%C3%ADa'],
    ['Isabel', 'Tocino Biscarolasaga',                         'F', '1949-03-09', 1, 'https://es.wikipedia.org/wiki/Isabel_Tocino'],
    ['Jaime', 'García Añoveros',                               'M', '1932-01-24', 1, 'https://es.wikipedia.org/wiki/Jaime_Garc%C3%ADa_A%C3%B1overos'],
    ['Jaime', 'Lamo de Espinosa Michels de Champourcin',       'M', '1941-04-04', 1, 'https://es.wikipedia.org/wiki/Jaime_Lamo_de_Espinosa'],
    ['Jaime', 'Mayor Oreja',                                   'M', '1951-07-12', 1, 'https://es.wikipedia.org/wiki/Jaime_Mayor_Oreja'],
    ['Jaume', 'Matas Palou',                                   'M', '1956-10-05', 1, 'https://es.wikipedia.org/wiki/Jaume_Matas'],
    ['Francisco Javier', 'Arenas Bocanegra',                   'M', '1957-12-28', 1, 'https://es.wikipedia.org/wiki/Javier_Arenas'],
    ['Javier', 'Gómez-Navarro Navarrete',                      'M', '1945-09-13', 1, 'https://es.wikipedia.org/wiki/Javier_G%C3%B3mez_Navarro'],
    ['Javier Luis', 'Sáenz de Cosculluela',                    'M', '1944-10-11', 1, 'https://es.wikipedia.org/wiki/Javier_S%C3%A1enz_de_Cosculluela'],
    ['Javier', 'Moscoso del Prado Muñoz',                      'M', '1934-10-07', 1, 'https://es.wikipedia.org/wiki/Javier_Moscoso'],
    ['Javier', 'Solana Madariaga',                             'M', '1942-07-14', 1, 'https://es.wikipedia.org/wiki/Javier_Solana'],
    ['Jerónimo', 'Saavedra Acevedo',                           'M', '1936-07-03', 1, 'https://es.wikipedia.org/wiki/Jer%C3%B3nimo_Saavedra'],
    ['Jesús', 'Caldera Sánchez-Capitán',                       'M', '1957-10-31', 1, 'https://es.wikipedia.org/wiki/Jes%C3%BAs_Caldera'],
    ['Jesús María', 'Posada Moreno',                           'M', '1945-04-04', 1, 'https://es.wikipedia.org/wiki/Jes%C3%BAs_Posada_Moreno'],
    ['Jesús', 'Sancho Rof',                                    'M', '1940-12-16', 1, 'https://es.wikipedia.org/wiki/Jes%C3%BAs_Sancho_Rof'],
    ['Joan', 'Clos Matheu',                                    'M', '1949-06-29', 1, 'https://es.wikipedia.org/wiki/Joan_Clos'],
    ['Joan', 'Lerma Blasco',                                   'M', '1951-07-15', 1, 'https://es.wikipedia.org/wiki/Joan_Lerma'],
    ['Joan', 'Majó Cruzate',                                   'M', '1939-03-30', 1, 'https://fpabloiglesias.es/entrada-db/majo-cruzate-juan/'],
    ['Joan', 'Subirats Humet',                                 'M', '1951-05-17', 1, 'https://es.wikipedia.org/wiki/Joan_Subirats'],
    ['José Joaquín', 'Almunia Amann',                          'M', '1948-06-17', 1, 'https://es.wikipedia.org/wiki/Joaqu%C3%ADn_Almunia'],
    ['Joaquín', 'Garrigues Walker',                            'M', '1933-09-30', 1, 'https://es.wikipedia.org/wiki/Joaqu%C3%ADn_Garrigues_Walker'],
    ['Jordi', 'Sevilla Segura',                                'M', '1956-03-19', 1, 'https://es.wikipedia.org/wiki/Jordi_Sevilla'],
    ['Jordi', 'Solé Tura',                                     'M', '1930-05-23', 1, 'https://es.wikipedia.org/wiki/Jordi_Sol%C3%A9_Tura'],
    ['Jorge', 'Fernández Díaz',                                'M', '1950-04-06', 1, 'https://es.wikipedia.org/wiki/Jorge_Fern%C3%A1ndez_D%C3%ADaz'],
    ['Jorge', 'Semprún Maura',                                 'M', '1923-12-10', 1, 'https://es.wikipedia.org/wiki/Jorge_Sempr%C3%BAn'],
    ['José Antonio', 'Alonso Suárez',                          'M', '1960-03-28', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Antonio_Alonso_Su%C3%A1rez'],
    ['José Antonio', 'Griñán Martínez',                        'M', '1946-06-07', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Antonio_Gri%C3%B1%C3%A1n'],
    ['José', 'Barrionuevo Peña',                               'M', '1942-03-13', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Barrionuevo'],
    ['José', 'Blanco López',                                   'M', '1962-02-06', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Blanco_L%C3%B3pez'],
    ['José', 'Bono Martínez',                                  'M', '1950-12-14', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Bono'],
    ['José Claudio', 'Aranzadi Martínez',                      'M', '1946-10-09', 1, 'https://es.wikipedia.org/wiki/Claudio_Aranzadi'],
    ['José Enrique', 'Martínez Genique',                       'M', '1935-01-02', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Enrique_Mart%C3%ADnez_Genique'],
    ['José', 'Guirao Cabrera',                                 'M', '1959-06-09', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Guirao'],
    ['José Ignacio', 'Wert Ortega',                            'M', '1950-02-18', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Ignacio_Wert'],
    ['José', 'Lladó Fernández Urrutia',                        'M', '1934-03-29', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Llad%C3%B3'],
    ['José Luis', 'Ábalos Meco',                               'M', '1959-12-09', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Luis_%C3%81balos'],
    ['José Luis', 'Álvarez Álvarez',                           'M', '1930-04-04', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Luis_%C3%81lvarez_y_%C3%81lvarez'],
    ['José Luis', 'Corcuera Cuesta',                           'M', '1945-07-02', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Luis_Corcuera'],
    ['José Luis', 'Escrivá Belmonte',                          'M', '1960-12-05', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Luis_Escriv%C3%A1'],
    ['José Luis', 'García Ferrero',                            'M', '1929-10-30', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Luis_Garc%C3%ADa_Ferrero'],
    ['José Luis', 'Leal Maldonado',                            'M', '1939-08-01', 0, 'https://elpais.com/diario/2001/10/24/economia/1003874418_850215.html'],
    ['José Luis', 'Rodríguez Zapatero',                        'M', '1960-08-04', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Luis_Rodr%C3%ADguez_Zapatero'],
    ['José Manuel', 'Albares Bueno',                           'M', '1972-03-22', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Manuel_Albares'],
    ['José Manuel', 'García-Margallo Marfil',                  'M', '1944-08-13', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Manuel_Garc%C3%ADa-Margallo'],
    ['José Manuel', 'Otero Novas',                             'M', '1940-03-20', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Manuel_Otero'],
    ['José Manuel', 'Rodríguez Uribes',                        'M', '1968-10-09', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Manuel_Rodr%C3%ADguez_Uribes'],
    ['José Manuel', 'Romay Beccaría',                          'M', '1934-01-18', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Manuel_Romay_Beccar%C3%ADa'],
    ['José Manuel', 'Soria López',                             'M', '1958-01-05', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Manuel_Soria'],
    ['José María', 'Aznar López',                              'M', '1953-02-25', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Mar%C3%ADa_Aznar'],
    ['José María', 'Maravall Herrero',                         'M', '1942-04-07', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Mar%C3%ADa_Maravall'],
    ['José María', 'Michavila Núñez',                          'M', '1960-03-28', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Mar%C3%ADa_Michavila'],
    ['José', 'Montilla Aguilera',                              'M', '1955-01-15', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Montilla'],
    ['José Pedro', 'Pérez-Llorca Rodrigo',                     'M', '1940-11-30', 1, 'https://es.wikipedia.org/wiki/Jos%C3%A9_Pedro_P%C3%A9rez-Llorca'],
    ['Josep', 'Borrell Fontelles',                             'M', '1947-04-24', 1, 'https://es.wikipedia.org/wiki/Josep_Borrell'],
    ['Josep', 'Piqué Camps',                                   'M', '1955-02-21', 1, 'https://es.wikipedia.org/wiki/Josep_Piqu%C3%A9'],
    ['Juan Alberto', 'Belloch Julbe',                          'M', '1950-02-03', 1, 'https://es.wikipedia.org/wiki/Juan_Alberto_Belloch'],
    ['Juan Antonio', 'García Díez',                            'M', '1940-08-04', 1, 'https://dbe.rah.es/biografias/10359/juan-antonio-garcia-diez'],
    ['Juan Antonio', 'Ortega Díaz-Ambrona',                    'M', '1939-12-11', 1, 'https://es.wikipedia.org/wiki/Juan_Antonio_Ortega_y_D%C3%ADaz-Ambrona'],
    ['Juan Carlos', 'Aparicio Pérez',                          'M', '1955-04-20', 1, 'https://es.wikipedia.org/wiki/Juan_Carlos_Aparicio'],
    ['Juan Carlos', 'Campo Moreno',                            'M', '1961-10-17', 1, 'https://es.wikipedia.org/wiki/Juan_Carlos_Campo'],
    ['Juan', 'Costa Climent',                                  'M', '1965-04-10', 1, 'https://es.wikipedia.org/wiki/Juan_Costa'],
    ['Juan Fernando', 'López Aguilar',                         'M', '1961-06-10', 1, 'https://es.wikipedia.org/wiki/Juan_Fernando_L%C3%B3pez_Aguilar'],
    ['Juan Ignacio', 'Zoido Álvarez',                          'M', '1957-01-21', 1, 'https://es.wikipedia.org/wiki/Juan_Ignacio_Zoido'],
    ['Juan José', 'Lucas Jiménez',                             'M', '1944-05-10', 1, 'https://es.wikipedia.org/wiki/Juan_Jos%C3%A9_Lucas'],
    ['Juan José', 'Rosón Pérez',                               'M', '1932-09-25', 1, 'https://es.wikipedia.org/wiki/Juan_Jos%C3%A9_Ros%C3%B3n'],
    ['Juan Manuel', 'Eguiagaray Ucelay',                       'M', '1945-12-25', 1, 'https://es.wikipedia.org/wiki/Juan_Manuel_Eguiagaray'],
    ['Juan', 'Rovira Tarazona',                                'M', '1930-05-05', 1, 'https://es.wikipedia.org/wiki/Juan_Rovira_Tarazona'],
    ['Julia', 'García-Valdecasas Salgado',                     'F', '1944-01-29', 1, 'https://es.wikipedia.org/wiki/Julia_Garc%C3%ADa-Valdecasas'],
    ['Julián', 'Campo Sainz de Rozas',                         'M', '1938-06-19', 1, 'https://es.wikipedia.org/wiki/Juli%C3%A1n_Campo'],
    ['Julián', 'García Valverde',                              'M', '1946-03-20', 1, 'https://elpais.com/diario/1991/03/12/espana/668732404_850215.html'],
    ['Julián', 'García Vargas',                                'M', '1945-10-19', 1, 'https://gee.mienciclo.com/articulo/julian-garcia-vargas'],
    ['Landelino', 'Lavilla Alsina',                            'M', '1934-08-06', 1, 'https://es.wikipedia.org/wiki/Landelino_Lavilla'],
    ['Leire', 'Pajín Iraola',                                  'F', '1976-09-16', 1, 'https://es.wikipedia.org/wiki/Leire_Paj%C3%ADn'],
    ['Leopoldo', 'Calvo-Sotelo Bustelo',                       'M', '1926-04-14', 1, 'https://es.wikipedia.org/wiki/Leopoldo_Calvo-Sotelo'],
    ['Loyola', 'de Palacio del Valle-Lersundi',                'F', '1950-09-16', 1, 'https://es.wikipedia.org/wiki/Loyola_de_Palacio'],
    ['Luis Carlos', 'Croissier Batista',                       'M', '1950-08-19', 1, 'https://fpabloiglesias.es/entrada-db/croissier-batista-luis-carlos/'],
    ['Luis', 'de Guindos Jurado',                              'M', '1960-01-16', 1, 'https://es.wikipedia.org/wiki/Luis_de_Guindos'],
    ['Luis', 'Gámir Casares',                                  'M', '1942-05-08', 1, 'https://es.wikipedia.org/wiki/Luis_G%C3%A1mir'],
    ['Luis', 'González Seara',                                 'M', '1936-06-07', 1, 'https://es.wikipedia.org/wiki/Luis_Gonz%C3%A1lez_Seara'],
    ['Luis Manuel', 'Cosculluela Montaner',                    'M', '1939-09-23', 1, 'https://es.wikipedia.org/wiki/Luis_Manuel_Cosculluela_Montaner'],
    ['Luis María', 'Atienza Serna',                            'M', '1957-08-30', 1, 'https://es.wikipedia.org/wiki/Luis_Mar%C3%ADa_Atienza'],
    ['Luis', 'Martínez Noval',                                 'M', '1948-07-03', 1, 'https://es.wikipedia.org/wiki/Luis_Mart%C3%ADnez_Noval'],
    ['Luis', 'Ortiz González',                                 'M', '1932-07-03', 1, 'https://es.wikipedia.org/wiki/Luis_Ortiz_Gonz%C3%A1lez'],
    ['Luis', 'Planas Puchades',                                'M', '1952-11-20', 1, 'https://es.wikipedia.org/wiki/Luis_Planas'],
    ['Magdalena', 'Álvarez Arza',                              'F', '1952-02-15', 1, 'https://es.wikipedia.org/wiki/Magdalena_%C3%81lvarez'],
    ['Magdalena', 'Valerio Cordero',                           'F', '1959-09-27', 1, 'https://es.wikipedia.org/wiki/Magdalena_Valerio'],
    ['Manuel', 'Castells Oliván',                              'M', '1942-02-09', 1, 'https://es.wikipedia.org/wiki/Manuel_Castells'],
    ['Manuel', 'Chaves González',                              'M', '1945-07-07', 1, 'https://es.wikipedia.org/wiki/Manuel_Chaves'],
    ['Manuel', 'Clavero Arévalo',                              'M', '1926-04-25', 1, 'https://es.wikipedia.org/wiki/Manuel_Clavero_Ar%C3%A9valo'],
    ['Manuel', 'Gutiérrez Mellado',                            'M', '1912-04-30', 1, 'https://es.wikipedia.org/wiki/Manuel_Guti%C3%A9rrez_Mellado'],
    ['Manuel', 'Jiménez de Parga Cabrera',                     'M', '1929-04-09', 1, 'https://es.wikipedia.org/wiki/Manuel_Jim%C3%A9nez_de_Parga'],
    ['Manuel', 'Núñez Pérez',                                  'M', '1933-10-28', 1, 'https://es.wikipedia.org/wiki/Manuel_N%C3%BA%C3%B1ez_P%C3%A9rez'],
    ['Manuel', 'Pimentel Siles',                               'M', '1961-08-30', 1, 'https://es.wikipedia.org/wiki/Manuel_Pimentel'],
    ['Marcelino', 'Oreja Aguirre',                             'M', '1935-02-13', 1, 'https://es.wikipedia.org/wiki/Marcelino_Oreja_Aguirre'],
    ['Margarita', 'Mariscal de Gante Mirón',                   'F', '1954-01-10', 1, 'https://es.wikipedia.org/wiki/Margarita_Mariscal_de_Gante'],
    ['Margarita', 'Robles Fernández',                          'F', '1956-11-10', 1, 'https://es.wikipedia.org/wiki/Margarita_Robles'],
    ['María Ángeles', 'Amador Millán',                         'M', '1949-10-10', 1, 'https://elpais.com/diario/1993/07/14/espana/742600824_850215.html'],
    ['María Antonia', 'Trujillo Rincón',                       'M', '1960-12-18', 1, 'https://es.wikipedia.org/wiki/Mar%C3%ADa_Antonia_Trujillo'],
    ['María del Carmen', 'Calvo Poyato',                       'M', '1957-06-07', 1, 'https://es.wikipedia.org/wiki/Carmen_Calvo'],
    ['María Dolores', 'de Cospedal García',                    'M', '1965-12-13', 1, 'https://es.wikipedia.org/wiki/Mar%C3%ADa_Dolores_de_Cospedal'],
    ['María Elvira', 'Rodríguez Herrer',                       'M', '1949-05-15', 1, 'https://es.wikipedia.org/wiki/Elvira_Rodr%C3%ADguez'],
    ['María Fátima', 'Báñez García',                           'M', '1967-01-06', 1, 'https://es.wikipedia.org/wiki/F%C3%A1tima_B%C3%A1%C3%B1ez'],
    ['María Isabel', 'Celaá Diéguez',                          'M', '1949-05-23', 1, 'https://es.wikipedia.org/wiki/Isabel_Cela%C3%A1'],
    ['María Jesús', 'Montero Cuadrado',                        'M', '1966-02-04', 1, 'https://es.wikipedia.org/wiki/Mar%C3%ADa_Jes%C3%BAs_Montero'],
    ['María Jesús', 'San Segundo Gómez de Cadiñanos',          'M', '1958-03-25', 1, 'https://es.wikipedia.org/wiki/Mar%C3%ADa_Jes%C3%BAs_San_Segundo'],
    ['María Luisa', 'Carcedo Roces',                           'M', '1953-08-30', 1, 'https://es.wikipedia.org/wiki/Mar%C3%ADa_Luisa_Carcedo'],
    ['María Soraya', 'Sáenz de Santamaría Antón',              'M', '1971-06-10', 1, 'https://es.wikipedia.org/wiki/Soraya_S%C3%A1enz_de_Santamar%C3%ADa'],
    ['María Teresa', 'Fernández de la Vega Sanz',              'M', '1949-06-15', 1, 'https://es.wikipedia.org/wiki/Mar%C3%ADa_Teresa_Fern%C3%A1ndez_de_la_Vega'],
    ['Mariano', 'Fernández Bermejo',                           'M', '1948-02-10', 1, 'https://es.wikipedia.org/wiki/Mariano_Fern%C3%A1ndez_Bermejo'],
    ['Mariano', 'Rajoy Brey',                                  'M', '1955-03-27', 1, 'https://es.wikipedia.org/wiki/Mariano_Rajoy'],
    ['Matías', 'Rodríguez Inciarte',                           'M', '1948-03-23', 1, 'https://es.wikipedia.org/wiki/Mat%C3%ADas_Rodr%C3%ADguez_Inciarte'],
    ['Matilde', 'Fernández Sanz',                              'F', '1950-01-24', 1, 'https://es.wikipedia.org/wiki/Matilde_Fern%C3%A1ndez'],
    ['Màxim', 'Huerta Hernández',                              'M', '1971-01-26', 1, 'https://es.wikipedia.org/wiki/M%C3%A1ximo_Huerta'],
    ['Mercedes', 'Cabrera Calvo-Sotelo',                       'F', '1951-12-03', 1, 'https://es.wikipedia.org/wiki/Mercedes_Cabrera'],
    ['Meritxell', 'Batet Lamaña',                              'F', '1973-03-19', 1, 'https://es.wikipedia.org/wiki/Meritxell_Batet'],
    ['Miguel Ángel', 'Moratinos Cuyaubé',                      'M', '1951-06-08', 1, 'https://es.wikipedia.org/wiki/Miguel_%C3%81ngel_Moratinos'],
    ['Miguel', 'Arias Cañete',                                 'M', '1950-02-24', 1, 'https://es.wikipedia.org/wiki/Miguel_Arias_Ca%C3%B1ete'],
    ['Miguel', 'Boyer Salvador',                               'M', '1939-02-05', 1, 'https://es.wikipedia.org/wiki/Miguel_Boyer'],
    ['Miguel', 'Sebastián Gascón',                             'M', '1957-05-13', 1, 'https://es.wikipedia.org/wiki/Miguel_Sebasti%C3%A1n'],
    ['Miquel', 'Iceta Llorens',                                'M', '1960-08-17', 1, 'https://es.wikipedia.org/wiki/Miquel_Iceta'],
    ['Nadia', 'Calviño Santamaría',                            'F', '1968-10-03', 1, 'https://es.wikipedia.org/wiki/Nadia_Calvi%C3%B1o'],
    ['Narcís', 'Serra Serra',                                  'M', '1943-05-30', 1, 'https://es.wikipedia.org/wiki/Narc%C3%ADs_Serra'],
    ['Pablo', 'Iglesias Turrión',                              'M', '1978-10-17', 1, 'https://es.wikipedia.org/wiki/Pablo_Iglesias_Turri%C3%B3n'],
    ['Pascual', 'Pery Junquera',                               'M', '1911-10-17', 1, 'https://es.wikipedia.org/wiki/Pascual_Pery'],
    ['Pedro', 'Duque Duque',                                   'M', '1963-03-14', 1, 'https://es.wikipedia.org/wiki/Pedro_Duque'],
    ['Pedro', 'Morenés Eulate',                                'M', '1948-09-17', 1, 'https://es.wikipedia.org/wiki/Pedro_Moren%C3%A9s'],
    ['Pedro', 'Sánchez Pérez-Castejón',                        'M', '1972-02-29', 1, 'https://es.wikipedia.org/wiki/Pedro_S%C3%A1nchez'],
    ['Pedro', 'Solbes Mira',                                   'M', '1942-08-31', 1, 'https://es.wikipedia.org/wiki/Pedro_Solbes'],
    ['Pilar', 'Alegría Continente',                            'F', '1977-11-01', 1, 'https://es.wikipedia.org/wiki/Pilar_Alegr%C3%ADa'],
    ['Pilar', 'del Castillo Vera',                             'F', '1952-07-31', 1, 'https://es.wikipedia.org/wiki/Pilar_del_Castillo'],
    ['Pilar', 'Llop Cuenca',                                   'F', '1973-08-03', 1, 'https://es.wikipedia.org/wiki/Pilar_Llop'],
    ['Pío', 'Cabanillas Alonso',                               'M', '1958-12-09', 1, 'https://es.wikipedia.org/wiki/P%C3%ADo_Cabanillas_Alonso'],
    ['Pío', 'Cabanillas Gallas',                               'M', '1923-11-13', 1, 'https://es.wikipedia.org/wiki/P%C3%ADo_Cabanillas'],
    ['Rafael', 'Arias-Salgado Montalvo',                       'M', '1942-01-26', 1, 'https://es.wikipedia.org/wiki/Rafael_Arias-Salgado'],
    ['Rafael', 'Calvo Ortega',                                 'M', '1933-08-26', 1, 'https://es.wikipedia.org/wiki/Rafael_Calvo_Ortega'],
    ['Rafael', 'Catalá Polo',                                  'M', '1961-06-21', 1, 'https://es.wikipedia.org/wiki/Rafael_Catal%C3%A1_Polo'],
    ['Ramón', 'Jáuregui Atondo',                               'M', '1948-09-01', 1, 'https://es.wikipedia.org/wiki/Ram%C3%B3n_J%C3%A1uregui'],
    ['Raquel', 'Sánchez Jiménez',                              'F', '1975-11-18', 1, 'https://es.wikipedia.org/wiki/Raquel_S%C3%A1nchez_Jim%C3%A9nez'],
    ['Reyes', 'Maroto Illera',                                 'F', '1973-12-19', 1, 'https://es.wikipedia.org/wiki/Reyes_Maroto'],
    ['Ricardo', 'de la Cierva Hoces',                          'M', '1926-11-09', 1, 'https://es.wikipedia.org/wiki/Ricardo_de_la_Cierva'],
    ['Rodolfo', 'Martín Villa',                                'M', '1934-10-03', 1, 'https://es.wikipedia.org/wiki/Rodolfo_Mart%C3%ADn_Villa'],
    ['Rodrigo', 'de Rato Figaredo',                            'M', '1949-03-18', 1, 'https://es.wikipedia.org/wiki/Rodrigo_Rato'],
    ['Román', 'Escolano Olivares',                             'M', '1965-09-20', 1, 'https://es.wikipedia.org/wiki/Rom%C3%A1n_Escolano'],
    ['Rosa', 'Aguilar Rivero',                                 'F', '1957-07-07', 1, 'https://es.wikipedia.org/wiki/Rosa_Aguilar'],
    ['Rosa', 'Conde Gutiérrez del Álamo',                      'F', '1947-09-07', 1, 'https://es.wikipedia.org/wiki/Rosa_Conde'],
    ['Salvador', 'Illa Roca',                                  'M', '1966-05-05', 1, 'https://es.wikipedia.org/wiki/Salvador_Illa'],
    ['Salvador', 'Sánchez-Terán Hernández',                    'M', '1934-04-19', 1, 'https://es.wikipedia.org/wiki/Salvador_S%C3%A1nchez-Ter%C3%A1n'],
    ['Santiago', 'Rodríguez-Miranda Gómez',                    'M', '1940-01-01', 0, 'https://es.wikipedia.org/wiki/Santiago_Rodr%C3%ADguez-Miranda'],
    ['Sebastián', 'Martín-Retortillo Baquer',                  'M', '1931-02-07', 1, 'https://es.wikipedia.org/wiki/Sebasti%C3%A1n_Mart%C3%ADn-Retortillo'],
    ['Soledad', 'Becerril Bustamante',                         'F', '1944-08-16', 1, 'https://es.wikipedia.org/wiki/Soledad_Becerril'],
    ['Soraya', 'Sáenz de Santamaría Antón',                    'F', '1971-06-10', 1, 'https://es.wikipedia.org/wiki/Soraya_S%C3%A1enz_de_Santamar%C3%ADa'],
    ['Teresa', 'Ribera Rodríguez',                             'F', '1969-05-19', 1, 'https://es.wikipedia.org/wiki/Teresa_Ribera'],
    ['Tomás', 'de la Quadra-Salcedo Fernández del Castillo',   'M', '1946-01-02', 1, 'https://es.wikipedia.org/wiki/Tom%C3%A1s_de_la_Quadra-Salcedo'],
    ['Trinidad', 'Jiménez García-Herrera',                     'F', '1962-06-04', 1, 'https://es.wikipedia.org/wiki/Trinidad_Jim%C3%A9nez'],
    ['Valeriano', 'Gómez Sánchez',                             'M', '1957-12-15', 1, 'https://es.wikipedia.org/wiki/Valeriano_G%C3%B3mez'],
    ['Vicente', 'Albero Silla',                                'M', '1944-12-06', 1, 'https://es.wikipedia.org/wiki/Vicente_Albero'],
    ['Virgilio', 'Zapatero Gómez',                             'M', '1946-06-26', 1, 'https://es.wikipedia.org/wiki/Virgilio_Zapatero'],
    ['Yolanda', 'Díaz Pérez',                                  'F', '1971-05-06', 1, 'https://es.wikipedia.org/wiki/Yolanda_D%C3%ADaz'],
]
# fmt: on


def apply_migration(apps, schema_editor):
    Person = apps.get_model("people", "Person")
    BirthSource = apps.get_model("people", "BirthSource")

    for row in DATA:
        full_name = clean_spanish_name(f"{row[0]} {row[1]}")
        person = Person(
            full_name=full_name,
            id_name=people_id_from_name(full_name),
            first_name=clean_spanish_name(row[0]),
            last_name=clean_spanish_name(row[1]),
            birth_date=row[3],
            genre=row[2],
        )
        person.save()
        birthsource = BirthSource(
            person=person,
            name=urlparse(row[5]).netloc,
            url=row[5],
            is_exact=row[4],
            date=row[3],
        )
        birthsource.save()


def revert_migration(apps, schema_editor):
    Person = apps.get_model("people", "Person")
    BirthSource = apps.get_model("people", "BirthSource")
    Person.objects.all().delete()
    BirthSource.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration),
    ]
