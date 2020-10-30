import {serviceBase} from "./serviceBase";
import config from './config';
import { authHeader } from '../helpers';

const getAll = () => {
    let opt = {
        method: 'GET',
        headers: authHeader()
    };
    return fetch(`${config.apiUrl}/logs`, opt)
        .then(serviceBase.handleResponse)
        .then(l => {
            return l;
        });
}

export const logService = {
    getAll
}

export default logService;