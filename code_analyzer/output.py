import csv
import os
import json


def make_output(file_output_format, report):
    """Make output to cli or file."""
    if not file_output_format:
        print('--------------------')
        print('Report:')
        print('--------------------')
        [print(f'"{tuple_[0]}" - {tuple_[1]}') for tuple_ in report]
        print('--------------------')
        return

    if file_output_format:
        file_name = f'code_analyzer_report.{file_output_format}'
        try:
            with open(os.path.join(os.getcwd(), file_name), 'w') as file_report:
                if file_output_format == 'txt':
                    [file_report.write(f'"{tuple_[0]}" - {tuple_[1]}\n') for tuple_ in report]
                elif file_output_format== 'json':
                    json.dump(dict(report), file_report)
                elif file_output_format == 'csv':
                    csv_writer = csv.writer(file_report, delimiter='-', lineterminator='\n')
                    [csv_writer.writerow(tuple_) for tuple_ in report]
        except PermissionError:
            raise Exception('Can\'t save to file in current directory.  Access is denied.')
