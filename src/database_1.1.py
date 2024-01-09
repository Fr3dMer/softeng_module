from sqlalchemy import Table, Column, Integer, String,
#from sqlalchemy module import specific object

from sqlalchemy.ext.declarative import declarative_base
#import declarative_base from sqlalchemy.ext.declarative

Base = declarative_base
#instance of declarative. Create a declarative_base

#pip install sqlalchemy or conda install -c anaconda sqlalchemy

# create a SQLite engine
from sqlalchemy import create_engine
engine = create_engine('sqlite:///panel_app_db.db', echo = False)
#return just the output

if not database_exists(engine.url):
    create_database(engine.url)

print(database_exists(engine.url))

Base.metadata.create_all(engine)



class Samples (Base):
    __tablename__ = 'samples'
    sample_id = Column(varchar(255), primary_key = True)
    pateint_id = Column(varchar(255))
    unique_panel_id = Column(varchar(255), ForeignKey('panels.unique_panel_id'))
    date = Column(date)
    panels = relationship('Panels', back_populates = 'samples')

class Panels (Base):
    __tablename__ = 'panels'
    unique_panel_id = Column(varchar(255), primary_key = True)
    r_code = Column(varchar(255))
    version = Column(float)
    HGNC_id = Column(varchar(255))
    genes = Column(varchar(255))
    reference_sequence_GrCH37 = Column(varchar(255))
    reference_sequence_GrCH38 = Column(varchar(255))
    JSON = Column(JSON)
    BED_file = COlumn (varchar(max))
    samples = relationship('Samples', back_populates = 'panels')


