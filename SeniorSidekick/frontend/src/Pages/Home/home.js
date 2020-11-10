import React from 'react';
import HeroHeader from '../../Components/HomeHero/homehero';
import Benefits from '../../Components/Benefits/benefits';
import Testimonials from '../../Components/Testimonials/testimonials';

export default function Home() {
    return(
        <div>
            <HeroHeader />
            <Benefits />
            <Testimonials />
        </div>
    );
}