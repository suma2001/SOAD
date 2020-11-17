import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Container from "@material-ui/core/Container";
import Typography from "@material-ui/core/Typography";
import ErrorIcon from '@material-ui/icons/Error';
import EmojiEmotionsIcon from '@material-ui/icons/EmojiEmotions';
import SignalCellularAltIcon from '@material-ui/icons/SignalCellularAlt';
import Paper from '@material-ui/core/Paper';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  paper: {
    height: 140,
    width: 100,
  },
  control: {
    padding: theme.spacing(2),
  },
}));

export default function Benefits() {
  const classes = useStyles();

  return (
    <Container style={{backgroundColor: "#efeaf0"}} className={classes.control}>
    <Grid container className={classes.root} spacing={3} style={{marginBottom: "3%", marginTop: "1%"}}>
      <Grid item xs={12}>
        <Grid container justify="space-around" spacing={3}>
          <Grid container direction="column" justify="center" alignItems="center" xs={12} md={3} style={{margin: "2%"}}>
              <ErrorIcon fontSize="large" color="primary"/>
              <Typography data-testid="goal" variant="h3">
                  Goal
              </Typography>
              <Typography data-testid="goal_text" variant="body2" align="center" style={{fontWeight: "500"}}>
                  Connect elderly with young adults. Should add some more content in this part
              </Typography>
          </Grid>
          <Grid xs={12} md={3} container direction="column" justify="center" alignItems="center" style={{margin: "2%"}}>
              <EmojiEmotionsIcon fontSize="large" color="primary"/>
              <Typography data-testid="interactive" variant="h3">
                  Interactive
              </Typography>
              <Typography data-testid="interactive_text" variant="body2" align="center" style={{fontWeight: "500"}}>
                  User-friendly UI to make it accessible and easy for the seniors to interact with the website
              </Typography>
          </Grid>
          <Grid xs={12} md={3} container direction="column" justify="center" alignItems="center" style={{margin: "2%"}}>
              <SignalCellularAltIcon fontSize="large" color="primary"/>
              <Typography data-testid="connectivity" variant="h3">
                  Connectivity
              </Typography>
              <Typography data-testid="connectivity_text" variant="body2" align="center" style={{fontWeight: "500"}}>
                 Help foster the connectivity and sharing of meaningful experiences
                </Typography>
          </Grid>
        </Grid>
      </Grid>
    </Grid>
    <Container>
    <Paper style={{backgroundColor: "#63326E"}} variant="outlined" elevation={2}>
    <Grid container direction="column" justify="center" alignItems="center" xs={12} style={{margin: "5% 0"}}>
        <Typography data-testid="solution" variant="body2" style={{fontSize: "20px", fontWeight: "500", marginBottom: "2%"}}>
            SOLUTION
        </Typography>
        <Typography data-testid="potential" variant="h3" style={{color: "#EFBC9B"}}>
            Unlock the Potential
        </Typography>
        <Grid md={4} xs={12} >
        <Typography data-testid="solution_text" variant="body2"align="center" style={{fontWeight: "500"}}>
            A website that connects seniors with young volunteers to 
            help them with their daily tasks, activities and also have 
            a buddy to talk to when they want company
        </Typography>
        </Grid>
    </Grid>
    </Paper>
    </Container>
    </Container>
  );
}
