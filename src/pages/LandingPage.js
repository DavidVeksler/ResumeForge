import React, { useState, useEffect } from 'react';
import AppStorage from '../utils/storage';
import landingContent from '../data/landingContent.json';

// Import landing page components
import Navigation from '../components/landing/Navigation';
import HeroSection from '../components/landing/HeroSection';
import FeaturesSection from '../components/landing/FeaturesSection';
import HowItWorksSection from '../components/landing/HowItWorksSection';
import TestimonialsSection from '../components/landing/TestimonialsSection';
import Footer from '../components/landing/Footer';

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
