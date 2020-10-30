import { settingConstants } from '../constants/settingConstants';
import { produce } from 'immer';

export default function settings(state = { settings: [], categories: [], detectors: [] }, action) {
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
                            draft.categories.forEach(c => {
                                if (c.id === parseInt(s.group)) {
                                    c.hasSettingChanges = true;
                                }
                            });
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
        case settingConstants.SETTING_DESELECTED:
            return produce(state,
                draft => {
                    draft.settings.forEach(s => {
                        s.selected = false;
                    });
                    
                });
        case settingConstants.SETTINGS_SAVED_SUCCESSFULLY:
            return produce(state,
                draft => {
                    draft.settings.forEach(s => {
                        s.hasChanges = false;
                    });
                    draft.categories.forEach(c => {
                        c.hasSettingChanges = false;
                    });
                });
            case settingConstants.GET_DETECTORS_SUCCESS:
                return produce(state,
                    draft => {
                        draft.detectors = action.detectors;
                    });
                case settingConstants.DETECTOR_CHANGED_SUCCESS:
                    return produce(state,
                        draft => {
                            draft.detectors.forEach(d => {
                                if (d.id === action.id) {
                                    d.selected = !d.selected;
                                }
                            });
                        });
        default:
            return state;
    }
}
