# coding=utf-8
import os
import subprocess
import yaml
import click

from nwpc_hpc_model.loadleveler import QueryCategory, QueryCategoryList, QueryModel
from nwpc_hpc_model.loadleveler import record_parser
from nwpc_hpc_model.loadleveler import value_saver
from nwpc_hpc_model.loadleveler.filter_condition import get_property_data


config_file_name = "llclient.config.yaml"
default_config_file_path = os.path.join(os.path.dirname(__file__), "conf", config_file_name)


def get_config(config_file_path):
    """
    :param config_file_path: path of config file, which should be a YAML file.

    :return: config dict loading from config file.
    """
    config = None
    if not config_file_path:
        config_file_path = default_config_file_path
    with open(config_file_path, 'r') as f:
        config = yaml.load(f)
    return config


def get_user_name() -> str:
    if 'USER' in os.environ:
        return os.environ["USER"]
    else:
        cmquota_command = "whoami"
        pipe = subprocess.Popen([cmquota_command], stdout=subprocess.PIPE, shell=True)
        return pipe.communicate()[0].decode().rstrip()


def build_category_list(category_list_config):
    category_list = QueryCategoryList()
    for an_item in category_list_config:
        category = QueryCategory(
            category_id=an_item['id'],
            display_name=an_item['display_name'],
            label=an_item['display_name'],
            record_parser_class=getattr(record_parser, an_item['record_parser_class']),
            record_parser_arguments=tuple(an_item['record_parser_arguments']),
            value_saver_class=getattr(value_saver, an_item['value_saver_class']),
            value_saver_arguments=tuple(an_item['value_saver_arguments'])
        )
        category_list.append(category)
    return category_list


def run_llq_detail_command(command="/usr/bin/llq -l", params="-u nwp") -> str:
    """
    run llq detail command, default is llq -l.

    :param command:
    :param params:
    :return: command result string
    """
    pipe = subprocess.Popen([command + " " + params], stdout=subprocess.PIPE, shell=True)
    output = pipe.communicate()[0]
    output_string = output.decode()
    return output_string


def get_llq_detail_query_response(config, params=""):
    """
    get response of llq detail query.

    :param config: config dict
        {
            category_list: a list of categories
                [
                    {
                        id: "llq.id",
                        display_name: "Id",
                        label: "Job Step Id",
                        record_parser_class: "DetailLabelParser",
                        record_parser_arguments: ["Job Step Id"],
                        value_saver_class: "StringSaver",
                        value_saver_arguments: []
                    }
                ]
    :param params:
    :return: model dict, see nwpc_hpc_model_loadleveler.query_model.QueryModel.to_dict()
        {
            items: job info items, see nwpc_hpc_model_loadleveler.query_item.QueryItem.to_dict()
        }

    """
    output_lines = run_llq_detail_command(params=params).split("\n")
    category_list = build_category_list(config['category_list'])

    model = QueryModel.build_from_category_list(output_lines, category_list)
    model_dict = model.to_dict()
    return model_dict


@click.group()
def cli():
    """
    A command line tool for Loadleveler.
    """


@cli.command('query', short_help='llq short format')
@click.option('--config-file', help="config file path")
@click.option('-u', '--user-list', multiple=True, help="user list")
@click.option('-c', '--class-list', multiple=True, help="class list")
@click.option('-p', '--params', default="", help="llq params")
def query(config_file, user_list, class_list, params):
    """
    Query jobs in LoadLeveler and show in a simple format.
    """
    config = get_config(config_file)

    if params is None:
        params = ''
    if user_list:
        params += ' -u {user_list}'.format(user_list=" ".join(user_list))
    if class_list:
        params += ' -c {class_list}'.format(class_list=" ".join(class_list))

    model_dict = get_llq_detail_query_response(config, params)

    max_class_length = 0
    max_owner_length = 0
    for an_item in model_dict['items']:
        job_class = get_property_data(an_item, "llq.class")
        if len(job_class) > max_class_length:
            max_class_length = len(job_class)
        job_owner = get_property_data(an_item, "llq.owner")
        if len(job_owner) > max_owner_length:
            max_owner_length = len(job_owner)

    for an_item in model_dict['items']:
        job_id = get_property_data(an_item, "llq.id")
        job_class = get_property_data(an_item, "llq.class")
        job_owner = get_property_data(an_item, "llq.owner")
        job_script = get_property_data(an_item, "llq.job_script")
        job_status = get_property_data(an_item, "llq.status")
        click.echo("{job_id} {job_status} {job_class} {job_owner} {job_script}".format(
            job_id=click.style(job_id, bold=True),
            job_class=click.style(("{job_class: <" + str(max_class_length) + "}").format(job_class=job_class), fg='blue'),
            job_owner=click.style(("{job_owner: <" + str(max_owner_length) + "}").format(job_owner=job_owner), fg='cyan'),
            job_script=job_script,
            job_status=click.style("{job_status: <2}".format(job_status=job_status), fg='yellow'),
        ))


@cli.command('detail', short_help='llq detail format')
@click.option('--config-file', help="config file path")
@click.option('-u', '--user-list', multiple=True, help="user list")
@click.option('-c', '--class-list', multiple=True, help="class list")
@click.option('-p', '--params', default="", help="llq params")
def detail(config_file, user_list, class_list, params):
    """
    Query jobs in LoadLeveler and show in a detailed format.
    """
    config = get_config(config_file)

    if params is None:
        params = ''
    if user_list:
        params += ' -u {user_list}'.format(user_list=" ".join(user_list))
    if class_list:
        params += ' -c {class_list}'.format(class_list=" ".join(class_list))

    model_dict = get_llq_detail_query_response(config, params)

    for an_item in model_dict['items']:
        job_id = get_property_data(an_item, "llq.id")
        job_class = get_property_data(an_item, "llq.class")
        job_owner = get_property_data(an_item, "llq.owner")
        job_script = get_property_data(an_item, "llq.job_script")
        job_status = get_property_data(an_item, "llq.status")
        job_err = get_property_data(an_item, "llq.err")
        job_out = get_property_data(an_item, "llq.out")
        click.echo("""{job_id} {job_status} {job_class} {job_owner}
  Script: {job_script}
     Out: {job_out}
     Err: {job_err}
""".format(
            job_id=click.style(job_id, bold=True),
            job_class=click.style(job_class, fg='blue'),
            job_owner=click.style(job_owner, fg='cyan'),
            job_script=job_script,
            job_status=click.style(job_status, fg='yellow'),
            job_err=job_err,
            job_out=job_out
        ))


def query_user_llq(config, user_name, long=False):
    model_dict = get_llq_detail_query_response(config)

    max_class_length = 0
    max_owner_length = 0
    for an_item in model_dict['items']:
        job_owner = get_property_data(an_item, "llq.owner")
        if user_name not in job_owner:
            continue
        job_class = get_property_data(an_item, "llq.class")
        if len(job_class) > max_class_length:
            max_class_length = len(job_class)
        if len(job_owner) > max_owner_length:
            max_owner_length = len(job_owner)

    for an_item in model_dict['items']:
        job_id = get_property_data(an_item, "llq.id")
        job_class = get_property_data(an_item, "llq.class")
        job_owner = get_property_data(an_item, "llq.owner")
        if user_name not in job_owner:
            continue
        job_script = get_property_data(an_item, "llq.job_script")
        job_status = get_property_data(an_item, "llq.status")
        if long:
            job_err = get_property_data(an_item, "llq.err")
            job_out = get_property_data(an_item, "llq.out")
            click.echo("""{job_id} {job_status} {job_class} {job_owner}
              Script: {job_script}
                 Out: {job_out}
                 Err: {job_err}
            """.format(
                job_id=click.style(job_id, bold=True),
                job_class=click.style(job_class, fg='blue'),
                job_owner=click.style(job_owner, fg='cyan'),
                job_script=job_script,
                job_status=click.style(job_status, fg='yellow'),
                job_err=job_err,
                job_out=job_out
            ))
        else:
            click.echo("{job_id} {job_status} {job_class} {job_owner} {job_script}".format(
                job_id=click.style(job_id, bold=True),
                job_class=click.style(("{job_class: <" + str(max_class_length) + "}").format(job_class=job_class), fg='blue'),
                job_owner=click.style(("{job_owner: <" + str(max_owner_length) + "}").format(job_owner=job_owner), fg='cyan'),
                job_script=job_script,
                job_status=click.style("{job_status: <2}".format(job_status=job_status), fg='yellow'),
            ))


@cli.command('llqn', short_help='query own jobs')
@click.option('--config-file', help="config file path")
@click.option('-l', '--long', is_flag=True, default=False, help="use long description")
def llqn(config_file, long):
    """
    Query login user's jobs in LoadLeveler.
    """
    config = get_config(config_file)
    user_name = get_user_name()

    query_user_llq(config, user_name, long)


@cli.command('llqu', short_help='query user jobs')
@click.option('--config-file', help="config file path")
@click.option('-l', '--long', is_flag=True, default=False, help="use long description")
@click.argument('user_name')
def llqu(config_file, user_name, long):
    """
    Query some user's jobs in LoadLeveler.
    """
    config = get_config(config_file)

    query_user_llq(config, user_name, long)


if __name__ == "__main__":
    cli()
