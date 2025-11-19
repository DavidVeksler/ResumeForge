import React from 'react';

const TestimonialCard = ({ name, role, company, rating, text, avatar }) => (
  <div className="col-lg-4 mb-4">
    <div className="testimonial-card h-100">
      <div className="testimonial-rating mb-3">
        {[...Array(rating)].map((_, i) => (
          <i key={i} className="bi bi-star-fill"></i>
        ))}
      </div>
      <blockquote className="mb-4">
        "{text}"
      </blockquote>
      <div className="testimonial-author">
        <div className="author-avatar">{avatar}</div>
        <div>
          <div className="author-name">{name}</div>
          <div className="author-role">{role} at {company}</div>
        </div>
      </div>
    </div>
  </div>
);

const TestimonialsSection = ({ testimonials }) => {
  return (
    <section id="testimonials" className="testimonials-section py-5">
      <div className="container">
        <div className="text-center mb-5">
          <h2 className="display-5 fw-bold mb-3">
            Success <span className="text-primary">Stories</span>
          </h2>
          <p className="lead text-muted">
            See what our users are saying about their results
          </p>
        </div>
        <div className="row">
          {testimonials.map((testimonial) => (
            <TestimonialCard
              key={testimonial.id}
              name={testimonial.name}
              role={testimonial.role}
              company={testimonial.company}
              rating={testimonial.rating}
              text={testimonial.text}
              avatar={testimonial.avatar}
            />
          ))}
        </div>
      </div>
    </section>
  );
};

export default TestimonialsSection;
