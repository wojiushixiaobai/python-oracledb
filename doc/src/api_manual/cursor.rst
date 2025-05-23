.. _cursorobj:

*******************
API: Cursor Objects
*******************

A cursor object can be created with :meth:`Connection.cursor()`.

Cursor Methods
==============

.. method:: Cursor.__enter__()

    The entry point for the cursor as a context manager. It returns itself.

    .. dbapimethodextension::

.. method:: Cursor.__exit__()

    The exit point for the cursor as a context manager. It closes the cursor.

    .. dbapimethodextension::

.. method:: Cursor.__iter__()

    Returns the cursor itself to be used as an iterator.

    .. dbapimethodextension:: It is mentioned in PEP 249 as an optional extension.

.. method:: Cursor.arrayvar(typ, value, [size])

    Creates an array variable associated with the cursor of the given type and
    size and returns a :ref:`variable object <varobj>`. The value is either an
    integer specifying the number of elements to allocate or it is a list and
    the number of elements allocated is drawn from the size of the list. If the
    value is a list, the variable is also set with the contents of the list. If
    the size is not specified and the type is a string or binary, 4000 bytes
    is allocated. This is needed for passing arrays to PL/SQL (in cases where
    the list might be empty and the type cannot be determined automatically) or
    returning arrays from PL/SQL.

    Array variables can only be used for PL/SQL associative arrays with
    contiguous keys. For PL/SQL associative arrays with sparsely populated keys
    or for varrays and nested tables, the approach shown in this
    `example <https://github.com/oracle/python-oracledb/blob/main/
    samples/plsql_collection.py>`__ needs to be used.

    .. dbapimethodextension::

.. method:: Cursor.bindnames()

    Returns the list of bind variable names bound to the statement. Note that a
    statement must have been prepared first.

    .. dbapimethodextension::

.. method:: Cursor.callfunc(name, return_type, parameters=[], \
        keyword_parameters={})

    Calls a PL/SQL function with the given name and returns its value.

    The ``return_type`` parameter for :meth:`~Cursor.callfunc()` is expected to
    be a Python type, one of the :ref:`oracledb types <types>` or an
    :ref:`Object Type <dbobjecttype>`.

    The sequence of parameters must contain one entry for each parameter that
    the PL/SQL function expects. Any keyword parameters will be included after
    the positional parameters.

    Use :meth:`Cursor.var()` to define any OUT or IN OUT parameters, if
    necessary.

    See :ref:`plsqlfunc` for examples.

    For consistency and compliance with the PEP 8 naming style, the parameter
    ``keywordParameters`` was renamed to ``keyword_parameters``. The old name
    will continue to work for a period of time.

    .. dbapimethodextension::

    .. note::

        In line with the Python DB API, it is not recommended to call
        :meth:`Cursor.setinputsizes()` prior to calling
        :meth:`~Cursor.callfunc()`. Use :meth:`Cursor.var()` instead. In
        existing code that calls :meth:`~Cursor.setinputsizes()`, the first
        item in the :meth:`~Cursor.setinputsizes()` parameter list refers to
        the return value of the PL/SQL function.

.. method:: Cursor.callproc(name, parameters=[], keyword_parameters={})

    Calls a PL/SQL procedure with the given name.

    The sequence of parameters must contain one entry for each parameter that
    the procedure expects. The result of the call is a modified copy of the
    input sequence. Input parameters are left untouched; output and
    input/output parameters are replaced with possibly new values. Keyword
    parameters will be included after the positional parameters and are not
    returned as part of the output sequence.

    Use :meth:`Cursor.var()` to define any OUT or IN OUT parameters if
    necessary.

    No query result set is returned by :meth:`~Cursor.callproc()`. Instead, use
    :ref:`REF CURSOR <refcur>` parameters or :ref:`Implicit Results
    <implicitresults>`.

    See :ref:`plsqlproc` for an example.

    For consistency and compliance with the PEP 8 naming style, the parameter
    ``keywordParameters`` was renamed to ``keyword_parameters``. The old name
    will continue to work for a period of time.

    .. note::

        The DB API definition does not allow for keyword parameters.

.. method:: Cursor.close()

    Closes the cursor now, rather than whenever __del__ is called. The cursor
    will be unusable from this point forward; an Error exception will be raised
    if any operation is attempted with the cursor.

.. method:: Cursor.execute(statement, parameters=[], ** keyword_parameters)

    Executes a statement against the database. See :ref:`sqlexecution`.

    Parameters may be passed as a dictionary or sequence or as keyword
    parameters. If the parameters are a dictionary, the values will be bound by
    name and if the parameters are a sequence the values will be bound by
    position. Note that if the values are bound by position, the order of the
    variables is from left to right as they are encountered in the statement
    and SQL statements are processed differently than PL/SQL statements. For
    this reason, it is generally recommended to bind parameters by name instead
    of by position.

    Parameters passed as a dictionary are name and value pairs. The name maps
    to the bind variable name used by the statement and the value maps to the
    Python value you wish bound to that bind variable.

    A reference to the statement will be retained by the cursor. If *None* or
    the same string object is passed in again, the cursor will execute that
    statement again without performing a prepare or rebinding and redefining.
    This is most effective for algorithms where the same statement is used, but
    different parameters are bound to it (many times). Note that parameters
    that are not passed in during subsequent executions will retain the value
    passed in during the last execution that contained them.

    For maximum efficiency when reusing a statement, it is best to use the
    :meth:`Cursor.setinputsizes()` method to specify the parameter types and
    sizes ahead of time; in particular, *None* is assumed to be a string of
    length 1 so any values that are later bound as numbers or dates will raise
    a TypeError exception.

    If the statement is a query, the cursor is returned as a convenience to the
    caller (so it can be used directly as an iterator over the rows in the
    cursor); otherwise, *None* is returned.

    .. note::

        The DB API definition does not define the return value of this method.

.. method:: Cursor.executemany(statement, parameters, batcherrors=False, \
        arraydmlrowcounts=False)

    Executes a SQL statement once using all bind value mappings or sequences
    found in the sequence parameters. This can be used to insert, update, or
    delete multiple rows in a table with a single python-oracledb call. It can
    also invoke a PL/SQL procedure multiple times. See :ref:`batchstmnt`.

    The ``statement`` parameter is managed in the same way as the
    :meth:`Cursor.execute()` method manages it.

    The ``parameters`` parameter can be a list of tuples, where each tuple item
    maps to one bind variable placeholder in ``statement``. It can also be a
    list of dictionaries, where the keys match the bind variable placeholder
    names in ``statement``. If there are no bind values, or values have
    previously been bound, the ``parameters`` value can be an integer
    specifying the number of iterations.

    In python-oracledb Thick mode, if the size of the buffers allocated for any
    of the parameters exceeds 2 GB, you will receive the error ``DPI-1015:
    array size of <n> is too large``. If you receive this error, decrease the
    number of rows being inserted.

    When *True*, the ``batcherrors`` parameter enables batch error support
    within Oracle Database and ensures that the call succeeds even if an
    exception takes place in one or more of the sequence of bind values. The
    errors can then be retrieved using :meth:`Cursor.getbatcherrors()`.

    When *True*, the ``arraydmlrowcounts`` parameter enables DML row counts to
    be retrieved from Oracle after the method has completed. The row counts can
    then be retrieved using :meth:`Cursor.getarraydmlrowcounts()`.

    Both the ``batcherrors`` parameter and the ``arraydmlrowcounts`` parameter
    can only be *True* when executing an insert, update, delete, or merge
    statement; in all other cases an error will be raised.

    For maximum efficiency, it is best to use the
    :meth:`Cursor.setinputsizes()` method to specify the bind value types and
    sizes. In particular, if the type is not explicitly specified, the value
    *None* is assumed to be a string of length 1 so any values that are later
    bound as numbers or dates will raise a TypeError exception.

.. method:: Cursor.fetchall()

    Fetches all (remaining) rows of a query result, returning them as a list of
    tuples. An empty list is returned if no more rows are available. Note that
    the cursor's arraysize attribute can affect the performance of this
    operation, as internally reads from the database are done in batches
    corresponding to the arraysize.

    An exception is raised if the previous call to :meth:`Cursor.execute()`
    did not produce any result set or no call was issued yet.

    See :ref:`fetching` for an example.

.. method:: Cursor.fetchmany(size=cursor.arraysize)

    Fetches the next set of rows of a query result, returning a list of tuples.
    An empty list is returned if no more rows are available. Note that the
    cursor's arraysize attribute can affect the performance of this operation.

    The number of rows to fetch is specified by the parameter. If it is not
    given, the cursor's ``arraysize`` attribute determines the number of rows
    to be fetched. If the number of rows available to be fetched is fewer than
    the amount requested, fewer rows will be returned.

    An exception is raised if the previous call to :meth:`Cursor.execute()`
    did not produce any result set or no call was issued yet.

    See :ref:`fetching` for an example.

.. method:: Cursor.fetchone()

    Fetches the next row of a query result set, returning a single tuple or
    *None* when no more data is available.

    An exception is raised if the previous call to :meth:`Cursor.execute()`
    did not produce any result set or no call was issued yet.

    See :ref:`fetching` for an example.

.. method:: Cursor.getarraydmlrowcounts()

    Retrieves the DML row counts after a call to :meth:`Cursor.executemany()`
    with ``arraydmlrowcounts`` enabled. This will return a list of integers
    corresponding to the number of rows affected by the DML statement for each
    element of the array passed to :meth:`Cursor.executemany()`.

    This method is only available for Oracle Database 12.1 and later.

    .. dbapimethodextension::

.. method:: Cursor.getbatcherrors()

    Retrieves the exceptions that took place after a call to
    :meth:`Cursor.executemany()` with ``batcherrors`` enabled. This will return a
    list of Error objects, one error for each iteration that failed. The offset
    can be determined by looking at the offset attribute of the error object.

    .. dbapimethodextension::

.. method:: Cursor.getimplicitresults()

    Returns a list of cursors which correspond to implicit results made
    available from a PL/SQL block or procedure without the use of OUT ref
    cursor parameters. The PL/SQL block or procedure opens the cursors and
    marks them for return to the client using the procedure
    dbms_sql.return_result. In python-oracledb Thick mode, closing the parent
    cursor will result in the automatic closure of the implicit result set
    cursors. See :ref:`implicitresults`.

    This method is only available for Oracle Database 12.1 (or later). For
    python-oracledb :ref:`Thick <enablingthick>` mode, Oracle Client 12.1 (or
    later) is additionally required.

    .. dbapimethodextension::

       It is most like the DB API method nextset(), but unlike that method
       (which requires that the next result set overwrite the current result
       set), this method returns cursors which can be fetched independently of
       each other.

.. method:: Cursor.parse(statement)

    This can be used to parse a statement without actually executing it
    (parsing step is done automatically by Oracle when a statement is
    :meth:`executed <Cursor.execute>`).

    .. dbapimethodextension::

    .. note::

        You can parse any DML or DDL statement. DDL statements are executed
        immediately and an implied commit takes place. You can also parse
        PL/SQL statements.

.. method:: Cursor.prepare(statement, tag, cache_statement=True)

    This can be used before a call to :meth:`Cursor.execute()` or
    :meth:`Cursor.executemany()` to define the statement that will be
    executed. When this is done, the prepare phase will not be performed when
    the call to :meth:`Cursor.execute()` or :meth:`Cursor.executemany()` is
    made with *None* or the same string object as the statement.

    If the ``tag`` parameter is specified and the ``cache_statement`` parameter
    is *True*, the statement will be returned to the statement cache with the
    given tag.

    If the ``cache_statement`` parameter is *False*, the statement will be
    removed from the statement cache (if it was found there) or will simply not
    be cached.

    See :ref:`Statement Caching <stmtcache>` for more information.

    .. dbapimethodextension::

.. method:: Cursor.scroll(value=0, mode="relative")

    Scrolls the cursor in the result set to a new position according to the
    mode.

    If mode is *relative* (the default value), the value is taken as an offset
    to the current position in the result set. If set to *absolute*, value
    states an absolute target position. If set to *first*, the cursor is
    positioned at the first row and if set to *last*, the cursor is set to the
    last row in the result set.

    An error is raised if the mode is *relative* or *absolute* and the scroll
    operation would position the cursor outside of the result set.

    .. dbapimethodextension:: It is mentioned in PEP 249 as an optional extension.

.. method:: Cursor.setinputsizes(*args, **keywordArgs)

    This can be used before calls to :meth:`Cursor.execute()` or
    :meth:`Cursor.executemany()` to predefine memory areas used for
    :ref:`bind variables <bind>`. Each parameter should be a type object
    corresponding to the data that will be used for a bind variable placeholder
    in the SQL or PL/SQL statement. Alternatively, it can be an integer
    specifying the maximum length of a string bind variable value.

    Use keyword parameters when :ref:`binding by name <bindbyname>`. Use
    positional parameters when :ref:`binding by position <bindbyposition>`. The
    parameter value can be *None* to indicate that python-oracledb should
    determine the required space from the data value provided.

    The parameters or keyword names correspond to the bind variable
    placeholders used in the SQL or PL/SQL statement. Note this means that for
    use with :meth:`Cursor.executemany()` it does not correspond to the number
    of bind value mappings or sequences being passed.

    When repeated calls to :meth:`Cursor.execute()` or
    :meth:`Cursor.executemany()` are made binding different string data
    lengths, using :meth:`~Cursor.setinputsizes()` can help reduce the
    database's SQL "version count" for the statement. See :ref:`Reducing the
    SQL Version Count <sqlversioncount>`.

    .. note::

        :meth:`Cursor.setinputsizes()` should not be used for bind variables
        passed to :meth:`Cursor.callfunc()` or
        :meth:`Cursor.callproc()`. Instead, use :meth:`Cursor.var()`.

        If :meth:`Cursor.setinputsizes()` is used with
        :meth:`Cursor.callfunc()`, the first parameter in the list refers to
        the return value of the PL/SQL function.

.. method:: Cursor.setoutputsize(size, [column])

    This method does nothing and is retained solely for compatibility with the
    DB API. Python-oracledb automatically allocates as much space as needed to
    fetch LONG and LONG RAW columns, and also to fetch CLOB as string and BLOB
    as bytes.

.. method:: Cursor.var(typ, [size, arraysize, inconverter, outconverter, \
        typename, encoding_errors, bypass_decode, convert_nulls])

    Creates a :ref:`variable object <varobj>` with the specified
    characteristics. This method can be used for binding to PL/SQL IN and OUT
    parameters where the length or type cannot be determined automatically from
    the Python variable being bound. It can also be used in :ref:`input
    <inputtypehandlers>` and :ref:`output <outputtypehandlers>` type handlers.

    The ``typ`` parameter specifies the type of data that should be stored in the
    variable. This should be one of the :ref:`database type constants
    <dbtypes>`, :ref:`DB API constants <types>`, an object type returned from
    the method :meth:`Connection.gettype()` or one of the following Python
    types:

    .. list-table-with-summary::
        :header-rows: 1
        :class: wy-table-responsive
        :align: center
        :summary: The first column is the Python Type. The second column is the corresponding Database Type.

        * - Python Type
          - Database Type
        * - bool
          - :attr:`oracledb.DB_TYPE_BOOLEAN`
        * - bytes
          - :attr:`oracledb.DB_TYPE_RAW`
        * - datetime.date
          - :attr:`oracledb.DB_TYPE_DATE`
        * - datetime.datetime
          - :attr:`oracledb.DB_TYPE_DATE`
        * - datetime.timedelta
          - :attr:`oracledb.DB_TYPE_INTERVAL_DS`
        * - decimal.Decimal
          - :attr:`oracledb.DB_TYPE_NUMBER`
        * - float
          - :attr:`oracledb.DB_TYPE_NUMBER`
        * - int
          - :attr:`oracledb.DB_TYPE_NUMBER`
        * - str
          - :attr:`oracledb.DB_TYPE_VARCHAR`

    The ``size`` parameter specifies the length of string and raw variables and is
    ignored in all other cases. If not specified for string and raw variables,
    the value *4000* is used.

    The ``arraysize`` parameter specifies the number of elements the variable will
    have. If not specified the bind array size (usually *1*) is used. When a
    variable is created in an output type handler this parameter should be set
    to the cursor's array size.

    The ``inconverter`` and ``outconverter`` parameters specify methods used for
    converting values to/from the database. More information can be found in
    the section on :ref:`variable objects<varobj>`.

    The ``typename`` parameter specifies the name of a SQL object type and must be
    specified when using type :data:`oracledb.OBJECT` unless the type object
    was passed directly as the first parameter.

    The ``encoding_errors`` parameter specifies what should happen when decoding
    byte strings fetched from the database into strings. It should be one of
    the values noted in the builtin
    `decode <https://docs.python.org/3/library/stdtypes.html#bytes.decode>`__
    function.

    The ``bypass_decode`` parameter, if specified, should be passed as a
    boolean value. Passing a *True* value causes values of database types
    :data:`~oracledb.DB_TYPE_VARCHAR`, :data:`~oracledb.DB_TYPE_CHAR`,
    :data:`~oracledb.DB_TYPE_NVARCHAR`, :data:`~oracledb.DB_TYPE_NCHAR` and
    :data:`~oracledb.DB_TYPE_LONG` to be returned as bytes instead of str,
    meaning that python-oracledb does not do any decoding. See :ref:`Fetching raw
    data <fetching-raw-data>` for more information.

    The ``convert_nulls`` parameter, if specified, should be passed as a boolean
    value. Passing the value *True* causes the ``outconverter`` to be called
    when a null value is fetched from the database; otherwise, the
    ``outconverter`` is only called when non-null values are fetched from the
    database.

    For consistency and compliance with the PEP 8 naming style, the parameter
    ``encodingErrors`` was renamed to ``encoding_errors``. The old name will
    continue to work as a keyword parameter for a period of time.

    .. versionchanged:: 1.4.0

        The ``convert_nulls`` parameter was added.

    .. dbapimethodextension::

Cursor Attributes
=================

.. attribute:: Cursor.arraysize

    This read-write attribute can be used to tune the number of rows internally
    fetched and buffered by internal calls to the database when fetching rows
    from SELECT statements and REF CURSORS.  The value can drastically affect
    the performance of a query since it directly affects the number of network
    round trips between Python and the database.  For methods like
    :meth:`Cursor.fetchone()` and :meth:`Cursor.fetchall()` it does not change
    how many rows are returned to the application. For
    :meth:`Cursor.fetchmany()` it is the default number of rows to fetch.

    The attribute is only used for tuning row and SODA document fetches from
    the database.  It does not affect data inserts.

    Due to the performance benefits, the default ``Cursor.arraysize`` is *100*
    instead of the *1* that the Python DB API recommends.

    See :ref:`Tuning Fetch Performance <tuningfetch>` for more information.

.. attribute:: Cursor.bindvars

    This read-only attribute provides the bind variables used for the last
    statement that was executed on the cursor. The value will be either a list
    or a dictionary, depending on whether binding was done by position or
    name. Care should be taken when referencing this attribute. In particular,
    elements should not be removed or replaced.

    .. dbapiattributeextension::

.. attribute:: Cursor.connection

    This read-only attribute returns a reference to the connection object on
    which the cursor was created.

    .. dbapimethodextension:: It is mentioned in PEP 249 as an optional extension.

.. attribute:: Cursor.description

    This read-only attribute contains information about the columns used in a
    query. It is a sequence of :ref:`FetchInfo <fetchinfoobj>` objects, one per
    column. This attribute will be *None* for statements that are not SELECT or
    WITH statements, or if the cursor has not had :meth:`Cursor.execute()`
    invoked yet.

    .. versionchanged:: 1.4.0

        Previously, this attribute was a sequence of 7-tuples.  Each of these
        tuples contained information describing one query column: "(name, type,
        display_size, internal_size, precision, scale, null_ok)".

.. attribute:: Cursor.fetchvars

    This read-only attribute specifies the list of variables created for the
    last query that was executed on the cursor.  Care should be taken when
    referencing this attribute. In particular, elements should not be removed
    or replaced.

    .. dbapiattributeextension::

.. attribute:: Cursor.inputtypehandler

    This read-write attribute specifies a method called for each value that is
    bound to a statement executed on the cursor and overrides the attribute
    with the same name on the connection if specified. The method signature is
    handler(cursor, value, arraysize) and the return value is expected to be a
    variable object or *None* in which case a default variable object will be
    created. If this attribute is *None*, the default behavior will take place
    for all values bound to the statements.

    See :ref:`inputtypehandlers`.

    .. dbapiattributeextension::

.. attribute:: Cursor.lastrowid

    This read-only attribute returns the rowid of the last row modified by the
    cursor. If no row was modified by the last operation performed on the
    cursor, the value *None* is returned.

.. attribute:: Cursor.outputtypehandler

    This read-write attribute specifies a method called for each column that is
    to be fetched from this cursor. The method signature is
    handler(cursor, metadata) and the return value is expected to be a
    :ref:`variable object <varobj>` or *None* in which case a default variable
    object will be created. If this attribute is *None*, then the default
    behavior will take place for all columns fetched from this cursor.

    See :ref:`outputtypehandlers`.

    .. dbapiattributeextension::

    .. versionchanged:: 1.4.0

        The method signature was changed. The previous signature
        handler(cursor, name, default_type, length, precision, scale) will
        still work but is deprecated and will be removed in a future version.

.. attribute:: Cursor.prefetchrows

    This read-write attribute can be used to tune the number of rows that the
    Oracle Client library fetches when a SELECT statement is executed. This
    value can reduce the number of round-trips to the database that are
    required to fetch rows but at the cost of additional memory. Setting this
    value to *0* can be useful when the timing of fetches must be explicitly
    controlled.

    The attribute is only used for tuning row fetches from the database.  It
    does not affect data inserts.

    Queries that return LOBs and similar types will never prefetch rows, so the
    ``prefetchrows`` value is ignored in those cases.

    See :ref:`Tuning Fetch Performance <tuningfetch>` for more information.

    .. dbapimethodextension::

.. attribute:: Cursor.rowcount

    This read-only attribute specifies the number of rows that have currently
    been fetched from the cursor (for select statements) or that have been
    affected by the operation (for insert, update, delete, and merge
    statements). For all other statements the value is always *0*. If the
    cursor or connection is closed, the value returned is *-1*.

.. attribute:: Cursor.rowfactory

    This read-write attribute specifies a method to call for each row that is
    retrieved from the database. Ordinarily, a tuple is returned for each row
    but if this attribute is set, the method is called with the tuple that
    would normally be returned, and the result of the method is returned
    instead.

    See :ref:`rowfactories`.

    .. dbapiattributeextension::

.. attribute:: Cursor.scrollable

    This read-write boolean attribute specifies whether the cursor can be
    scrolled or not. By default, cursors are not scrollable, as the server
    resources and response times are greater than nonscrollable cursors. This
    attribute is checked and the corresponding mode set in Oracle when calling
    the method :meth:`Cursor.execute()`.

    .. dbapiattributeextension::

.. attribute:: Cursor.statement

    This read-only attribute provides the string object that was previously
    prepared with :meth:`Cursor.prepare()` or executed with
    :meth:`Cursor.execute()`.

    .. dbapiattributeextension::

.. attribute:: Cursor.warning

    This read-only attribute provides an :ref:`oracledb._Error<exchandling>`
    object giving information about any database warnings (such as PL/SQL
    compilation warnings) that were generated during the last call to
    :meth:`Cursor.execute()` or :meth:`Cursor.executemany()`. This value is
    automatically cleared on the next call to :meth:`Cursor.execute()` or
    :meth:`Cursor.executemany()`. If no warning was generated the value
    *None* is returned.

    See :ref:`plsqlwarning` for more information.

    .. dbapiattributeextension::

    .. versionadded:: 2.0.0
