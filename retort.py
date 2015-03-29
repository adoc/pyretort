try:
    from urllib.parse import urlparse, parse_qs
except ImportError:
    from urlparse import urlparse, parse_qs

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.exc
from sqlalchemy.ext.declarative import declarative_base


class Context:
    """A self contained SQLAlchemy context.
    """

    def __init__(self, connection_string, model):
        """
        """
        self.model = model
        self.connection_string = connection_string
        self.Base = model.Base
        self.MetaData = model.Base.metadata
        self.schema = None
        self.database = None
        self.parse_connection_string()
        self.Engine = sqlalchemy.create_engine(self.connection_string,
                                               echo=False,
                                               convert_unicode=True)
        self.Session = sqlalchemy.orm.sessionmaker(bind=self.Engine)(
                                                                autoflush=False)
        self.MetaData.bind = self.Engine

    def parse_connection_string(self):
        """
        """
        result = urlparse(self.connection_string)

        query = parse_qs(result.query)
        if 'schema' in query:
            self.schema = query['schema'][0]

        self.database = result.path.strip('/')

    def get_table_list(self):
        """Return a list of table names from the current metadata.
        """
        if hasattr(self.model, '__flush_order__'):
            return [model.__tablename__ for model in self.model.__flush_order__]
        else:
            return self.MetaData.tables.keys()

    def init_table(self, table_name):
        return sqlalchemy.Table(table_name, self.MetaData, autoload=True)

    def commit(self):
        self.Session.commit()


class SourceContext(Context):
    """
    """
    def iter_tables(self):
        for table_name in self.get_table_list():
            yield table_name, self.init_table(table_name)

    def iter_records(self, table):
        for record in self.Session.query(table).all():
            yield record


class DestinationContext(Context):
    """
    """
    def create_table(self, source_table):
        source_table.metadata.create_all(self.Engine)


def quick_mapper(table):
    """Returns a SQLAlchemy declarative model given the ``table``
    object.
    src: http://www.tylerlesmann.com/2009/apr/27/copying-databases-across-platforms-sqlalchemy/
    """
    Base = declarative_base()
    class GenericMapper(Base):
        __table__ = table
    return GenericMapper