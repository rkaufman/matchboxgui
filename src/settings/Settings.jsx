import React from 'react';
import {withRouter} from 'react-router';
import { Switch, Route } from 'react-router-dom';
import { connect } from 'react-redux';
import {Drawer, DrawerContent} from '@progress/kendo-react-layout';
import {settingActions} from '../actions/settingActions'
import { bindActionCreators } from "redux";
import Mxserver from './Mxserver';
import VideoSettings from './VideoSettings';
import NetworkConfiguration from './NetworkConfigurationSettings';
import DetectionSettings from './DetectionSettings';
import SettingItem from './SettingItem';
import './settings.css';

export class Settings extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            expanded: true,
            selectedId: this.items.findIndex(x=>x.selected===true)
        }
    }
    componentDidMount() {
        this.props.settingAction.getSettings();
    }

    items = [
        {text: "MXSERVER", icon:"fa fa-server fa-x3", selected: true, route: "/settings/mxserver"},
        {text: "Video Source", icon:"fa fa-video-camera fa-x3", selected: true, route: "/settings/video"},
        {text: "Network Configuration", icon:"fa fa-share-alt fa-x3", selected: true, route: "/settings/network"},
        {text: "Set Detection", icon:"fa fa-cogs fa-x3", selected: true, route: "/settings/detection"},
    ]
    handleClick = ()=>{
        
    }
    onSelect = (e)=>{
        this.setState({selectedId: e.itemIndex});
        this.props.history.push(e.itemTarget.props.route);
    }
    setSelectedItem = (pathName) => {
        let currentPath = this.items.find(item => item.route === pathName);
        if (currentPath && currentPath.text) {
            return currentPath.text;
        }
    }
    drawerProps = {
        position: 'start',
        mode: 'push',
        width: 300
    }
    render(){
        let selected = this.setSelectedItem(this.props.location.pathName)
        return(<Drawer expanded={this.state.expanded}
                    className="setting-drawer"
                    items={this.items.map((item)=>({
                        ...item, selected: item.text === selected
                    }))}{...this.drawerProps}
                    onSelect={this.onSelect}
                    item={SettingItem}>
                        <DrawerContent>
                            <Switch>
                                <Route exact path="/settings/mxserver" component={Mxserver}/>
                                <Route exact path="/settings/video" component={VideoSettings}/>
                                <Route exact path="/settings/network" component={NetworkConfiguration}/>
                                <Route exact path="/settings/detection" component={DetectionSettings}/>
                            </Switch>
                        </DrawerContent>
                    </Drawer>)
    }
}

const mapStateToProps = (state,ownProps)=>{
    return {
        settings: state.settings,
        history: ownProps.history
    }
}
const mapDispatchToProps = (dispatch)=>{
    return{
        settingAction: bindActionCreators(settingActions, dispatch)
    }
}
export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Settings));
