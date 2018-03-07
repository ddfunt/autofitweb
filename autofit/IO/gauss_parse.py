import re
from autofit.engine import structure

class GaussianFile:
    _constants = None
    _dipoles = None
    _structure = None

    def __init__(self, filename=None):
        if filename:
            self.raw, self.completed = self._read_file(filename)

    def _read_file(self, filepath):

        with open(filepath, 'r') as f:
            data = f.read()
        completed = self._check_termination(data)
        return data, completed

    @property
    def constants(self):
        if not self._constants:
            names = ('A', 'B', 'C')
            search_string = r' Rotational constants \(MHZ\).*? Nuclear'
            matches = re.findall(search_string, self.raw, re.DOTALL)
            selected = matches[-1].split('\n')[1].split()
            constants = {name:float(x) for x, name in zip(selected, names)}
            self._constants = constants

        return self._constants

    @property
    def dipoles(self):
        if not self._dipoles:
            names = ('u_A', 'u_B', 'u_C')
            search_string = r' Dipole moment \(Debye\).*? Quartic'
            matches = re.findall(search_string, self.raw, re.DOTALL)
            wanted = matches[-1]
            dipoles = wanted.split('\n')[1].split()

            self._dipoles = {name:float(x) for x, name in zip(dipoles[:3], names)}
        return self._dipoles

    @property
    def structure(self):
        if not self._structure:
            search_string = r' Principal axis orientation:  .*? Rotational constants'
            matches = re.findall(search_string, self.raw, re.DOTALL)
            wanted = matches[-1]
            #print(wanted)
            search = r'\d.*-?\d\.\d{6}.*-?\d\.\d{6}.*-?\d\.\d{6}'
            rows = re.findall(search, wanted, re.MULTILINE)
            self._structure = structure.Structure.from_gauss(rows)
            for key, value in self.constants.items():
                setattr(self._structure, key, value)
            for key, value in self.dipoles.items():
                setattr(self._structure, key, value)
            #self._structure.A, self.structure.B, self._structure.C = self.constants
            #self._structure.u_A, self._structure.u_B, self._structure.u_C = self.dipoles
        return self._structure



    def _get_constants_non_picket(self ):
        search_string = r'^ Rotational constants \(GHZ\).*'
        matches = re.findall(search_string, self.raw, re.MULTILINE)
        print(matches[-1])

    def _check_termination(self, data):
        result = re.findall(r'^ Normal termination of  Gaussian.*', data, re.MULTILINE)
        if result:
            return True
        else:
            return False


if __name__ == '__main__':
   fname = "C:\\Users\\mtm5k\\Dropbox (BrightSpec)\\BrightSpec_Data\\G09 Files\\B3LYP-31Gdp\\DNT.out"

   g = GaussianFile(fname)
   print(g.constants)
   print(g.dipoles)
   print(g.structure.calc_constants())
   print(g.constants)