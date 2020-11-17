import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardHeader from "@material-ui/core/CardHeader";
import CardContent from "@material-ui/core/CardContent";
import Avatar from "@material-ui/core/Avatar";
import Typography from "@material-ui/core/Typography";
import { red } from "@material-ui/core/colors";
import Grid from '@material-ui/core/Grid';

const useStyles = makeStyles((theme) => ({
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
  typography: {
      marginLeft: "43%",
      fontSize: "26px",
  },
}));

export default function VolunteerList() {
  const classes = useStyles();
  return (
    <div className={classes.root}>
    <Typography className={classes.typography}>List of Volunteers</Typography>
    <Grid container justify="space-evenly">
    <Grid sm={5}>
    <Card className={classes.card}>
      <CardHeader classes={{subheader: classes.subheader,}}
        avatar={
          <Avatar aria-label="person" className={classes.avatar}>
            P
          </Avatar>
        }
        title="FirstName LastName"
        subheader="City, State"
      />
      <CardContent>
        <Typography variant="body2" color="secondary" component="p">
        Alyssa Barnes is a 23-year-old health centre receptionist who enjoys cycling, swimming and reading. She is smart and generous
        </Typography>
      </CardContent>
    </Card>
    </Grid>
    <Grid sm={5}>
    <Card className={classes.card}>
      <CardHeader classes={{subheader: classes.subheader,}}
        avatar={
          <Avatar aria-label="person" className={classes.avatar}>
            R
          </Avatar>
        }
        title="Random Random"
        subheader="City, State"
      />
      <CardContent>
        <Typography variant="body2" color="secondary" component="p">
        Katherine Rogers is a 27-year-old chef at chain restaurant who enjoys walking, appearing in the background on TV and eating out. She is energetic and creative
        </Typography>
      </CardContent>
    </Card>
    </Grid>
    </Grid>
    </div>
  );
}
