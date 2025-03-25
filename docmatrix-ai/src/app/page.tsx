'use client';

import Link from 'next/link';
import Image from 'next/image';
import ProductCard from '@/components/shared/ProductCard';

export default function Home() {
  const products = [
    {
      title: 'ContractAI',
      description: 'Automate contract review and analysis with 80% time savings.',
      category: 'Legal Tech',
      timeSaving: '80%',
      href: '/products/ContractAI',
      icon: '📄'
    },
    {
      title: 'ExpenseDocAI',
      description: 'Transform expense processing with intelligent automation.',
      category: 'Finance',
      timeSaving: '90%',
      href: '/products/ExpenseDocAI',
      icon: '🧾'
    },
    {
      title: 'HR-DocAI',
      description: 'Streamline HR document management and compliance.',
      category: 'Human Resources',
      timeSaving: '75%',
      href: '/products/HR-DocAI',
      icon: '👥'
    },
    {
      title: 'SupplyDocAI',
      description: 'Accelerate supply chain documentation processing.',
      category: 'Supply Chain',
      timeSaving: '85%',
      href: '/products/SupplyDocAI',
      icon: '📦'
    }
  ];

  const stats = [
    { number: '85%', label: 'Time Saved' },
    { number: '99%', label: 'Accuracy' },
    { number: '500+', label: 'Enterprise Clients' },
    { number: '24/7', label: 'Support' }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-primary to-primary-dark text-white py-20 lg:py-32">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h1 className="text-4xl lg:text-6xl font-bold mb-6 leading-tight">
                Transform Document Processing with AI Intelligence
              </h1>
              <p className="text-xl mb-8 text-gray-100">
                DocMatrix AI helps enterprises automate document-heavy processes, reducing manual work by up to 85% while improving accuracy and compliance.
              </p>
              <div className="flex flex-wrap gap-4">
                <Link
                  href="/login"
                  className="bg-white text-primary px-8 py-4 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
                >
                  Get Started
                </Link>
                <Link
                  href="/company/contact"
                  className="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold hover:bg-white hover:text-primary transition-colors"
                >
                  Contact Sales
                </Link>
              </div>
            </div>
            <div className="relative h-[500px] rounded-lg overflow-hidden shadow-2xl">
              <div className="absolute inset-0 bg-gradient-to-br from-primary to-primary-dark opacity-20"></div>
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-white text-center">
                  <h3 className="text-2xl font-bold mb-4">Demo Platform</h3>
                  <p className="text-lg">Coming Soon</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat) => (
              <div key={stat.label} className="text-center">
                <div className="text-4xl lg:text-5xl font-bold text-primary mb-2">
                  {stat.number}
                </div>
                <div className="text-gray-600">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Products Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold mb-4">
              Our AI-Powered Solutions
            </h2>
            <p className="text-xl text-gray-600">
              Choose the right solution for your business needs
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {products.map((product) => (
              <ProductCard key={product.title} {...product} />
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl lg:text-4xl font-bold text-center mb-12">
            Why Choose DocMatrix AI?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                title: 'AI-Powered Processing',
                description: 'Advanced machine learning models trained on millions of documents for accurate extraction.',
                icon: '🤖'
              },
              {
                title: 'Enterprise Security',
                description: 'SOC 2 Type II certified with end-to-end encryption and compliance features.',
                icon: '🔒'
              },
              {
                title: 'Easy Integration',
                description: 'Seamless integration with your existing systems and workflows.',
                icon: '🔄'
              }
            ].map((feature) => (
              <div key={feature.title} className="bg-white p-8 rounded-lg shadow-lg">
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-primary text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl lg:text-4xl font-bold mb-6">
            Ready to Transform Your Document Workflows?
          </h2>
          <p className="text-xl mb-8">
            Join hundreds of enterprises that trust DocMatrix AI for their document processing needs.
          </p>
          <div className="flex justify-center gap-4">
            <Link
              href="/login"
              className="bg-white text-primary px-8 py-4 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
            >
              Get Started
            </Link>
            <Link
              href="/company/contact"
              className="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold hover:bg-white hover:text-primary transition-colors"
            >
              Contact Sales
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
} 