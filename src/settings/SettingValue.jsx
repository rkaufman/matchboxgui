import React from 'react'
import InputSelector from './InputSelector';
import { connect } from 'react-redux';
import { bindActionCreators } from "redux";
import {settingActions} from '../actions/settingActions'

export class SettingValue extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            selected:this.props.setting
        }
    }
    change = (e) => {
        let original = this.props.settings.find(s => parseInt(s._settingId) === parseInt(e.target.id));
        let next = JSON.parse(JSON.stringify(original));
        if (original._controlType._name === 'checkbox') {
            next._setting = e.target.checked.toString();
        } else {
            next._setting = e.target.value.toString();
        }
        this.props.actions.settingChanged({ next });
    }
    render() {
        return(<InputSelector {...this.props.setting} settingChanged={this.change.bind(this)}/>);
    }
}

const mapStateToProps = (state)=>{

    return {
        settings: state.settings.settings
    };
}
const mapActionsToProps = (dispatch) => {
    return {
        actions: bindActionCreators(settingActions,dispatch)
    }
}
export default connect(mapStateToProps, mapActionsToProps)(SettingValue);