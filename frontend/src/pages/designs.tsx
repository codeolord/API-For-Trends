import React, { useEffect, useState } from 'react'
import Head from 'next/head'
import DashboardLayout from '@/components/DashboardLayout'
import { Button, LoadingCard } from '@/components/Cards'
import { designsApi } from '@/lib/api'
import { Plus, Download } from 'lucide-react'

interface Design {
  id: number
  title: string
  description: string
  trend_id: number
  image_url: string
  status: string
  created_at: string
}

export default function DesignsPage() {
  const [designs, setDesigns] = useState<Design[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchDesigns = async () => {
      try {
        const response = await designsApi.list(0, 50)
        setDesigns(response.data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch designs')
      } finally {
        setLoading(false)
      }
    }

    fetchDesigns()
  }, [])

  return (
    <>
      <Head>
        <title>Designs - POD Platform</title>
      </Head>

      <DashboardLayout>
        <div className="space-y-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-foreground">AI Designs</h1>
              <p className="text-muted mt-2">
                Auto-generated designs ready for print-on-demand
              </p>
            </div>
            <Button variant="primary">
              <Plus size={18} className="mr-2" />
              Generate Design
            </Button>
          </div>

          {error && (
            <div className="bg-red-900/20 border border-red-800 rounded-lg p-4 text-red-200">
              Error: {error}
            </div>
          )}

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <LoadingCard key={i} />
              ))}
            </div>
          ) : designs.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {designs.map((design) => (
                <div
                  key={design.id}
                  className="bg-slate-900 rounded-lg border border-slate-800 overflow-hidden hover:border-primary transition"
                >
                  {design.image_url && (
                    <div className="w-full h-48 bg-slate-800 flex items-center justify-center">
                      <img
                        src={design.image_url}
                        alt={design.title}
                        className="w-full h-full object-cover"
                        onError={(e) => {
                          e.currentTarget.src =
                            'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"%3E%3Crect fill="%23374151" width="100" height="100"/%3E%3C/svg%3E'
                        }}
                      />
                    </div>
                  )}
                  <div className="p-4">
                    <h3 className="font-semibold text-foreground">{design.title}</h3>
                    <p className="text-muted text-sm mt-1">{design.description}</p>
                    <div className="mt-4 flex items-center justify-between">
                      <span
                        className={`text-xs px-2 py-1 rounded ${
                          design.status === 'draft'
                            ? 'bg-yellow-900/30 text-yellow-200'
                            : 'bg-green-900/30 text-green-200'
                        }`}
                      >
                        {design.status}
                      </span>
                      <Button variant="outline" size="sm">
                        <Download size={16} />
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="bg-slate-900 rounded-lg border border-slate-800 p-12 text-center">
              <p className="text-muted">No designs yet</p>
              <Button variant="primary" className="mt-4">
                Generate First Design
              </Button>
            </div>
          )}
        </div>
      </DashboardLayout>
    </>
  )
}
