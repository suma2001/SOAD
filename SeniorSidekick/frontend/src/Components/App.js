import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { ThemeProvider } from "@material-ui/core/styles";
import theme from './theme';
import Header from './Components/Header/header';
import Footer from './Components/Footer/footer';
import Home from './Pages/Home/home';
import Login from './Pages/Login/login';
import Register from './Pages/Register/register';
import RequestService from './Pages/RequestService/service';
import VolunteerList from './Pages/VolunteerList/vlist';
import Profile from './Pages/Profile/profile';
import ContactUs from './Pages/ContactUs/contact';
import Feedback from './Pages/Feedback/feedback';
import SimpleMap from '../SimpleMap';

function App() {
  return (
    <Router>
      <ThemeProvider theme={theme}>
      <div className="App">
        {/* <Header/> */}
        <Route exact path="/">
          <Home />
        </Route>
        <Route exact path="/login">
          <Login />
        </Route>
        <Route exact path="/register">
          <Register />
        </Route>
        <Route exact path="/request-service">
          <RequestService />
        </Route>
        <Route exact path="/volunteer-list">
          <VolunteerList />
        </Route>
        {/* <Route exact path="/profile">*/} {/*make this as /profile:id later for each volunteer*/}
          {/* <Profile />
        </Route>
        <Route exact path="/contact-us">
          <ContactUs />
          </Route> */}
        <Route exact path="/feedback">
          <Feedback />
        </Route>
        <Route exact path="/map">
          <SimpleMap />
        </Route>
        <Footer />
      </div>
      </ThemeProvider>
    </Router>
  );
}

export default App;