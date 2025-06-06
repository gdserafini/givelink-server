from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session
from config.settings import Settings
from src.models.exceptions import DatabaseConnectionError
import subprocess
from src.models.db_schemas import RolesModel, UserModel
from sqlalchemy import select
from src.models.role_model import RoleEnum, RoleLevelEnum, RoleIdEnum
from src.utils.logging import logger


engine = create_engine(Settings().DATABASE_URL)


def get_session(): # pragma: no cover
    with Session(engine) as session:
        yield session


def setup_db() -> None:
    from src.service.security import get_password_hash
    try:
        with engine.connect() as connection:
            logger.info(f'session.py - Database successfully connected - {connection.__class__}')
            inspector = inspect(engine)
            if 'users' not in inspector.get_table_names():
                logger.info('session.py - Not found db tables, running migrations...')
                subprocess.run(['alembic', 'upgrade', 'head'], check=True)
                logger.info('session.py - Finished migrations')
        with Session(engine) as session:
            roles = session.scalar(select(RolesModel).limit(1))
            if not roles:
                logger.info('session.py - Table "roles" is empty, inserting default roles...')
                default_roles = [
                    RolesModel(id=RoleIdEnum.USER.value, role=RoleEnum.USER.value, level=RoleLevelEnum.USER.value),
                    RolesModel(id=RoleIdEnum.ADMIN.value, role=RoleEnum.ADMIN.value, level=RoleLevelEnum.ADMIN.value),
                ]
                session.add_all(default_roles)
                session.commit()
                logger.info('session.py - Default roles inserted')
            user_admin = session.scalar(
                select(UserModel).where(
                    UserModel.username == 'admin'
                )
            )
            if not user_admin:
                logger.info('session.py - Admin user not found, inserting default admin user... - admin')
                admin = UserModel(
                    username='admin',
                    email='admin@givelink.com',
                    password=get_password_hash(Settings().ADMIN_SYSTEM_PASSWORD),
                    role_id=RoleIdEnum.ADMIN.value,
                    avatar_url=''
                )
                session.add(admin)
                session.commit()
                logger.info('session.py - Admin user inserted - admin')
        logger.info('session.py - Database succesfully configured')
    except Exception as e:
        logger.info(f'session.py - Database error - {e}')
        detail = f'Database connection error: {e}'
        raise DatabaseConnectionError(message=detail)
