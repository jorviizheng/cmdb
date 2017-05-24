from __future__ import print_function
import sys
sys.path.append('.')
from handlers.base_handler import BaseHandler
from tornado.gen import coroutine, Return
from tornado.log import gen_log
from operator import eq
from tornado.options import options
import queries
from queries.pool import Connection,ConnectionBusyError,PoolConnectionException
from queries.pool import PoolFullError


class AsyncPgsql(BaseHandler):

    def __init__(self):

        pqsql_uri = queries.uri(options.pqsql_host, options.pqsql_port, options.pqsql_db, options.pqsql_user,
                                options.pqsql_password)

        self.pool = queries.TornadoSession(pqsql_uri, pool_max_size=options.pool_max_size, pool_idle_ttl=options.pool_idle_ttl)
        self.cur = ''

    @coroutine
    def execute(self, sql_str):
        try:
            self.cur = yield self.pool.query(sql_str)
        except Exception as err:
            gen_log.error('error sql:%s' % sql_str)
            gen_log.error('error:%s' % err)
            raise err
        else:
            if self.cur.count() == 0:
                raise Return(0)
            else:
                raise Return(self.cur.items())
        finally:
            self.cur.free()


    @coroutine
    def query_update(self, sql_str):
        try:
            self.cur = yield self.pool.query(sql_str)
        except Exception as err:
            gen_log.error('error sql:%s' % sql_str)
            gen_log.error('error:%s' % err)
            raise err
        else:
            raise Return(self.cur.count())
        finally:
            self.cur.free()

    @coroutine
    def _get_table_rows(self, table_name):
        allowed_keys = set()
        try:
            self.cur = yield self.pool.query(
                "SELECT column_name FROM information_schema.columns WHERE table_name = '%s'" % table_name)
        except Exception as err:
            gen_log.error('error:%s' % err)
            raise err
        else:
            for row in self.cur.items():
                allowed_keys.add(row['column_name'])
            raise Return(allowed_keys)
        finally:
            self.cur.free()

    @coroutine
    def _insert(self, table_name, row_dict, replace=False):
        allowed_keys = yield self._get_table_rows(table_name)
        keys = allowed_keys.intersection(row_dict)

        if len(row_dict) > len(keys):
            unknown_keys = set(row_dict) - allowed_keys
            print("skipping keys: %s", ", ".join(unknown_keys))

        columns = ", ".join(keys)
        values_template = ", ".join(["%s"] * len(keys))

        if replace:
            sql_str = "REPLACE INTO %s (%s) VALUES (%s)" % (
                table_name, columns, values_template)
        else:
            sql_str = "INSERT INTO %s (%s) VALUES (%s)" % (
                table_name, columns, values_template)
        try:
            values = tuple(row_dict[key] for key in keys)
        except Exception as err:
            raise err
        try:
            self.cur = yield self.pool.query(sql_str, values)
        except Exception as err:
            gen_log.error('error sql:%s' % sql_str)
            gen_log.error('error:%s' % err)
            raise err
        else:
            raise Return(self.cur.count())
        finally:
            self.cur.free()

    @coroutine
    def _update(self, table_name, row_dict, search_dict=None):
        allowed_keys = yield self._get_table_rows(table_name)
        keys = allowed_keys.intersection(row_dict)

        if len(row_dict) > len(keys):
            unknown_keys = set(row_dict) - allowed_keys
            print("skipping keys: %s", ", ".join(unknown_keys))
        set_columes = 'set '
        set_index = 0
        for key in keys:
            set_index += 1
            if set_index < len(row_dict):
                set_columes += "%s='%s'," % (key, row_dict[key])
            else:
                set_columes += "%s='%s'" % (key, row_dict[key])

        search_flag = 'where '
        if search_dict:
            if len(search_dict) > 1:
                index = 0
                for key in search_dict:
                    index += 1
                    if index != len(search_dict):
                        search_flag += "%s='%s' and " % (key, search_dict[key])
                    else:
                        search_flag += "%s='%s'" % (key, search_dict[key])
            elif len(search_dict) == 1:
                for key in search_dict:
                    search_flag += "%s='%s'" % (key, search_dict[key])
            else:
                search_flag = ''

        sql_str = "UPDATE  %s  %s  %s" % (
            table_name, set_columes, search_flag)
        gen_log.info(sql_str)
        try:
            self.cur = yield self.pool.query(sql_str)
        except Exception as err:
            gen_log.error('error sql:%s' % sql_str)
            gen_log.error('error:%s' % err)
            raise err
        else:
            raise Return(self.cur.count())
        finally:
            self.cur.free()

    @coroutine
    def _select(self, table_name, col_dict, search_dict=None, limit_dict=None, order=None):
        try:
            allowed_keys = yield self._get_table_rows(table_name)
        except Exception as err:
            raise err

        select_columes = ''
        if col_dict != '*':
            keys = allowed_keys.intersection(col_dict)
            if len(col_dict) > len(keys):
                unknown_keys = set(col_dict) - allowed_keys
                print("skipping keys: %s", ", ".join(unknown_keys))

            select_index = 0
            for key in keys:
                select_index += 1
                if select_index < len(keys):
                    select_columes += "%s," % key
                else:
                    select_columes += "%s" % key
        else:
            select_columes = '*'

        search_flag = ''
        if search_dict:
            if len(search_dict) > 1:
                index = 0
                for key in search_dict:
                    index += 1
                    if index != len(search_dict):
                        search_flag += "%s='%s' and " % (key, search_dict[key])
                    else:
                        search_flag += "%s='%s'" % (key, search_dict[key])
            elif len(search_dict) == 1:
                for key in search_dict:
                    search_flag += "%s='%s'" % (key, search_dict[key])
            else:
                search_flag = ''

        limit_flag = ''
        if limit_dict:
            limit_flag = 'limit %s offset %s' % (limit_dict['length'], limit_dict['start'])

        order_str = ''
        if order:
            order_str = 'order by %s %s' % (order['order_colume'], order['order_type'])

        if eq(search_flag, ''):
            sql_str = "select  %s from %s %s %s" % (
                select_columes, table_name, order_str, limit_flag)
        else:
            sql_str = "select  %s from %s  where %s %s %s" % (
                select_columes, table_name, search_flag, order_str, limit_flag)

        try:
            self.cur = yield self.pool.query(sql_str)
        except Exception as err:
            gen_log.error('error_sql:%s ' % sql_str)
            gen_log.error('error:%s ' % err)
            raise err
        else:
            if self.cur.count() == 0:
                raise Return(0)
            else:
                raise Return(self.cur.items())
        finally:
            self.cur.free()

    @coroutine
    def _delete(self, table_name, search_dict=None):
        search_flag = 'where '
        if search_dict:
            if len(search_dict) > 1:
                index = 0
                for key in search_dict:
                    index += 1
                    if index != len(search_dict):
                        search_flag += "%s='%s' and " % (key, search_dict[key])
                    else:
                        search_flag += "%s='%s'" % (key, search_dict[key])
            elif len(search_dict) == 1:
                for key in search_dict:
                    search_flag += "%s='%s'" % (key, search_dict[key])
            else:
                raise Return({'status': 'error'})

        sql_str = "delete from  %s %s" % (table_name, search_flag)

        try:
            self.cur = yield self.pool.query(sql_str)
        except Exception as err:
            raise err
        else:
            raise Return(self.cur.count())
        finally:
            self.cur.free()

