from config import Config
from decorator_utils import memoized
import re


class DataFormatter():

    def __init__(self, master_data):
        self._master_data = master_data

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

    def _get_service_msg(self, active_check_list, notification_check_list):
        msg = ['', '']
        one_set = False

        active_length = len(active_check_list)
        notif_length = len(notification_check_list)

        if active_length:
            msg[0] = 'active check disabled : {0}<br/><br/>'.format(
                active_length)
            one_set = True
        if notif_length:
            msg[1] = 'notification disabled : {0} services'.format(
                notif_length)
            one_set = True
        if not one_set:
            msg = ['NA', '']
        return '{0}{1}'.format(msg[0], msg[1])

    def _get_detailed_service_msg(self, active_service_list, notif_service_list,
                                  max_serivce_count):

        msg = ['', '']
        one_set = False

        active_length = len(active_service_list)
        notif_length = len(notif_service_list)

        if active_length:
            one_set = True
            if active_length == max_serivce_count:
                msg[0] = 'ALL'
            elif active_length < Config.SERVICE_COUNT_THRESHOLD:
                msg[0] = ','.join(active_service_list)
            else:
                msg[0] = '<a href="{0}">{1}</a>'.format(
                    Config.SERVICE_MESSAGE_LINK, Config.DEFAULT_SERIVCE_MESSAGE)
            msg[0] += '<br/><br/>'

        if notif_length:
            one_set = True
            if notif_length == max_serivce_count:
                msg[1] = 'ALL'
            elif notif_length < Config.SERVICE_COUNT_THRESHOLD:
                msg[1] = ','.join(notif_service_list)
            else:
                msg[1] = '<a href="{0}">{1}</a>'.format(
                    Config.SERVICE_MESSAGE_LINK, Config.DEFAULT_SERIVCE_MESSAGE)
        if not one_set:
            msg = ['NA', '']
        return '{0}{1}'.format(msg[0], msg[1])

    def _get_host_msg(self, active_check, notification_check):
        msg = ['', '']
        one_set = False
        if active_check == '0':
            msg[0] = 'active check disabled<br/><br/>'
            one_set = True
        if notification_check == '0':
            msg[1] = 'notification check disabled'
            one_set = True
        if not one_set:
            msg = ['NA', '']
        return '{0}{1}'.format(msg[0], msg[1])

    def get_formatted_data(self):
        sorted_hostnames = sorted(self._master_data, cmp=self._sort_func)
        if sorted_hostnames:
            report_div = self._format_data(sorted_hostnames)
        else:
            report_div = '<div><p><b>{0}</b></p>{1}</div>'.format(
                Config.MAIL_HEADING, Config.EMPTY_REPORT_MESSAGE)
        return report_div

    def _format_data(self, sorted_hostnames):
        header_str = ''
        for cell in Config.REPORT_HEADER:
            header_str = '{0}<td style="padding:10px; border:1px solid;text-align:center;"><b>{1}</b></td>'.format(
                header_str, cell)

        out_arr = [header_str]

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
                '{0}'.format(hostname),
                self._get_host_msg(
                    host_active_checks_enabled, host_notifications_enabled),
                self._get_service_msg(
                    service_active_checks_enabled_list, service_notifications_enabled_list),
                self._get_detailed_service_msg(
                    service_active_checks_enabled_list, service_notifications_enabled_list, max_serivce_count),
            ]
            row_str = ''
            for cell in row:
                row_str = '{0}<td style = "padding: 10px;border: 1px solid;text-align: center;">{1}</td>'.format(
                    row_str, cell)

            out_arr.append(row_str)
        table = '<table  border="1" cellpadding="2" cellspacing="0" width="100%" >'
        for row in out_arr:
            table = '{0}<tr>{1}</tr>'.format(table, row)
        table = table + '</table>'
        report_div = '<div><p><b>{0}</b></p>{1}</div>'.format(
            Config.MAIL_HEADING, table)
        return report_div
