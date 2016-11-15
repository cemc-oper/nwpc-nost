import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

class SubmitAnalyticsApp extends Component{
    constructor(props) {
        super(props);
    }

    render() {
        const { params } = this.props;
        return (
            <div className="container">
                <h2>Auth</h2>
                <div className="row">
                    <div className="col-md-12">
                        <form className="form-horizontal">
                            <div className="form-group">
                                <label className="col-sm-2 control-label">Host</label>
                                <div className="col-sm-10">
                                    <input type="text" className="form-control" />
                                </div>
                            </div>

                            <div className="form-group">
                                <label className="col-sm-2 control-label">Port</label>
                                <div className="col-sm-10">
                                    <input type="text" className="form-control"/>
                                </div>
                            </div>

                            <div className="form-group">
                                <label className="col-sm-2 control-label">User</label>
                                <div className="col-sm-10">
                                    <input type="text" className="form-control"/>
                                </div>
                            </div>

                            <div className="form-group">
                                <label className="col-sm-2 control-label">Password</label>
                                <div className="col-sm-10">
                                    <input type="password" className="form-control"/>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
                <h2>Config</h2>
                <div className="row">
                    <div className="col-md-12">
                        <form className="form-horizontal">
                            <div className="form-group">
                                <label className="col-sm-2 control-label">Error Log File</label>
                                <div className="col-sm-10">
                                    <input type="text" className="form-control"/>
                                </div>
                            </div>
                            <div className="form-group">
                                <label className="col-sm-2 control-label">Count Type</label>
                                <div className="col-sm-2">
                                    <select className="form-control">
                                        <option>Day</option>
                                        <option>Weekday</option>
                                        <option>System</option>
                                    </select>
                                </div>
                            </div>
                            <div className="form-group">
                                <label className="col-sm-2 control-label">Start Date</label>
                                <div className="col-sm-10">
                                    <input type="date" className="form-control"/>
                                </div>
                            </div>
                            <div className="form-group">
                                <label className="col-sm-2 control-label">End Date</label>
                                <div className="col-sm-10">
                                    <input type="date" className="form-control"/>
                                </div>
                            </div>
                            <div className="form-group">
                                <div className="col-sm-offset-2 col-sm-10">
                                    <button type="button" className="btn btn-default">Run</button>
                                </div>
                            </div>
                        </form>
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
