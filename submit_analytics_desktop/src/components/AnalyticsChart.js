import React, { Component, PropTypes } from 'react';
import * as d3time from 'd3-time'
import * as d3_time_format from 'd3-time-format'
import ErrorAnalyzerBarChart from "../components/ErrorAnalyzerBarChart"

export default  class AnalyticsChart extends Component{
    constructor(props) {
        super(props);
    }

    render() {
        let day_formatter = d3_time_format.timeFormat("%Y-%m-%d");
        let day_parser = d3_time_format.timeParse("%Y-%m-%d");
        const {analytics_result} = this.props;
        // console.log('AnalyticsChart', analytics_result);
        if(analytics_result === null){
            return (
            <div>

            </div>
            )
        }
        if(analytics_result.type == "count"){
            const {data} = analytics_result;
            const { begin_date, end_date, count_type, count_result } = data;
            let x_axis;
            let y_axis;
            let series;
            if(count_type == "day") {
                let x_range = d3time.timeDay.range(day_parser(begin_date), day_parser(end_date));
                let x_data = x_range.map(function (item, index) {
                    return day_formatter(item);
                });
                x_axis = [{
                    type: 'category',
                    data: x_data,
                    axisTick: {
                        alignWithLabel: true
                    }
                }];
                y_axis = [{
                    type: 'value'
                }];
                let values = x_data.map(function (item, index) {
                    if (item in count_result) {
                        return count_result[item]
                    }
                    else
                        return 0;
                });
                let bar_data = {
                    name: 'count',
                    type: 'bar',
                    barWidth: '60%',
                    data: values
                };
                series = [bar_data];
                let chart_data = {
                    x_axis: x_axis,
                    y_axis: y_axis,
                    series: series
                };
                return (
                    <div>
                        <ErrorAnalyzerBarChart data={chart_data} />
                    </div>
                )
            }else{
                return (
                    <div>

                    </div>
                )
            }
        } else {
            return (
            <div>

            </div>
            )
        }

    }
}

AnalyticsChart.propTypes = {
    analytics_result: PropTypes.object
};
