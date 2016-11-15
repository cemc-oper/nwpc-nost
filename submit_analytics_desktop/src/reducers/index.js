import { combineReducers } from 'redux'
import { routerReducer as routing } from 'react-router-redux'

function error_reducer(state={
    status: {
        is_fetching: false,
        last_updated: null
    },
    auth:{},
    config:{},
    count:{},
    range:{}
}, action) {
    switch(action){
        default:
            return state
    }
}


const submitAnalyticsAppReducer = combineReducers({
    error_log: error_reducer,
    routing
});

export default submitAnalyticsAppReducer;