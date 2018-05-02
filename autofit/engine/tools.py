from autofit.engine.structure import Atom, Structure
from autofit.engine.db_base import get_session
import math



class Chisq:


    def __init__(self, *args, item=None):
        self.error = self.calc_error(*args)
        self.item = item

    @property
    def total_error(self):
        return round(sum(self.error), 4)

    def calc_error(self, *args, **kwargs):
        chisq = [round(((a-b)**2) / b, 4) for a, b in zip(*args) if a]
        return chisq

    def __lt__(self, other):
        return self.total_error < other

    def __eq__(self, other):
        return self.total_error == other

    def __gt__(self, other):
        return self.total_error > other

    def __repr__(self):
        return 'Chisq({})'.format(sum(self.error))


def find_matches(a, b, c, max_response=10):
    session = get_session()
    scaler = 0.1
    print(a, b, c)
    filters = (Structure.A <= (a+ a*scaler) if a > 0 else None,
                Structure.A >= (a* (1-scaler)) if a > 0 else None,
                Structure.B <= (b + b * scaler) if b > 0 else None,
                Structure.B >= (b * (1 - scaler)) if b > 0 else None,
                Structure.C <= (c + c * scaler) if c > 0 else None,
                Structure.C >= (c * (1 - scaler)) if c > 0 else None)
    print(filters)
    #filters = [f for f in filters if f]
    response = session.query(Structure).filter( *filters
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