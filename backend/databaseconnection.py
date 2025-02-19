import logging
from uuid import uuid4
from asyncpg import Connection
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy import update, delete, or_, not_, func, desc, nulls_last, insert
from contextlib import asynccontextmanager
from models import *
from datetime import date, timedelta
import random


class CConnection(Connection):
    def _get_unique_id(self, prefix: str) -> str:
        return f'__asyncpg_{prefix}_{uuid4()}__'


class DataBaseWorker:
    def __init__(self, user, password, host, port, database):
        self.super_user_login = None
        self.super_user_password = None
        self.log = logging.getLogger('DataBaseWorker')
        self.log.info(f'Connecting to database')
        try:
            self.engine = create_async_engine(f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}",
                                              connect_args={
                                                  "statement_cache_size": 0,
                                                  "prepared_statement_cache_size": 0,
                                                  "connection_class": CConnection,
                                              })

            self.connection = self.engine.connect()
            self.session = async_sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
        except Exception as e:
            self.log.error("Ошибка при подключении к БД", e)

        self.session = async_sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    async def initialize_connection(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await conn.commit()
            self.log.info('Connected')

    @asynccontextmanager
    async def create_session(self):
        async with self.session() as db:
            try:
                yield db
            except:
                await db.rollback()
                raise
            finally:
                await db.close()

    # ----------------------- USERS ---------------------
    async def new_user(self, user: User) -> None:
        async with self.create_session() as session:
            session.add(user)
            await session.commit()

    async def get_users_by_email(self, email: str) -> list[User]:
        async with self.create_session() as session:
            stmt = select(User).where(User.email == email)
            result = (await session.execute(stmt)).scalars().all()
            return result

    async def get_users_from_token(self, user_id: int, email: str) -> list[User]:
        async with self.create_session() as session:
            stmt = select(User).where(User.id == user_id, User.email == email)
            result = (await session.execute(stmt)).scalars().all()
            return result

    async def get_users(self, limit: int = 10, offset: int = 0) -> list[User]:
        async with self.create_session() as session:
            stmt = select(User).order_by(User.id).limit(limit).offset(offset)
            result = (await session.execute(stmt)).scalars().all()
            return result

    async def count_users(self) -> int:
        async with self.create_session() as session:
            stmt = select(func.count(User.id))
            result = (await session.execute(stmt)).scalars().first()
            return result

    async def approve_user(self, user_id: int, approved: bool = False):
        async with self.create_session() as session:
            stmt = update(User).where(User.id == user_id).values(approved=approved)
            await session.execute(stmt)
            await session.commit()

    async def update_user_current_code(self, user_id: int, current_code: str | None):
        async with self.create_session() as session:
            stmt = update(User).where(User.id == user_id).values(current_code=current_code)
            await session.execute(stmt)
            await session.commit()

    # ----------------------------- SUBSCRIPTIONS ---------------------------
    async def is_subscription_exists(self, subscription_id: str) -> bool:
        async with self.create_session() as session:
            stmt = select(Subscription).where(Subscription.id == subscription_id)
            result = (await session.execute(stmt)).scalars().all()
            return bool(len(result))

    async def new_subscription(self, subscription: Subscription):
        async with self.create_session() as session:
            session.add(subscription)
            await session.commit()

    async def get_subscriptions(self) -> list[Subscription]:
        async with self.create_session() as session:
            stmt = select(Subscription)
            result = (await session.execute(stmt)).scalars().all()
            return result

    # ----------------------------- TEXTS ---------------------------
    async def is_filed_exists(self, field_id: str) -> bool:
        async with self.create_session() as session:
            stmt = select(TextField).where(TextField.id == field_id)
            result = (await session.execute(stmt)).scalars().all()
            return bool(len(result))

    async def new_field(self, field: TextField):
        async with self.create_session() as session:
            session.add(field)
            await session.commit()

    async def is_text_exists(self, field_id: str, language: str) -> bool:
        async with self.create_session() as session:
            stmt = select(GeneralTexts).where(
                GeneralTexts.field_id == field_id, GeneralTexts.language == language
            )
            result = (await session.execute(stmt)).scalars().all()
            return bool(len(result))

    async def new_text(self, text: GeneralTexts):
        async with self.create_session() as session:
            session.add(text)
            await session.commit()

    async def update_general_text(self, field_id: str, language: str, text: str):
        async with self.create_session() as session:
            stmt = update(GeneralTexts).where(
                GeneralTexts.field_id == field_id, GeneralTexts.language == language
            ).values(text=text)
            await session.execute(stmt)
            await session.commit()

    async def get_general_fields(self, limit: int = 10, offset: int = 0) -> list[TextField]:
        async with self.create_session() as session:
            stmt = select(TextField).order_by(TextField.id).limit(limit).offset(offset)
            result = (await session.execute(stmt)).scalars().all()
            return result

    async def count_general_fields(self) -> int:
        async with self.create_session() as session:
            stmt = select(func.count(TextField.id))
            result = (await session.execute(stmt)).scalars().first()
            return result

    async def get_general_texts_by_filed_id(self, field_id: str, language: str | None) -> list[GeneralTexts]:
        async with self.create_session() as session:
            stmt = select(GeneralTexts).where(
                GeneralTexts.field_id == field_id,
                or_(
                    GeneralTexts.language == language,
                    language is None
                )
            )
            result = (await session.execute(stmt)).scalars().all()
            return result

    async def get_general_texts_by_language(self, language: str) -> list[GeneralTexts]:
        async with self.create_session() as session:
            stmt = select(GeneralTexts).where(GeneralTexts.language == language)
            result = (await session.execute(stmt)).scalars().all()
            return result
