# models/utils/client_workout_association.py
from sqlalchemy import Table, Column, Integer, ForeignKey
from database import Base

clientWorkoutAssociation_table = Table(
    'client_workout',
    Base.metadata,
    Column('client_id', Integer, ForeignKey('clients.id')),
    Column('workout_id', Integer, ForeignKey('workouts.id'))
)
