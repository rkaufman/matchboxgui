import { createStore, applyMiddleware } from 'redux';
import thunkMiddleware from 'redux-thunk';
import { createLogger } from 'redux-logger';
import rootReducer from '../reducers';
import {routerMiddleware} from 'react-router-redux';
import reduxImmutableStateInvariant from 'redux-immutable-state-invariant';
import history from './history';

const loggerMiddleware = createLogger();

function configureStore(hist){
    return createStore(
        rootReducer,
        applyMiddleware(
            thunkMiddleware,
            loggerMiddleware,
            routerMiddleware(hist),
            reduxImmutableStateInvariant()
        )
    );
}

const store = configureStore(history);

export default store;
