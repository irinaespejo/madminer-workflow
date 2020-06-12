#!/usr/bin/python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import yaml
from ast import literal_eval
from madminer import MadMiner
from pathlib import Path


##########################
#### Global variables ####
##########################

project_dir = Path(__file__).parent.parent

data_dir = str(project_dir.joinpath('data'))


##########################
#### Argument parsing ####
##########################

input_file = sys.argv[1]

with open(input_file, 'r') as f:
    spec = yaml.safe_load(f)


###########################
### Miner configuration ###
###########################

miner = MadMiner()

# Add parameters
for parameter in spec['parameters']:
    param_range = parameter.pop('parameter_range')
    param_range = literal_eval(param_range)
    param_range = [float(val) for val in param_range]

    miner.add_parameter(**parameter, parameter_range=tuple(param_range))

# Add benchmarks
for benchmark in spec['benchmarks']:
    param_values = {}

    for i, _ in enumerate(spec['parameters']):
        name = benchmark[f'parameter_name_{i+1}']
        value = benchmark[f'value_{i+1}']
        param_values[name] = value

    miner.add_benchmark(param_values, benchmark['name'])


##########################
#### Morphing setting ####
##########################

miner.set_morphing(**spec['set_morphing'])


##########################
### Save configuration ###
##########################

os.makedirs(data_dir, exist_ok=True)

config_file_name = 'madminer_config.h5'
config_file_path = data_dir + '/' + config_file_name

miner.save(config_file_path)
