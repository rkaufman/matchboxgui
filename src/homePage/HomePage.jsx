import React from 'react';
import {ListView} from '@progress/kendo-react-listview';
import StatusRender from '../components/StatusRender';
import LogRender from '../components/LogRender';
import {bindActionCreators} from 'redux';
import './HomePage.css';
import {CameraPlaceHolder} from '../components/CameraPlaceHolder';
import Camera from '../components/Camera';
import { connect } from 'react-redux';
import {statusActions} from "../actions/statusActions";
import { logActions } from "../actions";
import { Pager }from '@progress/kendo-react-data-tools';

export class HomePage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            cameraStatus: "Disconnected",
            skip: 0,
            take: 5
        };
    }
    componentDidMount() {
        this.props.statActions.getStatuses();
        this.props.lgActions.getLogs();
    }
    handlePageChange = (e) => {
      this.setState({
        skip: e.skip,
        take: e.take
      });
    }

    render() {
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
                    <CameraPlaceHolder className="camera-placeholder" status={this.state.cameraStatus}/>
                    <Camera hidden/>
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
        lgActions: bindActionCreators(logActions, dispatch)
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(HomePage)
