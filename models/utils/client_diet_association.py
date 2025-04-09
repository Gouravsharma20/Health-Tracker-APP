# models/utils/client_diet_association.py

from sqlalchemy import Table, Column, Integer, ForeignKey
from database import Base

clientDietAssociation_table = Table(
    'client_diet',
    Base.metadata,
    Column('client_id', Integer, ForeignKey('clients.id')),
    Column('diet_id', Integer, ForeignKey('diets.id'))
)
