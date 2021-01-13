from backend.models import Location
from sqlalchemy.orm import Session


def list(db: Session, user_id: int) -> list:
    locations = db.query(Location).filter(Location.user_id == user_id).all()

    return locations


def create(db: Session, name: str, user_id: int) -> None:
    location = Location(name=name, user_id=user_id)

    db.add(location)
    db.commit()


def update(db: Session, location_id: int, user_id: int, name: str) -> None:
    # TODO: Add check on expired

    db.query(Location).filter(Location.user_id == user_id).filter(
        Location.id == location_id
    ).update({Location.name: name})
    db.commit()


def delete(db: Session, location_id: int) -> None:
    # TODO: Add check on activity

    db.query(Location).filter(Location.id == location_id).delete()
    db.commit()
