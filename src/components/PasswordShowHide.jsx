import React from 'react';

class PasswordShowHide extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            hidden: true
        }
        this.handlePasswordChange = this.handlePasswordChange.bind(this);
        this.toggleShow = this.toggleShow.bind(this);
    }
    componentDidMount(){
        if(this.props.password){
            this.setState({password: this.props.password});
        }
    }
    handlePasswordChange(e){
        this.setState({password:e.target.value});
    }
    toggleShow(){
        this.setState({hidden: !this.state.hidden});
    }
    render(){
        return(
            <div>
                <input type={this.state.hidden?'password':'text'}
                value={this.state.password}
                onChange={this.handlePasswordChange}/>
                <button onClick={this.toggleShow}>Show / Hide</button>
            </div>
        )
    }
}

export default PasswordShowHide;