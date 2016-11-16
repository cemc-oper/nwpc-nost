import React, { Component, PropTypes } from 'react';

export default  class HpcAuth extends Component{
    constructor(props) {
        super(props);
    }

    getAuth() {
        let auth = new Object();
        let host_node = this.refs.host;
        auth.host = host_node.value;
        let port_node = this.refs.port;
        auth.port = port_node.value;
        let user_node = this.refs.user;
        auth.user = user_node.value;
        let password_node = this.refs.password;
        auth.password = password_node.value;
        return auth;
    }

    render() {
        const {host, port, user, password} = this.props;
        return (
            <div>
                <h2>登录</h2>
                <div className="row">
                    <div className="col-md-12">
                        <form>
                            <div className="form-group">
                                <label>主机</label>
                                <input type="text" className="form-control" ref="host" value={host}/>
                            </div>

                            <div className="form-group">
                                <label>端口</label>
                                <input type="text" className="form-control" ref="port" value={port}/>
                            </div>

                            <div className="form-group">
                                <label>用户</label>
                                <input type="text" className="form-control" ref="user" value={user}/>
                            </div>

                            <div className="form-group">
                                <label>密码</label>
                                <input type="password" className="form-control" ref="password" value={password}/>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        );
    }
}

HpcAuth.propTypes = {
    host: PropTypes.string,
    port: PropTypes.number,
    user: PropTypes.string,
    password: PropTypes.string
}
