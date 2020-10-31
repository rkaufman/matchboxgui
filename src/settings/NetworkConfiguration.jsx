import React from 'react';
import { Toolbar, ToolbarItem, Button, ToolbarSpacer } from '@progress/kendo-react-buttons'
import { Splitter } from '@progress/kendo-react-layout';
import { Form, Field, FormElement } from '@progress/kendo-react-form';
import { Input } from '@progress/kendo-react-inputs';

export class NetworkConfiguration extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            panes: [
                { size: '30%', min: '20px', collapsible: true },
                { size: '30%', min: '20px', collapsible: true },
                { collapsible: true }
            ],
            ipAddress: '0.0.0.0',
            netmask: '0.0.0.0',
            gateway: '0.0.0.0',
            dhcp: true
        }
    }
    handleSubmit = (e) => {

    }
    onSplitterChange = (e) => {
        this.setState({
            panes: e.newState
        });
    }

    render() {
        return (<div className="full-height">
            <Toolbar>
                <ToolbarItem><h2><b>Network Configuration</b></h2></ToolbarItem>
                <ToolbarSpacer />
                <ToolbarItem><Button title="Restore original network configuration."><b>Reset to Default</b></Button></ToolbarItem>
            </Toolbar>
            <Splitter panes={this.state.panes} onChange={this.onSplitterChange} orientation={'horizontal'}>
                <div className="pane-content">
                    <h3><b>Current Network Configuration</b></h3>
                    <div><label>IP Address: </label>&nbsp;<label>{this.state.ipAddress}</label></div>
                    <div><label>Subnet Mask: </label>&nbsp;<label>{this.state.netmask}</label></div>
                    <div><label>Default Gateway: </label>&nbsp;<label>{this.state.gateway}</label></div>
                </div>
                <div>
                    <h3><b>New Network Configuration</b></h3>
                    <Form onSubmit={this.handleSubmit} render={(props) => (
                        <FormElement>
                            <fieldset className="k-form-fieldset">
                                <div className="mb-3">
                                    <Field name={'ipAddress'} component={Input} label={'IP Address:'} />
                                </div>
                                <div className="mb-3">
                                    <Field name={'netmask'} component={Input} label={'Subnet Mask:'} />
                                </div>
                                <div className="mb-3">
                                    <Field name={'gateway'} component={Input} label={'Default Gateway:'} />
                                </div>
                            </fieldset>
                            <div className="k-form-buttons">
                                <Button type={'submit'} primary={true}
                                    title="Changes the device network settings. CAUTION: this could interrupt connectivity!"
                                    disabled={!props.allowSubmit}><b>Set Network Configuration</b></Button>
                                <Button onClick={props.onFormReset}>Clear</Button>
                            </div>
                        </FormElement>
                    )} />
                </div>
                <div>
                    <h3><b>Dynamic IP Address</b></h3>
                    <label style={{float: 'left', marginLeft: '25%'}}>Enable DHCP</label>
                    <label className="switch">
                        <input type="checkbox" checked={this.state.dhcp}></input>
                            <span className="slider round"></span>
                         
                     </label>
                 </div>
            </Splitter>
        </div>
        );
    }
}

export default NetworkConfiguration;
