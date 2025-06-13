import React from 'react'
import { Handle, Position } from 'reactflow'
import { Users, Star } from 'lucide-react'

interface PaperNodeData {
  title: string
  authors: string[]
  centrality: number
  isSearchResult: boolean
  isSelected: boolean
  onSelect: () => void
}

interface PaperNodeProps {
  data: PaperNodeData
}

export default function PaperNode({ data }: PaperNodeProps) {
  const { title, authors, centrality, isSearchResult, isSelected, onSelect } = data

  const truncatedTitle = title.length > 50 ? title.substring(0, 50) + '...' : title
  const authorText = authors.length > 2 
    ? `${authors[0]} et al.` 
    : authors.join(', ')

  return (
    <div
      onClick={onSelect}
      className={`
        relative p-3 rounded-lg border-2 cursor-pointer transition-all duration-200 min-w-48 max-w-64
        ${isSelected 
          ? 'border-primary-500 bg-primary-50 shadow-lg' 
          : isSearchResult
            ? 'border-primary-300 bg-white shadow-md hover:shadow-lg'
            : 'border-secondary-200 bg-white hover:border-secondary-300 hover:shadow-md'
        }
      `}
    >
      <Handle type="target" position={Position.Top} className="w-2 h-2" />
      
      {/* Centrality indicator */}
      {centrality > 0.01 && (
        <div className="absolute -top-2 -right-2 w-6 h-6 bg-yellow-400 rounded-full flex items-center justify-center">
          <Star className="w-3 h-3 text-yellow-800" />
        </div>
      )}
      
      {/* Search result indicator */}
      {isSearchResult && (
        <div className="absolute -top-1 -left-1 w-3 h-3 bg-primary-500 rounded-full"></div>
      )}
      
      <div className="space-y-2">
        <h3 className="font-medium text-sm text-secondary-900 leading-tight">
          {truncatedTitle}
        </h3>
        
        <div className="flex items-center text-xs text-secondary-600">
          <Users className="w-3 h-3 mr-1" />
          <span className="truncate">{authorText}</span>
        </div>
        
        {centrality > 0.001 && (
          <div className="text-xs text-secondary-500">
            Centrality: {centrality.toFixed(3)}
          </div>
        )}
      </div>
      
      <Handle type="source" position={Position.Bottom} className="w-2 h-2" />
    </div>
  )
}