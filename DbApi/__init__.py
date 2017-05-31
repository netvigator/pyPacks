"""
pgdb - DB-SIG compliant module for PygreSQL.

(c) 1999, Pascal Andre <andre@via.ecp.fr>.
See package documentation for further information on copyright.

Inline documentation is sparse.  See DB-SIG 2.0 specification for
usage information.

    basic usage:

    pgdb.connect(connect_string) -> connection
            connect_string = 'host:database:user:password'
            All parts are optional. You may also pass host through
            password as keyword arguments. To pass a port, pass it in
            the host keyword parameter:
                    pgdb.connect(host='localhost:5432')

    connection.cursor() -> cursor

    connection.commit()

    connection.close()

    connection.rollback()

    cursor.execute(query[, params])
            execute a query, binding params (a dictionary) if it is
            passed. The binding syntax is the same as the % operator
            for dictionaries, and no quoting is done.

    cursor.executemany(query, list of params)
            execute a query many times, binding each param dictionary
            from the list.

    cursor.fetchone() -> [value, value, ...]

    cursor.fetchall() -> [[value, value, ...], ...]

    cursor.fetchmany([size]) -> [[value, value, ...], ...]
            returns size or cursor.arraysize number of rows from result
            set. Default cursor.arraysize is 1.

    cursor.description -> [(column_name, type_name, display_size,
            internal_size, precision, scale, null_ok), ...]

            Note that precision, scale and null_ok are not implemented.

    cursor.rowcount
            number of rows available in the result set. Available after
            a call to execute.

    cursor.close()
"""

