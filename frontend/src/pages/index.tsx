import React from 'react'
import Head from 'next/head'
import DashboardLayout from '@/components/DashboardLayout'
import { Button } from '@/components/Cards'
import { Sparkles, Zap, BarChart3, ArrowRight } from 'lucide-react'
import Link from 'next/link'

export default function Home() {
  return (
    <>
      <Head>
        <title>POD Trends - AI-Powered Design & Trend Analysis</title>
      </Head>

      <DashboardLayout>
        <div className="space-y-12">
          {/* Hero Section */}
          <div className="text-center py-12">
            <div className="inline-flex items-center gap-2 bg-slate-900 border border-primary/20 rounded-full px-4 py-2 mb-6">
              <Sparkles size={16} className="text-primary" />
              <span className="text-sm text-primary">AI-Powered Trend Detection</span>
            </div>
            <h1 className="text-5xl font-bold text-foreground mb-4">
              Turn Market Trends Into <span className="text-primary">Profitable Designs</span>
            </h1>
            <p className="text-xl text-muted max-w-2xl mx-auto mb-8">
              Automatically research trends, analyze demand, generate original designs, and
              publish to print-on-demand platforms—all powered by AI.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/trends">
                <Button variant="primary" size="lg">
                  View Trends <ArrowRight size={18} className="ml-2" />
                </Button>
              </Link>
              <Button variant="outline" size="lg">
                Watch Demo
              </Button>
            </div>
          </div>

          {/* Features Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 py-12">
            {[
              {
                icon: <BarChart3 className="text-blue-500" size={32} />,
                title: 'Trend Analysis',
                description:
                  'AI scores trends by demand, competition, growth, and profitability',
              },
              {
                icon: <Sparkles className="text-purple-500" size={32} />,
                title: 'AI Design Generation',
                description:
                  'Generate original, print-ready designs from top trends automatically',
              },
              {
                icon: <Zap className="text-yellow-500" size={32} />,
                title: 'Automated Publishing',
                description:
                  'Push designs to Printful and Shopify with one click',
              },
            ].map((feature, i) => (
              <div
                key={i}
                className="bg-slate-900 rounded-lg border border-slate-800 p-8 hover:border-primary transition"
              >
                <div className="mb-4">{feature.icon}</div>
                <h3 className="text-lg font-semibold text-foreground mb-2">
                  {feature.title}
                </h3>
                <p className="text-muted">{feature.description}</p>
              </div>
            ))}
          </div>

          {/* Quick Stats */}
          <div className="bg-slate-900 border border-slate-800 rounded-lg p-12">
            <h2 className="text-2xl font-bold text-foreground mb-8 text-center">
              Platform Overview
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              {[
                { label: 'Products Analyzed', value: '10,000+' },
                { label: 'Trends Detected', value: '2,500+' },
                { label: 'AI Designs Generated', value: '5,000+' },
                { label: 'Success Rate', value: '87%' },
              ].map((stat, i) => (
                <div key={i} className="text-center">
                  <p className="text-3xl font-bold text-primary mb-2">{stat.value}</p>
                  <p className="text-muted text-sm">{stat.label}</p>
                </div>
              ))}
            </div>
          </div>

          {/* CTA Section */}
          <div className="bg-gradient-to-r from-primary/10 to-secondary/10 border border-primary/20 rounded-lg p-12 text-center">
            <h2 className="text-2xl font-bold text-foreground mb-4">
              Ready to Find Your Next Winning Design?
            </h2>
            <p className="text-muted mb-8 max-w-2xl mx-auto">
              Start analyzing trends, generating designs, and publishing to POD platforms
              automatically.
            </p>
            <Link href="/trends">
              <Button variant="primary" size="lg">
                Explore Trends Now
              </Button>
            </Link>
          </div>
        </div>
      </DashboardLayout>
    </>
  )
}
