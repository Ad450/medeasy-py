from typing import TypeVar, Generic, Optional, Union

from sqlalchemy import create_engine, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker


from domain.models import Base
from infrastructure.env_configs import EnvironmentConfig

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):

    @property
    def __get_connection_string(self) -> str:
        return EnvironmentConfig.get_env_variable(variable="POSTGRES_URL")

    def __init__(self, model: T):
        connection_string = self.__get_connection_string
        engine = create_engine(connection_string)
        self.__session = sessionmaker(engine)
        Base.metadata.create_all(engine)

    def save(self, item: T | list[T]) -> Optional[Union[T, list[T]]]:
        try:
            with self.__session.begin() as session:
                if isinstance(item, list):
                    session.add_all(item)
                else:
                    session.add(item)
                session.commit()
                return item
        except SQLAlchemyError as e:
            print(f"Exception saving item: {e.code}")
            print("We are throwing an expcetion here")
            return None

    def get_by_id(self, item_id: int) -> Optional[T]:
        with self.__session as session:
            result = session.get(T, item_id)
            return result

    def update(self, update: T, item_id: int) -> Optional[T]:
        existing_item = self.get_by_id(item_id)
        if not existing_item:
            return None
        with self.__session as session:
            for key, value in update:
                setattr(existing_item, key, value)
            session.commit()
            return update

    def get(self) -> list[T]:
        with self.__session as session:
            return session.query(T).all()

    def get_by_email(self, email: str) -> Optional[T]:
        try:
            with self.__session as session:
                statement = select(T).filter_by(email=email)
                rows = session.execute(statement).all()
                if isinstance(rows, list):
                    return rows[0]
                else:
                    return None
        except Exception as e:
            print(f"Exception at: {e}")
            return None









