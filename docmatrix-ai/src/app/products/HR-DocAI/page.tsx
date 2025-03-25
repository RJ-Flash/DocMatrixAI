'use client';

import Link from 'next/link';
import Image from 'next/image';

export default function HRDocAI() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-primary text-white py-20">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h1 className="text-4xl lg:text-5xl font-bold mb-6">
                Transform HR Document Management
              </h1>
              <p className="text-lg mb-8">
                HR-DocAI streamlines HR document management with intelligent compliance monitoring and automated lifecycle management, saving teams 75% of their time.
              </p>
              <div className="flex flex-wrap gap-4">
                <Link
                  href="/company/contact"
                  className="bg-white text-primary px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
                >
                  Request Demo
                </Link>
                <Link
                  href="/resources/documentation"
                  className="border-2 border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white hover:text-primary transition-colors"
                >
                  Learn More
                </Link>
              </div>
            </div>
            <div className="relative h-[400px] rounded-lg overflow-hidden">
              <Image
                src="/images/hr-ai-hero.jpg"
                alt="HR-DocAI Platform Interface"
                fill
                className="object-cover"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Key Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                title: 'Document Lifecycle Management',
                description: 'Automated tracking and management of employee documents throughout their lifecycle.',
                icon: '📋'
              },
              {
                title: 'Compliance Automation',
                description: 'Real-time monitoring and alerts for document compliance requirements.',
                icon: '✓'
              },
              {
                title: 'HRIS Integration',
                description: 'Seamless integration with popular HRIS and employee management systems.',
                icon: '🔄'
              }
            ].map((feature) => (
              <div key={feature.title} className="bg-white p-6 rounded-lg shadow-lg">
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gray-50 py-20">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-6">Ready to Transform Your HR Document Management?</h2>
          <p className="text-lg text-gray-600 mb-8">
            Join leading organizations that have automated their HR document processes with HR-DocAI.
          </p>
          <div className="flex justify-center gap-4">
            <Link
              href="/company/contact"
              className="bg-primary text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-dark transition-colors"
            >
              Schedule a Demo
            </Link>
            <Link
              href="/products"
              className="border-2 border-primary text-primary px-6 py-3 rounded-lg font-semibold hover:bg-primary hover:text-white transition-colors"
            >
              View All Products
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
} 