import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardHeader from "@material-ui/core/CardHeader";
import CardContent from "@material-ui/core/CardContent";
import Avatar from "@material-ui/core/Avatar";
import Typography from "@material-ui/core/Typography";
import { red } from "@material-ui/core/colors";

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
  }
}));

export default function VolunteerList() {
  const classes = useStyles();
  return (
    <div className={classes.root}>
    <Typography className={classes.typography}>List of Volunteers</Typography>
    <Card className={classes.card}>
      <CardHeader classes={{subheader: classes.subheader,}}
        avatar={
          <Avatar aria-label="person" className={classes.avatar}>
            P
          </Avatar>
        }
        title="Prahitha Movva"
        subheader="Visakhapatnam, Andhra Pradesh"
      />
      <CardContent>
        <Typography variant="body2" color="secondary" component="p">
          Biography comes here
        </Typography>
      </CardContent>
    </Card>
    <Card className={classes.card}>
      <CardHeader classes={{subheader: classes.subheader,}}
        avatar={
          <Avatar aria-label="person" className={classes.avatar}>
            R
          </Avatar>
        }
        title="Random Random"
        subheader="Visakhapatnam, Andhra Pradesh"
      />
      <CardContent>
        <Typography variant="body2" color="secondary" component="p">
          Biography comes here
        </Typography>
      </CardContent>
    </Card>
    </div>
  );
}
