#!/usr/bin/env python
"""

# Original Author: Tyler Lesmann
# Original Source: http://www.tylerlesmann.com/2009/apr/27/copying-databases-across-platforms-sqlalchemy/

# TODO: Look at https://gist.github.com/thoas/1589496 if any
#   "sequencing" issues come in to play.

"""

import sys
import getopt

import retort


def migrate(src_connection_string, dest_connection_string,
            models_module):
    """
    """
    models = __import__(models_module)

    print("Creating source database session...")
    src_ctx = retort.SourceContext(src_connection_string, models)
    print("Creating destination database session...")
    dest_ctx = retort.DestinationContext(dest_connection_string, models)


    print("Iterating Tables...")
    for table_name, src_table in src_ctx.iter_tables():
        orig_src_table = src_table
        print "Processing source model table: %s" % table_name
        dest_ctx.create_table(src_table)

        Model = retort.quick_mapper(src_table)

        columns = src_table.columns.keys()

        for record in src_ctx.iter_records(src_table):
            data = dict(
                [(str(column), getattr(record, column)) for column in columns]
            )
            dest_ctx.Session.merge(Model(**data))

        print("Committing Data")
        dest_ctx.commit()

        print("Make sure to use the 'fix_sequences' script if needed."
              "(e.g. for Destination Postgres)")


def usage(argv):
    return """
Migrate schema and data.
Give a source and target connection string and 

Usage: %s -s source_server -d destination_server models_module
    -s, -d = driver://user[:password]@host[:port]/database[?schema=schema_name]

Example: %s
    """ % (argv[0], argv[0])


def main(argv):
    """Main script entry point. Passed ``sys.argv``.
    """
    optlist, models = getopt.getopt(argv[1:], 's:d:')
    print(models)
    options = dict(optlist)
    print(options)
    if not all([opt in options for opt in ('-s', '-d')]):
        print(usage(argv))
        sys.exit(1)
    else:
        migrate(options['-s'], options['-d'], *models)


if __name__ == '__main__':
    main(sys.argv)