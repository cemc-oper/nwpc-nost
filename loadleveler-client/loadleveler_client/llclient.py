# coding=utf-8
import json
import os
import subprocess
import click

from nwpc_hpc_model.loadleveler import QueryCategory, QueryCategoryList, QueryModel
from nwpc_hpc_model.loadleveler import record_parser
from nwpc_hpc_model.loadleveler import value_saver
from nwpc_hpc_model.loadleveler.filter_condition import get_property_data


config_file_name = "loadleveler_status.config"
default_config_file_path = os.path.join(os.path.dirname(__file__), "conf", config_file_name)


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


def get_config(config_file_path):
    """
    :param config_file_path: path of config file, which should be a YAML file.

    :return: config dict loading from config file.
    """
    config = None
    with open(config_file_path, 'r') as f:
        config = json.load(f)
    return config


@click.group()
def cli():
    """
    A command line tool for Loadleveler.
    """


@cli.command()
@click.option('-c', '--config-file', help="config file path")
@click.option('-p', '--params', help="llq params")
def query(config_file, params):
    if config_file:
        config_file_path = config_file
    else:
        config_file_path = default_config_file_path
    config = get_config(config_file_path)

    model_dict = get_llq_detail_query_response(config, params)

    for an_item in model_dict['items']:
        job_id = get_property_data(an_item, "llq.id")
        job_class = get_property_data(an_item, "llq.class")
        job_owner = get_property_data(an_item, "llq.owner")
        job_script = get_property_data(an_item, "llq.job_script")
        job_status = get_property_data(an_item, "llq.status")
        print("{job_id} {job_status} {job_class} {job_owner} {job_script}".format(
            job_id=job_id,
            job_class=job_class,
            job_owner=job_owner,
            job_script=job_script,
            job_status=job_status
        ))


@cli.command()
@click.option('-c', '--config-file', help="config file path")
@click.option('-p', '--params', help="llq params")
def detail(config_file, params):
    if config_file:
        config_file_path = config_file
    else:
        config_file_path = default_config_file_path
    config = get_config(config_file_path)

    model_dict = get_llq_detail_query_response(config, params)

    for an_item in model_dict['items']:
        job_id = get_property_data(an_item, "llq.id")
        job_class = get_property_data(an_item, "llq.class")
        job_owner = get_property_data(an_item, "llq.owner")
        job_script = get_property_data(an_item, "llq.job_script")
        job_status = get_property_data(an_item, "llq.status")
        job_err = get_property_data(an_item, "llq.err")
        job_out = get_property_data(an_item, "llq.out")
        print("""{job_id} {job_status} {job_class} {job_owner}
  Script: {job_script}
     Out: {job_out}
     Err: {job_err}
""".format(
            job_id=job_id,
            job_class=job_class,
            job_owner=job_owner,
            job_script=job_script,
            job_status=job_status,
            job_err=job_err,
            job_out=job_out
        ))


def llqn(config, user_name):
    model_dict = get_llq_detail_query_response(config)

    for an_item in model_dict['items']:
        job_id = get_property_data(an_item, "llq.id")
        job_class = get_property_data(an_item, "llq.class")
        job_owner = get_property_data(an_item, "llq.owner")
        if user_name not in job_owner:
            continue
        job_script = get_property_data(an_item, "llq.job_script")
        job_status = get_property_data(an_item, "llq.status")
        print("{job_id} {job_status} {job_class} {job_owner} {job_script}".format(
            job_id=job_id,
            job_class=job_class,
            job_owner=job_owner,
            job_script=job_script,
            job_status=job_status
        ))


@cli.command()
@click.option('-c', '--config-file', help="config file path")
def llqn(config_file):
    if config_file:
        config_file_path = config_file
    else:
        config_file_path = default_config_file_path
    config = get_config(config_file_path)
    user_name = get_user_name()

    llqn(config, user_name)


@cli.command()
@click.option('-c', '--config-file', help="config file path")
@click.argument('user_name')
def llqu(config_file, user_name):
    if config_file:
        config_file_path = config_file
    else:
        config_file_path = default_config_file_path
    config = get_config(config_file_path)

    llqn(config, user_name)


if __name__ == "__main__":
    cli()
