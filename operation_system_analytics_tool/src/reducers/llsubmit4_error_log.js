import {
    RESPONSE_ANALYTICS_RESULT,
    CHANGE_ERROR_LOG_PATH,
    REQUEST_ERROR_LOG_INFO,
    RECEIVE_ERROR_LOG_INFO,
    CHANGE_ANALYZER_CONFIG
} from '../actions/llsubmit4_error_log_action'
import moment from 'moment'

export default function llsubmit4_error_log_reducer(state={
    status: {
        is_fetching: false,
        last_updated: null
    },
    auth:{},
    error_log_analyzer_config:{
        analytics_type: 'day',
        first_date: moment().subtract(1, 'days').subtract(1, 'weeks'),
        last_date: moment().subtract(1, 'days')
    },
    analytics_chart:{
        analytics_result:null
    },
    error_log_data_config:{
        error_log_path: '/cma/g1/nwp/sublog/llsubmit4.error.log',
        info: null
    }
}, action) {
    switch(action.type){
        case RESPONSE_ANALYTICS_RESULT:
            return Object.assign({}, state, {
                analytics_chart: {
                    analytics_result: action.analytics_result
                }
            });
        case CHANGE_ERROR_LOG_PATH:
            return Object.assign({}, state, {
                error_log_data_config: {
                    error_log_path: action.error_log_path,
                    info: null
                }
            });
        case REQUEST_ERROR_LOG_INFO:
            return Object.assign({}, state, {
                error_log_data_config: {
                    error_log_path: state.error_log_data_config.error_log_path,
                    info: null
                }
            });
        case RECEIVE_ERROR_LOG_INFO:
            let info = action.error_log_info_response.data;
            let info_range = info.range;
            info_range.start_date_time = moment(info_range.start_date_time+" +0000", "YYYY-MM-DDTHH:mm:ss Z");
            info_range.end_date_time = moment(info_range.end_date_time+" +0000", "YYYY-MM-DDTHH:mm:ss Z");

            return Object.assign({}, state, {
                error_log_data_config: {
                    error_log_path: state.error_log_data_config.error_log_path,
                    info: info
                }
            });
            break;
        case CHANGE_ANALYZER_CONFIG:
            return Object.assign({}, state, {
                error_log_analyzer_config: action.config
            });
            break;
        default:
            return state;
    }
}