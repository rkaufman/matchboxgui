import React from 'react';
import {withRouter} from 'react-router';
import {bindActionCreators} from 'redux';
import {userActions, settingActions} from '../actions';
import {
    Toolbar,
    ToolbarItem,
    ToolbarSpacer,
    Button,
    DropDownButton,
    DropDownButtonItem
} 
from '@progress/kendo-react-buttons';
import './header.css';
import { connect } from 'react-redux';

export class Header extends React.Component{
    constructor(props){
        super(props);
        this.state = {}
    }
    logoutClick = function (){
        this.props.usrActions.logout().then(()=> {
            this.props.history.push('/login');
        });
    }
    accountClick = (e)=>{
        this.props.history.push('/account');
    }
    saveSettings = () => {
        this.props.stgActions.saveSettings();
    }
    statusClick = ()=>{
        this.props.history.push('/status');
    }
    settingsClick = (e)=>{
        if(e.item.to) {
            this.props.history.push(e.item.to);
        } else if(e.item.action){
            switch(e.item.action){
                default:
                    this.logoutClick();
            }
        }
    }
    render = () => {
        const saveBtn = this.props.showSaveSettingsButton === true
            ? <Button icon="save" onClick={this.saveSettings}>Save Settings</Button>
            : <span/>;
        return(<Toolbar className="header">
                   <ToolbarItem>
                       <img src="/mb-logo.png" alt="MB"/>
                   </ToolbarItem>
                   <ToolbarSpacer/>
                   <ToolbarItem>
                       <p>Matchbox Edge</p>
                   </ToolbarItem>
                   <ToolbarSpacer/>
                   <ToolbarItem>
                        {saveBtn}
                       <Button icon="check-circle" onClick={this.statusClick}>Status</Button>
                       <Button icon="user" onClick={this.accountClick}>Account</Button>
                       <DropDownButton icon="gear" text="Settings" onItemClick={this.settingsClick}>
                           <DropDownButtonItem icon="gear" text="Settings" to="/settings"/>
                           <DropDownButtonItem icon="logout" text="Logout" action="logout"/>
                       </DropDownButton>
                   </ToolbarItem>
               </Toolbar>);
    }
}

function mapStateToProps (state, ownProps) {
    let showSaveSettingsButton = state.settings.settings.filter(s => s.hasChanges === true).length > 0;
    return{
        history: ownProps.history,
        loggedIn: state.authentication.loggedIn,
        showSaveSettingsButton
    };
}

function mapActionsToProps (dispatch){
    return{
        usrActions: bindActionCreators(userActions, dispatch),
        stgActions: bindActionCreators(settingActions, dispatch)
    }
}
export default withRouter(connect(mapStateToProps, mapActionsToProps)(Header));