import React from 'react';
import Hero from '../components/Hero';
import Features from '../components/Features';
import About from '../components/About';
import Contributors from '../components/Contributors';
import Footer from '../components/Footer';

const LandingPage: React.FC = () => {
  return (
    <div className="bg-slate-900 min-h-screen">
      <Hero />
      <Features />
      <About />
      <Contributors />
      <Footer />
    </div>
  );
};

export default LandingPage;
