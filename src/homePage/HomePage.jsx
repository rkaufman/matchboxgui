import React from 'react';
import {ListView} from '@progress/kendo-react-listview';
import StatusRender from '../components/StatusRender';
import LogRender from '../components/LogRender';
import {bindActionCreators} from 'redux';
import './HomePage.css';
import CameraPlaceHolder from '../components/CameraPlaceHolder';
import { connect } from 'react-redux';
import {statusActions} from "../actions/statusActions";
import { logActions } from "../actions";
import { Pager }from '@progress/kendo-react-data-tools';
import { settingActions } from "../actions";

export class HomePage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            cameraStatus: "Disconnected",
            skip: 0,
            take: 5,
            //statusTimeout:setInterval(()=>{
            //    this.props.statActions.getStatuses();
            //}, 30000),
            //logTimeout: setInterval(()=>{
            //    this.props.lgActions.getLogs();
            //}, 5000)
        };
    }
    componentDidMount() {
        this.props.statActions.getStatuses();
        this.props.lgActions.getLogs();
        this.props.setActions.getSettings();
    }
    componentWillUnmount() {
        if(this.state.logTimeout){
            clearInterval(this.state.logTimeout);
        }
        if(this.state.statusTimeout){
            clearInterval(this.state.statusTimeout);
        }
    }

    handlePageChange = (e) => {
      this.setState({
        skip: e.skip,
        take: e.take
      });
    }
    render() {
        let cameraStatus = this.props.statuses.filter(s => s.name === "StatusType.STREAM");
        return (
            <span>
                <div className="col-md-2 status-panel full-height">
                    <ListView data={this.props.statuses}
                        item={StatusRender}
                        className="lv-status vertical-center"/>
                </div>
                <div className="col-md-4 status-panel full-height">
                    <ListView data={this.props.logs.slice(this.state.skip, this.state.skip + this.state.take)}
                        item={LogRender}
                        className="lv-status"
                        style={{textAlign:'left'}}/>
                    <Pager skip={this.state.skip} take={this.state.take} onPageChange={this.handlePageChange} total={this.props.logs.length}/>
                </div>
                <div className="col-md-6  status-panel full-height">
                    <CameraPlaceHolder className="camera-placeholder" status={cameraStatus.length > 0 ? cameraStatus.status : false}/>
                </div>
            </span>
        );
    }
}

const mapStateToProps = (state,ownProps)=>{
    return {
        statuses: state.status.statuses,
        history: ownProps.history,
        logs: state.log.logs
    }
}
const mapDispatchToProps = (dispatch)=>{
    return{
        statActions: bindActionCreators(statusActions, dispatch),
        lgActions: bindActionCreators(logActions, dispatch),
        setActions: bindActionCreators(settingActions, dispatch)
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(HomePage)
