#!/usr/bin/env python3

import credstash
import re
from pathlib import Path
import os

def replace_secrets(line):
    output = line
    for secret_placeholder in re.findall('__.*?__', line):
        secret_name = secret_placeholder.strip("_").lstrip("_")
        try:
            secret_value = credstash.getSecret(secret_name)
        except Exception as e:
            print("Unable to find the requested credential '%s'" % secret_name)
            raise(e)
        output = output.replace(secret_placeholder, secret_value)
    return output

def main():
    script_path = Path(os.path.realpath(__file__)).parent
    config_path = script_path.joinpath('config')
    template_file = script_path.joinpath('local_template.json')
    output_file = config_path.joinpath('local.json')

    with template_file.open() as f:
        template = f.readlines()

    completed_file = []
    for line in template:
        completed_file.append(replace_secrets(line))

    with output_file.open('w') as f:
        f.writelines(completed_file)


if __name__ == '__main__':
    main()
