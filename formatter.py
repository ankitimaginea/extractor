from config import Config


class DataFormatter():
    HEADERS = ['name', 'host_status', 'service_status', 'service_info']

    def __init__(self, master_data):
        self._master_data = master_data

    def get_formatted_data(self):
        header_str = ''
        for cell in DataFormatter.HEADERS:
            header_str = '{0}<td style="padding:2px; border:1px solid;text-align:center;"><b>{1}</b></td>'.format(
                header_str, cell)

        out_arr = [header_str]

        for hostname, host_data in self._master_data.items():
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
                    if data['active_checks_enabled'] == '0':
                        host_active_checks_enabled = '0'
                    if data['notifications_enabled'] == '0':
                        host_notifications_enabled = '0'

            row = [
                '<b>{0}</b>'.format(hostname),
                '<b>active_checks_enabled</b> = {0}<br/><br/> notifications_enabled = {1}'.format(
                    host_active_checks_enabled, host_notifications_enabled),
                '<b>active_checks_enabled 0</b> for {0} services<br/><br/> <b>notifications_enabled 0</b> for {1} services'.format(
                    len(service_active_checks_enabled_list), len(
                        service_notifications_enabled_list)
                ),
                '<b>active_checks_enabled 0 </b>for [{0}] services<br/><br/> <b>notifications_enabled 0 </b>for {1} services'.format(
                    ', '.join(service_active_checks_enabled_list), ', '.join(
                        service_notifications_enabled_list)
                )

            ]
            row_str = ''
            for cell in row:
                row_str = '{0}<td style = "padding: 2px;border: 1px solid;text-align: center;">{1}</td>'.format(
                    row_str, cell)

            out_arr.append(row_str)
        table = '<table >'
        for row in out_arr:
            table = '{0}<tr>{1}</tr>'.format(table, row)
        table = table + '</table>'
        return table
