import React from 'react';

const Courses = () => {
  const courses = [
    {
      title: 'Full Stack Web Development',
      description: 'Become a full stack developer with MERN stack',
      duration: '6 months',
      level: 'Beginner to Advanced',
      price: '₹25,000',
      popular: true
    },
    {
      title: 'Data Science & Machine Learning',
      description: 'Master Data Science and ML with Python',
      duration: '8 months',
      level: 'Intermediate',
      price: '₹35,000',
      popular: true
    },
    {
      title: 'Android Development',
      description: 'Build Android apps with Kotlin and Java',
      duration: '5 months',
      level: 'Beginner',
      price: '₹20,000',
      popular: false
    },
    {
      title: 'Competitive Programming',
      description: 'Excel in coding interviews and competitions',
      duration: '4 months',
      level: 'Advanced',
      price: '₹15,000',
      popular: true
    },
    {
      title: 'System Design',
      description: 'Learn to design scalable systems',
      duration: '3 months',
      level: 'Advanced',
      price: '₹18,000',
      popular: false
    },
    {
      title: 'UI/UX Design',
      description: 'Master design thinking and prototyping',
      duration: '4 months',
      level: 'Beginner',
      price: '₹22,000',
      popular: false
    }
  ];

  return (
    <section className="py-20 bg-white">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-800 mb-4">
            Popular Courses
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Choose from our wide range of industry-relevant courses
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {courses.map((course, index) => (
            <div key={index} className="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-all hover-scale">
              {course.popular && (
                <div className="bg-red-500 text-white text-sm font-bold px-4 py-1 text-center">
                  Most Popular
                </div>
              )}
              <div className="p-6">
                <h3 className="text-xl font-bold text-gray-800 mb-3">{course.title}</h3>
                <p className="text-gray-600 mb-4">{course.description}</p>
                
                <div className="space-y-2 mb-6">
                  <div className="flex items-center text-gray-600">
                    <span className="font-medium mr-2">Duration:</span>
                    {course.duration}
                  </div>
                  <div className="flex items-center text-gray-600">
                    <span className="font-medium mr-2">Level:</span>
                    {course.level}
                  </div>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-2xl font-bold text-blue-600">{course.price}</span>
                  <button className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-colors">
                    Enroll Now
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="text-center mt-12">
          <button className="border-2 border-blue-500 text-blue-500 px-8 py-3 rounded-lg font-bold text-lg hover:bg-blue-50 transition-colors">
            View All Courses
          </button>
        </div>
      </div>
    </section>
  );
};

export default Courses;