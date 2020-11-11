import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { ThemeProvider } from "@material-ui/core/styles";
import theme from './theme';
import Header from './Components/Header/header';
import Footer from './Components/Footer/footer';
import Home from './Pages/Home/home';
import VolunteerLogin from './Pages/Login/volunteerLogin';
import VolunteerRegister from './Pages/Register/volunteerRegister';
import ElderLogin from './Pages/Login/elderLogin';
import ElderRegister from './Pages/Register/elderRegister';
import RequestService from './Pages/RequestService/service';
import VolunteerList from './Pages/VolunteerList/vlist';
import Profile from './Pages/Profile/profile';
import ContactUs from './Pages/ContactUs/contact';
import Feedback from './Pages/Feedback/feedback';

function App() {
  return (
    <Router>
      <ThemeProvider theme={theme}>
      <div className="App">
        <Header />
        <Route exact path="/">
          <Home />
        </Route>
        <Route exact path="/volunteer-login">
          <VolunteerLogin />
        </Route>
        <Route exact path="/volunteer-register">
          <VolunteerRegister />
        </Route>
        <Route exact path="/elder-login">
          <ElderLogin />
        </Route>
        <Route exact path="/elder-register">
          <ElderRegister />
        </Route>
        {/*<Route exact path="/request-service">
          <RequestService />
        </Route>
        <Route exact path="/volunteer-list">
          <VolunteerList />
        </Route>
        <Route exact path="/profile"> {/*make this as /profile:id later for each volunteer*/}
          {/* <Profile />
        </Route>
        <Route exact path="/contact-us">
          <ContactUs />
        </Route>
        <Route exact path="/feedback">
          <Feedback />
        </Route> */}
        <Footer />
      </div>
      </ThemeProvider>
    </Router>
  );
}

export default App;