#!/usr/bin/env python3

"""
Simple rofi script for showing all passwords in a
pass password-store and copying it to the clipboard
"""

# .password-store directory
password_store = '.password-store'

# Theme (see rofi-theme-selector)
theme = 'android_notification'

# prompt
prompt = 'pass: '

from pathlib import Path
import subprocess

def list_files():
    home = Path.home()
    pass_dir = home / password_store

    # remove base path in rofi list, but keep the paths
    # inside the password-store directory
    rm = str(pass_dir) + '/'

    files = []
    for file in pass_dir.rglob('*.gpg'):
        files.append(str(file).replace(rm, '').replace('.gpg', ''))

    return sorted(files)

def main():
    keys = list_files()

    proc = subprocess.run(['rofi', '-dmenu', '-p', prompt,
                            '-theme', theme],
                            input='\n'.join(keys),
                            encoding='utf-8',
                            stdout=subprocess.PIPE)

    if proc.returncode == 1:    # none selected
        exit()

    key = proc.stdout.strip()
    if key in keys:
        # Copy the password to the clipboard
        proc = subprocess.run(['pass', '-c', str(key)],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)

if __name__ == '__main__':
    main()
