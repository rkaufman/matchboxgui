import React from 'react';
import { connect } from 'react-redux';
import {ListView} from '@progress/kendo-react-listview';
import SettingItem from './SettingItem';
import SettingValue from './SettingValue';

export class RegularSettings extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            selected: {},
            changed: []
        }
        this.onSelect = this.onSelect.bind(this);
    }
    
    onSelect = (e)=> {
        let id = parseInt(e.currentTarget.getAttribute("data-id"));
        let setting = this.props.settings.find(x => x._settingId === id);
        this.setState({
            selected: setting
        });
    }
    onSettingChanged = (e) => {
        //update state of selected

    }
    filterSettings = () => {
        let filt = [];
        this.props.settings.map(s => { if (parseInt(s._group) === this.props.categoryId) filt.push(s); });
        return filt;
    }
        
    render() {
        const settings = this.props.categoryId > 0 ? this.filterSettings() : [];
        return(<span>
                <ListView style={{width:"25%", float:"left", backgroundColor:"transparent"}} data={settings} item={(x)=><SettingItem {...x} click={this.onSelect}/>}/>
                <SettingValue setting={this.state.selected}/>
                </span>
            );
    }
}
const mapStateToProps = (state,ownProps)=>{

    return {
        history: ownProps.history,
        category: state.settings.categories,
        settings: state.settings.settings
    };
}
export default connect(mapStateToProps)(RegularSettings);