import sys
import yaml
import random

# Accessing the first argument (index 1 as 0 is the script name)
argument = int(sys.argv[1])
potentialItems = list(range(6351, 6351 + argument))

with open('./includes/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

random.shuffle(potentialItems)
config['PotentialNumbers'] = potentialItems

class CustomDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(CustomDumper, self).increase_indent(flow=True, indentless=indentless)

with open('./includes/config.yaml', 'w') as f:
  # Dump the data to the file as YAML
  yaml.dump(config, f, Dumper=CustomDumper, default_flow_style=None)