from autofit.engine.structure import Atom, Structure
from autofit.engine.db_base import get_session
import time




class Chisq:

    def __init__(self, *args, item=None):
        self.error = self.calc_error(*args)
        self.item = item


    def calc_error(self, *args, total=False):
        chisq = [(a-b)**2 for a, b in zip(*args)]
        if total:
            return sum(chisq)
        else:
            return chisq

    def __lt__(self, other):
        return sum(self.error) < other

    def __eq__(self, other):
        return sum(self.error) == other

    def __gt__(self, other):
        return sum(self.error) > other

    def __repr__(self):
        return f'Chisq({sum(self.error)})'


def find_matches(a, b, c, max_response=10):
    session = get_session()
    scaler = 0.1
    response = session.query(Structure).filter( Structure.A <= (a+ a*scaler),
                                                Structure.A >= (a* (1-scaler)),
                                                Structure.B <= (b + b * scaler),
                                                Structure.B >= (b * (1 - scaler)),
                                                Structure.C <= (c + c * scaler),
                                                Structure.C >= (c * (1 - scaler))
                                                ).all()
    errors = [(Chisq((a,b,c), x.constants, item=x)) for x in response]
    errors.sort()
    return errors[:max_response]

if __name__ == '__main__':

    wanted = (128219.0383156, 24723.5657114, 23865.7215197)
    wanted = (27663.68, 4714.188, 4235.085)  # ethyl cyanide
    wanted = (5028.844, 1569.364, 1205.826)  # anisole
    wanted = (10341.76, 3876.195, 2912.36)  # glycine
    ans = find_matches(*wanted)
    for a in ans:
        print(a.item.name, (sum(a.error)))