import React, { useEffect } from 'react'
import Head from 'next/head'
import DashboardLayout from '@/components/DashboardLayout'
import { TrendCard, LoadingCard, Button, ScoreCard } from '@/components/Cards'
import { useTrendStore } from '@/lib/store'
import { TrendingUp, BarChart3, Zap, Target } from 'lucide-react'

export default function TrendsPage() {
  const { trends, loading, error, fetchTrends } = useTrendStore()

  useEffect(() => {
    fetchTrends()
  }, [fetchTrends])

  return (
    <>
      <Head>
        <title>Trends - POD Platform</title>
      </Head>

      <DashboardLayout>
        <div className="space-y-8">
          {/* Header */}
          <div>
            <h1 className="text-3xl font-bold text-foreground">Trend Analysis</h1>
            <p className="text-muted mt-2">
              AI-powered trend detection across all major marketplaces
            </p>
          </div>

          {/* Top Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <ScoreCard
              label="Total Trends"
              value={trends.length}
              icon={<TrendingUp size={24} />}
              color="text-blue-500"
            />
            <ScoreCard
              label="Avg Score"
              value={
                trends.length > 0
                  ? trends.reduce((sum, t) => sum + t.overall_score, 0) /
                    trends.length
                  : 0
              }
              icon={<BarChart3 size={24} />}
              color="text-purple-500"
            />
            <ScoreCard
              label="High Demand"
              value={trends.filter((t) => t.demand_score > 70).length}
              icon={<Zap size={24} />}
              color="text-yellow-500"
            />
            <ScoreCard
              label="Profitable"
              value={trends.filter((t) => t.profitability_score > 70).length}
              icon={<Target size={24} />}
              color="text-green-500"
            />
          </div>

          {/* Action Button */}
          <div className="flex gap-3">
            <Button variant="primary">Refresh Trends</Button>
            <Button variant="outline">Export Report</Button>
          </div>

          {/* Trends Grid */}
          <div>
            <h2 className="text-xl font-semibold text-foreground mb-4">
              Top Trends
            </h2>
            {error && (
              <div className="bg-red-900/20 border border-red-800 rounded-lg p-4 text-red-200 mb-4">
                Error: {error}
              </div>
            )}
            {loading ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {[...Array(6)].map((_, i) => (
                  <LoadingCard key={i} />
                ))}
              </div>
            ) : trends.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {trends.map((trend) => (
                  <TrendCard key={trend.id} trend={trend} />
                ))}
              </div>
            ) : (
              <div className="bg-slate-900 rounded-lg border border-slate-800 p-12 text-center">
                <p className="text-muted">No trends available</p>
                <Button variant="primary" className="mt-4">
                  Start Analysis
                </Button>
              </div>
            )}
          </div>
        </div>
      </DashboardLayout>
    </>
  )
}
