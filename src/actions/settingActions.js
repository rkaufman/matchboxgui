import * as types from './actionTypes';
import settingService from "../services/settingService";


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
const settingChanged = (setting) => {
    return { type: types.SETTING_CHANGED, setting };
}
const settingSelected = (setting) => {
    return { type: types.SETTING_DESELECTED, setting };
}
const settingDeselected = (setting) => {
    return { type: types.SETTING_DESELECTED, setting };
}
const settingCategorySelected = (category) => {
    return { type: types.SETTING_CATEGORY_SELECTED, category };
}
const settingCategoryDeselected = (category) => {
    return { type: types.SETTING_CATEGORY_DESELECTED, category };
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
export const settingActions = {
    getSettings,
    getSettingCategories,
    settingChanged,
    settingSelected,
    settingDeselected,
    settingCategorySelected,
    settingCategoryDeselected
}
export default settingActions;
