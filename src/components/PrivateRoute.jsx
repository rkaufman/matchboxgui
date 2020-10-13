import React from 'react';
import { Route, Redirect } from 'react-router-dom';

export const PrivateRoute = ({ component: Component, loggedIn, ...rest }) => (
    <Route {...rest} render={props => {
        if(loggedIn === true){
            return <Component {...props}/>
        }
        return <Redirect to={{ pathname: '/login', state: { from: props.location } }} />
    }} />
)

export default PrivateRoute;