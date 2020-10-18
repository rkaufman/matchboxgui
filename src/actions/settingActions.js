import * as types from './actionTypes';
import settingService from "../services/settingService";

export const settingActions = {
    getSettings
}
const getSettingSuccess = (settings)=>{
    return {type: types.GET_SETTINGS_SUCCESS, settings};
}
const getSettingFailure = (err)=>{
    return {type: types.GET_SETTINGS_FAILURE, err};
}
function getSettings(){
    return (dispatch)=>{
        return settingService.getAll().then(s=>{
            dispatch(getSettingSuccess(s));
        }).catch(e=>{
            dispatch(getSettingFailure(e));
        })
    }
}

export default settingActions;
