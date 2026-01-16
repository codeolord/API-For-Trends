import React from 'react'
import Link from 'next/link'
import { Menu, Sparkles, TrendingUp, LayoutGrid } from 'lucide-react'

export const Header: React.FC = () => {
  return (
    <header className="bg-slate-950 border-b border-slate-800 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <Sparkles className="text-primary" size={28} />
            <span className="text-xl font-bold text-foreground">POD Trends</span>
          </Link>

          <nav className="hidden md:flex items-center gap-8">
            <Link
              href="/trends"
              className="text-muted hover:text-foreground transition"
            >
              <span className="flex items-center gap-2">
                <TrendingUp size={18} />
                Trends
              </span>
            </Link>
            <Link
              href="/designs"
              className="text-muted hover:text-foreground transition"
            >
              <span className="flex items-center gap-2">
                <LayoutGrid size={18} />
                Designs
              </span>
            </Link>
            <Link
              href="/products"
              className="text-muted hover:text-foreground transition"
            >
              Products
            </Link>
          </nav>

          <button className="md:hidden p-2 text-muted hover:text-foreground">
            <Menu size={24} />
          </button>
        </div>
      </div>
    </header>
  )
}

export const Sidebar: React.FC = () => {
  return (
    <aside className="hidden lg:block w-64 bg-slate-950 border-r border-slate-800 h-screen sticky top-16">
      <div className="p-6">
        <div className="mb-8">
          <h3 className="text-muted text-xs font-semibold uppercase tracking-wider mb-4">
            Filters
          </h3>
          <div className="space-y-3">
            <input
              type="text"
              placeholder="Search trends..."
              className="w-full px-3 py-2 bg-slate-900 border border-slate-800 rounded text-foreground text-sm placeholder-muted focus:outline-none focus:border-primary"
            />
            <select className="w-full px-3 py-2 bg-slate-900 border border-slate-800 rounded text-foreground text-sm focus:outline-none focus:border-primary">
              <option>All Categories</option>
              <option>Apparel</option>
              <option>Home Decor</option>
              <option>Accessories</option>
            </select>
            <select className="w-full px-3 py-2 bg-slate-900 border border-slate-800 rounded text-foreground text-sm focus:outline-none focus:border-primary">
              <option>Score: All</option>
              <option>80+</option>
              <option>60-79</option>
              <option>40-59</option>
            </select>
          </div>
        </div>

        <div>
          <h3 className="text-muted text-xs font-semibold uppercase tracking-wider mb-4">
            Quick Stats
          </h3>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-muted">Total Trends</span>
              <span className="text-foreground font-semibold">1,245</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted">This Week</span>
              <span className="text-foreground font-semibold">+47</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted">Avg Score</span>
              <span className="text-foreground font-semibold">68.2</span>
            </div>
          </div>
        </div>
      </div>
    </aside>
  )
}
