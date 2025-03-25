'use client';

import Link from 'next/link';
import Image from 'next/image';

export default function About() {
  const teamMembers = [
    {
      name: 'Sarah Chen',
      role: 'CEO & Co-founder',
      image: '/images/team/sarah-chen.jpg',
      bio: 'Former Head of AI at Google Cloud, with 15+ years of experience in enterprise software.'
    },
    {
      name: 'Michael Rodriguez',
      role: 'CTO & Co-founder',
      image: '/images/team/michael-rodriguez.jpg',
      bio: 'Previously led machine learning teams at Microsoft and Oracle.'
    },
    {
      name: 'Emily Johnson',
      role: 'VP of Product',
      image: '/images/team/emily-johnson.jpg',
      bio: 'Product leader with experience at Dropbox and Adobe.'
    }
  ];

  const values = [
    {
      title: 'Innovation First',
      description: 'We push the boundaries of what's possible with AI technology.',
      icon: '💡'
    },
    {
      title: 'Customer Success',
      description: 'Our customers' success is our success. We're committed to delivering exceptional value.',
      icon: '🎯'
    },
    {
      title: 'Ethical AI',
      description: 'We develop AI responsibly, ensuring transparency and fairness in our solutions.',
      icon: '⚖️'
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-primary text-white py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-4xl lg:text-5xl font-bold mb-6">
              Our Mission
            </h1>
            <p className="text-xl mb-8">
              We're on a mission to transform knowledge work by automating document-heavy processes and empowering people to focus on higher-value activities.
            </p>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Our Values</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {values.map((value) => (
              <div key={value.title} className="bg-white p-6 rounded-lg shadow-lg text-center">
                <div className="text-4xl mb-4">{value.icon}</div>
                <h3 className="text-xl font-bold mb-2">{value.title}</h3>
                <p className="text-gray-600">{value.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="bg-gray-50 py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Our Leadership Team</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {teamMembers.map((member) => (
              <div key={member.name} className="bg-white rounded-lg shadow-lg overflow-hidden">
                <div className="relative h-64">
                  <Image
                    src={member.image}
                    alt={member.name}
                    fill
                    className="object-cover"
                  />
                </div>
                <div className="p-6">
                  <h3 className="text-xl font-bold mb-2">{member.name}</h3>
                  <p className="text-primary font-medium mb-4">{member.role}</p>
                  <p className="text-gray-600">{member.bio}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-6">Join Our Team</h2>
          <p className="text-xl text-gray-600 mb-8">
            We're always looking for talented individuals who share our vision and values.
          </p>
          <div className="flex justify-center gap-4">
            <Link
              href="/company/careers"
              className="bg-primary text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-dark transition-colors"
            >
              View Open Positions
            </Link>
            <Link
              href="/company/contact"
              className="border-2 border-primary text-primary px-6 py-3 rounded-lg font-semibold hover:bg-primary hover:text-white transition-colors"
            >
              Contact Us
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
} 