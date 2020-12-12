import React from 'react';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import InputLabel from '@material-ui/core/InputLabel';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import { withStyles } from '@material-ui/core/styles';
import { Link } from '@material-ui/core';
import { browserHistory } from 'react-router';

const useStyles = theme => ({
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 5),
  },
  services: {
    width: '100%',
    padding: '17px',
    marginTop: theme.spacing(1),
    borderRadius: '4px',
  },
  formControl: {
    minWidth: "100%",
  },
});

class ServiceForm extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      name: '',
      time: '',
      services: [],
      validationError: '',
    }
  }

  componentDidMount() {
    fetch("http://127.0.0.1:8000/api/services/")
    .then((response) => {
      return response.json();
    })
    .then(data => {
      let servicesFromApi = data.map(service => {
        return {value: service.id, display: service.name}
      });
      this.setState({
        services: [{value: '', display: '(Select the service)'}].concat(servicesFromApi)
      });
    }).catch(error => {
      console.log(error);
    })
  }

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value});
  }


  handleSubmit = (event) => {
    var body = this.state
    console.log(body)
    fetch('http://127.0.0.1:8000/api/requestservice/', {
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
    browserHistory.push("/volunteer-list");
    // <Link to="/volunteer-list"/>
    event.preventDefault();
  }

  render() {
    // const classes = useStyles();
    const { name, time } = this.state;

    const {classes} = this.props;

    // const [services, setService] = React.useState('');
    // const [open, setOpen] = React.useState(false);

    // const handleChange = (event) => {
    //   setService(event.target.value);
    // };

    // const handleClose = () => {
    //   setOpen(false);
    // };

    // const handleOpen = () => {
    //   setOpen(true);
    // };
    return (
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <div className={classes.paper}>
          <form onSubmit={this.handleSubmit} className={classes.form} noValidate>
          {/* <FormControl className={classes.formControl}>
          <InputLabel id="demo-controlled-open-select-label">Select your service</InputLabel>
          <Select
            labelId="demo-controlled-open-select-label"
            id="demo-controlled-open-select"
            open={open}
            onClose={handleClose}
            onOpen={handleOpen}
            value={service_name}
            onChange={handleChange}
          >
            <MenuItem value="">
              <em>None</em>
            </MenuItem>
            {this.state.services.map((service) => 
                <MenuItem value={service.value}>{service.value}</MenuItem>)}
            
            <MenuItem value="Medicines">Medicines</MenuItem>
            <MenuItem value="Groceries">Groceries</MenuItem>
            <MenuItem value="Walking">Walking</MenuItem>
          </Select>
          </FormControl> */}
          <select className={classes.services} value={name}
                onChange={e => this.setState({name: e.target.value, validationError: e.target.value === "" ? "You must select a service" : ""})}>
                {this.state.services.map((service) => 
                <option key={service.value} value={service.value}>
                  {service.display}
                </option>)}
              </select>
              <div style={{color: 'red', marginTop: '5px'}}>
                {this.state.validationError}
              </div>
              <TextField
                variant="outlined"
                margin="normal"
                required
                name="time"
                value={time}
                label="Datetime"
                onChange={this.handleChange}
                type="datetime-local"
                id="time"
                autoComplete="time"
              />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              className={classes.submit}
              // href="/volunteer-list"
            >
              Request Service
            </Button>
          </form>
        </div>
      </Container>
    );
  }

}


export default withStyles(useStyles)(ServiceForm);