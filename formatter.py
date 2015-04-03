from config import Config
from cache_decorator import memoized
import re


class DataFormatter():

    def __init__(self, master_data):
        self._master_data = master_data
        self._cache = {}

    @memoized
    def _key_func(self, line):
        matchObj = re.match(
            r'([a-z]*)(\d+)([a-z]*)', line, re.M | re.I)
        category = matchObj.group(1)
        number = matchObj.group(2)
        subindex = matchObj.group(3)
        return (category, int(number), subindex)

    def _sort_func(self, line1, line2):

        cat1, number1, subindex1 = self._key_func(line1)
        cat2, number2, subindex2 = self._key_func(line2)
        cmp_key1 = 10000
        cmp_key2 = 10000
        if cat1 > cat2:
            cmp_key1 = 20000
        elif cat1 < cat2:
            cmp_key2 = 20000

        cmp_key1 += number1 * 10
        cmp_key2 += number2 * 10
        if subindex1 > subindex2:
            cmp_key1 += 1
        else:
            cmp_key2 += 1
        return cmp(cmp_key1, cmp_key2)

    def _get_service_msg(self, check_list, for_active=True):
        check_length = len(check_list)
        if for_active:
            if check_length:
                return 'active check disabled : {0}'.format(check_length)
            else:
                return ''
        else:
            if check_length:
                return 'notification disabled : {0} services'.format(len(check_list))
            else:
                return ''

    def _get_detailed_service_msg(self, service_list, max_serivce_count):
        service_list_len = len(service_list)
        if service_list_len == 0:
            return ''
        if service_list_len == max_serivce_count:
            return 'ALL'
        elif service_list_len < Config.SERVICE_COUNT_THRESHOLD:
            return ','.join(service_list)
        return Config.DEFAULT_SERIVCE_MESSAGE

    def _get_host_msg(self, check_flag, for_active=True):
        if for_active:
            if check_flag == '0':
                return 'active check disabled'
            else:
                return ''
        else:
            if check_flag == '0':
                return 'notification check disabled'
            else:
                return 'NA'

    def get_formatted_data(self):
        header_str = ''
        for cell in Config.REPORT_HEADER:
            header_str = '{0}<td style="padding:2px; border:1px solid;text-align:center;"><b>{1}</b></td>'.format(
                header_str, cell)

        out_arr = [header_str]
        sorted_hostnames = sorted(self._master_data, cmp=self._sort_func)
        for hostname in sorted_hostnames:
            max_serivce_count = Config.MAX_SERVICE_COUNT[
                self._key_func(hostname)[0]]
            host_data = self._master_data[hostname]
            host_active_checks_enabled = '-'
            host_notifications_enabled = '-'

            service_active_checks_enabled_list = []
            service_notifications_enabled_list = []

            for data in host_data:
                if data['type'] == 'servicestatus':
                    if data['active_checks_enabled'] == '0':
                        service_active_checks_enabled_list.append(
                            data['service_description'])
                    if data['notifications_enabled'] == '0':
                        service_notifications_enabled_list.append(
                            data['service_description'])
                if data['type'] == 'hoststatus':
                    host_active_checks_enabled = data['active_checks_enabled']
                    host_notifications_enabled = data['notifications_enabled']

            row = [
                '<b>{0}</b>'.format(hostname),
                '<b>{0}<br/><br/>{1}'.format(
                    self._get_host_msg(host_active_checks_enabled),
                    self._get_host_msg(host_notifications_enabled, False)),
                '<b>{0}<br/><br/>{1}'.format(
                    self._get_service_msg(service_active_checks_enabled_list),
                    self._get_service_msg(
                        service_notifications_enabled_list, False)
                ),
                '{0}<br/><br/>{1}'.format(
                    self._get_detailed_service_msg(
                        service_active_checks_enabled_list, max_serivce_count),
                    self._get_detailed_service_msg(
                        service_notifications_enabled_list, max_serivce_count)
                )

            ]
            row_str = ''
            for cell in row:
                row_str = '{0}<td style = "padding: 2px;border: 1px solid;text-align: center;">{1}</td>'.format(
                    row_str, cell)

            out_arr.append(row_str)
        table = '<table  border="1" cellpadding="2" cellspacing="0" width="100%" >'
        for row in out_arr:
            table = '{0}<tr>{1}</tr>'.format(table, row)
        table = table + '</table>'
        report_div = '<div><p><b>{0}</b></p>{1}</div>'.format(
            Config.MAIL_HEADING, table)
        return report_div
