import React from 'react'
import { TrendingUp, BarChart3, PieChart, Zap } from 'lucide-react'

interface ScoreCardProps {
  label: string
  value: number
  icon: React.ReactNode
  color: string
}

export const ScoreCard: React.FC<ScoreCardProps> = ({
  label,
  value,
  icon,
  color,
}) => {
  return (
    <div className="bg-slate-900 rounded-lg p-4 border border-slate-800">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-muted text-sm font-medium">{label}</p>
          <p className={`text-2xl font-bold mt-1 ${color}`}>{value.toFixed(1)}</p>
        </div>
        <div className={`${color} opacity-20`}>{icon}</div>
      </div>
    </div>
  )
}

interface TrendCardProps {
  trend: any
  onClick?: () => void
}

export const TrendCard: React.FC<TrendCardProps> = (props) => {
  const { trend, onClick } = props
  return (
    <div
      onClick={onClick}
      className="bg-slate-900 rounded-lg p-6 border border-slate-800 hover:border-primary transition cursor-pointer"
    >
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-foreground">{trend.niche}</h3>
          <p className="text-muted text-sm mt-1">{trend.category}</p>
        </div>
        <div className={`text-2xl font-bold ${
          trend.overall_score > 70
            ? 'text-green-500'
            : trend.overall_score > 40
            ? 'text-yellow-500'
            : 'text-red-500'
        }`}>
          {trend.overall_score.toFixed(0)}
        </div>
      </div>

      <div className="grid grid-cols-4 gap-2 mb-4">
        <div className="text-center">
          <p className="text-muted text-xs">Demand</p>
          <p className="text-sm font-semibold text-foreground">{trend.demand_score.toFixed(0)}</p>
        </div>
        <div className="text-center">
          <p className="text-muted text-xs">Growth</p>
          <p className="text-sm font-semibold text-foreground">{trend.growth_score.toFixed(0)}</p>
        </div>
        <div className="text-center">
          <p className="text-muted text-xs">Competition</p>
          <p className="text-sm font-semibold text-foreground">{trend.competition_score.toFixed(0)}</p>
        </div>
        <div className="text-center">
          <p className="text-muted text-xs">Profit</p>
          <p className="text-sm font-semibold text-foreground">{trend.profitability_score.toFixed(0)}</p>
        </div>
      </div>

      <div className="flex items-center justify-between text-sm">
        <span className="text-muted">
          Avg: ${trend.avg_price.toFixed(2)} | Reviews: {trend.total_reviews}
        </span>
        <TrendingUp size={16} className="text-primary" />
      </div>
    </div>
  )
}

export const LoadingCard: React.FC = () => {
  return (
    <div className="bg-slate-900 rounded-lg p-6 border border-slate-800 animate-pulse">
      <div className="h-8 bg-slate-800 rounded mb-4"></div>
      <div className="h-4 bg-slate-800 rounded mb-2"></div>
      <div className="h-4 bg-slate-800 rounded mb-4"></div>
      <div className="grid grid-cols-4 gap-2">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="h-12 bg-slate-800 rounded"></div>
        ))}
      </div>
    </div>
  )
}

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline'
  size?: 'sm' | 'md' | 'lg'
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  className = '',
  ...props
}) => {
  const baseClasses = 'font-semibold rounded-lg transition'
  const variants = {
    primary: 'bg-primary text-white hover:bg-blue-600',
    secondary: 'bg-secondary text-white hover:bg-purple-600',
    outline: 'border border-primary text-primary hover:bg-primary hover:text-white',
  }
  const sizes = {
    sm: 'px-3 py-1 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  }

  return (
    <button
      className={`${baseClasses} ${variants[variant]} ${sizes[size]} ${className}`}
      {...props}
    />
  )
}
