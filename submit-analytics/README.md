# Submit Analytics

A analytics tool for log of llsubmit4.

## Introduction

Analysis the Submission error log of llsubmit4.

## One-dimensional summary

Summarize data by a single dimension.

### Submission failures per day

The number of tasks which is failed to submit per day in the specified date range, 
ignore items which is zero.

~~~
{
    "2016-11-09": 7,
    "2016-11-10": 2,
    "2016-11-12": 19,
    "2016-11-13": 6,
    "2016-11-08": 8,
    "2016-11-07": 6,
    "2016-11-11": 7
}
~~~

### Submission failures per hour

The number of tasks which is failed to submit per hour in the specified date range, 
ignore items which are zero.

~~~
{
    "2016-11-08 16:00:00": 2,
    "2016-11-12 04:00:00": 1,
    "2016-11-08 05:00:00": 1,
    "2016-11-12 03:00:00": 8,
    "2016-11-10 16:00:00": 1,
    /* ... */
    "2016-11-13 05:00:00": 1,
    "2016-11-12 16:00:00": 7,
    "2016-11-12 09:00:00": 1,
    "2016-11-11 11:00:00": 1
},
~~~

### Submission failures per system

The number of tasks which is failed to submit by each system in the specified date range,
ignore items which are zero.

~~~
{
    "gda_gsi_v1r5": 3,
    "grapes_meso_v4_1": 5,
    "gmf_grapes_gfs_v2_0": 4,
    "gmf_gsi_v1r5": 43
}
~~~

### Summarize by week

The number of tasks grouped by week in the specified date range,
ignore items which are zero.

~~~
{
    "0": 6,
    "1": 8,
    "2": 7,
    "3": 2,
    "4": 7,
    "5": 19,
    "6": 6
},
~~~

### Summarize by hour

The number of tasks grouped by hour in the specified date range,
ignore items which are zero.

~~~
{
    "15": 7,
    "11": 1,
    "16": 15,
    "05": 4,
    /* ... */
    "01": 2,
    "03": 12,
    "14": 1,
    "23": 2,
    "10": 1
}
~~~

## Two-dimensional summary

Summarize data by two dimensions.

### X-axis

* hour
* week

### Y-axis

* week
* system
* date

### Example

#### hour/week

~~~
{
    "0": {
        "1": 1,
        "2": 2,
        "3": 9,
        "4": 2,
        "5": 1,
        "6": 1
    },
    "1": {
        "2": 14,
        "3": 1,
        "4": 2,
        "5": 8,
        "6": 18
    /* ... */
}
~~~

#### week/system

~~~
{
    "0": {
        "rafs": 7,
        "geps_t639": 64,
        "haze_v3_1": 12,
        "geps_post_lev2_1_1": 15,
        "obs_rafs": 36,
        "meps_grapes_v2_0_4": 68
    },
    "1": {
        "rafs": 8,
        "geps_t639": 47,
        "haze_v3_1": 20,
        "geps_post_lev2_1_1": 2,
        "obs_rafs": 35,
        "meps_grapes_v2_0_4": 60
    },
    /* ... */
}
~~~

## Query

### Log information

Get summary information for a log.

~~~
{

    "range": {
        "start_date_time": "2016-10-10T14:59:46",
        "end_date_time": "2016-11-26T16:59:17"
    }
}
~~~


## Installation

Please use Python 3.

## Run

Please run llsubmit4_error_analyzer.py --help to see the usage.
