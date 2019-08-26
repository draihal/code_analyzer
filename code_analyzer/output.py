import csv
import json
import logging
import os


def make_output_to_cli(report):
    """Make output to cli."""
    print('--------------------')
    print('Report:')
    print('--------------------')
    [print(f'"{tuple_[0]}" - {tuple_[1]}') for tuple_ in report]
    print('--------------------')
    return


def output_format_to_file(file_report, file_output_format, report):
    """Make output format for file."""
    if file_output_format == 'txt':
        [file_report.write(f'"{tuple_[0]}" - {tuple_[1]}\n') for tuple_ in report]
    elif file_output_format == 'json':
        json.dump(dict(report), file_report)
    elif file_output_format == 'csv':
        csv_writer = csv.writer(file_report, delimiter='-', lineterminator='\n')
        [csv_writer.writerow(tuple_) for tuple_ in report]


def make_output_to_file(file_output_format, report):
    """Make output to file."""
    file_name = f'code_analyzer_report.{file_output_format}'
    try:
        with open(os.path.join(os.getcwd(), file_name), 'w') as file_report:
            output_format_to_file(file_report, file_output_format, report)
    except PermissionError:
        logging.info('Can\'t save to file in current directory.  Access is denied.')
        raise Exception('Can\'t save to file in current directory.  Access is denied.')


def make_output(file_output_format, report):
    """Make output to cli or file."""
    return make_output_to_cli(report) if not file_output_format \
        else make_output_to_file(file_output_format, report)
