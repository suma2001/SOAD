import React, {Component} from "react";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardHeader from "@material-ui/core/CardHeader";
import CardContent from "@material-ui/core/CardContent";
import Avatar from "@material-ui/core/Avatar";
import Typography from "@material-ui/core/Typography";
import { red } from "@material-ui/core/colors";
import Grid from '@material-ui/core/Grid';
import axios from "axios";
import { withStyles } from '@material-ui/core/styles';
import PhoneIcon from '@material-ui/icons/Phone';
import Link from '@material-ui/core/Link';
import { Redirect } from 'react-router';
import Button from "@material-ui/core/Button";

const useStyles = theme => ({
  root: {
    maxWidth: "90%",
    margin: "5%",
  },
  card: {
    margin: "2% 0",
    backgroundColor: "#63326E",
    color: "#EFBC9B",
  },
  subheader: {
    color: "#EFBC9B",
  },
  avatar: {
    backgroundColor: red[500],
  },
  phone: {
    marginLeft: "1%",
  },
  typography: {
      marginLeft: "43%",
      fontSize: "26px",
  },
});

class ElderList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      elders: [],
      elderobjs: [],
      elder: '',
      volunteer: ''
    }
  }
  
  async componentDidMount() {
    try { 
        const vol = await fetch('http://127.0.0.1:8000/api/test_volunteer/'+localStorage.getItem('token')+'/');
        console.log("Vol: ", vol);
        const vollist = await vol.json();
        this.setState({
            elders: vollist.elder_ids
        });
        console.log(this.state.elders);
        var i, eldid, eld, l=[];
        for (i = 0; i < this.state.elders.length; i++) {
            eldid = this.state.elders[i];
            console.log(typeof(eldid));
            eld = await fetch('http://127.0.0.1:8000/api/elder/id/'+ eldid.toString() +'/');
            const obj = await eld.json();
            l.push(obj);
          }
        this.setState({
            elderobjs: l,
        })
        console.log(this.state.elderobjs);
    } catch (e) {
        console.log(e);
    }
  
  }

  handleSubmit = helper => event =>{
    this.setState({
      elder: helper.id,
      volunteer: localStorage.getItem('token')
    })
    var body = this.state
    
    console.log(JSON.stringify({
      elder: helper.id,
      volunteer: localStorage.getItem('token')
    }))
    // this.state.volunteer = volunteer.id
    fetch('http://127.0.0.1:8000/api/Deleteelders/', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        elder: helper.id,
        volunteer: localStorage.getItem('token')
      })
    }).then(function(response) {
      
      console.log(response);
      return response.json();
    });

    event.preventDefault();
  }

  // handleSubmit = text => event=> {
  //   console.log(text)
  //   event.preventDefault()
    
  // }

  render() {
    const {classes} = this.props;
    var val;
    return (
      <div className={classes.root}>
      <Typography className={classes.typography}>List of Elders</Typography>
      <Grid container justify="space-evenly">
      {this.state.elderobjs.map(obj => (
        <Grid sm={5}>
        <Card className={classes.card}>
            <CardHeader 
                    avatar={
                        <Avatar aria-label="person" className={classes.avatar}>
                          {obj.user.username[0]}
                        </Avatar>
                      }
                title={obj.user.username} 
                subheader={obj.user.email}
                action={
                    <span>
                      {/* <PhoneIcon/> */}
                      <Button variant="contained" onClick={this.handleSubmit(obj)}>Ask</Button>
                    </span>}
                />
          <CardContent>
            <Typography variant="body2" color="secondary" component="p">
                Age: {obj.elder_age}
            </Typography>
            <Typography variant="body2" color="secondary" component="p">
                Phone No: {obj.phone_no} 
            </Typography>
            <Typography variant="body2" color="secondary" component="p">
                Address: {obj.address_line1}, {obj.address_line2},  {obj.area},  {obj.city},  {obj.state},  {obj.country},  {obj.pincode}
            </Typography>
            
          </CardContent>
        </Card>
        </Grid>
      ))}
      </Grid>
      
      </div>
    );
}
}

export default withStyles(useStyles)(ElderList);
