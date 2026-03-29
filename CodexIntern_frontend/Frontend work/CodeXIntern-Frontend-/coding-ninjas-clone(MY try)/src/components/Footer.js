import React from 'react';

const Footer = () => {
  const footerSections = [
    {
      title: 'Courses',
      links: ['Full Stack Web Dev', 'Data Science', 'Android Development', 'Competitive Programming', 'Machine Learning']
    },
    {
      title: 'Company',
      links: ['About Us', 'Careers', 'Contact Us', 'Privacy Policy', 'Terms & Conditions']
    },
    {
      title: 'Resources',
      links: ['Blog', 'Events', 'Campus Ninjas', 'Placements', 'Scholarships']
    },
    {
      title: 'Support',
      links: ['Help Center', 'Discussion Forum', 'Doubt Support', 'System Requirements', 'Download App']
    }
  ];

  return (
    <footer className="bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-8">
          {/* Company Info */}
          <div className="lg:col-span-2">
            <div className="flex items-center space-x-2 mb-6">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">CN</span>
              </div>
              <span className="text-xl font-bold">Coding Ninjas</span>
            </div>
            <p className="text-gray-400 mb-6">
              India's best platform to learn coding and get placed in dream companies.
            </p>
            <div className="flex space-x-4">
              {['📘', '🐦', '📷', '💼', '🎬'].map((icon, index) => (
                <button key={index} className="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-blue-500 transition-colors">
                  {icon}
                </button>
              ))}
            </div>
          </div>

          {/* Footer Links */}
          {footerSections.map((section, index) => (
            <div key={index}>
              <h3 className="font-bold text-lg mb-4">{section.title}</h3>
              <ul className="space-y-2">
                {section.links.map((link, linkIndex) => (
                  <li key={linkIndex}>
                    <a href="#" className="text-gray-400 hover:text-white transition-colors">
                      {link}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="border-t border-gray-800 mt-12 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-400 text-center md:text-left">
              © 2024 Coding Ninjas. All rights reserved.
            </p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              {['Privacy Policy', 'Terms of Service', 'Cookie Policy'].map((item, index) => (
                <a key={index} href="#" className="text-gray-400 hover:text-white transition-colors">
                  {item}
                </a>
              ))}
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;