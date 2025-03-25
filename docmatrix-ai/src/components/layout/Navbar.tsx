'use client';

import Link from 'next/link';
import { useState } from 'react';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  const handleToggle = () => setIsOpen(!isOpen);

  return (
    <nav className="bg-white py-3 shadow-sm fixed top-0 w-full z-50">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center">
          <Link 
            href="/" 
            className="text-xl font-bold"
            aria-label="DocMatrix AI Home"
          >
            DocMatrix AI
          </Link>
          
          <button
            className="lg:hidden"
            onClick={handleToggle}
            aria-label="Toggle navigation menu"
            aria-expanded={isOpen}
          >
            <span className="block w-6 h-0.5 bg-gray-600 mb-1"></span>
            <span className="block w-6 h-0.5 bg-gray-600 mb-1"></span>
            <span className="block w-6 h-0.5 bg-gray-600"></span>
          </button>

          <div className={`lg:flex items-center ${isOpen ? 'block absolute top-full left-0 right-0 bg-white shadow-md' : 'hidden'} lg:static lg:shadow-none`}>
            <ul className="lg:flex space-y-2 lg:space-y-0 lg:space-x-8 p-4 lg:p-0">
              <li>
                <Link 
                  href="/products/ContractAI"
                  className="block text-gray-700 hover:text-primary transition-colors"
                  aria-label="Products"
                >
                  Products
                </Link>
              </li>
              <li>
                <Link 
                  href="/resources/documentation"
                  className="block text-gray-700 hover:text-primary transition-colors"
                  aria-label="Technology"
                >
                  Technology
                </Link>
              </li>
              <li>
                <Link 
                  href="/company/about"
                  className="block text-gray-700 hover:text-primary transition-colors"
                  aria-label="About"
                >
                  About
                </Link>
              </li>
            </ul>
            <div className="flex flex-col lg:flex-row gap-2 p-4 lg:p-0 lg:ml-8">
              <Link 
                href="/login"
                className="px-4 py-2 text-gray-600 border border-gray-300 rounded hover:bg-gray-50 transition-colors text-center"
                aria-label="Log in to your account"
              >
                Log In
              </Link>
              <Link 
                href="/company/contact"
                className="px-4 py-2 bg-primary text-white rounded hover:bg-primary-dark transition-colors text-center"
                aria-label="Request a product demo"
              >
                Request Demo
              </Link>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar; 