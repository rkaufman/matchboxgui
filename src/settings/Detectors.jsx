import React from 'react';
import { Card, CardBody, CardTitle, CardActions } from '@progress/kendo-react-layout';
import { Button } from '@progress/kendo-react-buttons';
import { settingActions } from '../actions'
import { bindActionCreators } from "redux";
import { connect } from 'react-redux';


class Detectors extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
        }
    }
    componentDidMount = () => {
        this.props.settingAction.getDetectors();
    }
    changeDetector = (e)=> {
        let det = this.props.detectors.filter(d => d.id === parseInt(e.target.id))[0];
        this.props.settingAction.changeDetector(parseInt(e.target.id), det.selected);
    }
    render() {
        return (<span>
                    <div className="row">
                        <div style={{ display: 'flex', justifyContent: 'space-evenly' }}>
                            {this.props.detectors.map(d => {
                                let st = d.selected === true ? {width: 200, backgroundColor: 'white', color: '#3d3d3d', marginTop: '5%'} : { width: 200, backgroundColor: '#3d3d3d', color: 'white', marginTop: '5%' }
                                let c = d.selected === true ? 'card-button-selected' : 'card-button';
                                return(<Card style={st} orientation='horizontal'>
                                           <CardBody>
                                               <CardTitle><i className={d.icon}/></CardTitle>
                                               <CardTitle><b>{d.name}</b></CardTitle>
                                               <CardActions orientation='horizontal' style={{ textAlign: 'center' }
}><Button look='clear' onClick={this.changeDetector} id={d.id} className={c}>{d.selected === true
    ? 'Deselect'
    : 'Select'}</Button></CardActions>
                                           </CardBody>
                                       </Card>
                                    );
                    })}

                        </div>
                    </div>
                    <div className="row">
                <div className="col-md-12" style={{paddingTop:'5em', fontSize:'large'}}>
                    <p>More than one detector can be selected a the same time. Selecting only one will tell Matchbox Edge to only look for that type of item, &quot;Face&quot; will only search for faces, etc.</p></div>
                    </div>
                </span>);
    }
}
const mapStateToProps = (state) => {
    return {
        detectors: state.settings.detectors
    }
}
const mapDispatchToProps = (dispatch) => {
    return {
        settingAction: bindActionCreators(settingActions, dispatch)
    }
}
export default connect(mapStateToProps, mapDispatchToProps)(Detectors);
