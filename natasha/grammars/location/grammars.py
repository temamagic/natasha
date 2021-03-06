# coding: utf-8
from __future__ import unicode_literals

from enum import Enum
from yargy.labels import (
    gram,
    gram_not,
    gram_not_in,
    dictionary,
    is_capitalized,
    gnc_match,
    length_eq,
    eq,
    gte,
    or_,
    in_,
)
from yargy.parser import OR
from yargy.normalization import NormalizationType
from natasha.grammars.location.interpretation import LocationObject, AddressObject


FEDERAL_DISTRICT_DICTIONARY = {
    'центральный',
    'северо-западный',
    'южный',
    'северо-кавказский',
    'приволжский',
    'уральский',
    'сибирский',
    'дальневосточный',
}

REGION_TYPE_DICTIONARY = {
    'край',
    'район',
    'область',
    'губерния',
    'уезд',
}

COMPLEX_OBJECT_PREFIX_DICTIONARY = {
    'северный',
    'северо-западный',
    'северо-восточный',
    'южный',
    'юго-западный',
    'юго-восточный',
    'западный',
    'восточный',
    'верхний',
    'вышний',
    'нижний',
    'великий',
    'дальний',
}

PARTIAL_OBJECT_PREFIX_DICTIONARY = {
    'север',
    'северо-восток',
    'северо-запад',
    'юг',
    'юго-восток',
    'юго-запад',
    'запад',
    'восток',
}


class Location(Enum):

    FederalDistrict = [
        {
            'labels': [
                gram('ADJF'),
                dictionary(FEDERAL_DISTRICT_DICTIONARY),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gnc_match(-1, solve_disambiguation=True),
                dictionary({'федеральный', }),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Descriptor,
            },
        },
        {
            'labels': [
                gnc_match(-1, solve_disambiguation=True),
                dictionary({'округ', }),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Descriptor,
            },
        },
    ]

    FederalDistrictAbbr = [
        {
            'labels': [
                gram('ADJF'),
                dictionary(FEDERAL_DISTRICT_DICTIONARY),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                eq('ФО'),
            ],
            'interpretation': {
                'attribute': LocationObject.Attributes.Descriptor,
            },
        },
    ]

    AutonomousDistrict = [
        {
            'labels': [
                gram('ADJF'),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gnc_match(-1, solve_disambiguation=True),
                dictionary({'автономный', }),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Descriptor,
            },
        },
        {
            'labels': [
                gnc_match(-1, solve_disambiguation=True),
                dictionary({'округ', }),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Descriptor,
            },
        },
    ]

    AutonomousDistrictAbbr = [
        {
            'labels': [
                gram('ADJF'),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                eq('АО'),
            ],
            'interpretation': {
                'attribute': LocationObject.Attributes.Descriptor,
            },
        },
    ]

    Region = [
        {
            'labels': [
                gram('ADJF'),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                dictionary(REGION_TYPE_DICTIONARY),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Descriptor,
            },
        },
    ]

    ComplexObject = [
        {
            'labels': [
                gram('ADJF'),
                dictionary(COMPLEX_OBJECT_PREFIX_DICTIONARY),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gram('NOUN'),
                gram('Geox'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
    ]

    PartialObject = [
        {
            'labels': [
                gram('NOUN'),
                dictionary(PARTIAL_OBJECT_PREFIX_DICTIONARY),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gram('NOUN'),
                gram('Geox'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
    ]

    # Донецкая народная республика / Российская Федерация
    AdjfFederation = [
        {
            'labels': [
                gram('ADJF'),
                is_capitalized(True),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gram('ADJF'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'optional': True,
            'repeatable': True,
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gnc_match(0, solve_disambiguation=True),
                dictionary({
                    'федерация',
                    'республика',
                    'империя',
                }),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Descriptor,
            },
        },
    ]

    # Соединенные Штаты / Соединенные Штаты Америки
    AdjxFederation = [
        {
            'labels': [
                gram('Adjx'),
                is_capitalized(True),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gram('Adjx'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'optional': True,
            'repeatable': True,
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gnc_match(0, solve_disambiguation=True),
                dictionary({
                    'штат',
                    'эмират',
                }),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gram('gent'),
            ],
            'optional': True,
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        }
    ]

    Object = [
        {
            'labels': [
                is_capitalized(True),
                gram('Geox'),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
    ]

STREET_DESCRIPTOR_DICTIONARY = {
    'улица',
    'площадь',
    'проспект',
    'проезд',
    'бульвар',
    'набережная',
    'шоссе',
    'вал',
    'аллея',
    'переулок',
    'тупик',
    'тракт',
    'дорога',
}

SHORT_STREET_DESCRIPTOR_RULE = [
    {
        'labels': {
            or_((
                dictionary({
                    'ул', # улица
                    'пр', # проспект / проезд?
                    'проспа', # проспект
                    'пр-том', # see kmike/github issue #88
                    'площадь', # площадь,
                    'пр-кт', # проспект
                    'пр-далее', # проезд
                    'б-литр', # бульвар, #88
                    'б-р', # бульвар
                    'бул', # бульвар
                    'наб', # набережная
                    'ш', # шоссе
                    'тупой', # тупик, #88
                    'дора', # дорога, #88
                }),
                in_({
                    'пер', # переулок, #88,
                    'н', # набережная
                }),
            )),
        },
        'normalization': NormalizationType.Original,
        'interpretation': {
            'attribute': AddressObject.Attributes.Street_Descriptor,
        },
    },
    {
        'labels': [
            eq('.'),
        ],
        'optional': True,
        'normalization': NormalizationType.Original,
    }
]

NUMERIC_STREET_PART_RULE = [ # 1-я, 10-й, 100500-ой и т.д.
    {
        'labels': [
            gram('INT'),
            gte(1),
        ],
        'normalization': NormalizationType.Original,
        'interpretation': {
            'attribute': AddressObject.Attributes.Street_Name,
        },
    },
    {
        'labels': [
            eq('-'),
        ],
        'normalization': NormalizationType.Original,
        'interpretation': {
            'attribute': AddressObject.Attributes.Street_Name,
        },
    },
    {
        'labels': [
            gram_not_in({
                'PUNCT',
                'QUOTE',
                'LATN',
                'NUMBER',
                'PHONE',
                'EMAIL',
                'RANGE',
                'END-OF-LINE',
            }),
        ],
        'normalization': NormalizationType.Original,
        'interpretation': {
            'attribute': AddressObject.Attributes.Street_Name,
        },
    }
]

NUMERIC_STREET_PART_WITHOUT_SUFFIX_RULE = NUMERIC_STREET_PART_RULE[:1]

HOUSE_NUMBER_FULL_GRAMMAR = [ # дом 1, дом 2 и т.д.
    {
        'labels': [
            dictionary({
                'дом',
            }),
        ],
        'normalization': NormalizationType.Inflected,
        'interpretation': {
            'attribute': AddressObject.Attributes.House_Number_Descriptor,
        },
    },
    {
        'labels': [
            gram('INT'),
            gte(1),
        ],
        'interpretation': {
            'attribute': AddressObject.Attributes.House_Number,
        },
    }
]

HOUSE_NUMBER_SHORT_GRAMMAR = [
    {
        'labels': [
            dictionary({
                'далее', # д. #88
            })
        ],
        'normalization': NormalizationType.Original,
        'interpretation': {
            'attribute': AddressObject.Attributes.House_Number_Descriptor,
        },
    },
    {
        'labels': [
            eq('.'),
        ],
        'optional': True,
        'normalization': NormalizationType.Original,
    },
    HOUSE_NUMBER_FULL_GRAMMAR[-1],
]

HOUSE_NUMBER_GRAMMAR = [
    OR(
        OR(
            HOUSE_NUMBER_SHORT_GRAMMAR,
            HOUSE_NUMBER_FULL_GRAMMAR,
        ),
        HOUSE_NUMBER_FULL_GRAMMAR[-1:]
    )
]

HOUSE_LETTER_FULL_GRAMMAR = [
    {
        'labels': [
            dictionary({
                'литер',
            }),
        ],
    },
    {
        'labels': [
            is_capitalized(True),
            length_eq(1),
        ],
        'normalization': NormalizationType.Original,
        'interpretation': {
            'attribute': AddressObject.Attributes.House_Number_Letter
        },
    }
]


HOUSE_LETTER_SHORT_GRAMMAR = [
    {
        'labels': [
            or_((
                eq('лит'), # литер
                eq('л'),
            )),
        ],
    },
    {
        'labels': [
            eq('.'),
        ],
        'optional': True,
        'normalization': NormalizationType.Original,
    },
    HOUSE_LETTER_FULL_GRAMMAR[-1],
]

HOUSE_LETTER_ONLY_LETTER_GRAMMAR = [
    HOUSE_LETTER_FULL_GRAMMAR[-1],
]

HOUSE_LETTER_GRAMMAR = [
    OR(
        OR(
            HOUSE_LETTER_FULL_GRAMMAR,
            HOUSE_LETTER_SHORT_GRAMMAR,
        ),
        HOUSE_LETTER_ONLY_LETTER_GRAMMAR,
    )
]

OPTIONAL_COMMA_GRAMMAR = [
    {
        'labels': [
            eq(','),
        ],
        'optional': True,
        'normalization': NormalizationType.Original,
    }
]

class Address(Enum):

    # Садовая улица
    AdjFull = [
        {
            'labels': [
                gram('ADJF'),
                gram_not('Abbr'),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': AddressObject.Attributes.Street_Name,
            },
        },
        {
            'labels': [
                gram('ADJF'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'repeatable': True,
            'optional': True,
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': AddressObject.Attributes.Street_Name,
            },
        },
        {
            'labels': [
                dictionary(STREET_DESCRIPTOR_DICTIONARY),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': AddressObject.Attributes.Street_Descriptor,
            },
        },
    ]

    # улица Садовая
    AdjFullReversed = [
        {
            'labels': [
                dictionary(STREET_DESCRIPTOR_DICTIONARY),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': AddressObject.Attributes.Street_Descriptor,
            },
        },
        {
            'labels': [
                gram('ADJF'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'repeatable': True,
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': AddressObject.Attributes.Street_Name,
            },
        },
    ]

    # ул. Садовая
    AdjShort = SHORT_STREET_DESCRIPTOR_RULE + AdjFull[:2]

    # Садовая ул.
    AdjShortReversed = AdjFull[:2] + SHORT_STREET_DESCRIPTOR_RULE

    # улица Красных Десантников
    AdjNounFull = [AdjFullReversed[0]] + AdjFull[:2] + [
        {
            'labels': [
                gram('gent'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'repeatable': True,
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': AddressObject.Attributes.Street_Name,
            },
        }
    ]

    # ул. Красных Десантников
    AdjNounShort = AdjShort + [
        AdjNounFull[-1]
    ]

    # улица Карла Маркса
    GentFullReversed = [
        AdjFullReversed[0],
        {
            'labels': [
                gram('gent'),
                gram_not('Abbr'),
            ],
            'normalization': NormalizationType.Original,
            'interpretation': {
                'attribute': AddressObject.Attributes.Street_Name,
            },
        },
        {
            'labels': [
                gram('gent'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True)
            ],
            'optional': True,
            'repeatable': True,
            'normalization': NormalizationType.Original,
            'interpretation': {
                'attribute': AddressObject.Attributes.Street_Name,
            },
        },
    ]

    # улица К. Маркса
    GentFullReversedWithShortcut = [
        GentFullReversed[0],
        {
            'labels': [
                gram('Abbr'),
            ],
            'normalization': NormalizationType.Original,
            'interpretation': {
                'attribute': AddressObject.Attributes.Street_Name,
            },
        },
        {
            'labels': [
                eq('.'),
            ],
            'normalization': NormalizationType.Original,
        },
    ] + GentFullReversed[1:]

    # улица В. В. Ленина
    GentFullReversedWithExtendedShortcut = GentFullReversedWithShortcut[:3] + GentFullReversedWithShortcut[1:3] + GentFullReversedWithShortcut[3:]

    # пр. Маршала жукова
    GentShortReversed = SHORT_STREET_DESCRIPTOR_RULE + GentFullReversed[1:]

    # пр. К. Маркса
    GentShortReversedWithShortcut = SHORT_STREET_DESCRIPTOR_RULE + GentFullReversedWithShortcut[1:]

    # пл. В. В. Ленина
    GentShortReversedWithExtendedShortcut = SHORT_STREET_DESCRIPTOR_RULE + GentFullReversedWithExtendedShortcut[1:]

    # Николая Ершова улица
    GentFull = GentFullReversed[1:] + GentFullReversed[:1]

    # Обуховской Обороны пр-кт
    GentShort = GentShortReversed[2:] + SHORT_STREET_DESCRIPTOR_RULE

    # 1-я новорублевская улица
    AdjFullWithNumericPart = NUMERIC_STREET_PART_RULE + AdjFull

    # улица 1-я новорублевская
    AdjFullReversedWithNumericPart = AdjFullReversed[:1] + AdjFullWithNumericPart[:-1]

    # 1-я новорублевская ул.
    AdjShortWithNumericPart = AdjFullWithNumericPart[:-1] + SHORT_STREET_DESCRIPTOR_RULE

    # ул. 1-я промышленная
    AdjShortReversedWithNumericPart = SHORT_STREET_DESCRIPTOR_RULE + AdjFullWithNumericPart[:-1]

    # проспект 50 лет октября
    GentFullReversedWithNumericPrefix = GentFullReversed[:1] + NUMERIC_STREET_PART_WITHOUT_SUFFIX_RULE + GentFullReversed[1:2] + GentFullReversed[1:]

    # пр-т. 50 лет советской власти
    GentShortReversedWithNumericPrefix = GentShortReversed[:2] + NUMERIC_STREET_PART_WITHOUT_SUFFIX_RULE + GentFullReversed[1:2] + GentFullReversed[1:]

    # 2-ой проезд Перова Поля
    GentNumericSplittedByFullDescriptor = NUMERIC_STREET_PART_RULE + GentFullReversed

    # 7-я ул. текстильщиков
    GentNumericSplittedByShortDescriptor = NUMERIC_STREET_PART_RULE + GentShortReversed

    '''
    Street names with house numbers
    '''

    # Зеленая улица, дом 7
    AdjFullWithHn = AdjFull + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR

    # улица Зеленая, дом 7
    AdjFullReversedWithHn = AdjFullReversed + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR

    # ул. Нижняя Красносельская дом 7
    AdjShortWithHn = AdjShort + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR

    # Настасьинский пер., дом 2
    AdjShortReversedWithHn = AdjShortReversed + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR

    # улица Красной Гвардии, дом 2
    AdjNounFullWithHn = AdjNounFull + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR

    # ул. Брянской пролетарской дивизии дом 2
    AdjNounShortWithHn = AdjNounShort + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR

    # Николая Ершова улица дом 1
    GentFullWithHn = GentFull + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR

    # улица Карла Маркса дом 1
    GentFullReversedWithHn = GentFullReversed + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR

    # улица К. Маркса, дом 1
    GentFullReversedWithShortcutWithHn = GentFullReversedWithShortcut + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR

    # улица В. И. Ленина, дом 1
    GentFullReversedWithExtendedShortcutWithHn = GentFullReversedWithExtendedShortcut + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR

    # Обуховской Обороны пр-кт дом 1
    GentShortWithHn = GentShort + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR

    # пр-кт Обуховской Обороны дом 1
    GentShortReversedWithHn = GentShortReversed + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR

    # ул. К. Маркса, дом 1
    GentShortReversedWithShortcutWithHn = GentShortReversedWithShortcut + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR

    # ул. В. И. Ленина, дом 1
    GentShortReversedWithExtendedShortcutWithHn = GentShortReversedWithExtendedShortcut + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR

    # 1-я новорублевская улица дом 1
    AdjFullWithNumericPartWithHn = AdjFullWithNumericPart + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR

    # улица 1-я новорублевская, дом 1
    AdjFullReversedWithNumericPartWithHn = AdjFullReversedWithNumericPart + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR

    # 1-я новорублевская ул. дом 1
    AdjShortWithNumericPartWithHn = AdjShortWithNumericPart + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR

    # ул. 1-я промышленная, дом 1
    AdjShortReversedWithNumericPartWithHn = AdjShortReversedWithNumericPart + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR

    # проспект 50 лет октября, дом 1
    GentFullReversedWithNumericPrefixWithHn = GentFullReversedWithNumericPrefix + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR

    # пр-т. 50 лет советской власти, дом 1
    GentShortReversedWithNumericPrefixWithHn = GentShortReversedWithNumericPrefix + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR

    # 2-ой проезд Перова Поля, дом 1
    GentNumericSplittedByFullDescriptorWithHn = GentNumericSplittedByFullDescriptor + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR

    # 7-я ул. текстильщиков, дом 1
    GentNumericSplittedByShortDescriptorWithHn = GentNumericSplittedByShortDescriptor + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR

    '''
    Street names with house numbers and letters
    '''

    # Зеленая улица, дом 7
    AdjFullWithHnAndLetter = AdjFull + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + HOUSE_LETTER_GRAMMAR

    # улица Зеленая, дом 7
    AdjFullReversedWithHnAndLetter = AdjFullReversed + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + HOUSE_LETTER_GRAMMAR

    # ул. Нижняя Красносельская дом 7
    AdjShortWithHnAndLetter = AdjShort + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + HOUSE_LETTER_GRAMMAR

    # Настасьинский пер., дом 2
    AdjShortReversedWithHnAndLetter = AdjShortReversed + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + HOUSE_LETTER_GRAMMAR

    # улица Красной Гвардии, дом 2
    AdjNounFullWithHnAndLetter = AdjNounFull + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + HOUSE_LETTER_GRAMMAR

    # ул. Брянской пролетарской дивизии дом 2
    AdjNounShortWithHnAndLetter = AdjNounShort + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + HOUSE_LETTER_GRAMMAR

    # Николая Ершова улица дом 1
    GentFullWithHnAndLetter = GentFull + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + HOUSE_LETTER_GRAMMAR

    # улица Карла Маркса дом 1
    GentFullReversedWithHnAndLetter = GentFullReversed + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + HOUSE_LETTER_GRAMMAR

    # улица К. Маркса, дом 1
    GentFullReversedWithShortcutWithHnAndLetter = GentFullReversedWithShortcut + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + HOUSE_LETTER_GRAMMAR

    # улица В. И. Ленина, дом 1
    GentFullReversedWithExtendedShortcutWithHnAndLetter = GentFullReversedWithExtendedShortcut + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + HOUSE_LETTER_GRAMMAR

    # Обуховской Обороны пр-кт дом 1
    GentShortWithHnAndLetter = GentShort + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + HOUSE_LETTER_GRAMMAR

    # пр-кт Обуховской Обороны дом 1
    GentShortReversedWithHnAndLetter = GentShortReversed + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + HOUSE_LETTER_GRAMMAR

    # ул. К. Маркса, дом 1
    GentShortReversedWithShortcutWithHnAndLetter = GentShortReversedWithShortcut + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + HOUSE_LETTER_GRAMMAR


    # ул. В. И. Ленина, дом 1
    GentShortReversedWithExtendedShortcutWithHnAndLetter = GentShortReversedWithExtendedShortcut + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + HOUSE_LETTER_GRAMMAR

    # 1-я новорублевская улица дом 1
    AdjFullWithNumericPartWithHnAndLetter = AdjFullWithNumericPart + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + HOUSE_LETTER_GRAMMAR

    # улица 1-я новорублевская, дом 1
    AdjFullReversedWithNumericPartWithHnAndLetter = AdjFullReversedWithNumericPart + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + HOUSE_LETTER_GRAMMAR

    # 1-я новорублевская ул. дом 1
    AdjShortWithNumericPartWithHnAndLetter = AdjShortWithNumericPart + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + HOUSE_LETTER_GRAMMAR

    # ул. 1-я промышленная, дом 1
    AdjShortReversedWithNumericPartWithHnAndLetter = AdjShortReversedWithNumericPart + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + HOUSE_LETTER_GRAMMAR

    # проспект 50 лет октября, дом 1
    GentFullReversedWithNumericPrefixWithHnAndLetter = GentFullReversedWithNumericPrefix + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + HOUSE_LETTER_GRAMMAR

    # пр-т. 50 лет советской власти, дом 1
    GentShortReversedWithNumericPrefixWithHnAndLetter = GentShortReversedWithNumericPrefix + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + HOUSE_LETTER_GRAMMAR

    # 2-ой проезд Перова Поля, дом 1
    GentNumericSplittedByFullDescriptorWithHnAndLetter = GentNumericSplittedByFullDescriptor + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + HOUSE_LETTER_GRAMMAR

    # 7-я ул. текстильщиков, дом 1
    GentNumericSplittedByShortDescriptorWithHnAndLetter = GentNumericSplittedByShortDescriptor + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + HOUSE_LETTER_GRAMMAR

