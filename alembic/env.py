from logging.config import fileConfig

from sqlalchemy import engine_from_config, MetaData
from sqlalchemy import pool

from alembic import context

from app.adapters.models.base import Base
from app.setup.config.settings import AppSettings, load_settings

from alembic.autogenerate import renderers
from geoalchemy2 import Geometry


@renderers.dispatch_for(Geometry)
def render_geometry(type_, autogen_context):
    return None


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata: MetaData = Base.metadata

settings: AppSettings = load_settings()

sync_dsn = settings.postgres.dsn.replace("+asyncpg", "+psycopg2")
config.set_main_option("sqlalchemy.url", sync_dsn)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        include_object=include_object,
        version_table_schema="public",
        default_schema="public",
        compare_type=True,
        compare_schema=False,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            include_object=include_object,
            version_table_schema="public",
            default_schema="public",
            compare_type=True,
            compare_server_default=True,
            compare_schema=False
        )

        with context.begin_transaction():
            context.run_migrations()


def include_object(obj, name, type_, reflected, compare_to):
    if type_ == "table":
        schema = getattr(obj, "schema", None)
        is_public_schema = (schema == "public") or (schema is None)
        if not is_public_schema:
            return False

        app_tables = {
            "road_networks",
            "road_nodes",
            "road_edges",
            "road_network_versions",
            "users"
        }
        return name in app_tables

    if type_ in {"index", "column"}:
        parent_table = getattr(obj, "table", None)
        if parent_table is not None and getattr(parent_table, "schema", None) not in [None, "public"]:
            return False

    return True


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
