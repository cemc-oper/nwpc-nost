import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'

import HpcAuth from '../components/HpcAuth'
import ErrorAnalyzerConfig from '../components/ErrorAnalyzerConfig'

class SubmitAnalyticsApp extends Component{
    constructor(props) {
        super(props);
    }

    render() {
        const { params } = this.props;
        return (
            <div className="container">
                <div className="row">
                    <div className="col-sm-4">
                        <HpcAuth />
                        <ErrorAnalyzerConfig />
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
