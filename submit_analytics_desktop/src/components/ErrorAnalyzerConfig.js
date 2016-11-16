import React, { Component, PropTypes } from 'react';

export default  class ErrorAnalyzerConfig extends Component{
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <h2>配置</h2>
                <div className="row">
                    <div className="col-md-12">
                        <form>
                            <div className="form-group">
                                <label className="">错误日志路径</label>
                                <input type="text" className="form-control"/>
                            </div>
                            <div className="form-group">
                                <label>统计类型</label>
                                <select className="form-control">
                                    <option>Day</option>
                                    <option>Weekday</option>
                                    <option>System</option>
                                </select>
                            </div>
                            <div className="form-group">
                                <label>起始日期</label>
                                <input type="date" className="form-control"/>
                            </div>
                            <div className="form-group">
                                <label>结束日期</label>
                                <input type="date" className="form-control"/>
                            </div>
                            <div className="form-group">
                                <button type="button" className="btn btn-default">运行</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        );
    }
}