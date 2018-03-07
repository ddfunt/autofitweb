import numpy as np
import mendeleev

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, String, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base


class BaseTable:


    id = Column(Integer, primary_key=True)


convention = {
  "ix": 'ix_%(column_0_label)s',
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
Base = declarative_base(cls=BaseTable)


class Atom(Base):
    __tablename__ = 'atom'
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    mass = Column(Float)
    structure_id = Column(Integer, ForeignKey('structure.id'))

    def __init__(self, mass, x, y, z):
        self.mass = mass
        self.x = x
        self.y = y
        self.z = z

    @property
    def point(self):
        return (self.x, self.y, self.z)

    def skew(self,):
        v = np.array([self.x, self.y, self.z])
        skv = np.roll(np.roll(np.diag(v.flatten()), 1, 1), -1, 0)
        return skv - skv.T

    @property
    def intertia_matrix(self):
        return -1 * np.dot(self.skew(), self.skew())

    @property
    def tensor_product(self):
        return self.mass * self.intertia_matrix

    def __repr__(self):
        return 'Atom(mass:{mass}, x,y,z:{x},{y},{z})'.format(mass=self.mass,
                                                            x=self.x,
                                                            y=self.y,
                                                            z=self.z
                                                            )

class Constants(Base):
    __tablename__ = 'constants'
    A = Column(Float)
    B = Column(Float)
    C = Column(Float)

class Dipoles(Base):
    __tablename__ = 'dipoles'
    u_A = Column(Float)
    u_B = Column(Float)
    u_C = Column(Float)

class Structure(Base):
    __tablename__ = 'structure'
    atoms = relationship('Atom')
    name = Column(String(255))
    mass = Column(Float)
    A =  Column(Float)
    B = Column(Float)
    C = Column(Float)
    u_A = Column(Float)
    u_B = Column(Float)
    u_C = Column(Float)
    chemspyder_id = Column(Integer)

    @property
    def constants(self):
        return [self.A, self.B, self.C]

    @property
    def dipoles(self):
        pass

    @classmethod
    def from_matrix(cls, input_array, mass_col=0):
        instance = cls()
        instance.atoms = []
        for atom in input_array:
            atom = atom.tolist()
            mass = atom.pop(mass_col)
            instance.atoms.append(Atom(mass, *atom))
        return instance

    @classmethod
    def from_gauss(cls, data, ):
        instance = cls()
        instance.atoms = []
        for row in data:
            _, atomic_num, *xyz = row.split()
            element = mendeleev.element(int(atomic_num))
            mass = element.isotopes[0].mass
            xyz = [float(x) for x in xyz]
            atom = Atom(mass, *xyz)

            instance.atoms.append(atom)
        instance.mass = sum([m.mass for m in instance.atoms])
        return instance

    @property
    def position_matrix(self):
        return np.array([x.point for x in self.atoms])

    @property
    def mass_vector(self):
        return np.array([x.mass for x in self.atoms])


    def calc_constants(self):
        inertia_list = [atom.tensor_product for atom in self.atoms]
        tensor_sum = np.sum(inertia_list, 0)
        constants, _ = np.linalg.eig(tensor_sum)
        self.A, self.B, self.C = 505379.006/np.sort(constants)
        return self.A, self.B, self.C


if __name__ == '__main__':

    test = np.array([[1,2,3,4], [2,4,5,6]])
    s = Structure.from_matrix(test)

    print(s.calc_constants())