import json
import subprocess
import os
from config import Config


class Parser():

    def __init__(self):
        self.file_lines = []

    def _get_file_lines(self):
        p = subprocess.Popen(['ssh', 'root@opsice1a.ord.app.dy', 'cat',
                              '/var/spool/icinga/status.dat'], stdout=subprocess.PIPE)
        out, err = p.communicate()
        lines = out.split('\n')
        return lines

    def _get_file_lines_local(self):
        abs_dir = os.path.dirname(__file__)
        source_file_name = os.path.join(abs_dir, 'data/status.dat')
        f = open(source_file_name)
        return [line for line in f.readlines()]

    def parse(self):
        if Config.USE_LOCAL_FILE:
            file_lines = self._get_file_lines_local()
        else:
            file_lines = self._get_file_lines()
        master_data = self._create_blocks(file_lines)
        return master_data

    def _create_blocks(self, file_lines):
        '''
        create blocks as mentioned in block_headers variables,
        discard the rest
        '''
        current_mode = Config.START
        matched_header = None
        master_data = {}
        for line in file_lines:
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
