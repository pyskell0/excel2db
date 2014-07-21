from pprint import pprint
import re
import json
from db import db
from web.utils import storage
import xlrd
import config

with open(config.metadata_file) as f:
    # column metadatas
    table_metas = json.load(f)
    table_name = table_metas['table']
    data_file_path= table_metas['file_path']
    col_metas = table_metas['columns']

book = xlrd.open_workbook(data_file_path)
table = book.sheet_by_index(0)
num_of_rows = table.nrows


tmp_col_metas = [None] * len(table.row_values(0))
for n, col in enumerate(table.row_values(0)):
    if col in col_metas.keys():
        tmp_col_metas[n] = col_metas[col]


def _float(val):
    if val is None:
        return None

    if type(val) is float:
        return val

    return float(val) if type(val) in [str, unicode] else val

def _int(val):
    if val is None:
        return None
    if type(val) is int:
        return val

    val = _float(val)

    if type(val) is float or type(val) is long:
        return int(round(val,0))

def _unicode(val):
    if val is None:
        return None
    if type(val) is unicode:
        return val.strip()

    if type(val) in [float, int]:
        if val%1 == 0:
            val = int(val)
        return unicode(val).strip()
    if type(val) is str:
        return val.decode('utf8').strip()

type_converters = {
    'int': _int,
    'float': _float,
    'varchar': _unicode,
}

def get_foreign_key_value(tab_name, col_name, col_val, id='id'):
    sql = 'select ' + id + ' from ' + tab_name + ' where ' + col_name + '=$' + col_name
    rows = db.query(sql, vars={col_name: col_val}).list()
    if len(rows) == 0:
        # MODIFIED
        sql = 'insert into ' + tab_name + ' (' + col_name + ') values ($' + col_name + ')'
        db.query(sql, vars={col_name: col_val})
        rs = db.query('select max(' + id +') id from ' + tab_name)
        return rs[0].id
        #raise Exception("table -> column: [%s -> %s] = '%s'. return []")
    else:
        return _int(rows[0][id])

def deal_col(row_num, col_num, val):
    meta = tmp_col_metas[col_num]
    msg = 'row, col: [%s, %s] -> %s' % (row_num, col_num, val)
    if not meta['nullable'] and val is None:
        raise Exception("can't be null. " + msg)
    
    if 'many_to_many' in meta and val is not None:
        fk_tab = meta['many_to_many']
        val_in = get_foreign_key_value(fk_tab['table'], fk_tab['column'], val)
        val_in = type_converters[fk_tab['key_type']](val_in)
        sql = 'insert into ' + fk_tab['inner_table'] +\
            '(' + fk_tab['key'] +', ' + meta['key'] + ') values ($' + fk_tab['key'] +', $' + meta['key'] + ')'

        return '__m2m', (sql, {fk_tab['key']: val_in}, meta)

    if 'foreign key' in meta and val is not None:
        fk_tab = meta['foreign key']
        val = get_foreign_key_value(fk_tab['table'], fk_tab['column'], val)

    val = type_converters[meta['type']](val)
    return meta['column'], val


def get_vars_list(id='id'):
    for row_ind in xrange(1, num_of_rows):
        row = table.row_values(row_ind)
        vars_ = []
        for col_ind, val in enumerate(row):
            if tmp_col_metas[col_ind] is not None:
                vars_.append(deal_col(row_ind, col_ind, val))

        vars_ = dict(vars_)
        fin_keys = filter(lambda x: not x.startswith('__'), vars_.keys())
        fin_vars = {}
        for k in fin_keys:
            fin_vars[k] = vars_[k]
        sql = 'insert into ' + table_name + ' (' + ', '.join(map(lambda x: '`' + x + '`', fin_keys)) + ') values ($' + ', $'.join(fin_keys) + ')'
        pprint(fin_vars)
        pprint(table_name)
        try:
            #import pdb; pdb.set_trace()
            db.query(sql, vars=fin_vars)
        except Exception, e:
            import traceback
            print e
            traceback.print_exc()
            match = re.compile("Duplicate entry.+for key '(\w+)'").match(e.args[1])
            if match:
                key = match.group(1)
                sets = ', '.join(map(lambda x: x + ' = $' + x, fin_keys))
                sql = 'update ' + table_name + ' set ' + sets + ' where ' + key +' = $' + key
                db.query(sql, vars=fin_vars)
        else:
            if len(fin_keys) < len(vars_):
                rs = db.query('select max(id) id from ' + table_name)
                id = rs[0].id
                m2m_sql, m2m_vars, meta = vars_['__m2m']
                m2m_vars[meta['key']] = id
                db.query(m2m_sql, vars=m2m_vars)

if __name__ == '__main__':
    get_vars_list()

