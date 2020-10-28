import { settingConstants } from '../constants/settingConstants';
import { produce } from 'immer';

export default function settings(state = { settings: [], categories: [] }, action) {
    switch (action.type) {
        case settingConstants.GET_SETTINGS_SUCCESS:
            return produce(state, draft => {
                draft.settings = action.settings;
            });
        case settingConstants.GET_SETTINGS_CATEGORIES_SUCCESS:
            return produce(state,
                draft => {
                    draft.categories = action.categories;
                });
        case settingConstants.SETTING_CHANGED:
            return produce(state,
                draft => {
                    draft.settings.forEach(s => {
                        if (s.id === action.setting.id) {
                            s.setting = action.setting.setting;
                            s.hasChanges = true;
                        }
                    });
                });
        case settingConstants.SETTING_SELECTED:
            return produce(state,
                draft => {
                    draft.settings.forEach(s => {
                        s.selected = false;
                        if (s.id === action.setting.id) {
                            s.selected = true;
                        }
                    });
                });
        case settingConstants.SETTINGS_SAVED_SUCCESSFULLY:
            return produce(state,
                draft => {
                    draft.settings.forEach(s => {
                        s.hasChanges = false;
                    });
                });
        default:
            return state;
    }
}
