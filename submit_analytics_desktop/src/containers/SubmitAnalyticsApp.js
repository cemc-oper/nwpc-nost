import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

class SubmitAnalyticsApp extends Component{
    constructor(props) {
        super(props);
    }

    render() {
        const { params } = this.props;
        return (
            <div>
                Hello World!
            </div>
        );
    }
}


function mapStateToProps(state){
    return {
    }
}

export default connect(mapStateToProps)(SubmitAnalyticsApp)
