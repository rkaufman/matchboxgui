import React from 'react';
import {withRouter} from 'react-router';
import {bindActionCreators} from 'redux';
import {userActions} from '../actions';
import {
    Toolbar,
    ToolbarItem,
    ToolbarSeparator,
    ToolbarSpacer,
    Button,
    ButtonGroup,
    DropDownButton,
    DropDownButtonItem,
    SplitButton,
    SplitButtonItem
} from '@progress/kendo-react-buttons';
import './header.css';
import { connect } from 'react-redux';

export class Header extends React.Component{
    constructor(props){
        super(props);
        this.state = {}
        this.logoutClick = this.logoutClick.bind(this);
    }
    logoutClick = function (){
        this.props.usrAction.logout().then(()=>{
            this.props.history.push('/login')
        });
    }
    accountClick = (e)=>{
        this.props.history.push('/users')
    }
    render = () => {
        return(<Toolbar className="header">
            <ToolbarItem>
                <img src="mb-logo.png" alt="MB" />
            </ToolbarItem>
            <ToolbarSpacer/>
            <ToolbarItem>
                <p>Matchbox</p>
            </ToolbarItem>
            <ToolbarSpacer/>
            <ToolbarItem>
                <Button icon="check-circle">Status</Button>
                <Button icon="user" onClick={this.accountClick}>Account</Button>
                <DropDownButton icon="gear" text="Settings">
                    <DropDownButtonItem icon="logout" text="Logout" onClick={this.logoutClick}/>
                </DropDownButton>
            </ToolbarItem>
        </Toolbar>)
    }
}

function mapStateToProps (state, ownProps){

    return{
        history: ownProps.history
    };
}

function mapActionsToProps (dispatch){
    return{
        usrActions: bindActionCreators(userActions)
    }
}
export default connect(mapStateToProps, mapActionsToProps)(Header);