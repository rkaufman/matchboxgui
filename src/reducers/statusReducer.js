import { produce } from 'immer';
import * as actionTypes from '../actions/actionTypes';

export default function status(state = {statuses:[]}, action) {
    switch (action.type) {
        case actionTypes.GET_STATUSES_SUCCESS:
            return produce(state, (draft)=>{
                draft.statuses = action.stats;
            });
        default:
            return state;
    }
}
