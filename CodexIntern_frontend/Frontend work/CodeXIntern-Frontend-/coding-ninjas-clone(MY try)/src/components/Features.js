import React from 'react';

const Features = () => {
  const features = [
    {
      icon: '💻',
      title: 'Learn from Experts',
      description: 'Learn from industry experts having 10+ years of experience'
    },
    {
      icon: '📚',
      title: 'Structured Curriculum',
      description: 'Well-structured curriculum designed by industry experts'
    },
    {
      icon: '🤝',
      title: '1:1 Mentorship',
      description: 'Get personal guidance and doubt resolution from mentors'
    },
    {
      icon: '🏆',
      title: 'Placement Support',
      description: 'Get placement assistance with 1000+ hiring partners'
    },
    {
      icon: '⚡',
      title: 'Fast-track Courses',
      description: 'Accelerated learning paths for quick career growth'
    },
    {
      icon: '📱',
      title: 'Mobile Learning',
      description: 'Learn on the go with our mobile app and platform'
    }
  ];

  return (
    <section className="py-20 bg-gray-50">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-800 mb-4">
            Why Choose Coding Ninjas?
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            We provide the best learning experience with industry-relevant curriculum and expert mentorship
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow hover-scale">
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-bold text-gray-800 mb-3">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;