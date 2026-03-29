import React from 'react';

const Hero = () => {
  return (
    <section className="gradient-bg text-white py-20">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
            Master Coding Skills with 
            <span className="text-yellow-300"> Coding Ninjas</span>
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-blue-100">
            India's best coding platform to learn, practice and get ready for your dream tech job
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-white text-blue-600 px-8 py-4 rounded-lg font-bold text-lg hover:bg-blue-50 transition-colors hover-scale">
              Explore Courses
            </button>
            <button className="border-2 border-white text-white px-8 py-4 rounded-lg font-bold text-lg hover:bg-white hover:text-blue-600 transition-colors hover-scale">
              Free Trial
            </button>
          </div>
          <div className="mt-12 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            {[
              { number: '50,000+', label: 'Students Placed' },
              { number: '300+', label: 'Expert Mentors' },
              { number: '1000+', label: 'Companies' },
              { number: '4.8/5', label: 'Student Rating' }
            ].map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-3xl font-bold text-yellow-300">{stat.number}</div>
                <div className="text-blue-100 mt-2">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;