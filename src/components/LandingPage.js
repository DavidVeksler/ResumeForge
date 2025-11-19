import React, { useState, useEffect } from 'react';
import AppStorage from '../utils/storage';
import landingContent from '../data/landingContent.json';

// Import landing page components
import Navigation from './landing/Navigation';
import HeroSection from './landing/HeroSection';
import FeaturesSection from './landing/FeaturesSection';
import HowItWorksSection from './landing/HowItWorksSection';
import TestimonialsSection from './landing/TestimonialsSection';
import Footer from './landing/Footer';

const LandingPage = ({ onGetStarted }) => {
  const [email, setEmail] = useState('');

  // Load saved email on mount
  useEffect(() => {
    const savedEmail = AppStorage.getUserEmail();
    if (savedEmail) {
      setEmail(savedEmail);
    }
  }, []);

  const handleEmailSubmit = (e) => {
    e.preventDefault();
    if (email) {
      AppStorage.saveUserEmail(email);
      onGetStarted();
    }
  };

  return (
    <div className="landing-page">
      <Navigation onGetStarted={onGetStarted} />

      <HeroSection
        content={landingContent.hero}
        stats={landingContent.stats}
        email={email}
        setEmail={setEmail}
        onSubmit={handleEmailSubmit}
      />

      <FeaturesSection features={landingContent.features} />

      <HowItWorksSection steps={landingContent.howItWorks} />

      <TestimonialsSection testimonials={landingContent.testimonials} />

      <Footer />
    </div>
  );
};

export default LandingPage;
