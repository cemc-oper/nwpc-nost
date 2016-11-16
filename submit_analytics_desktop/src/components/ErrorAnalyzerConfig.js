import React, { Component, PropTypes } from 'react';

export default  class ErrorAnalyzerConfig extends Component{
    constructor(props) {
        super(props);
    }

    getConfig() {
      let config = new Object();
      config.error_log_path = this.refs.error_log_path_node.value;
      config.analytics_type = this.refs.analytics_type_node.value;
      config.start_date = this.refs.start_date_node.value;
      config.end_date = this.refs.end_date_node.value;
      return config;
    }

    render() {
        const { error_log_path, analytics_type, start_date, end_date } = this.props;
        return (
            <div>
                <h2>配置</h2>
                <div className="row">
                    <div className="col-md-12">
                        <form>
                            <div className="form-group">
                                <label className="">错误日志路径</label>
                                <input type="text" className="form-control" ref="error_log_path_node" value={error_log_path} />
                            </div>
                            <div className="form-group">
                                <label>统计类型</label>
                                <select className="form-control" ref="analytics_type_node">
                                    <option value="day">Day</option>
                                    <option value="weekday">Weekday</option>
                                    <option value="system">System</option>
                                </select>
                            </div>
                            <div className="form-group">
                                <label>起始日期</label>
                                <input type="date" className="form-control" ref="start_date_node" value={start_date} />
                            </div>
                            <div className="form-group">
                                <label>结束日期</label>
                                <input type="date" className="form-control" ref="end_date_node" value={end_date} />
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        );
    }
}

ErrorAnalyzerConfig.propTypes = {
    error_log_path: PropTypes.string,
    analytis_type: PropTypes.string,
    start_date: PropTypes.string,
    end_date: PropTypes.string
}
