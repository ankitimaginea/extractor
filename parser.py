import json
from config import Config
from emailer import Emailer
from formatter import DataFormatter


class Parser():

    def __init__(self, input_file, output_file):
        self._input_file_name = input_file
        self._output_file = output_file
        self._temp_file = 'temp_refine_file.txt'

    def parse(self):
        master_data = self._create_blocks()
        return master_data

    def _create_blocks(self):
        '''
        create blocks as mentioned in block_headers variables,
        discard the rest
        '''
        temp_file = open(self._input_file_name, 'r')
        current_mode = Config.START
        matched_header = None
        master_data = {}
        for line in temp_file:
            if current_mode == Config.START:
                if line.find('{') > -1:
                    header = line.split('{')[0].strip()
                    if header in Config.BLOCK_HEADERS:
                        current_mode = Config.BLOCK
                        json_obj = {header: {}}
            elif current_mode == Config.BLOCK:
                if line.find('}') > -1:
                    current_mode = Config.START
                    if self._check_filter(json_obj):
                        # append only if passed by filters
                        master_data = self._reset_obj_by_header_key(
                            json_obj, master_data)
                else:
                    arr = line.split('=')
                    if(len(arr)) > 1 and arr[0].strip() in Config.LOOKUP_VALUES:
                        json_obj[header][arr[0].strip()] = arr[1].strip()
        temp_file.close()
        return master_data

    def _reset_obj_by_header_key(self, json_obj, master_data):
        temp_obj = {}
        for category, data_obj in json_obj.items():
            pass
        header = data_obj[Config.HEADER_KEY]
        try:
            group_obj_list = master_data[header]
        except KeyError, e:
            group_obj_list = []
            master_data[header] = group_obj_list

        temp_obj['type'] = category
        for key, value in data_obj.items():
            if key != Config.HEADER_KEY:
                temp_obj[key] = value
        group_obj_list.append(temp_obj)
        return master_data

    def _check_filter(self, json_obj):
        for _, data_obj in json_obj.items():
            pass
        and_result = True
        for and_filter_map in Config.FILTERS:
            or_result = False
            for key, value in and_filter_map.items():
                try:
                    or_result = (value in data_obj[key]) or or_result
                except KeyError, e:
                    pass
            and_result = and_result and or_result
        return and_result

    def _group_by_key(self, json_array):
        for data_obj in json_array:
            for title, json_obj in data_obj.items():
                print title, json_obj
        Config.GROUP_BY_KEY


if __name__ == '__main__':
    parser = Parser('data/status.dat', 'output_file')
    master_data = parser.parse()
    data_formatter = DataFormatter(master_data)
    message = data_formatter.get_formatted_data()
    emailer = Emailer()
    emailer.send_email('report', message, 'ankit.singh@imaginea.com')
