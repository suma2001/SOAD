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
import PersonIcon from '@material-ui/icons/Person';
import HomeIcon from '@material-ui/icons/Home';
import Switch from '@material-ui/core/Switch';

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
  title: {
    fontSize: "20px",
    fontWeight: "fontWeightMedium",
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

class Profile extends Component {
  constructor(props) {
    super(props);
    this.state = {
      volunteer: '',
      username: '',
      email: '',
      availability: ''
    }
  }
  
  async componentDidMount() {
    // const { id } = this.props.location.state
    // console.log(id);
    try { 
        const res = await fetch('http://127.0.0.1:8000/api/test_volunteer/'+localStorage.getItem('token')+'/');
        const volunteer = await res.json();
        // console.log(this.props.location.state);
        console.log(volunteer);
        this.setState({
            volunteer: volunteer,
            username: volunteer.user.username,
            email: volunteer.user.email,
            availability: volunteer.availability
        });
        console.log(volunteer.user.username);
    } catch (e) {
        console.log(e);
    }
  
  }

  handleChange = (event) => {
    this.setState({
        availability: true
    });
  };

  render() {
    const {classes} = this.props;
    // console.log(data);
    var val;
    return (
      <div className={classes.root}>
      <Typography className={classes.typography}>Profile</Typography>
      <Grid container spacing={3} justify="space-evenly">
          <Grid item xs={6}>
            <Card className={classes.card} >
                <CardHeader classes={{subheader: classes.subheader, title: classes.title,}}
                    avatar={
                        <Avatar aria-label="Recipe" className={classes.avatar}>
                            <PersonIcon />
                        </Avatar>}

                    title={this.state.username}
                    subheader={this.state.email}
                    
                />
                <CardContent style={{alignContent: "center"}}>
                <Typography variant="subtitle2" color="secondary">
                Alyssa Barnes is a 23-year-old health centre receptionist who enjoys cycling, swimming and reading. She is smart and generous.
                </Typography>
                {/* <h6>{volunteer.services_available}</h6> */}
                </CardContent>
            </Card>
          </Grid>

          <Grid item xs={6}>
            <Card className={classes.card} >
                <CardHeader classes={{subheader: classes.subheader, title: classes.title, }}
                    avatar={
                        <Avatar aria-label="Recipe" className={classes.avatar}>
                            <HomeIcon />
                        </Avatar>}

                    title="ADDRESS"
                    
                />
                <CardContent style={{alignContent: "center"}}>
                <Typography variant="subtitle2" color="secondary">
                        {this.state.volunteer.address_line1}, {this.state.volunteer.address_line2},  {this.state.volunteer.area},  {this.state.volunteer.city},  {this.state.volunteer.state},  {this.state.volunteer.country},  {this.state.volunteer.pincode}
                </Typography>
                <Typography variant="subtitle2" color="secondary">
                    Availability <Switch
                    checked={this.state.volunteer.availability}
                    onChange={this.handleChange}
                    name="checkedA"
                    inputProps={{ 'aria-label': 'secondary checkbox' }}
                />
                </Typography>
                
                
                {/* <h6>{volunteer.services_available}</h6> */}
                </CardContent>
            </Card>
          </Grid>

      </Grid>
      </div>
    );
}
}

export default withStyles(useStyles)(Profile);
