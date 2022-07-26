import pandas as pd
from .models import FileStorage
import json


class Csv_handling:

    def check_format(self, file, format):
        data = pd.read_csv(file, sep=';')
        data_ = data.columns.to_list()
        revised_data_frame = []
        ultimate_data_frame = []
        unmatching_heads = []
        for f in format:
            revised_data_frame.append(f.lower().strip())

        for d in data_:
            if d.lower().strip() in revised_data_frame:
                ultimate_data_frame.append(d)
            else:
                unmatching_heads.append(d)
        return {
            'matched': ultimate_data_frame,
            'unmathced': unmatching_heads
        }

    def get_ultimate_list(self, file_id, format_data):
        file = FileStorage.objects.get(id=file_id)
        format_data = json.loads(format_data)
        print(format_data)
        updated_list = []
        with open(file.file.path, 'r') as stream:
            # print([x for x in format_data['matched']])
            dataframe = pd.read_csv(
                stream,
                delimiter=';',
            )
            dataframes = dataframe.columns.values.tolist()
            for f in format_data['matched']:
                for d in dataframes:
                    if d.lower().split() == f.lower().split():
                        updated_list.append(d)
                    else:
                        continue
            ultimate_list = [{'heading': x, 'data': []} for x in updated_list]

            for i in range(0, len(ultimate_list)):
                for d in dataframe:
                    if d == ultimate_list[i]['heading']:
                        print(True)
                        ultimate_list[i]['data'].append(
                            dataframe[d].to_list())
            stream.close()
            return ultimate_list
