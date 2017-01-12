#!/cma/g3/wangdp/usr/local/bin/python3
import argparse
import subprocess


def run_cdp_command(command):
    echo_pipe = subprocess.Popen(["echo", command], stdout=subprocess.PIPE)
    cdp_pipe = subprocess.Popen(['cdp'], stdin=echo_pipe.stdout, stdout=subprocess.PIPE, shell=True)
    echo_pipe.stdout.close()
    cdp_output = cdp_pipe.communicate()[0]
    return cdp_output


def delete_handler(node, name=None, user=None):
    print("delete {node}".format(node=node))
    command = "login {name} {user} 1; cancel -y {node}; exit".format(
        name=name, user=user, node=node
    )
    print(run_cdp_command(command))
    return


def load_handler(def_file, name=None, user=None):
    print("load {def_file}".format(def_file=def_file))
    command = "login {name} {user} 1; play {def_file}; exit".format(
        name=name, user=user, def_file=def_file
    )
    print(run_cdp_command(command))
    return


def replace_handler(node, def_file, name=None, user=None):
    print("replace {node} with {def_file}".format(node=node, def_file=def_file))
    command = "login {name} {user} 1; play -r {node} {def_file}; exit".format(
        name=name, user=user, node=node, def_file=def_file
    )
    print(run_cdp_command(command))
    return


def main():
    parser = argparse.ArgumentParser(description="SMS client tool.")
    login_parser = argparse.ArgumentParser(add_help=False)
    login_parser.add_argument("-n", "--name", help="sms host name")
    login_parser.add_argument("-u", "--user", help="sms user name")

    subparsers = parser.add_subparsers(title='sub commands',  dest='sub_command')

    # delete
    parser_delete = subparsers.add_parser('delete',
                                          parents=[login_parser],
                                          description="Delete node(s) given. Same to cancel(cdp) in sms."
                                                      "By default, user -y option in cdp commands.")
    parser_delete.add_argument('node', help='The name of the node to be deleted')

    # load
    parser_load = subparsers.add_parser("load",
                                        parents=[login_parser],
                                        description="Define, validate and send the suites to the SMS. "
                                                    "Same to play(cdp) in sms.")
    parser_load.add_argument('def_file', help='The name of the file that contain the definitions.')

    # replace
    parser_replace = subparsers.add_parser("replace",
                                           parents=[login_parser],
                                           description="Replace the node given in the SMS")
    parser_replace.add_argument('node',
                                help='path to node. must exist in the client definition. '
                                     'This is also the node we want to replace in the server')
    parser_replace.add_argument('def_file', help='path to client definition file. '
                                                 'provides the definition of the new node')

    args = parser.parse_args()

    if args.sub_command == 'delete':
        delete_handler(args.node, name=args.name, user=args.user)
    elif args.sub_command == 'load':
        load_handler(args.def_file, name=args.name, user=args.user)
    elif args.sub_command == 'replace':
        replace_handler(args.node, args.def_file, name=args.name, user=args.user)


if __name__ == "__main__":
    main()