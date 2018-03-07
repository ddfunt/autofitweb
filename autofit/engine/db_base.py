from sqlalchemy import create_engine
from sqlalchemy import Column, Integer

from autofit.IO import paths
from autofit.engine.structure import Atom, Structure, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


engine = create_engine('sqlite:///{}'.format(paths.Paths.db_path()))
Base.metadata.create_all(engine)
if not database_exists(engine.url):
    create_database(engine.url)


def get_session():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session




if __name__ == '__main__':
    print(get_session())