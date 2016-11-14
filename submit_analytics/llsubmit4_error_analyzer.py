import subprocess
import re
import datetime
import argparse
import json


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


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
        DESCRIPTION
            Analytic llsubmit4 error log.""")

    sub_parsers = parser.add_subparsers(title="sub commands", dest="sub_command")

    range_parser = sub_parsers.add_parser('range', description="get time range in error log file.")
    range_parser.add_argument("-f", "--file", help="log file path", dest="log_file_path")
    range_parser.add_argument("--pretty-print", help="print pretty result.", action="store_true")
    range_parser.set_defaults(func=range_handler)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()