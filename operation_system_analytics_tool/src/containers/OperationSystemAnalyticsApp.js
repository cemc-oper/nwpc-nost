import React, { Component, PropTypes } from 'react'
import { dispatch } from 'redux'
import { connect } from 'react-redux'
import {ipcRenderer} from 'electron'
// const electron = require('electron');

import HpcAuth from '../components/HpcAuth/index'
import ErrorAnalyzerConfig from '../components/ErrorAnalyzerConfig'
import AnalyticsChart from '../components/AnalyticsChart'

import {receiveAnalyticsResult} from '../actions/llsubmit4_error_log_action'

import { saveSession, loadSession, requestTestSession, receiveTestSessionResponse} from '../actions/session_action'

class OperationSystemAnalyticsApp extends Component{
    constructor(props) {
        super(props);
    }

    componentDidMount() {
        const { dispatch } = this.props;
        ipcRenderer.on('llsubmit4-error-analytics-reply', function (event, result) {
            let analytics_result = JSON.parse(result);
            dispatch(receiveAnalyticsResult(analytics_result));
        });

        ipcRenderer.on('session-system-test-session-reply', function (event, result) {
            let test_result = result;
            console.log(test_result);
            dispatch(receiveTestSessionResponse(test_result));
        })
    }

    handleRunClick() {
        let auth = this.refs.hpc_auth.getSession();
        let config = this.refs.error_analyzer_config.getConfig();

        ipcRenderer.send('llsubmit4-error-analytics-message', auth, config);
    }

    testSession(session) {
        const { dispatch } = this.props;
        dispatch(requestTestSession(session));
        ipcRenderer.send('session-system-test-session-message', session);
    }

    saveSession(session) {
        const { dispatch } = this.props;
        dispatch(saveSession(session));
    }

    loadSession(session) {
        const { dispatch } = this.props;
        dispatch(loadSession(session));
    }

    render() {
        const { analytics_chart, session_system } = this.props;
        const { analytics_result } = analytics_chart;
        const { session_list, current_session } = session_system;
        return (
            <div className="container-fluid">
                <div className="row">
                    <div className="col-sm-12">
                        <HpcAuth
                            ref="hpc_auth"
                            current_session={current_session}
                            handler={{
                                test_click_handler: this.testSession.bind(this),
                                save_click_handler: this.saveSession.bind(this),
                                load_session_handler: this.loadSession.bind(this),
                                bar_editor_change_handler: this.loadSession.bind(this)
                            }}
                            session_list={session_list}
                        />
                        </div>
                    </div>
                <div className="row">
                    <div className="col-sm-4">
                        <ErrorAnalyzerConfig ref="error_analyzer_config"
                          error_log_path="/cma/g1/nwp/sublog/llsubmit4.error.log"
                          analytics_type="day"
                          begin_date="2016-11-07"
                          end_date="2016-11-14"/>
                        <div className="row">
                            <div className="col-sm-12">
                            <form>
                                <div className="form-group">
                                    <button type="button" className="btn btn-primary"
                                        onClick={this.handleRunClick.bind(this)}>
                                        运行
                                        </button>
                                </div>
                            </form>
                            </div>
                        </div>
                    </div>
                    <div className="col-sm-8">
                        <div className="panel panel-success">
                            <div className="panel-heading">
                                <h3 className="panel-title">统计结果</h3>
                            </div>
                            <div className="panel-body">
                                <AnalyticsChart
                                    analytics_result={analytics_result}
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

OperationSystemAnalyticsApp.propTypes = {
    analytics_chart: PropTypes.shape({
        analytics_result: PropTypes.object
    }),
    session_system: PropTypes.shape({
        session_list: PropTypes.arrayOf(PropTypes.shape({
            name: PropTypes.string
        })),
        current_session: PropTypes.object
    })
};


function mapStateToProps(state){
    return {
        analytics_chart: state.llsubmit4_error_log.analytics_chart,
        session_system: state.session_system
    }
}

export default connect(mapStateToProps)(OperationSystemAnalyticsApp)