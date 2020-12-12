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
import SimpleMap from './SimpleMap';
import Elderlist from './Pages/ElderList/elderlist';

function App() {
  return (
    <Router>
      <ThemeProvider theme={theme}>
      <div className="App">
        <Header/>
        <Route exact path="/">
          <Home />
          <Footer />
        </Route>
        <Route exact path="/login">
          <Login />
          <Footer />
        </Route>
        <Route exact path="/register">
          <Register />
          <Footer />
        </Route>
        <Route exact path="/request-service">
          <RequestService />
          <Footer />
        </Route>
        <Route exact path="/volunteer-list">
          <VolunteerList />
          <Footer />
        </Route>
        <Route exact path="/profile"> {/*make this as /profile:id later for each volunteer*/}
          <Profile />
          <Footer />
        </Route>
        {/* <Route exact path="/contact-us">
          <ContactUs />
          </Route>  */}
        <Route exact path="/feedback">
          <Feedback />
          <Footer />
        </Route>
        <Route exact path="/elders">
          <Elderlist />
          <Footer />
        </Route>
        <Route exact path="/map">
          <SimpleMap />
          <Footer />
        </Route>
      </div>
      </ThemeProvider>
    </Router>
  );
}

export default App;