from __future__ import print_function

from tornado.testing import AsyncTestCase, AsyncHTTPClient,gen_test
from tornado.escape import json_encode
from jinja2 import Template
import os
TEST_URL = "http://127.0.0.1:8085/provison/v1/server"



class TempateTest(AsyncTestCase):

    @gen_test(timeout=60)
    def test_add(self):

        post_data = {"server_id":17,"server_name":"slave23","manager_ip":"172.16.250.23","ilo4_user_name":"admin","ilo4_user_passwd":"cGFzc3dvcmQ=","server_ip":"172.16.251.106","server_group":"test","server_idc":"成都","pt_id":2}
        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch(TEST_URL, method='PUT', body=json_encode(post_data))
        print(response.body)

    @gen_test(timeout=6)
    def test_template(self):
        file_path = os.path.join(os.path.dirname(__file__), "../templates/dhcpd.conf.template")
        template_file = open(file_path)
        try:
            template_buffer = template_file.read()
        except FileNotFoundError as err:
            raise err
        finally:
            template_file.close()

        template = Template(template_buffer)
        # template_values = [C:98:EC:2F:EE:7C', 'pxe_name': 'centos7.0', 'boot_path': '/var/lib/tftpboot/uefi/grub/CentOS7.0', 'boot_file_name': 'bootx64.efi', 'kickstarts_profile_name': 'centos7.0.ks', 'dhcp_subnet': '172.16.251.0', 'dhcp_netmask': '255.255.255.0', 'dhcp_routers': '172.16.251.1', 'dhcp_domain_name': 'idc-chengdu.wanda.com', 'dhcp_domain_name_servers': '172.16.251.20', 'dhcp_next_server': '172.16.251.30', 'dhcp_server_ip': '172.16.251.30', 'dhcp_range': '172.16.251', 'dhcp_range_start': 100, 'dhcp_range_end': 254, 'dhcp_config_path': '/etc/dhcp'}, {'server_ip': '172.16.251.112', 'manager_ip': '172.16.250.22', 'mac_address': '1C:98:EC:1B:62:30', 'pxe_name': 'centos7.2_wanda_20170324', 'boot_path': '/var/lib/tftpboot/uefi/grub/CentOS7.2_wanda_20170324', 'boot_file_name': 'bootx64.efi', 'kickstarts_profile_name': 'centos7.2_wanda_20170324.ks', 'dhcp_subnet': '172.16.251.0', 'dhcp_netmask': '255.255.255.0', 'dhcp_routers': '172.16.251.1', 'dhcp_domain_name': 'idc-chengdu.wanda.com', 'dhcp_domain_name_servers': '172.16.251.20', 'dhcp_next_server': '172.16.251.30', 'dhcp_server_ip': '172.16.251.30', 'dhcp_range': '172.16.251', 'dhcp_range_start': 100, 'dhcp_range_end': 254, 'dhcp_config_path': '/etc/dhcp'}, {'server_ip': '172.16.251.124', 'manager_ip': '172.16.250.24', 'mac_address': '1C:98:EC:2F:EE:7C', 'pxe_name': 'centos7.0', 'boot_path': '/var/lib/tftpboot/uefi/grub/CentOS7.0', 'boot_file_name': 'bootx64.efi', 'kickstarts_profile_name': 'centos7.0.ks', 'dhcp_subnet': '172.16.251.0', 'dhcp_netmask': '255.255.255.0', 'dhcp_routers': '172.16.251.1', 'dhcp_domain_name': 'idc-chengdu.wanda.com', 'dhcp_domain_name_servers': '172.16.251.20', 'dhcp_next_server': '172.16.251.30', 'dhcp_server_ip': '172.16.251.30', 'dhcp_range': '172.16.251', 'dhcp_range_start': 100, 'dhcp_range_end': 254, 'dhcp_config_path': '/etc/dhcp'}, {'server_ip': '172.16.251.112', 'manager_ip': '172.16.250.22', 'mac_address': '1C:98:EC:1B:62:30', 'pxe_name': 'centos7.2_wanda_20170324', 'boot_path': '/var/lib/tftpboot/uefi/grub/CentOS7.2_wanda_20170324', 'boot_file_name': 'bootx64.efi', 'kickstarts_profile_name': 'centos7.2_wanda_20170324.ks', 'dhcp_subnet': '172.16.251.0', 'dhcp_netmask': '255.255.255.0', 'dhcp_routers': '172.16.251.1', 'dhcp_domain_name': 'idc-chengdu.wanda.com', 'dhcp_domain_name_servers': '172.16.251.20', 'dhcp_next_server': '172.16.251.30', 'dhcp_server_ip': '172.16.251.30', 'dhcp_range': '172.16.251', 'dhcp_range_start': 100, 'dhcp_range_end': 254, 'dhcp_config_path': '/etc/dhcp'}, {'server_ip': '172.16.251.123', 'manager_ip': '172.16.250.23', 'mac_address': '1C:98:EC:2F:3D:58', 'pxe_name': 'redhat7.2_wanda_20170324', 'boot_path': '/var/lib/tftpboot/uefi/grub/Redhat7.2_wanda_20170324', 'boot_file_name': 'bootx64.efi', 'kickstarts_profile_name': 'redhat7.2_wanda_20170324.ks', 'dhcp_subnet': '172.16.251.0', 'dhcp_netmask': '255.255.255.0', 'dhcp_routers': '172.16.251.1', 'dhcp_domain_name': 'idc-chengdu.wanda.com', 'dhcp_domain_name_servers': '172..16.251', 'dhcp6.251.123']
        template_values = '123'


        print(template.render(hosts=template_values))