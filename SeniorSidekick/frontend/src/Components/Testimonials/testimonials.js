import React from 'react';
import Grid from '@material-ui/core/Grid';
import Carousel from 'react-bootstrap/Carousel';
import Container from "@material-ui/core/Container";
import Avatar from '@material-ui/core/Avatar';
import { makeStyles } from '@material-ui/core/styles';
import p1 from '../../Images/p1.jpg';
import p2 from '../../Images/p2.jpg';
import p3 from '../../Images/p3.jpg';
import p4 from '../../Images/p4.jpg';
import p5 from '../../Images/p5.jpg';

const useStyles = makeStyles((theme) => ({
    root: {
      display: 'flex',
      '& > *': {
        margin: theme.spacing(1),
      },
    },
    large: {
      width: theme.spacing(7),
      height: theme.spacing(7),
    },
  }));

export default function Testimonials() {
    const classes = useStyles();
    return(
        <div>
            <Carousel style={{backgroundColor: "#efeaf0"}}>
            <Carousel.Item interval={2000} style={{padding: "3% 0"}}>
            <Container>
                <Grid item xs={12}>
                    <Grid container justify="space-between" spacing={3}>
                        <Grid md={3} xs={12} container direction="column" justify="center" alignItems="center" >
                            <Avatar alt="person1" src={p1} className={classes.large} />
                            <p>A really helpful app/service!</p>
                        </Grid>
                        <Grid md={3} xs={12} container direction="column" justify="center" alignItems="center" >
                            <Avatar alt="person2" src={p2} className={classes.large} />
                            <p>A really helpful app/service!</p>
                        </Grid>
                        <Grid md={3} xs={12} container direction="column" justify="center" alignItems="center" >
                            <Avatar alt="person3" src={p3} className={classes.large} />
                            <p>A really helpful app/service!</p>
                        </Grid>
                    </Grid>
                </Grid>
                </Container>
            </Carousel.Item>
            <Carousel.Item interval={2000} style={{padding: "3% 0"}}>
            <Container>
                <Grid item xs={12}>
                    <Grid container justify="space-between" spacing={3}>
                        <Grid  md={3} xs={12} container direction="column" justify="center" alignItems="center" >
                            <Avatar alt="person4" src={p4} className={classes.large} />
                            <p>A really helpful app/service!</p>
                        </Grid>
                        <Grid  md={3} xs={12} container direction="column" justify="center" alignItems="center" >
                            <Avatar alt="person5" src={p5} className={classes.large} />
                            <p>A really helpful app/service!</p>
                        </Grid>
                        <Grid  md={3} xs={12} container direction="column" justify="center" alignItems="center" >
                            <Avatar alt="person1" src={p1} className={classes.large} />
                            <p>A really helpful app/service!</p>
                        </Grid>
                    </Grid>
                </Grid>
                </Container>
            </Carousel.Item>
            <Carousel.Item interval={2000} style={{padding: "3% 0"}}>
            <Container>
                <Grid item xs={12}>
                    <Grid container justify="space-between" spacing={3}>
                        <Grid  md={3} xs={12} container direction="column" justify="center" alignItems="center" >
                            <Avatar alt="person2" src={p2} className={classes.large} />
                            <p>A really helpful app/service!</p>
                        </Grid>
                        <Grid  md={3} xs={12} container direction="column" justify="center" alignItems="center" >
                            <Avatar alt="person5" src={p5} className={classes.large} />
                            <p>A really helpful app/service!</p>
                        </Grid>
                        <Grid  md={3} xs={12} container direction="column" justify="center" alignItems="center" >
                            <Avatar alt="person4" src={p4} className={classes.large} />
                            <p>A really helpful app/service!</p>
                        </Grid>
                    </Grid>
                </Grid>
                </Container>
            </Carousel.Item>
            </Carousel>
        </div>
    );
}