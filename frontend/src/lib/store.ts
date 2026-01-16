import { create } from 'zustand'

interface Trend {
  id: number
  niche: string
  category: string
  overall_score: number
  demand_score: number
  competition_score: number
  growth_score: number
  profitability_score: number
  avg_price: number
  total_reviews: number
  target_audience: any
  created_at: string
}

interface TrendStore {
  trends: Trend[]
  loading: boolean
  error: string | null
  setTrends: (trends: Trend[]) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  fetchTrends: () => Promise<void>
}

export const useTrendStore = create<TrendStore>((set) => ({
  trends: [],
  loading: false,
  error: null,
  setTrends: (trends) => set({ trends }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  fetchTrends: async () => {
    set({ loading: true, error: null })
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/trends?limit=50`
      )
      if (!response.ok) throw new Error('Failed to fetch trends')
      const data = await response.json()
      set({ trends: data })
    } catch (error) {
      set({ error: error instanceof Error ? error.message : 'Unknown error' })
    } finally {
      set({ loading: false })
    }
  },
}))
