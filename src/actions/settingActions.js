import * as types from './actionTypes';
import settingService from "../services/settingService";
import { actions as toastrActions } from 'react-redux-toastr';
import store from '../helpers/store';


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
    return { type: types.SETTING_SELECTED, setting };
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
const settingsSavedSuccessfully = () => {
    return { type: types.SETTINGS_SAVED_SUCCESSFULLY, success:true };
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

function saveSettings() {
    const state = store.getState();
    const changed = state.settings.settings.filter(s => s.hasChanges === true);
    return (dispatch) => {
        return settingService.saveSettings(changed).then(success => {
            if (success && success === true) {
                dispatch(toastrActions.add({
                    type: 'success',
                    message: 'Successfully saved settings.',
                    title: 'Successfully Saved'
                }));
                dispatch(settingsSavedSuccessfully);
            } else {
                throw 'Failed to save settings';
            }
            
        }).catch(e => {
            dispatch(toastrActions.add({
                type: 'error',
                title: 'Failed to Save',
                attention: true,
                message: 'Failed to save the settings with the following error: ' + e
            }));
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
    settingCategoryDeselected,
    saveSettings
}
export default settingActions;
