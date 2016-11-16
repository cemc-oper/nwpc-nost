import React, { Component, PropTypes } from 'react';

export default  class HpcAuth extends Component{
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <h2>登录</h2>
                <div className="row">
                    <div className="col-md-12">
                        <form>
                            <div className="form-group">
                                <label>主机</label>
                                <input type="text" className="form-control" />
                            </div>

                            <div className="form-group">
                                <label>端口</label>
                                <input type="text" className="form-control"/>
                            </div>

                            <div className="form-group">
                                <label>用户</label>
                                <input type="text" className="form-control"/>
                            </div>

                            <div className="form-group">
                                <label>密码</label>
                                <input type="password" className="form-control"/>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        );
    }
}