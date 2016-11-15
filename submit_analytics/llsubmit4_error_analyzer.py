import subprocess
import re
import datetime
import argparse
import json
from collections import defaultdict


def get_system_from_path(path):
    if path == "/":
        return None
    if not path.startswith('/'):
        return None
    index = path.find('/', 1)
    return path[1: index]


def run_command(command):
    pipe = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error_output = pipe.communicate()
    output_string = None
    if output is not None:
        output_string = output.decode()
    error_output_string = None
    if error_output is not None:
        error_output_string = error_output.decode()
    return output_string, error_output_string


def parse_error_log(log_string):
    p = re.compile('^\[(.*)\]\[(.*)\](.*): (.*) (.*) (.*) (.*)$')
    m = p.match(log_string)
    date_string = m.group(1)
    command = m.group(2)
    message = m.group(3)
    job_script = m.group(4)
    path = m.group(5)
    total_tries = m.group(6)
    current_try_no = m.group(7)
    record = dict()
    record['date'] = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%Z')
    record['command'] = command
    record['message'] = message
    record['info'] = {
        'job_script': job_script,
        'path': path,
        'total_tries': total_tries,
        'current_try_no': current_try_no
    }
    return record


def range_handler(args):
    log_file_path = args.log_file_path

    command = "head -n 1 {log_file_path}".format(log_file_path=log_file_path)
    output_string, error_string = run_command(command)
    record = parse_error_log(output_string)
    start_date = record['date']

    command = "tail -n 1 {log_file_path}".format(log_file_path=log_file_path)
    output_string, error_string = run_command(command)
    parse_error_log(output_string)
    end_date = record['date']

    # with open(log_file_path, 'r') as log_file:
    #     for line in log_file:
    #         record = parse_error_log(line)
    #         print(record['date'])

    result = {
        'app': 'llsubmit4_error_analyzer',
        'type': 'range',
        'timestamp': datetime.datetime.now().timestamp(),
        'data': {
            'start_date_time': start_date.strftime('%Y-%m-%dT%H:%M:%S%Z'),
            'end_date_time': end_date.strftime('%Y-%m-%dT%H:%M:%S%Z')
        }
    }
    if args.pretty_print:
        print(json.dumps(result, indent=4))
    else:
        print(json.dumps(result))


def count_handler(args):
    begin_date = args.begin_date
    end_date = args.end_date
    log_file_path = args.log_file_path
    count_type = args.count_type

    if begin_date:
        begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    if end_date:
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    count_result = defaultdict(int)
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            record = parse_error_log(line)
            # check date
            if begin_date:
                if record['date'].date() < begin_date.date():
                    continue
            if end_date:
                if record['date'].date() >= end_date.date():
                    continue

            # check count_type
            if count_type == 'day':
                count_result[record['date'].strftime("%Y-%m-%d")] += 1
            elif count_type == 'weekday':
                count_result[record['date'].weekday()] += 1
            elif count_type == 'system':
                system = get_system_from_path(record['info']['path'])
                count_result[system] += 1
            else:
                raise Exception('count type unsupported', count_type)
    result = {
        'app': 'llsubmit4_error_analyzer',
        'type': 'count',
        'timestamp': datetime.datetime.now().timestamp(),
        'data': {
            'count_type': count_type,
            'begin_date': begin_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'count_result': count_result
        }
    }

    print(json.dumps(result, indent=4))


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
        DESCRIPTION
            Analytic llsubmit4 error log.""")

    sub_parsers = parser.add_subparsers(title="sub commands", dest="sub_command")

    range_parser = sub_parsers.add_parser('range', description="get time range in error log file.")
    range_parser.add_argument("-f", "--file", help="log file path", dest="log_file_path", required=True)
    range_parser.add_argument("--pretty-print", help="print pretty result.", action="store_true")
    range_parser.set_defaults(func=range_handler)

    count_parser = sub_parsers.add_parser('count', description="count errors in error log file.")
    count_parser.add_argument("-f", "--file", help="log file path", dest="log_file_path", required=True)
    count_parser.add_argument("--begin-date", help="begin date, YYYY-MM-DD")
    count_parser.add_argument("--end-date", help="end date, YYYY-MM-DD")
    count_parser.add_argument("--begin-time", help="begin time, hh:mm:ss")
    count_parser.add_argument("--end-time", help="end time, hh:mm:ss")
    count_parser.add_argument("--type", dest="count_type", help="count type", required=True,
                              choices=['day', 'weekday', 'system'])
    count_parser.set_defaults(func=count_handler)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()