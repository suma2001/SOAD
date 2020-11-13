import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Container from "@material-ui/core/Container";
import Typography from "@material-ui/core/Typography";
import CopyrightIcon from '@material-ui/icons/Copyright';
import TwitterIcon from '@material-ui/icons/Twitter';
import InstagramIcon from '@material-ui/icons/Instagram';
import FacebookIcon from '@material-ui/icons/Facebook';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  control: {
    padding: theme.spacing(2),
  },
}));

export default function Benefits() {
  const classes = useStyles();

  return (
    <div style={{backgroundColor: "#63326E"}}>
    <Container style={{backgroundColor: "#63326E"}} className={classes.control}>
    <Grid container className={classes.root} spacing={3} style={{margin: "3% 0"}}>
      <Grid item xs={12}>
        <Grid container justify="space-around" spacing={3}>
          <Grid container direction="row" justify="space-evenly" md={3} xs={12} style={{margin: "2%"}} >
              <TwitterIcon fontSize="large" style={{color: "#EFBC9B", marginTop: "2%"}} />
              <InstagramIcon fontSize="large" style={{color: "#EFBC9B", marginTop: "2%"}}/>
              <FacebookIcon fontSize="large" style={{color: "#EFBC9B", marginTop: "2%"}}/>
          </Grid>
          <Grid md={3} xs={12} container direction="column" justify="center" alignItems="center" style={{margin: "2%"}}>
              <Typography variant="h3" style={{color: "#EFBC9B"}}>
                  Senior Sunshine
              </Typography>
              <Typography variant="body2" align="center" style={{fontWeight: "500", color: "#EFBC9B"}}>
                  Making aging a happy process
              </Typography>
          </Grid>
          <Grid md={3} xs={12} container direction="column" justify="center" alignItems="center" style={{margin: "2%"}}>
              <Typography variant="h5" style={{color: "#EFBC9B"}}>
                <CopyrightIcon style={{marginRight: "5px", color: "#EFBC9B"}} />
                Copyright 2020
              </Typography>
              <Typography variant="body2" align="center" style={{fontWeight: "500", color: "#EFBC9B"}}>
                 Senior Sunshine
                </Typography>
          </Grid>
        </Grid>
      </Grid>
    </Grid>
    </Container>
    </div>
  );
}
