from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session
from config.settings import Settings
from src.models.exceptions import DatabaseConnectionError
import subprocess
from src.models.db_schemas import RolesModel, UserModel
from sqlalchemy import select
from src.models.role_model import RoleEnum, RoleLevelEnum, RoleIdEnum


engine = create_engine(Settings().DATABASE_URL)


def get_session(): # pragma: no cover
    with Session(engine) as session:
        yield session


def setup_db() -> None:
    from src.service.security import get_password_hash
    try:
        with engine.connect() as connection:
            print(f'Successfully connection: {connection}')
            inspector = inspect(engine)
            if 'users' not in inspector.get_table_names():
                print('Not found db tables, running migrations...')
                subprocess.run(['alembic', 'upgrade', 'head'], check=True)
                print('Finished migrations.')
        with Session(engine) as session:
            roles = session.scalar(select(RolesModel).limit(1))
            if not roles:
                print('Table "roles" is empty, inserting default roles...')
                default_roles = [
                    RolesModel(id=RoleIdEnum.USER.value, role=RoleEnum.USER.value, level=RoleLevelEnum.USER.value),
                    RolesModel(id=RoleIdEnum.ADMIN.value, role=RoleEnum.ADMIN.value, level=RoleLevelEnum.ADMIN.value),
                ]
                session.add_all(default_roles)
                session.commit()
                print('Default roles inserted.')
            user_admin = session.scalar(
                select(UserModel).where(
                    UserModel.username == 'admin'
                )
            )
            if not user_admin:
                print('Admin user not found, inserting default admin user...')
                admin = UserModel(
                    username='admin',
                    email='admin@givelink.com',
                    password=get_password_hash(Settings().ADMIN_SYSTEM_PASSWORD),
                    role_id=RoleIdEnum.ADMIN.value,
                    avatar_url=''
                )
                session.add(admin)
                session.commit()
                print('Admin user inserted.')
    except Exception as e:
        detail = f'Database connection error: {e}'
        raise DatabaseConnectionError(message=detail)
