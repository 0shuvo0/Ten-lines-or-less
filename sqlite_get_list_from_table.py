# coding: utf-8

'''
get_list_from_table() + get_dict_from_table() is 12 lines because of the
uniqueness test in the dict routine and because doing camelize() inline
would make the code too difficult to understand.
'''

import collections, sqlite3

db_filename = 'my.db'

def get_list_from_table(sqlite_connection, table_name):
    '''convert an sqlite database table into a list of namedtuples'''
    def camelize(s):  # 'aa_bb_cc_dd' --> 'AaBbCcDd'
        return ''.join(x.title() for x in s.split('_'))
    cursor = sqlite_connection.execute("SELECT * FROM {}".format(table_name))
    col_names = ' '.join(x[0] for x in cursor.description)
    nt = collections.namedtuple(camelize(table_name), col_names)
    return [nt(*x) for x in cursor.fetchall()]

def get_dict_from_table(sqlite_connection, table_name, key_col_name='id'):
    '''convert an sqlite database table into a dict of namedtuples
       useful for tables where each row has a unique primary key'''
    the_list = get_list_from_table(sqlite_connection, table_name)
    the_dict = {x._asdict()[key_col_name]: x for x in the_list}
    assert len(the_dict) == len(the_list), 'In {}, {} is not unique: {} {}'.format(
        table_name, key_col_name, len(the_dict), len(the_list))
    return the_dict

def get_services():
    with sqlite3.connect(db_filename) as conn:
        return get_dict_from_table(conn, 'service')

def get_employee_dict():
    with sqlite3.connect(db_filename) as conn:
        return get_dict_from_table(conn, 'employee', 'employee_id')

services = get_services()
employee_dict = get_employee_dict()

for dataset in [services, employee_dict]:
    if isinstance(dataset, dict):
        print('\n'.join(str(x) for x in dataset.itervalues()))
    else:
        print('\n'.join(str(x) for x in dataset))
    print('')
