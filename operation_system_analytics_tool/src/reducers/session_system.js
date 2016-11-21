import { SAVE_SESSION, LOAD_SESSION } from '../actions/session_action'

export default function session_reducer(state={
    status: {
        is_fetching: false,
        last_updated: null
    },
    session_list: [
        {
            name: 'nwp',
            host: 'uranus-bk.hpc.nmic.cn',
            port: 22,
            user: 'nwp',
            password: 'nwpop'
        },
        {
            name: 'nwp_qu',
            host: 'uranus-bk.hpc.nmic.cn',
            port: 22,
            user: 'nwp_qu',
            password: 'nwpop'
        }
    ],
    current_session: {
        host: "uranus-bk.hpc.nmic.cn",
        port: 22,
        user: "nwp",
        password: "nwpop"
    },
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
        case LOAD_SESSION:
            return Object.assign({}, state, {
                current_session: action.session
            });
        default:
            return state;
    }
}