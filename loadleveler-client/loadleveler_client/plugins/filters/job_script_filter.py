# coding=utf-8
from nwpc_hpc_model.workload.query_item import get_property_data
from nwpc_hpc_model.workload.loadleveler.filter import Filter
from nwpc_hpc_model.workload.loadleveler.filter_condition import (
    create_greater_value_checker, create_value_in_checker,
    PropertyFilterCondition
)

filter_info = {
    'name': 'job_script_filter'
}


def create_filter(pattern):
    job_script_condition = PropertyFilterCondition(
        "llq.job_script",
        data_checker=create_value_in_checker(pattern),
        data_parser=get_property_data
    )
    a_filter = Filter()
    a_filter.conditions.append(job_script_condition)
    return {
        'name': filter_info['name'],
        'filter': a_filter
    }
