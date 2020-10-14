import React from 'react'
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
import './header.css'

export class Header extends React.Component{
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
                <Button icon="user">Account</Button>
                <Button icon="gear">Settings</Button>
            </ToolbarItem>
        </Toolbar>)
    }
}

export default Header;