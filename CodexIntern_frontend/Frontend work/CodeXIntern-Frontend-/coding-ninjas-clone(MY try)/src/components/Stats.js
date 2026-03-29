import React from 'react';

const Stats = () => {
  const stats = [
    {
      number: '1000+',
      label: 'Hiring Partners',
      icon: '🏢'
    },
    {
      number: '50K+',
      label: 'Students Placed',
      icon: '🎓'
    },
    {
      number: '300+',
      label: 'Expert Mentors',
      icon: '👨‍🏫'
    },
    {
      number: '4.8/5',
      label: 'Student Rating',
      icon: '⭐'
    }
  ];

  return (
    <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-700 text-white">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Our Impact in Numbers
          </h2>
          <p className="text-xl text-blue-100 max-w-2xl mx-auto">
            Trusted by thousands of students and hundreds of companies
          </p>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
          {stats.map((stat, index) => (
            <div key={index} className="text-center">
              <div className="text-4xl mb-4">{stat.icon}</div>
              <div className="text-4xl md:text-5xl font-bold text-yellow-300 mb-2">
                {stat.number}
              </div>
              <div className="text-xl text-blue-100 font-medium">
                {stat.label}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Stats;