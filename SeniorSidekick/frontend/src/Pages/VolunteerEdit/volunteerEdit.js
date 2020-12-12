import React from 'react';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';

function Copyright() {
  return (
    <Typography variant="body2" color="textSecondary" align="center" style={{paddingBottom: '20px'}}>
      {'Copyright © '}
      <Link color="inherit" href="https://material-ui.com/">
        Senior Sunshine
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
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
    marginTop: theme.spacing(3),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

export default function VolunteerEdit() {
  const classes = useStyles();

  return (
    <Container component="main" maxWidth="md">
      <CssBaseline />
      <div className={classes.paper}>
        <Typography component="h1" variant="h5">
          Edit Profile
        </Typography>
        <form className={classes.form} noValidate>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={4}>
              <TextField
                autoComplete="fname"
                name="firstName"
                variant="outlined"
                required
                fullWidth
                id="firstName"
                label="First Name"
                autoFocus
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <TextField
                variant="outlined"
                required
                fullWidth
                id="lastName"
                label="Last Name"
                name="lastName"
                autoComplete="lname"
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <TextField
                autoComplete="age"
                name="age"
                variant="outlined"
                required
                fullWidth
                id="age"
                label="Age"
                autoFocus
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                variant="outlined"
                required
                fullWidth
                id="email"
                label="Email Address"
                name="email"
                autoComplete="email"
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                variant="outlined"
                required
                fullWidth
                id="phone number"
                label="Phone Number"
                name="phone number"
                autoComplete="phone number"
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                variant="outlined"
                required
                fullWidth
                id="address line 1"
                label="Address line 1"
                name="address line 1"
                autoComplete="address line 1"
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                variant="outlined"
                required
                fullWidth
                id="address line 2"
                label="Address line 2"
                name="address line 2"
                autoComplete="address line 2"
              />
            </Grid>
            <Grid item xs={4}>
              <TextField
                variant="outlined"
                required
                fullWidth
                id="area"
                label="Area"
                name="area"
                autoComplete="area"
              />
            </Grid>
            <Grid item xs={4}>
              <TextField
                variant="outlined"
                required
                fullWidth
                id="city"
                label="City"
                name="city"
                autoComplete="city"
              />
            </Grid>
            <Grid item xs={4}>
              <TextField
                variant="outlined"
                required
                fullWidth
                id="state"
                label="State"
                name="state"
                autoComplete="state"
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                variant="outlined"
                required
                fullWidth
                id="country"
                label="Country"
                name="country"
                autoComplete="country"
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                variant="outlined"
                required
                fullWidth
                id="pincode"
                label="Pincode"
                name="pincode"
                autoComplete="pincode"
              />
            </Grid>
          </Grid>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
          >
            Submit
          </Button>
        </form>
      </div>
      <Box mt={5}>
        <Copyright />
      </Box>
    </Container>
  );
}