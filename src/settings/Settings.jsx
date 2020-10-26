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
            selectedSettings: []
        }
    }
    componentDidMount() {
        this.props.settingAction.getSettingCategories();
        this.props.settingAction.getSettings();
    }

    handleClick = ()=>{
        
    }
    onSelect = (e)=> {
        //this.setState({
        //    selectedSettings: this.props.settings.find(x=>x.id === e.itemTarget.props.id)
        //});
        this.props.history.push(e.itemTarget.props.route);
    }
    setSelectedItem = (pathName) => {
        let currentPath = this.props.categories.find(item => item.route === pathName);
        if (currentPath && currentPath.text) {
            return currentPath.text;
        }
    }
    drawerProps = {
        position: 'start',
        mode: 'push',
        width: 300
    }
    render() {
        let selected = this.props.categories.length === 0 ? '' : this.setSelectedItem(this.props.location.pathName);
        return(<Drawer expanded={this.state.expanded}
                       className="setting-drawer"
                       items={this.props.categories.map((item) => ({
                        ...item,
                        selected: item.text === selected
                    }))}{...this.drawerProps}
                       onSelect={this.onSelect}
                       item={SettingItem}>
                   <DrawerContent style={{paddingLeft: "1%"}}>
                       <Switch>
                           <Route exact path="/settings/mxserver" component={()=><Mxserver setting={this.state.selectedSettings}/>}/>
                           <Route exact path="/settings/video" component={VideoSettings}/>
                           <Route exact path="/settings/network" component={NetworkConfiguration}/>
                           <Route exact path="/settings/detection" component={DetectionSettings}/>
                       </Switch>
                   </DrawerContent>
               </Drawer>);
    }
}

const mapStateToProps = (state,ownProps)=>{
    return {
        settings: state.settings.settings,
        categories: state.settings.categories,
        history: ownProps.history
    }
}
const mapDispatchToProps = (dispatch)=>{
    return{
        settingAction: bindActionCreators(settingActions, dispatch)
    }
}
export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Settings));
