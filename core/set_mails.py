import argparse
import json
import random
import string
import math

class NameKeyGenerator:
    def __init__(self, text_file=None, url=None):
        self.text_file = text_file
        self.url = url

    def generate_key(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=20))

    def generate_name_key_data(self):
        with open(self.text_file, "r") as name_file:
            names = name_file.readlines()

        num_names = len(names)
        num_files = math.ceil(num_names / 50)

        name_key_data = {}
        for name in names:
            name = name.strip()
            key = self.generate_key()
            name_key_data[name] = str(self.url)+str(key)

        output_name = self.text_file.replace(".txt", ".json")
        with open(output_name, "w") as output:
            json.dump(name_key_data, output, indent=4)
            output.write('\n')
        return name_key_data