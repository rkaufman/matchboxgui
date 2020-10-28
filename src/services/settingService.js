import config from './config';
import { authHeader } from '../helpers';
import history from "../helpers/history";


function getAll(){
    let requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/setting`, requestOptions)
        .then(handleResponse)
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
        .then(handleResponse)
        .then(c => {
            return c.map((cat, i) => {
                cat.hasChanges = false;
                return cat;
            });
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
function handleResponse(response) {
    return response.text().then(text => {
        const data = text && JSON.parse(text);
        if (!response.ok) {
            if (response.status === 401) {
                // auto logout if 401 response returned from api
                localStorage.removeItem("auth_token");
                history.push('/login');
            }

            const error = (data && data.message) || response.statusText;
            return Promise.reject(error);
        }

        return data;
    });
}
export const settingService = {
    getAll,
    getCategories,
    saveSettings
}

export default settingService;
