import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Container from "@material-ui/core/Container";
import Typography from "@material-ui/core/Typography";
import ServiceForm from '../../Components/ServiceForm/index';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
}));

export default function RequestService() {
  const classes = useStyles();

  return (
    <div>
    <Container style={{backgroundColor: "#efeaf0"}}>
    <Grid container direction="column" justify="center" alignItems="center" xs={12} style={{margin: "5% 0"}}>
        <Typography variant="h3" color="primary">
            Request a service
        </Typography>
        <Grid md={4} xs={12} >
        <Typography variant="body2"align="center" style={{fontWeight: "500"}}>
            No matter what happens, your service is our duty
        </Typography>
        </Grid>
    </Grid>
    </Container>
    <ServiceForm />
    </div>
  );
}
