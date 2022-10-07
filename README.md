# typescript_cleaner.py

A simple utility to clean shell typescript files by removing terminal escape sequences and (optionally) applying backspace characters.

Typescript files (created using the `script` command) contain escape sequences for backspaces, font colors, tab completion, etc., which make them difficult to read (without using `cat`) or grep through. This utility aims to fix that. Just provide one or more typescript filepaths as an argument, and the script will automatically remove escape sequences (optionally leaving BELL and/or backspace characters) and output the result to a matching file with `_cleaned` appended to the filename. Files that contain `_cleaned` as a suffix as assumed to have already been cleaned and will be skipped.

Requires Python 3.6+ due to use of type hinting.


## Usage

---
    python3 typescript_cleaner.py [-h] [--keep_backspace] [--keep_bell] [filepaths ...]

    Cleans shell typescript files by removing terminal escape sequences and applying backspace characters

    positional arguments:
      filepaths         Paths to typescript files (i.e., logs created using the "script" command)

    optional arguments:
      -h, --help        show this help message and exit
      --keep_backspace  Keep BACKSPACE characters; useful for identifying things typed accidentally (like passwords)
      --keep_bell       Keep BELL characters; useful for identifying tab completion


## Examples

---
    # Create a typescript
    script -f ssh_session_$(date +%F).log
    
    # Remove all escape sequences and metacharacters
    python3 typescript_cleaner.py ssh_session_2022-09-24.log
    
    # Remove all escape sequences and metacharacters and files in and below the 'logs' directory
    python3 typescript_cleaner.py ./logs
    
    # Keep BELL characters (to show tab completion)
    python3 typescript_cleaner.py -keep_bell ssh_session_2022-09-24.log
    
    # Keep BACKSPACE characters
    python3 typescript_cleaner.py -keep_backspace ssh_session_2022-09-24.log
    
    # Keep BACKSPACE and BELL characters
    python3 typescript_cleaner.py -keep_backspace -keep_bell ssh_session_2022-09-24.log