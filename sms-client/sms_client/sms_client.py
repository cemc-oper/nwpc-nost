#!/usr/bin/env python3
import subprocess

import click


def run_cdp_command(command):
    echo_pipe = subprocess.Popen(["echo", command], stdout=subprocess.PIPE)
    cdp_pipe = subprocess.Popen(['cdp'], stdin=echo_pipe.stdout, stdout=subprocess.PIPE, shell=True)
    echo_pipe.stdout.close()
    cdp_output = cdp_pipe.communicate()[0]
    return cdp_output


@click.group()
def cli():
    """
    A command line client for SMS.
    """


@cli.command('load', help='load def')
@click.option('--name', help='sms server name', required=True)
@click.option('--user', help='sms server user', required=True)
@click.option('-d', '--def', 'def_file', required=True, type=click.Path(),
              help='the name of the file that contain the definitions')
def load(name, user, def_file):
    """
    Define, validate and send the suites to the SMS. Same to play(cdp) in sms.
    """
    click.echo("load {def_file}".format(def_file=def_file))
    command = "login {name} {user} 1; play {def_file}; exit".format(
        name=name, user=user, def_file=def_file
    )
    click.echo(run_cdp_command(command))
    return


@cli.command('delete', help='delete node(s)')
@click.option('--name', required=True, help='sms server name')
@click.option('--user', required=True, help='sms server user')
@click.option('--node', required=True, help='the name of the node to be deleted')
def delete(name, user, node):
    """
    Delete node(s) given. Same to cancel(cdp) in sms. By default, user -y option in cdp commands.
    """
    click.echo("delete {node}".format(node=node))
    command = "login {name} {user} 1; cancel -y {node}; exit".format(
        name=name, user=user, node=node
    )
    click.echo(run_cdp_command(command))
    return


@cli.command('replace', help='replace node(s)')
@click.option('--name', required=True, help='sms server name')
@click.option('--user', required=True, help='sms server user')
@click.option('-d', '--def', 'def_file', required=True, type=click.Path(),
              help='path to client definition file. '
                   'provides the definition of the new node.')
@click.option('-n', '--node', required=True,
              help='path to node. must exist in the client definition. '
                   'This is also the node we want to replace in the server')
def replace(name, user, def_file, node):
    """
    Replace the node given in the SMS.
    """
    click.echo("replace {node} with {def_file}".format(node=node, def_file=def_file))
    command = "login {name} {user} 1; play -r {node} {def_file}; exit".format(
        name=name, user=user, node=node, def_file=def_file
    )
    click.echo(run_cdp_command(command))
    return


if __name__ == "__main__":
    cli()
