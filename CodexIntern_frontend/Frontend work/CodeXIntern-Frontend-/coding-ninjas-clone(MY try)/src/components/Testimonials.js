import React from 'react';

const Testimonials = () => {
  const testimonials = [
    {
      name: 'Rahul Sharma',
      role: 'Placed at Amazon',
      image: '👨',
      review: 'Coding Ninjas changed my life! The mentors are amazing and the curriculum is industry-relevant.',
      rating: 5
    },
    {
      name: 'Priya Singh',
      role: 'Placed at Microsoft',
      image: '👩',
      review: 'The doubt support is exceptional. Got placed with 3 offers within 2 months of course completion.',
      rating: 5
    },
    {
      name: 'Amit Kumar',
      role: 'Placed at Google',
      image: '👨',
      review: 'Best investment in my career. The projects helped me build a strong portfolio.',
      rating: 5
    }
  ];

  const renderStars = (rating) => {
    return '⭐'.repeat(rating);
  };

  return (
    <section className="py-20 bg-gray-50">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-800 mb-4">
            What Our Students Say
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Hear from our successful alumni who transformed their careers with Coding Ninjas
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <div key={index} className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow hover-scale">
              <div className="flex items-center mb-6">
                <div className="text-4xl mr-4">{testimonial.image}</div>
                <div>
                  <h4 className="font-bold text-gray-800 text-lg">{testimonial.name}</h4>
                  <p className="text-blue-500">{testimonial.role}</p>
                </div>
              </div>
              
              <div className="text-yellow-400 text-lg mb-4">
                {renderStars(testimonial.rating)}
              </div>
              
              <p className="text-gray-600 italic">
                "{testimonial.review}"
              </p>
            </div>
          ))}
        </div>

        <div className="text-center mt-12">
          <button className="bg-blue-500 text-white px-8 py-3 rounded-lg font-bold text-lg hover:bg-blue-600 transition-colors">
            Read More Success Stories
          </button>
        </div>
      </div>
    </section>
  );
};

export default Testimonials;