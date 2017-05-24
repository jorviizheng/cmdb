import sys
sys.path.append('.')
from tornado.gen import coroutine, Return
from tornado.log import gen_log
from dal.server_dal import ServerDal


class ServerModel(object):

    def __init__(self):
        self.dal = ServerDal()
        self.server_id = 1
        self.idc_id = 1
        self.pt_id = 1
        self.dhcp_server_id = 1
        self.server_name = ''
        self.root_password = ''
        self.manager_ip = ''
        self.server_ip = ''
        self.server_group = ''
        self.server_type = ''
        self.system_type = ''
        self.tag = ''
        self.status = ''
        self.machine_type = ''
        self.sn = ''
        self.cpu = ''
        self.memory = ''
        self.hardisk = ''
        self.raid = ''
        self.rack_type = ''

    def get_model_json(self):
        return {
            self.dal.idc_id: self.idc_id,
            self.dal.pt_id: self.pt_id,
            self.dal.dhcp_server_id: self.dhcp_server_id,
            self.dal.server_name: self.server_name,
            self.dal.root_password: self.root_password,
            self.dal.manager_ip: self.manager_ip,
            self.dal.server_ip: self.server_ip,
            self.dal.server_group: self.server_group,
            self.dal.server_type: self.server_type,
            self.dal.system_type: self.system_type,
            self.dal.tag: self.tag,
            self.dal.status: self.status,
            self.dal.machine_type: self.machine_type,
            self.dal.sn: self.sn,
            self.dal.cpu: self.cpu,
            self.dal.memory: self.memory,
            self.dal.hardisk: self.hardisk,
            self.dal.raid: self.raid,
            self.dal.rack_type: self.rack_type
        }

    @coroutine
    def add_server(self, add_dict):
        col_dict = {
            self.dal.manager_ip: self.dal.manager_ip
        }
        search_dict = {
            self.dal.manager_ip: add_dict[self.dal.manager_ip]
        }
        duplicate_server = yield self.dal.select(col_dict, search_dict)
        if duplicate_server != 0:
            raise Exception('Server Exist')
        else:
            # add_dict = self.get_model_json()
            result = yield self.dal.insert(add_dict)
            raise Return(result)

    @coroutine
    def get_tag_by_id(self):
        col_dict = {
            self.dal.tag: self.dal.tag
        }
        search_dict = {
            self.dal.server_id: self.server_id
        }
        result = yield self.dal.select(col_dict, search_dict)
        if result:
            result = result[0][self.dal.tag]
        raise Return(result)

    @coroutine
    def get_server_list(self,limit_dict=None, order_dict=None):
        col_dict = '*'
        result = yield self.dal.select(col_dict,None,limit_dict, order_dict)
        raise Return(result)

    @coroutine
    def get_server_total(self):
        result = yield self.dal.select('*', None, None)
        if result != 0:
            result = len(result)

        raise Return(result)

    @coroutine
    def update_server(self, update_dict=None, search_dict=None):
        if not update_dict:
            update_dict = self.get_model_json()
        if not search_dict:
            search_dict = {
                self.dal.manager_ip: self.manager_ip
            }
        result = yield self.dal.update(update_dict, search_dict)
        raise Return(result)

    @coroutine
    def update_server_name(self, old_name):
        update_dict = self.get_model_json()
        search_dict = {
            self.dal.server_name: old_name
        }
        result = yield self.dal.update(update_dict,search_dict)
        raise Return(result)

    @coroutine
    def get_server_by_manager_ip(self):
        search_dict = {
            self.dal.manager_ip: self.manager_ip
        }
        result = yield self.dal.select('*', search_dict)
        if result != 0:
            result = result[0]
        raise Return(result)

    @coroutine
    def get_id_by_name(self):
        col_dict = {
            self.dal.server_id:self.dal.server_id
        }
        search_dict = {
            self.dal.server_name:self.server_name
        }
        result = yield self.dal.select(col_dict,search_dict)
        if result != 0:
            result = result[0][self.dal.server_id]
        raise Return(result)

    @coroutine
    def get_server_name_list(self):
        result = yield self.dal.select('*', None)
        raise Return(result)

    @coroutine
    def get_server_ip_by_name(self):
        search_dict = {
            self.dal.server_name: self.server_name
        }
        result = yield self.dal.select('*', search_dict)
        if result != 0:
            result = result[0][self.dal.server_ip]
        raise Return(result)

    @coroutine
    def get_server_by_name(self):
        search_dict = {
            self.dal.server_name: self.server_name
        }
        result = yield self.dal.select('*', search_dict)
        if result != 0:
            result = result[0]
        raise Return(result)

    @coroutine
    def delete_server_by_name(self):
        search_dict = {
            self.dal.server_name:self.server_name
        }
        result = yield self.dal.delete(search_dict)
        raise Return(result)

    @coroutine
    def get_server_for_tag(self, search_str):

        sql_str = "select * from %s where %s in (%s)" % (self.dal.table_name, self.dal.server_id, search_str)
        try:
            result = yield self.dal.execute(sql_str)
        except Exception as err:
            gen_log.error(err)
            raise err
        else:
            raise Return(result)

    @coroutine
    def get_server(self, col_dict=None, search_dict=None, limit_dict=None):
        if not col_dict:
            col_dict = '*'

        try:
            result = yield self.dal.select(col_dict,search_dict,limit_dict)
        except Exception as err:
            gen_log.error(err)
            raise err
        else:
            raise Return(result)

    #更新server tag标签
    @coroutine
    def update_tag(self, new_tags):
        update_dict = {
            self.dal.tag: new_tags
        }
        search_dict = {
            self.dal.server_id: self.server_id
        }
        try:
            result = yield self.dal.update(update_dict, search_dict)
        except Exception as err:
            gen_log.error(err)
            raise err
        else:
            raise Return(result)

    #获取服务器总数以及状态不正常的服务器数量
    @coroutine
    def get_servers_count(self):
        try:
            total_server_sql = 'select count(*)  from server'
            total_count = yield self.dal.execute(total_server_sql)

            error_server_sql = 'select count(*) from server where status != \'运行正常\''
            error_count = yield self.dal.execute(error_server_sql)

            result = dict()
            result['total_count'] = total_count if total_count == 0 else total_count[0]['count']
            result['error_count'] = error_count if error_count == 0 else error_count[0]['count']
        except Exception as error:
            gen_log.error(error)
            raise error
        else:
            raise Return(result)