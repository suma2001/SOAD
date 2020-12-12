import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import Container from "@material-ui/core/Container";
import content from '../../Images/content-image.jpg';

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

export default function HomeHero() {
  const classes = useStyles();
  console.log(localStorage.getItem('token'));

  return (
    <Container style={{backgroundColor: "#efeaf0"}} className={classes.control}>
    <Grid container className={classes.root} spacing={3} style={{margin: "3% 0"}}>
      <Grid item xs={12}>
        <Grid container justify="space-around" spacing={3}>
          <Grid md={4} xs={8}>
              <Typography variant="h3" style={{marginTop: "12%"}}>
                  Envision a community where aging is a positive experience
              </Typography>
              <Typography variant="body2" style={{fontWeight: "500"}}>Connect elderly with young adults</Typography>
              <Button href="/request-service" style={{backgroundColor: "#63326E", padding: "5px 20px", margin: "15px 5px"}} color="secondary">Get Help</Button>
              <Button href="/map" style={{backgroundColor: "#63326E", padding: "5px 20px", margin: "15px 5px"}} color="secondary">Offer Help</Button>
          </Grid>
          <Grid>
              <Container>
                  <img src={content} alt="content" />
              </Container>
          </Grid>
        </Grid>
      </Grid>
    </Grid>
    </Container>
  );
}
