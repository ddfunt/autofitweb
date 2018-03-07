import os
from math import sqrt
from autofit.IO.paths import Paths
import subprocess
from collections import OrderedDict

path = Paths.spcat()
names = OrderedDict([('A', '10000'),
                     ('B', '20000'),
                     ('C', '30000'),
                     ('delta_J', '200'),
                     ('delta_JK', '1100'),
                     ('delta_K', '2000'),
                     ('d_J', '40100'),
                     ('d_K', '41000'),
                     ('spin', 'spin')])

dipole_names = OrderedDict([('mu_A', '001'),
                            ('mu_B', '002'),
                            ('mu_C', '003'),])

limiters = {'linewidth': 1,
              'temp': 300,
              'maxJ': 100}

def calc_Q(constants, constraints):

    A = float(constants['A'])
    B = float(constants['B'])
    C = float(constants['C'])
    sigma = 1
    return int(5.314e6/sigma * sqrt(constraints['temp']**3 / (A * B * C)))


def int_writer(freq, dipoles, constants, constraints, J_min="00", inten="-10.0"):
    '''generates SPCAT INT input file'''

    Q_rot = calc_Q(constants, constraints)


    input_file = "Molecule \n"
    input_file += "0  91  %s  %s  %s  %s  %s %s  %s\n"%(Q_rot, J_min, constraints['maxJ'], inten, inten, freq, constraints['temp'])
    for name, value in dipoles.items():
        id = dipole_names[name]
        input_file += "{0: >4} {1: >6.3f} \n".format(id, float(value))

    with open(os.path.join(path, 'default.int'), "w") as f:
        f.write(input_file)

def var_writer(constants):
    '''generates SPCAT var file'''
    header = "anisole                                         Wed Mar Thu Jun 03 17:45:45 2010\n  99  8000   51    0    0.0000E+000    1.0000E+005    1.0000E+000 1.0000000000\na  %i  1  0  99  0  1  1  1  1  -1   0\n"
    header = header % constants['spin']
    conversion = ['200', '1100', '2000', '40100', '41000']
    for name, value in constants.items():
        id = names[name]
        if id in conversion:
            value *= -1E-3
        if id not in ['spin']:
            header += "{0}  {1: >11.13e} 1.0E+000 \n".format((id), float(value))

    with open(os.path.join(path, 'default.var'), 'w') as f:
        f.write(header)

def run_spcat():
    """Runs SPCAT at the saved location for the system.  The string formatting
    is required to solve issues when the user has a space in their windows
    username"""
    spcatpath = '"%s"' % os.path.join(path, 'SPCAT.exe')
    filepath = '"%s"' % os.path.join(path, 'default')
    if os.name == 'nt':
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.call("%s %s" % (spcatpath, filepath), shell=True)
