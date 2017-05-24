import sys
sys.path.append('.')
from tornado.gen import coroutine, Return
from dal.pxe_template_dal import PxeTemplateDal


class PxeTemplateModel(object):

    def __init__(self):
        self.dal = PxeTemplateDal()
        self.pt_id = 1
        self.ksp_id = 1
        self.pxe_name = ''
        self.boot_path = ''
        self.boot_file_name = ''

    #获取dhcp template
    @coroutine
    def get_pxe_templates(self):
        sql_str = 'select server_name,dm.server_ip,dm.manager_ip,mac_address,pxe_name,boot_path, \
        boot_file_name, kickstarts_profile_name,dhcp_next_server\
        from dhcp_map as dm ,pxe_template as pt,kickstarts as ks , dhcp_server as ds , server as s\
        where  s.pt_id = pt.pt_id and pt.ksp_id= ks.ksp_id  and ds.dhcp_server_id = s.dhcp_server_id and s.server_id = dm.server_id'


        result = yield self.dal.execute(sql_str)
        raise Return(result)


    #获取pxe 模板名称列表
    @coroutine
    def get_pxe_template_name_list(self):
        try:
            result = yield self.dal.select('*', None)
        except Exception as err:
            raise err
        else:
            raise Return(result)

    #获取对应的