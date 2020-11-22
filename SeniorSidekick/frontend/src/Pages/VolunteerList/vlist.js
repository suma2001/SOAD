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

class VolunteerList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      volunteers: [],
    }
  }

  async componentDidMount() {
    try { 
        const res = await fetch('http://127.0.0.1:8000/api/volunteers/1/');
        const volunteers = await res.json();
        this.setState({
            volunteers
        });
        console.log(volunteers);
    } catch (e) {
        console.log(e);
    }
  
  }
  render() {
    const {classes} = this.props;

    return (
      <div className={classes.root}>
      <Typography className={classes.typography}>List of Volunteers</Typography>
      <Grid container justify="space-evenly">
      {this.state.volunteers.map(volunteer => (
        <Grid sm={5}>
        <Card className={classes.card}>
          <CardHeader classes={{subheader: classes.subheader,}}
            avatar={
              <Avatar aria-label="person" className={classes.avatar}>
                P
              </Avatar>
            }
            title={volunteer.user.username}
            subheader={volunteer.phone_no}
            
            action={
              <span>
                <PhoneIcon/>
              </span>
              
            }
          />
          <CardContent>
            <Typography variant="body2" color="secondary" component="p">
            Alyssa Barnes is a 23-year-old health centre receptionist who enjoys cycling, swimming and reading. She is smart and generous
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

export default withStyles(useStyles)(VolunteerList);
