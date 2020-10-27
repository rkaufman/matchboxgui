import config from './config';
import { authHeader } from '../helpers';
import history from "../helpers/history";

export const settingService = {
    getAll,
    getCategories
}

function getAll(){
    let requestOptions = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/setting`, requestOptions)
        .then(handleResponse)
        .then(s => {
            return s.map((w, i) => {
                 var data = JSON.parse(w);
                 data.changed = false;
                 return data;
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
                cat.changed = "false";
                return cat;
            });
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
export default settingService;
