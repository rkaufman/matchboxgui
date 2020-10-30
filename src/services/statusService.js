import {serviceBase} from "./serviceBase";
import config from './config';
import { authHeader } from '../helpers';

const getAll = ()=>{
    let opt = {
        method: 'GET',
        headers: authHeader()
    }
    return fetch(`${config.apiUrl}/status`, opt)
        .then(serviceBase.handleResponse)
        .then(s=>{
            return s;
        });
}

export const statusService = {
    getAll
}
export default statusService;
