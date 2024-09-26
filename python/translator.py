# Description: This script translates Braille to English or English to Braille.
# Use python3 translator.py -h to see help on usage

import argparse
import textwrap


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.
    RETURNS: argparse.Namespace - The parsed arguments
    """
    parser = argparse.ArgumentParser(description="Translate Braille to English or vice versa.")
    parser.add_argument('input', nargs='+', help="Input string to translate")
    return parser.parse_args()


def get_input_type(input_string: str) -> str:
    """
    Determine the type of input string (Braille or text).
    INPUTS: input_string: str - The input string to check
    RETURNS: str - 'braille' if the input is Braille, 'text' if the input is English
    """
    if all(char in '.O' for char in input_string):
        return 'braille'
    elif all(char.isalnum() or char in ' ,.?!;()-' for char in input_string):
        return 'text'
    else:
        raise ValueError(f"Input string '{input_string}' is not a valid Braille or text string.")


def translate_braille_to_text(braille_string: str, braille_mapping: dict, number_map: dict) -> str:
    """
    Translate a given Braille string to English.
    INPUTS: braille_string: str - The Braille string to translate
            mapping: dict - A dictionary mapping Braille characters to English
            numbers: dict - A dictionary mapping Braille numbers to English
    RETURNS: str - The English translation of the input Braille string
    
    """
    translated = ''
    braille_chunks = textwrap.wrap(braille_string, 6)
    
    capital, number = False, False
    for chunk in braille_chunks:
        if chunk not in braille_mapping:
            raise ValueError(f"Invalid Braille character '{chunk}'")
        if braille_mapping[chunk] == 'capital':
            capital = True
        elif braille_mapping[chunk] == 'number':
            number = True
            continue
        elif braille_mapping[chunk] == 'decimal':
            continue
        else:
            if braille_mapping[chunk] == ' ': number = False # Stop translating numbers if space
            if number:
                translated += number_map[chunk]
            elif capital:
                translated += braille_mapping[chunk].upper() if capital else braille_mapping[chunk]
                capital = False
            else:
                translated += braille_mapping[chunk]
    return translated


def translate_text_to_braille(text_string: str, mapping: dict, number_map: dict) -> str:
    """
    Translate a given text string to Braille.
    INPUTS: text_string: str - The text string to translate
            mapping: dict - A dictionary mapping English characters to Braille
            number_map: dict - A dictionary mapping numbers to Braille
    RETURNS: str - The Braille translation of the input text string
    """
    translated = ''
    digit_active = False
    for char in text_string:
        if not char.isdigit():
            digit_active = False
        if char.isdigit():
            if digit_active:
                translated += number_map[char]
            else:
                translated += mapping['number'] + number_map[char]
                digit_active = True
        elif char.isupper():
            translated += mapping['capital'] + mapping[char.lower()]
        elif char == '.':
            translated += mapping['decimal']
        else:
            translated += mapping[char]
    return translated


def main(args):
    TEXT_TO_BRAILLE = {
        'a': 'O.....', 'b': 'O.O...', 'c': 'OO....', 'd': 'OO.O..', 'e': 'O..O..',
        'f': 'OOO...', 'g': 'OOOO..', 'h': 'O.OO..', 'i': '.OO...', 'j': '.OOO..',
        'k': 'O...O.', 'l': 'O.O.O.', 'm': 'OO..O.', 'n': 'OO.OO.', 'o': 'O..OO.',
        'p': 'OOO.O.', 'q': 'OOOOO.', 'r': 'O.OOO.', 's': '.OO.O.', 't': '.OOOO.',
        'u': 'O...OO', 'v': 'O.O.OO', 'w': '.OOO.O', 'x': 'OO..OO', 'y': 'OO.OOO',
        'z': 'O..OOO',  ',': '..O...', ';': '..O.O.', ':': '..OO..', '.': '..OO.O',
        '!': '..OOO.', '?': '..O..O', '(': '..O.OO', ')': '..O.OO', '/': '.O.O..',
        '-': '....O.', ' ': '......', 'capital': '.....O', 'number': '.O.OOO', 'decimal': '.O...O'
    }

    NUMBER_TO_BRAILLE = {
        '1': 'O.....', '2': 'O.O...', '3': 'OO....', '4': 'OO.O..',
        '5': 'O..O..', '6': 'OOO...', '7': 'OOOO..', '8': 'O.OO..', '9': '.OO...',
        'O': '.OOO..',
    }

    BRAILLE_TO_TEXT = {v: k for k, v in TEXT_TO_BRAILLE.items()}
    BRAILLE_TO_NUMBER = {v: k for k, v in NUMBER_TO_BRAILLE.items()}

    input_string = ' '.join(args.input)
    translated = ''

    try:
        input_type = get_input_type(input_string)

        if input_type == 'braille':
            translated = translate_braille_to_text(input_string, BRAILLE_TO_TEXT, BRAILLE_TO_NUMBER)
        else:
            translated = translate_text_to_braille(input_string, TEXT_TO_BRAILLE, NUMBER_TO_BRAILLE)
    except ValueError as e:
        print(f"Error occured while translating input: {e}")

    print(translated)

if __name__ == '__main__':
    args = parse_args()
    main(args)
