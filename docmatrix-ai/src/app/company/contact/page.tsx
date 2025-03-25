'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function Contact() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    company: '',
    product: 'ContractAI',
    message: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Here you would typically send the form data to your backend
    console.log('Form submitted:', formData);
    // Reset form
    setFormData({
      name: '',
      email: '',
      company: '',
      product: 'ContractAI',
      message: ''
    });
  };

  return (
    <div className="min-h-screen py-20">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold mb-8">Contact Us</h1>
          <p className="text-xl text-gray-600 mb-12">
            Get in touch with our team to learn more about DocMatrix AI's products and services.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
            <div>
              <h2 className="text-2xl font-bold mb-6">Get in Touch</h2>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                    Name
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  />
                </div>

                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                    Email
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  />
                </div>

                <div>
                  <label htmlFor="company" className="block text-sm font-medium text-gray-700 mb-1">
                    Company
                  </label>
                  <input
                    type="text"
                    id="company"
                    name="company"
                    value={formData.company}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  />
                </div>

                <div>
                  <label htmlFor="product" className="block text-sm font-medium text-gray-700 mb-1">
                    Product Interest
                  </label>
                  <select
                    id="product"
                    name="product"
                    value={formData.product}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  >
                    <option value="ContractAI">ContractAI</option>
                    <option value="ExpenseDocAI">ExpenseDocAI</option>
                    <option value="HR-DocAI">HR-DocAI</option>
                    <option value="SupplyDocAI">SupplyDocAI</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-1">
                    Message
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    value={formData.message}
                    onChange={handleChange}
                    required
                    rows={4}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  ></textarea>
                </div>

                <button
                  type="submit"
                  className="w-full bg-primary text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-dark transition-colors"
                >
                  Send Message
                </button>
              </form>
            </div>

            <div>
              <h2 className="text-2xl font-bold mb-6">Other Ways to Connect</h2>
              <div className="space-y-8">
                <div>
                  <h3 className="text-lg font-semibold mb-2">Sales Inquiries</h3>
                  <p className="text-gray-600 mb-2">
                    Interested in our products? Our sales team is here to help.
                  </p>
                  <a
                    href="mailto:sales@docmatrixai.com"
                    className="text-primary hover:text-primary-dark transition-colors"
                  >
                    sales@docmatrixai.com
                  </a>
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-2">Technical Support</h3>
                  <p className="text-gray-600 mb-2">
                    Need technical assistance? Our support team is available 24/7.
                  </p>
                  <a
                    href="mailto:support@docmatrixai.com"
                    className="text-primary hover:text-primary-dark transition-colors"
                  >
                    support@docmatrixai.com
                  </a>
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-2">Documentation</h3>
                  <p className="text-gray-600 mb-2">
                    Check out our comprehensive documentation and API reference.
                  </p>
                  <Link
                    href="/resources/documentation"
                    className="text-primary hover:text-primary-dark transition-colors"
                  >
                    View Documentation
                  </Link>
                </div>

                <div className="bg-gray-50 p-6 rounded-lg">
                  <h3 className="text-lg font-semibold mb-2">Office Location</h3>
                  <p className="text-gray-600">
                    123 Tech Street<br />
                    Suite 456<br />
                    San Francisco, CA 94105<br />
                    United States
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 