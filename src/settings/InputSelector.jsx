import React from 'react'
import { Checkbox, NumericTextBox, Slider, Input } from '@progress/kendo-react-inputs';
import { DropDownList } from '@progress/kendo-react-dropdowns';

export class InputSelector extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            text: props.setting,
            typing: false,
            typingTimeout: 0,
            fltValue: parseFloat(props.setting),
            fltTimeout: 0,
            intValue: parseInt(props.setting),
            intTimeout: 0
        }
    }
    inputChange = (e) => {
        if (this.state.typingTimeout) {
            clearTimeout(this.state.typingTimeout);
        }
        this.setState({
            text: e.value,
            typing: false,
            typingTimeout: setTimeout(() => {
                this.props.settingChanged(e);
            }, 2000)
        });
    }

    fltChanged = (e) => {
        if (this.state.fltTimeout) {
            clearTimeout(this.state.fltTimeout);
        }
        this.setState({
            fltValue: e.value,
            fltTimeout: setTimeout(() => {
                this.props.settingChanged(e);
            },
                500)
        });
    }
    intChanged = (e) => {
      if (this.state.intTimeout) {
        clearTimeout(this.state.intTimeout);
      }
      this.setState({
        intValue: e.value,
        intTimeout: setTimeout(() => {
            this.props.settingChanged(e);
          },
          500)
      });
    }

    render() {
        if (this.props.controlType === undefined) return <span />;
        let input = null;
        let videoInputModes = [
            { text: 'Onboard', id: 1 },
            { text: 'RTSP', id: 2 },
            { text: 'YouTube', id: 3 },
            { text: 'File', id: 4 }
        ];
        switch (this.props.controlType.name) {
            case 'checkbox':
                input =
                    <Checkbox checked={this.props.setting.toLowerCase() === 'true'} id={
                        this.props.id.toString()} onChange={this.props.settingChanged} />;
                break;
            case 'ddl':
                input =
                    <DropDownList dataItemKey="id" id={this.props.id.toString()} textField="text" value={this.props.setting} data={
                        videoInputModes} onChange={this.props.settingChanged} />;
                break;
            case 'number':
                input =
                    <NumericTextBox id={this.props.id.toString()} value={this.state.intValue} onChange={this.props.settingChanged} spinners={true} />;
                break;
            case 'decflt':
                input =
                    <Slider id={this.props.id.toString()} value={this.state.fltValue} step={
                        parseFloat(this.props.step)} max={parseFloat(this.props.max)} min={parseFloat(this.props.min)} onChange={this.fltChanged
                        } />;
                break;
            case 'pwd':
                input =
                    <Input type="password" placeholder={this.props.placeholder
                    } id={this.props.id.toString()} value={this.state.text} onChange={this.inputChange} />;
                break;
            case 'tb':
            default:
                input =
                    <Input type="text" placeholder={this.props.placeholder} id={this.props.id.toString()} value={this.state.text
                    } onChange={this.inputChange} />;
                break;
        }
        return (<div style={{ marginTop: "5%" }}>
            <div>
                <label>{this.props.label}</label></div>
            {input}
            <div>
                <p>{this.props.help}</p></div>
        </div>);
    }

}

export default InputSelector;
