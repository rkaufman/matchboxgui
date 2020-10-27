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
                        if (s._settingId === action.setting.next._settingId) {
                            s._setting = action.setting.next._setting;
                        }
                    });
                });
        default:
            return state;
    }
}
