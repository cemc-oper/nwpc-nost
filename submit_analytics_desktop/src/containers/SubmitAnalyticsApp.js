import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'
import {ipcRenderer} from 'electron'
// const electron = require('electron');

import HpcAuth from '../components/HpcAuth'
import ErrorAnalyzerConfig from '../components/ErrorAnalyzerConfig'

class SubmitAnalyticsApp extends Component{
    constructor(props) {
        super(props);
    }

    componentDidMount() {
        ipcRenderer.on('llsubmit4-error-analytics-reply', function (event, result) {
            let analytics_result = JSON.parse(result);
            console.log(analytics_result);
        })
    }

    handleRunClick() {
        let auth = this.refs.hpc_auth.getAuth();
        let config = this.refs.error_analyzer_config.getConfig();
        console.log(auth, config);

        ipcRenderer.send('llsubmit4-error-analytics-message', auth, config);
    }

    render() {
        const { params } = this.props;
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
                        <div>

                        </div>
                    </div>
                </div>
            </div>
        );
    }
}


function mapStateToProps(state){
    return {
    }
}

export default connect(mapStateToProps)(SubmitAnalyticsApp)
