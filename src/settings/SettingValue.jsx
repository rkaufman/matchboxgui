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
        let stgId = e.target.element && e.target.element.type === 'checkbox' ? parseInt(e.target.element.id) : parseInt(e.target.props.id);
        let original = this.props.settings.find(s => s.id === stgId);
        let next = JSON.parse(JSON.stringify(original));
        if (original.controlType.name === 'checkbox') {
            next.setting = e.value.toString();
        } else if (original.controlType.name === 'ddl') {
          next.setting = e.value;
        }else {
            next.setting = e.value.toString();
        }
        this.props.actions.settingChanged(next);
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
