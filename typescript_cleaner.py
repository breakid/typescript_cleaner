#!/usr/bin/env python3
import os
import re
import sys
from argparse import ArgumentParser

# Match character sequence between the ESC character (\x1b) and the BELL character (\x07)
# Source: https://superuser.com/questions/236930/how-to-clean-up-output-of-linux-script-command (converted from perl to Python regex)
META_CHAR_PATT = re.compile('\x1b([^\[\]]|\[.*?[a-zA-Z]|\].*?\x07)')


def clean_string(input_string: str, keep_backspace: bool=False, keep_bell: bool=False) -> str:
    # Remove terminal escape sequences
    input_string = META_CHAR_PATT.sub('', input_string)
    
    # Source: https://stackoverflow.com/questions/36576216/apply-control-characters-to-a-string-python
    cursor_position: int = 0
    displayed_string: list = []
    
    # Apply any backspace sequences, otherwise output the original character
    character: str
    for character in input_string:
        if character != '\x08' or keep_backspace:
            # Add the character to the string
            displayed_string[cursor_position:cursor_position+1] = character
            
            # Move the cursor forward
            cursor_position += 1
        else:
            # Remove backspace
            
            # Move the cursor backward
            cursor_position -= 1
            
            # Ignore undisplayed BELL characters when moving the cursor backwards
            while input_string[cursor_position] == '\x07':
                cursor_position -= 1
    
    # Remove BELL characters
    if not keep_bell:
        displayed_string = [c for c in displayed_string if c != '\x07']
    
    return ''.join(displayed_string[:cursor_position])


def clean_file(input_filepath: str, keep_backspace: bool=False, keep_bell: bool=False) -> None:
    print(f'[*] Cleaning: { input_filepath }...')
    
    output_filepath: str
    ext: str
    output_filepath, ext = os.path.splitext(input_filepath)
    
    # Prevent re-cleaning an already cleaned file
    if output_filepath.endswith('_cleaned'):
        return
    
    output_filepath = f'{ output_filepath }_cleaned{ ext }'
    
    # Read data without specifying an encoding
    with open(input_filepath, 'r') as in_file:
        # Force the output data to be UTF-8 encoded
        # NOTE: This should prevent exceptions from decoding errors while silently dropping un-decodable characters
        with open(output_filepath, 'w', encoding='utf-8') as out_file:
            line: str
            for line in in_file.readlines():
                out_file.write(clean_string(line, keep_backspace, keep_bell))
    
    print(f'[+] Done! Output written to: { output_filepath }')


if __name__ == '__main__':
    parser = ArgumentParser(description='Cleans shell typescript files by removing terminal escape sequences and (optionally) applying backspace characters')
    parser.add_argument('--keep_backspace', action="store_true", dest='keep_backspace', help='Keep BACKSPACE characters; useful for identifying things typed accidentally (like passwords)')
    parser.add_argument('--keep_bell', action="store_true", dest='keep_bell', help='Keep BELL characters; useful for identifying tab completion')
    parser.add_argument('filepaths', nargs='*', help='Paths to typescript files (i.e., logs created using the "script" command)')
    args = parser.parse_args()
    
    if len(args.filepaths) > 0:
        input_filepath: str
        for input_filepath in args.filepaths:
            
            if os.path.isdir(input_filepath):
                for root, dirs, files in os.walk(input_filepath):
                    for name in files:
                        clean_file(os.path.join(root, name), args.keep_backspace, args.keep_bell)
            elif os.path.isfile(input_filepath):
                clean_file(input_filepath, args.keep_backspace, args.keep_bell)
            else:
                print(f'[-] ERROR: "{ input_filepath }" does not exist')
    else:
        parser.print_help(sys.stderr)
