import React from 'react';
import { connect } from 'react-redux';
import { Switch, Route } from 'react-router-dom';

import { PrivateRoute, Header } from '../components';
import { HomePage } from '../homePage';
import { LoginPage } from '../loginPage';
import './App.css'
import '@progress/kendo-theme-default'

class App extends React.Component {
    render() {
        if(this.props.loggedIn){
            return (
                <div className="container mb-container full-height App">
                    <div className="row">
                        <Header/>
                    </div>
                    <div className="row full-height">
                        <Switch>
                            <PrivateRoute exact path="/" component={HomePage} loggedIn={this.props.loggedIn}/>
                            <PrivateRoute path="/status" component={HomePage} loggedIn={this.props.loggedIn}/>
                            <Route exact path="/login" component={LoginPage} />
                        </Switch>
                    </div>
                </div>
            );
        } else{
            return (
                <div className="container mb-container full-height App">
                    <div className="row full-height">
                        <Switch>
                            <Route exact path="/login" component={LoginPage} />
                            <PrivateRoute exact path="/" component={HomePage} loggedIn={this.props.loggedIn}/>
                            <PrivateRoute path="/status" component={HomePage} loggedIn={this.props.loggedIn}/>
                        </Switch>
                    </div>
                </div>
            );
        }
    }
}
const mapStateToProps = (state)=>{
    const {loggedIn} = state.authentication;
    return{
        loggedIn
    }
}
export default connect(mapStateToProps)(App);