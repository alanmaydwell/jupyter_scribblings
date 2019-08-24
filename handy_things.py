"""
Some handy functions. Intended to be used to interact with databases using Pandas
within a Jupyter notebook.
"""

import time
import pandas as pd
import cx_Oracle


def run_query(sql, connstr, params=(), maxrows=0):
    """Run SQL query and return the results - uses cx_Oracle
    """
    conn = cx_Oracle.connect(connstr)
    cursor = conn.cursor()
    cursor.execute(sql, params)
    if maxrows:
        results = cursor.fetchmany(maxrows)
    else:
        results = cursor.fetchall()
    conn.close()
    return results

def execute_sql(sql, connstr):
    """Execute sql. Also return any database error message"""
    conn = cx_Oracle.connect(connstr)
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
    except cx_Oracle.DatabaseError as e:
        message = str(e) 
    else:
        message = "PL/SQL procedure successfully completed."
    return message

def run_query_df(sql, connstr, params=()):
    """Run query and return results as dataframe"""
    conn = cx_Oracle.connect(connstr)
    df = pd.read_sql_query(sql, conn, params=params)
    conn.close()  
    return df

def run_query_chunk_df(sql, connstr, params=(), maxrows=20):
    """Run query and return results as dataframe but with number of rows limited"""
    conn = cx_Oracle.connect(connstr)
    #When chunksize parameter present pd.read_sql_query returns a generator rather than a dataframe
    chunks = pd.read_sql_query(sql, conn, params=params, chunksize=maxrows)
    #Get just the first chunk from the genearator (alternatively could iterate)
    df = next(chunks)
    conn.close()  
    return df 

def display_full_df(df, heading=""):
    """Display whole of data frame content - avoids auto truncation"""
    if heading:
        display(Markdown("#### " + str(heading)))
    with pd.option_context('display.max_columns', None, 'display.max_rows', None, 'display.max_colwidth', -1):
        display(df)
        
def nowstring():
    """Return current time/date as str"""
    return time.strftime("%H:%M:%S %d/%m/%Y")
