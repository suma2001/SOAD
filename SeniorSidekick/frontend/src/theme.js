import { createMuiTheme } from "@material-ui/core/styles";
const theme = createMuiTheme({
  palette: {
    primary: {
      main: "#63326E",
    },
    secondary: {
      main: "#EFBC9B",
    },
  },
  typography: {
    body1: {
      fontFamily: "Roboto Condensed",
    },
    body2: {
      fontFamily: "Abel",
    },
    h1: {
      fontFamily: "Yanone Kaffeesatz",
    },
    h3: {
        fontFamily: "Yanone Kaffeesatz",
      },
    h5: {
        fontFamily: "Yanone Kaffeesatz",
      },
  },
  margin : "0",
  padding: "0",
  body1: {
    fontWeight: 500,
  },
  button: {
    fontStyle: "Creepster",
  },
});
export default theme;
