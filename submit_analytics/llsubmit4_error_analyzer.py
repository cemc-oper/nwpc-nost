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


def get_record_field_value(record, name):
    if name == 'date':
        return record['date'].strftime("%Y-%m-%d")
    elif name == 'weekday':
        return record['date'].weekday()
    elif name == 'system':
        return get_system_from_path(record['info']['path'])
    elif name == 'date-hour':
        cur_datetime = record['date']
        cur_date = cur_datetime.date()
        zero_time = datetime.time(cur_datetime.hour)
        cur_hour = datetime.datetime.combine(cur_date, zero_time)
        return cur_hour.strftime("%Y-%m-%d %H:%M:%S")
    elif name == 'hour':
        return record['date'].hour
    else:
        raise Exception('name unsupported', name)


def info_handler(args):
    log_file_path = args.log_file_path

    command = "head -n 1 {log_file_path}".format(log_file_path=log_file_path)
    output_string, error_string = run_command(command)
    if len(error_string) > 0:
        result = {
            'app': 'llsubmit4_error_analyzer',
            'type': 'range',
            'timestamp': datetime.datetime.now().timestamp(),
            'error': 'head_command_error',
            'data': {
                'error_message': 'error in executing head command.',
                'output': {
                    'std_out': output_string,
                    'std_err': error_string
                },
                'request': {
                    'log_file_path': log_file_path,
                }
            }
        }
        print(json.dumps(result))
        return

    record = parse_error_log(output_string)
    start_date = record['date']

    command = "tail -n 1 {log_file_path}".format(log_file_path=log_file_path)
    output_string, error_string = run_command(command)
    if len(error_string) > 0:
        result = {
            'app': 'llsubmit4_error_analyzer',
            'type': 'range',
            'timestamp': datetime.datetime.now().timestamp(),
            'error': 'tail_command_error',
            'data': {
                'error_message': 'error in executing tail command.',
                'output': {
                    'std_out': output_string,
                    'std_err': error_string
                },
                'request': {
                    'log_file_path': log_file_path,
                }
            }
        }
        print(json.dumps(result))
        return

    record = parse_error_log(output_string)
    end_date = record['date']

    # with open(log_file_path, 'r') as log_file:
    #     for line in log_file:
    #         record = parse_error_log(line)
    #         print(record['date'])

    result = {
        'app': 'llsubmit4_error_analyzer',
        'type': 'info',
        'timestamp': datetime.datetime.now().timestamp(),
        'data': {
            'range': {
                'start_date_time': start_date.strftime('%Y-%m-%dT%H:%M:%S%Z'),
                'end_date_time': end_date.strftime('%Y-%m-%dT%H:%M:%S%Z')
            },
            'request': {
                'log_file_path': log_file_path,
            }
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
    try:
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

                count_result[get_record_field_value(record, count_type)] += 1

    except FileNotFoundError as e:
        result = {
            'app': 'llsubmit4_error_analyzer',
            'type': 'count',
            'error': 'file_not_found',
            'timestamp': datetime.datetime.now().timestamp(),
            'data': {
                'error_message': 'file is not found',
                'request': {
                    'log_file_path': log_file_path,
                    'begin_date': begin_date.strftime('%Y-%m-%d'),
                    'end_date': end_date.strftime('%Y-%m-%d'),
                    'count_type': count_type
                }
            }
        }
        print(json.dumps(result))
        return

    result = {
        'app': 'llsubmit4_error_analyzer',
        'type': 'count',
        'timestamp': datetime.datetime.now().timestamp(),
        'data': {
            'count_type': count_type,
            'begin_date': begin_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'count_result': count_result,
            'request': {
                'log_file_path': log_file_path,
                'begin_date': begin_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'count_type': count_type
            },
            'response': {
                'count_result': count_result,
            }
        }
    }

    print(json.dumps(result, indent=4))


def grid_handler(args):
    begin_date = args.begin_date
    end_date = args.end_date
    log_file_path = args.log_file_path
    x_type = args.x_type
    y_type = args.y_type

    if begin_date:
        begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    if end_date:
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    grid_result = dict()
    try:
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

                x_value = get_record_field_value(record, x_type)
                y_value = get_record_field_value(record, y_type)

                if x_value not in grid_result:
                    grid_result[x_value] = dict()
                if y_value not in grid_result[x_value]:
                    grid_result[x_value][y_value] = 0
                grid_result[x_value][y_value] += 1

    except FileNotFoundError as e:
        result = {
            'app': 'llsubmit4_error_analyzer',
            'type': 'grid',
            'error': 'file_not_found',
            'timestamp': datetime.datetime.now().timestamp(),
            'data': {
                'error_message': 'file is not found',
                'request': {
                    'log_file_path': log_file_path,
                }
            }
        }
        print(json.dumps(result))
        return

    result = {
        'app': 'llsubmit4_error_analyzer',
        'type': 'grid',
        'timestamp': datetime.datetime.now().timestamp(),
        'data': {
            'response': {
                'grid_result': grid_result,
            },
            'request': {
                'log_file_path': log_file_path,
                'x_type': x_type,
                'y_type': y_type,
                'begin_date': begin_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
            }
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

    info_parser = sub_parsers.add_parser('info', description="get log file info.")
    info_parser.add_argument("-f", "--file", help="log file path", dest="log_file_path", required=True)
    info_parser.add_argument("--pretty-print", help="print pretty result.", action="store_true")
    info_parser.set_defaults(func=info_handler)

    count_parser = sub_parsers.add_parser('count', description="count errors in error log file.")
    count_parser.add_argument("-f", "--file", help="log file path", dest="log_file_path", required=True)
    count_parser.add_argument("--begin-date", help="begin date, YYYY-MM-DD")
    count_parser.add_argument("--end-date", help="end date, YYYY-MM-DD")
    count_parser.add_argument("--begin-time", help="begin time, hh:mm:ss")
    count_parser.add_argument("--end-time", help="end time, hh:mm:ss")
    count_parser.add_argument("--type", dest="count_type", help="count type", required=True,
                              choices=['date', 'weekday', 'date-hour', 'hour', 'system', 'hour/weekday'])
    count_parser.set_defaults(func=count_handler)

    grid_parser = sub_parsers.add_parser('grid', description="get grid result.")
    grid_parser.add_argument("-f", "--file", help="log file path", dest="log_file_path", required=True)
    grid_parser.add_argument("--begin-date", help="begin date, YYYY-MM-DD")
    grid_parser.add_argument("--end-date", help="end date, YYYY-MM-DD")
    grid_parser.add_argument("--begin-time", help="begin time, hh:mm:ss")
    grid_parser.add_argument("--end-time", help="end time, hh:mm:ss")
    grid_parser.add_argument("--x-type", dest="x_type", help="x axis type", required=True, choices=['hour'])
    grid_parser.add_argument("--y-type", dest="y_type", help="y axis type", required=True, choices=['weekday', 'system'])
    grid_parser.set_defaults(func=grid_handler)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
