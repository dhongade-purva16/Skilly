import React from 'react';
import { Link } from 'react-router-dom';
import { Search, PlayCircle, ArrowRight, Shield, Users, Briefcase, Star, Code, PenTool, TrendingUp, Database, FileText, FileCheck } from 'lucide-react';
import '../../styles/landing.css';

const FlipCard = ({ className, children, isMain = false }: { className: string, children: React.ReactNode, isMain?: boolean }) => {
  return (
    <div className={`flip-card-container ${className}`}>
      <div className="flip-card-inner">
        <div className={`flip-card-front ${isMain ? 'main-card-face' : 'bg-card-face'}`}>
          {children}
        </div>
        <div className={`flip-card-back ${isMain ? 'main-card-face' : 'bg-card-face'}`}>
          {children}
        </div>
      </div>
    </div>
  );
};

export const Landing = () => {
  return (
    <div className="landing-page">
      <nav className="landing-nav">
        <div className="brand">
          <div className="brand-icon-wrapper" style={{ background: 'linear-gradient(135deg, #2F6FED 0%, #14213D 100%)', borderRadius: '50%', padding: '4px' }}>
            <Users size={28} color="#ffffff" strokeWidth={2.5} />
          </div>
          <span className="brand-text"><span style={{animationDelay: '0.1s'}}>S</span><span style={{animationDelay: '0.2s'}}>k</span><span style={{animationDelay: '0.3s'}}>i</span><span style={{animationDelay: '0.4s'}}>l</span><span style={{animationDelay: '0.5s'}}>l</span><span style={{animationDelay: '0.6s'}}>y</span></span>
        </div>
        <div className="nav-links">
          <Link to="/" className="active">Home</Link>
          <Link to="/">Find Internships</Link>
          <Link to="/">For Students</Link>
          <Link to="/">For Companies</Link>
          <Link to="/">Resources</Link>
          <Link to="/">About Us</Link>
        </div>
        <div className="nav-actions">
          <button className="icon-btn"><Search size={18} /></button>
          <Link to="/login" className="btn-login">Log In</Link>
          <Link to="/register" className="btn-signup">Sign Up</Link>
        </div>
      </nav>
      <div className="hero-scale-wrapper">
        <div className="hero-cards-container">
        
        {/* Left Card 2 */}
        <FlipCard className="card-left-2">
           <div className="brand" style={{fontSize: 12, marginBottom: 16}}><span className="brand-text"><span style={{animationDelay: '0.1s'}}>S</span><span style={{animationDelay: '0.2s'}}>k</span><span style={{animationDelay: '0.3s'}}>i</span><span style={{animationDelay: '0.4s'}}>l</span><span style={{animationDelay: '0.5s'}}>l</span><span style={{animationDelay: '0.6s'}}>y</span></span></div>
           <h4>Empowering<br/>Students<br/>Every Step</h4>
           <p>From learning to placement, we are with you.</p>
           <div style={{display: 'flex', alignItems: 'center', gap: 12, marginTop: 'auto'}}>
             <div style={{background: '#F1F5F9', borderRadius: '50%', width: 40, height: 40}} />
             <div><div style={{fontWeight: 700, color: '#14213D'}}>95%</div><div style={{fontSize: 10, color: '#64748B'}}>Placement Rate</div></div>
           </div>
        </FlipCard>

        {/* Left Card 1 */}
        <FlipCard className="card-left-1">
           <div className="brand" style={{fontSize: 14, marginBottom: 20}}><span className="brand-text"><span style={{animationDelay: '0.1s'}}>S</span><span style={{animationDelay: '0.2s'}}>k</span><span style={{animationDelay: '0.3s'}}>i</span><span style={{animationDelay: '0.4s'}}>l</span><span style={{animationDelay: '0.5s'}}>l</span><span style={{animationDelay: '0.6s'}}>y</span></span></div>
           <h4>Learn. Grow.<br/>Achieve.</h4>
           <p>Access expert-led resources and mentorship to enhance your skills.</p>
           <div className="top-resources">
             <h5>Top Resources</h5>
             <div className="resource-item">
               <div className="resource-icon" style={{color: '#2F6FED'}}><FileText size={16}/></div>
               <div className="resource-text"><h6>Resume Building</h6><span>Create a standout resume</span></div>
             </div>
             <div className="resource-item">
               <div className="resource-icon" style={{color: '#F59E0B'}}><FileCheck size={16}/></div>
               <div className="resource-text"><h6>Interview Prep</h6><span>Practice and ace your dream interview.</span></div>
             </div>
           </div>
           <button className="btn-explore">Explore Resources <ArrowRight size={14}/></button>
        </FlipCard>

        {/* MAIN CENTER CARD */}
        <FlipCard className="main-card-container" isMain={true}>
           
           <div className="main-card-top-nav">
             <div className="brand" style={{fontSize: 18}}>
               <div className="brand-icon-wrapper" style={{ background: 'linear-gradient(135deg, #2F6FED 0%, #14213D 100%)', borderRadius: '50%', padding: '3px' }}>
                 <Users size={24} color="#ffffff" strokeWidth={2.5} />
               </div>
               <span className="brand-text"><span style={{animationDelay: '0.1s'}}>S</span><span style={{animationDelay: '0.2s'}}>k</span><span style={{animationDelay: '0.3s'}}>i</span><span style={{animationDelay: '0.4s'}}>l</span><span style={{animationDelay: '0.5s'}}>l</span><span style={{animationDelay: '0.6s'}}>y</span></span>
             </div>
             <div className="main-card-nav-links">
               <span className="active">Home</span>
               <span>Opportunities</span>
               <span>Resources</span>
             </div>
             <div style={{width: 24, height: 24, borderRadius: '50%', background: '#E2E8F0'}} />
           </div>

           <div className="main-card-content">
             <div className="main-card-left">
                <div className="badge-mission">
                  <Shield size={14} />
                  Your Future. Our Mission.
                </div>
                <h1 className="hero-title">Connect.<br/>Collaborate.<br/>Create Impact.</h1>
                <p className="hero-subtitle">A collaborative platform bridging the gap between students, colleges, and industry for real-world impact.</p>
                <div className="hero-actions">
                  <button className="btn-primary-large">Find Internships <ArrowRight size={16} /></button>
                  <button className="btn-outline-large">How It Works <PlayCircle size={16} /></button>
                </div>
                <div className="stats-grid">
                  <div className="stat-item">
                    <div className="stat-value"><Users size={20} color="#2F6FED" strokeWidth={2.5}/> 10K+</div>
                    <div className="stat-label">Students</div>
                  </div>
                  <div className="stat-item">
                    <div className="stat-value"><Briefcase size={20} color="#2F6FED" strokeWidth={2.5}/> 2K+</div>
                    <div className="stat-label">Companies</div>
                  </div>
                  <div className="stat-item">
                    <div className="stat-value"><Users size={20} color="#2F6FED" strokeWidth={2.5}/> 18K+</div>
                    <div className="stat-label">Opportunities</div>
                  </div>
                  <div className="stat-item">
                    <div className="stat-value"><Star size={20} color="#2F6FED" fill="#2F6FED" /> 4.8</div>
                    <div className="stat-label">Student Rating</div>
                  </div>
                </div>
             </div>
             <div className="main-card-right">
                <div className="main-card-image"></div>
             </div>
           </div>

           <div className="popular-domains">
             <div className="domains-header">
               <h3>Popular Domains</h3>
               <Link to="/">View All <ArrowRight size={14}/></Link>
             </div>
             <div className="domains-grid">
               <div className="domain-card">
                 <div className="domain-icon dev"><Code size={24}/></div>
                 <h4>Development</h4>
                 <p>1200+ Openings</p>
               </div>
               <div className="domain-card">
                 <div className="domain-icon design"><PenTool size={24}/></div>
                 <h4>Design</h4>
                 <p>850+ Openings</p>
               </div>
               <div className="domain-card">
                 <div className="domain-icon marketing"><TrendingUp size={24}/></div>
                 <h4>Marketing</h4>
                 <p>950+ Openings</p>
               </div>
               <div className="domain-card">
                 <div className="domain-icon data"><Database size={24}/></div>
                 <h4>Data Science</h4>
                 <p>600+ Openings</p>
               </div>
             </div>
           </div>
        </FlipCard>

        {/* Right Card 1 */}
        <FlipCard className="card-right-1">
           <h4>For Companies,<br/>With Impact</h4>
           <p>Hire talented interns and build the future workforce with us.</p>
           <div style={{marginTop: 20, marginBottom: 20}}>
             <div style={{display: 'flex', alignItems: 'center', gap: 12, marginBottom: 12}}>
               <Briefcase size={20} color="#2F6FED"/> 
               <div><div style={{fontWeight: 700, color: '#14213D'}}>2K+</div><div style={{fontSize: 10, color: '#64748B'}}>Hiring Companies</div></div>
             </div>
           </div>
           <div className="bg-card-img" style={{backgroundImage: 'url(https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80)'}}></div>
           <button className="btn-post">Post Internship <ArrowRight size={14}/></button>
        </FlipCard>

        {/* Right Card 2 */}
        <FlipCard className="card-right-2">
           <h4>Real Experience.<br/>Real Impact.</h4>
           <p>Work on real projects and make a difference from day one.</p>
           <div className="bg-card-img" style={{backgroundImage: 'url(https://images.unsplash.com/photo-1515169067868-5387ec356754?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80)', height: 100, marginBottom: 20}}></div>
           <div style={{fontSize: 12, fontWeight: 600, color: '#14213D', marginBottom: 10}}>Why Skilly?</div>
           <div style={{display: 'flex', flexDirection: 'column', gap: 6, fontSize: 10, color: '#64748B'}}>
             <div style={{display: 'flex', gap: 6}}><Shield size={12} color="#2F6FED"/> Verified Opportunities</div>
             <div style={{display: 'flex', gap: 6}}><Users size={12} color="#2F6FED"/> Expert Mentorship</div>
             <div style={{display: 'flex', gap: 6}}><Code size={12} color="#2F6FED"/> Skill Development</div>
           </div>
        </FlipCard>

      </div>
      </div>
    </div>
  );
};