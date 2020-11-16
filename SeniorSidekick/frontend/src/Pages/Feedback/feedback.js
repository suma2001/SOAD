import React from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import Link from '@material-ui/core/Link';
import Paper from '@material-ui/core/Paper';
import Box from '@material-ui/core/Box';
import Grid from '@material-ui/core/Grid';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';

function Copyright() {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      {'Copyright © '}
      <Link color="inherit" href="https://material-ui.com/">
        Senior Sunshine
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const useStyles = theme => ({
  root: {
    height: '100vh',
  },
  image: {
    backgroundImage: 'url(https://www.northpennymca.org/wp-content/uploads/2017/02/Helping-Older-Adult.jpg)',
    backgroundRepeat: 'no-repeat',
    backgroundColor:
      theme.palette.type === 'light' ? theme.palette.grey[50] : theme.palette.grey[900],
    backgroundSize: 'cover',
    backgroundPosition: 'center',
  },
  paper: {
    margin: theme.spacing(8, 4),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
});

class Feedback extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      volunteer_name: '',
      service_done: '',
      time: '',
      rating: '',
      custom_feedback: '',
    }
  }

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value});
  }

  handleSubmit = (event) => {
    var body = this.state
    fetch('http://127.0.0.1:8000/api/feedback/', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body)
    }).then(function(response) {
      console.log(response)
      return response.json();
    });

    event.preventDefault();
  }

  render(){
    const { volunteer_name, service_done, time, rating, custom_feedback } = this.state;
    const {classes} = this.props;

    return (
      <Grid container component="main" className={classes.root}>
        <CssBaseline />
        <Grid item xs={false} sm={4} md={7} className={classes.image} />
        <Grid item xs={12} sm={8} md={5} component={Paper} elevation={6} square>
          <div className={classes.paper}>
            <Avatar className={classes.avatar}>
              <LockOutlinedIcon />
            </Avatar>
            <Typography component="h1" variant="h5">
              Feedback
            </Typography>
            <form onSubmit={this.handleSubmit} className={classes.form} noValidate>
              <TextField
                variant="outlined"
                margin="normal"
                required
                fullWidth
                name="volunteer_name"
                value={volunteer_name}
                onChange={this.handleChange}
                label="Volunteer Name"
                type="volunteer_name"
                id="volunteer_name"
                autoComplete="volunteer_name"
              />
              <Grid container justify="space-between">
              <TextField
                variant="outlined"
                margin="normal"
                required
                id="service_done"
                value={service_done}
                onChange={this.handleChange}
                label="Service"
                name="service_done"
                autoComplete="service_done"
                autoFocus
              />
              <TextField
                variant="outlined"
                margin="normal"
                required
                name="time"
                value={time}
                onChange={this.handleChange}
                label="Time"
                type="time"
                id="time"
                autoComplete="time"
              />
              <TextField
                variant="outlined"
                margin="normal"
                required
                id="rating"
                value={rating}
                onChange={this.handleChange}
                label="Rating"
                name="rating"
                autoComplete="rating"
                autoFocus
              />
              </Grid>
              <TextField
                variant="outlined"
                margin="normal"
                fullWidth
                name="custom_feedback"
                value={custom_feedback}
                onChange={this.handleChange}
                label="Feedback"
                type="custom_feedback"
                id="custom_feedback"
                autoComplete="custom_feedback"
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                color="primary"
                className={classes.submit}
              >
                Submit Feedback
              </Button>
              <Box mt={5}>
                <Copyright />
              </Box>
            </form>
          </div>
        </Grid>
      </Grid>
    );    
  }
}

export default withStyles(useStyles)(Feedback);