import config from './config';
import { authHeader } from '../helpers';
import { serviceBase } from './serviceBase';


function getAll(){
    let requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/setting`, requestOptions)
        .then(serviceBase.handleResponse)
        .then(s => {
            return s.map((w, i) => {
                 w.hasChanges = false;
                 return w;
            });
        });
}
function getCategories() {
    let requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/setting/category`, requestOptions)
        .then(serviceBase.handleResponse)
        .then(c => {
            return c.map((cat, i) => {
                cat.hasChanges = false;
                cat.hasSettingChanges = false;
                return cat;
            });
        });
}
const getDetectors = () => {
    let opts = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/setting/detectors`, opts)
        .then(serviceBase.handleResponse)
        .then(d => {
            return d;
        });
}
const changeDetector = (id) => {
    let opts = {
        method: 'PATCH',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/setting/detectors/${id}`, opts)
        .then(serviceBase.handleResponse)
        .then((s) => {
            if (s.status === 'success') {
                return true;
            }
            return false;
        });
}
const saveSettings = (settings) => {
    const authHdr = authHeader();
    authHdr['Content-Type'] = "application/json";
    const opt = {
        method: 'PATCH',
        headers: authHdr,
        body: JSON.stringify(settings)
    };
    return fetch(`${config.apiUrl}/setting`, opt)
        .then(r => {
            if (r.ok) return true;
            return Promise.reject(r.statusText());
        });
}

export const settingService = {
    getAll,
    getCategories,
    saveSettings,
    getDetectors,
    changeDetector
}

export default settingService;
