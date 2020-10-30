import { produce } from 'immer';
import * as actionTypes from '../actions/actionTypes';

const log = (state = { logs: [{message: 'No logs yet', date: Date.now(), msgType: 'info' }] }, action) => {
    switch (action.type) {
        case actionTypes.GET_LOGS_SUCCESS:
            return produce(state,
                draft => {
                    if (action.logs.length > 0) {
                        draft.logs = action.logs;
                    }
                });
        default:
            return state;
    }
}

export default log;