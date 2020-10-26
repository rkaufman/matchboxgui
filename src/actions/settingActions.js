import * as types from './actionTypes';
import settingService from "../services/settingService";

export const settingActions = {
    getSettings,
    getSettingCategories
}
const getSettingSuccess = (settings)=>{
    return {type: types.GET_SETTINGS_SUCCESS, settings};
}
const getSettingFailure = (err)=>{
    return {type: types.GET_SETTINGS_FAILURE, err};
}
const getSettingCategoriesSuccess = (categories) => {
    return { type: types.GET_SETTINGS_CATEGORIES_SUCCESS, categories };
}
const getSettingCategoriesFailure = (err) => {
    return { type: types.GET_SETTINGS_CATEGORIES_FAILURE, err };
}
function getSettings(){
    return (dispatch)=> {
        return settingService.getAll().then(s => {
            dispatch(getSettingSuccess(s));
        }).catch(e => {
            dispatch(getSettingFailure(e));
        });
    }
}

function getSettingCategories() {
    return (dispatch) => {
        return settingService.getCategories().then(s => {
            dispatch(getSettingCategoriesSuccess(s));
        }).catch(e => {
            dispatch(getSettingCategoriesFailure(e));
        });
    }
}

export default settingActions;
