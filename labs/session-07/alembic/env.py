"""Run by every alembic command: where the database is, and what it should contain.

`target_metadata` is what autogenerate compares the database against: the tables
described in models.py.
"""

from logging.config import fileConfig

from alembic import context
from alembic.migration import MigrationContext
from models import Base
from sqlalchemy import engine_from_config, pool
from sqlalchemy.types import TypeEngine

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def include_object(
    object_: object,
    name: str | None,
    type_: str,
    reflected: bool,
    compare_to: object | None,
) -> bool:
    """Leave alone the tables and indexes models.py does not describe.

    The database holds more than the four mapped tables: payments,
    driver_balances, session 5's star schema, and perhaps the index you created in
    session 4. Without this, autogenerate would write a drop for each of them.
    Columns are still compared, so a column missing from a mapped class is noticed.
    """
    if type_ in ("table", "index") and reflected and compare_to is None:
        return False
    return True


def compare_type(
    migration: MigrationContext,
    inspected_column: object,
    metadata_column: object,
    inspected_type: TypeEngine,
    metadata_type: TypeEngine,
) -> bool:
    """Two types differ if PostgreSQL spells them differently.

    Alembic's own comparison lets a bare Numeric pass for numeric(10, 2). This one
    does not.
    """
    dialect = migration.dialect
    return inspected_type.compile(dialect=dialect) != metadata_type.compile(
        dialect=dialect
    )


def run_migrations_offline() -> None:
    """Write the SQL out instead of running it: `alembic upgrade head --sql`."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        include_object=include_object,
        compare_type=compare_type,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Connect to the database and run the migrations there."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
            compare_type=compare_type,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
