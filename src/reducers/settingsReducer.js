import {settingConstants} from '../constants/settingConstants';
import {produce} from 'immer';

export default function settings(state = {settings:[]}, action){
    switch (action.type){
        case settingConstants.GET_SETTINGS_SUCCESS:
            return produce(state, draft=>{
                draft.settings = action.settings;
            });
        default:
            return state;
    }
}
