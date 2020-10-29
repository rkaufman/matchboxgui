import React from 'react';
import {withRouter} from 'react-router';
import { Switch, Route } from 'react-router-dom';
import { connect } from 'react-redux';
import {Drawer, DrawerContent} from '@progress/kendo-react-layout';
import {settingActions} from '../actions'
import { bindActionCreators } from "redux";
import RegularSettings from './RegularSettings';
import Detectors from './Detectors';
import CategoryItem from './CategoryItem';
import './settings.css';

export class Settings extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            expanded: true,
            selectedSettings: [],
            selectedCategory: null
        }
    }

    componentDidMount() {
        this.props.settingAction.getSettingCategories();
        this.props.settingAction.getSettings();
    }

    onSelect = (e) => {
        let settings = [];
        this.props.settings.map((x) => { if(parseInt(x.group) === e.itemTarget.props.id)settings.push(x);} );
        this.setState({
            selectedSettings: settings
        });

        this.props.history.push(e.itemTarget.props.route);
    }
    setSelectedItem = (pathName) => {
        let currentPath = this.props.categories.find(item => item.route === pathName);
        if (currentPath && currentPath.route) {
            return currentPath.name;
        }
        return '';
    }
    setSelectedId = (pathName) => {
        let currentPath = this.props.categories.find(item => item.route === pathName);
        if (currentPath) {
            return currentPath.id;
        }
        return 0;
    }
    drawerProps = {
        position: 'start',
        mode: 'push',
        width: 300
    }
    render() {
        const sel = this.props.categories.length === 0 ? '' : this.setSelectedItem(this.props.location.pathname);
        const selectedId = this.props.categories.length === 0 ? 0 : this.setSelectedId(this.props.location.pathname);
        return(<Drawer expanded={this.state.expanded}
                       className="setting-drawer full-height"
                       items={this.props.categories.map((item) => ({
                        id: item.id,
                        name: item.name,
                        route: item.route,
                        icon: item.icon,
                        selected: item.name === sel
                    }))}{...this.drawerProps}
                       onSelect={this.onSelect}
                       item={CategoryItem}>
                   <DrawerContent style={{paddingLeft: "1%"}}>
                       <Switch>
                           <Route exact path="/settings/mxserver" component={()=><RegularSettings categoryId={selectedId}/>}/>
                           <Route exact path="/settings/video" component={()=><RegularSettings categoryId={selectedId}/>}/>
                           <Route exact path="/settings/network" component={()=><RegularSettings categoryId={selectedId}/>}/>
                           <Route exact path="/settings/search" component={()=><RegularSettings categoryId={selectedId}/>}/>
                           <Route exact path="/settings/detection" component={()=><RegularSettings categoryId={selectedId}/>}/>
                           <Route exact path="/settings/detector" component={Detectors}/>
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
