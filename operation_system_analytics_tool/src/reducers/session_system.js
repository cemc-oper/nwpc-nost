import { SAVE_SESSION } from '../actions/session_action'

export default function session_reducer(state={
    status: {
        is_fetching: false,
        last_updated: null
    },
    session_list: [
        { name: 'nwp' },
        { name: 'nwp_qu' },
        { name: 'nwp_pd' },
        { name: 'nwp_sp' },
    ],
    save_session: {

    },
    test_session: {

    }
}, action) {
    switch(action.type){
        case SAVE_SESSION:
            return Object.assign({}, state, {
                session_list: state.session_list.concat([action.session])
            });
        default:
            return state;
    }
}