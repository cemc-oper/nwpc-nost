import React, { Component, PropTypes } from 'react'
import { dispatch } from 'redux'
import { connect } from 'react-redux'
import {ipcRenderer} from 'electron'
// const electron = require('electron');

import HpcAuth from '../components/HpcAuth'
import ErrorAnalyzerConfig from '../components/ErrorAnalyzerConfig'
import AnalyticsChart from '../components/AnalyticsChart'

import {receiveAnalyticsResult} from '../actions/index'

class SubmitAnalyticsApp extends Component{
    constructor(props) {
        super(props);
    }

    componentDidMount() {
        const { dispatch } = this.props;
        ipcRenderer.on('llsubmit4-error-analytics-reply', function (event, result) {
            let analytics_result = JSON.parse(result);
            dispatch(receiveAnalyticsResult(analytics_result));
        })
    }

    handleRunClick() {
        let auth = this.refs.hpc_auth.getAuth();
        let config = this.refs.error_analyzer_config.getConfig();

        ipcRenderer.send('llsubmit4-error-analytics-message', auth, config);
    }

    render() {
        const { analytics_chart } = this.props;
        const { analytics_result } = analytics_chart;
        return (
            <div className="container">
                <div className="row">
                    <div className="col-sm-4">
                        <HpcAuth ref="hpc_auth"
                          host="uranus-bk.hpc.nmic.cn"
                          port={22}
                          user="nwp"
                          password="nwpop"/>
                        <ErrorAnalyzerConfig ref="error_analyzer_config"
                          error_log_path="/cma/g1/nwp/sublog/llsubmit4.error.log"
                          analytics_type="day"
                          begin_date="2016-11-07"
                          end_date="2016-11-14"/>
                        <div className="row">
                            <div className="col-sm-12">
                            <form>
                                <div className="form-group">
                                    <button type="button" className="btn btn-default"
                                        onClick={this.handleRunClick.bind(this)}>
                                        运行
                                        </button>
                                </div>
                            </form>
                            </div>
                        </div>
                    </div>
                    <div className="col-sm-8">
                        <h2>统计结果</h2>
                        <AnalyticsChart
                            analytics_result={analytics_result}
                        />
                    </div>
                </div>
            </div>
        );
    }
}

SubmitAnalyticsApp.propTypes = {
    analytics_chart: PropTypes.shape({
        analytics_result: PropTypes.object
    }),
};


function mapStateToProps(state){
    return {
        analytics_chart: state.error_log.analytics_chart,
    }
}

export default connect(mapStateToProps)(SubmitAnalyticsApp)
