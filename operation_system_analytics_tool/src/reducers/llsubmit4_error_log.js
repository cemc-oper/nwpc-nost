import {
    REQUEST_ERROR_LOG_ANALYTICS,
    RESPONSE_ERROR_LOG_ANALYTICS,
    CHANGE_ERROR_LOG_PATH,
    LOAD_ERROR_LOG,
    SAVE_ERROR_LOG,
    REQUEST_ERROR_LOG_INFO,
    RECEIVE_ERROR_LOG_INFO,
    CHANGE_ANALYZER_CONFIG,
    CHANGE_ANALYZER_CONFIG_COMMAND
} from '../actions/llsubmit4_error_log_action'
import moment from 'moment'

function error_log_analyzer_config_reducer(state, action){
    switch(action.type) {
        case CHANGE_ANALYZER_CONFIG:
            let t = Object();
            t[action.config.analytics_command] = action.config;
            let command_map = Object.assign({}, state.command_map, t);

            let new_state = Object.assign({}, state, {
                command_map: command_map
            });
            return new_state;
            break;
        case CHANGE_ANALYZER_CONFIG_COMMAND:
           return Object.assign({}, state, {
                current_command: action.command
            });
            break;
        default:
            return state;
    }
}

export default function llsubmit4_error_log_reducer(state={
    status: {
        is_fetching: false,
        last_updated: null
    },
    auth:{},
    error_log_analyzer_config:{
        current_command: 'count',
        command_map: {
            'count': {
                analytics_command: 'count',
                analytics_type: 'date',
                first_date: moment().subtract(1, 'weeks'),
                last_date: moment().subtract(1, 'days')
            },
            'grid': {
                analytics_command: 'grid',
                x_type: 'hour',
                y_type: 'weekday',
                first_date: moment().subtract(1, 'weeks'),
                last_date: moment().subtract(1, 'days')
            }
        }
    },
    error_log_analyzer:{
        status: {
            is_fetching: false
        },
        analytics_result:null
    },
    error_log_data_config:{
        error_log_path: '/cma/g1/nwp/sublog/llsubmit4.error.log',
        info: null,
        error_log_list: [
            {
                name: 'nwp',
                path: '/cma/g1/nwp/sublog/llsubmit4.error.log'
            },
            {
                name: 'nwp_qu',
                path: '/cma/g1/nwp_qu/sublog/llsubmit4.error.log'
            },
            {
                name: 'nwp_pd',
                path: '/cma/g3/nwp_pd/sublog/llsubmit4.error.log'
            },
            {
                name: 'nwp_sp',
                path: '/cma/g1/nwp_sp/sublog/llsubmit4.error.log'
            }
        ]
    }
}, action) {
    switch(action.type){
        case REQUEST_ERROR_LOG_ANALYTICS:
            return Object.assign({}, state, {
                error_log_analyzer: {
                    status: {
                        is_fetching: true
                    },
                    analytics_result: state.error_log_analyzer.analytics_result
                }
            });
            break;
        case RESPONSE_ERROR_LOG_ANALYTICS:
            return Object.assign({}, state, {
                error_log_analyzer: {
                    status: {
                        is_fetching: false
                    },
                    analytics_result: action.analytics_result,
                }
            });
            break;
        case CHANGE_ERROR_LOG_PATH:
            return Object.assign({}, state, {
                error_log_data_config: {
                    error_log_path: action.error_log_path,
                    info: null,
                    error_log_list: state.error_log_data_config.error_log_list
                }
            });
            break;
        case LOAD_ERROR_LOG:
            return Object.assign({}, state, {
                error_log_data_config: {
                    error_log_path: action.error_log.path,
                    info: null,
                    error_log_list: state.error_log_data_config.error_log_list
                }
            });
            break;
        case SAVE_ERROR_LOG:
            return Object.assign({}, state, {
                error_log_data_config: {
                    error_log_path: state.error_log_data_config.error_log_path,
                    info: state.error_log_data_config.info,
                    error_log_list: state.error_log_data_config.error_log_list.concat([action.error_log])
                }
            });
            break;
            break;
        case REQUEST_ERROR_LOG_INFO:
            return Object.assign({}, state, {
                error_log_data_config: {
                    error_log_path: state.error_log_data_config.error_log_path,
                    info: null,
                    error_log_list: state.error_log_data_config.error_log_list
                }
            });
            break;
        case RECEIVE_ERROR_LOG_INFO:
            let info = action.error_log_info_response.data;
            let info_range = info.range;
            info_range.start_date_time = moment(info_range.start_date_time+" +0000", "YYYY-MM-DDTHH:mm:ss Z");
            info_range.end_date_time = moment(info_range.end_date_time+" +0000", "YYYY-MM-DDTHH:mm:ss Z");

            return Object.assign({}, state, {
                error_log_data_config: {
                    error_log_path: state.error_log_data_config.error_log_path,
                    info: info,
                    error_log_list: state.error_log_data_config.error_log_list
                }
            });
            break;
        case CHANGE_ANALYZER_CONFIG:
        case CHANGE_ANALYZER_CONFIG_COMMAND:
            return Object.assign({}, state, {
                error_log_analyzer_config: error_log_analyzer_config_reducer(state.error_log_analyzer_config, action)
            });
            break;
        default:
            return state;
    }
}