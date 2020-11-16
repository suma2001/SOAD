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

const useStyles = makeStyles((theme) => ({
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
  formControl: {
    minWidth: "100%",
  },
}));

export default function ServiceForm() {
  const classes = useStyles();
  const [service, setService] = React.useState('');
  const [open, setOpen] = React.useState(false);

  const handleChange = (event) => {
    setService(event.target.value);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleOpen = () => {
    setOpen(true);
  };

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        <form className={classes.form} noValidate>
        <FormControl className={classes.formControl}>
        <InputLabel id="demo-controlled-open-select-label">Select your service</InputLabel>
        <Select
          labelId="demo-controlled-open-select-label"
          id="demo-controlled-open-select"
          open={open}
          onClose={handleClose}
          onOpen={handleOpen}
          value={service}
          onChange={handleChange}
        >
          <MenuItem value="">
            <em>None</em>
          </MenuItem>
          <MenuItem value="Medicines">Medicines</MenuItem>
          <MenuItem value="Groceries">Groceries</MenuItem>
          <MenuItem value="Walking">Walking</MenuItem>
        </Select>
        </FormControl>
        <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="date"
            type="date"
            id="date"
            autoComplete="date"
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="time"
            type="time"
            id="time"
            autoComplete="time"
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
          >
            Request Service
          </Button>
        </form>
      </div>
    </Container>
  );
}