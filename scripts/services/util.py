from scripts.models.util import Sequence, SequenceType
from scripts.models import database


def create_sequence(name, type, projectid, currentvalue=0, increment=1):
    session = database.get_session()
    sequence = Sequence()
    sequence.Name = name
    sequence.Type = type
    sequence.ProjectId = projectid
    sequence.CurrentValue = currentvalue
    sequence.Increment = increment
    session.add(sequence)
    session.commit()
    session.close()


def getNext(name):
    session = database.get_session()
    seq = session.query(Sequence).filter(Sequence.Name == name).first()
    if seq:
        seq.CurrentValue = seq.CurrentValue + seq.Increment
        seq_name, next_value = seq.Name, seq.CurrentValue
        session.commit()
        session.close()
        return seq_name, next_value


def getNext(projectid, type):
    session = database.get_session()
    seq = session.query(Sequence).filter(Sequence.ProjectId == projectid, Sequence.Type == type).first()
    if seq:
        seq.CurrentValue = seq.CurrentValue + seq.Increment
        seq_name, next_value = seq.Name, seq.CurrentValue
        session.commit()
        session.close()
        return seq_name, next_value
