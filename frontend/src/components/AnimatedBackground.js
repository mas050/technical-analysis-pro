import React, { useEffect, useRef } from 'react';
import './AnimatedBackground.css';

const AnimatedBackground = () => {
  const particlesRef = useRef(null);

  useEffect(() => {
    // Generate particles dynamically
    const container = particlesRef.current;
    if (!container) return;

    // Determine particle count based on screen size - MORE PARTICLES!
    const isMobile = window.innerWidth < 768;
    const particleCount = isMobile ? 30 : 60;

    // Clear existing particles
    container.innerHTML = '';

    // Create particles with varying sizes
    for (let i = 0; i < particleCount; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';
      
      // Random positioning
      particle.style.left = `${Math.random() * 100}%`;
      particle.style.animationDelay = `${Math.random() * 30}s`;
      particle.style.animationDuration = `${15 + Math.random() * 15}s`;
      
      // More varied sizes (1px to 5px)
      const size = 1 + Math.random() * 4;
      particle.style.width = `${size}px`;
      particle.style.height = `${size}px`;
      
      // Vary opacity for depth
      particle.style.opacity = 0.3 + Math.random() * 0.7;
      
      container.appendChild(particle);
    }

    // Handle parallax scrolling
    const handleScroll = () => {
      const scrolled = window.pageYOffset;
      const orbs = document.querySelectorAll('.orb');
      const particles = document.querySelectorAll('.particle');
      
      orbs.forEach((orb, index) => {
        const speed = 0.2 + (index * 0.1);
        orb.style.transform = `translateY(${scrolled * speed}px)`;
      });
      
      particles.forEach((particle, index) => {
        const speed = 0.3 + (index * 0.02);
        particle.style.transform = `translateY(${scrolled * speed}px)`;
      });
    };

    window.addEventListener('scroll', handleScroll);
    
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return (
    <div className="animated-background">
      {/* Gradient Orbs */}
      <div className="orb orb-1"></div>
      <div className="orb orb-2"></div>
      <div className="orb orb-3"></div>
      <div className="orb orb-4"></div>
      
      {/* Floating Particles */}
      <div className="particles-container" ref={particlesRef}></div>
    </div>
  );
};

export default AnimatedBackground;
