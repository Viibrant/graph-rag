import { ExternalLink, Network, Star, Users } from 'lucide-react'
import { SearchResult } from '../types'

interface ListViewProps {
  results: SearchResult[]
  selectedPaper: string | null
  onPaperSelect: (paperId: string) => void
}

export default function ListView({ results, selectedPaper, onPaperSelect }: ListViewProps) {
  if (results.length === 0) {
    return (
      <div className="p-8 text-center text-secondary-500">
        <div className="w-16 h-16 bg-secondary-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <Network className="w-8 h-8" />
        </div>
        <p>No papers found</p>
        <p className="text-sm mt-1">Try a different search query</p>
      </div>
    )
  }

  return (
    <div className="divide-y divide-secondary-100">
      {results.map((paper) => (
        <div
          key={paper.id}
          onClick={() => onPaperSelect(paper.id)}
          className={`
            p-6 cursor-pointer transition-all duration-200 hover:bg-secondary-50
            ${selectedPaper === paper.id ? 'bg-primary-50 border-l-4 border-primary-500' : ''}
          `}
        >
          <div className="flex items-start justify-between">
            <div className="flex-1 min-w-0">
              <div className="flex items-center space-x-2 mb-2">
                <h3 className="text-lg font-semibold text-secondary-900 leading-tight">
                  {paper.title}
                </h3>
                {paper.score && paper.score > 0.5 && (
                  <Star className="w-4 h-4 text-yellow-500 flex-shrink-0" />
                )}
              </div>

              <div className="flex items-center text-secondary-600 mb-3">
                <Users className="w-4 h-4 mr-2 flex-shrink-0" />
                <span className="text-sm">
                  {paper.authors.length > 3
                    ? `${paper.authors.slice(0, 3).join(', ')} +${paper.authors.length - 3} more`
                    : paper.authors.join(', ')
                  }
                </span>
              </div>

              <div className="flex items-center space-x-4 text-sm text-secondary-500">
                {paper.score && (
                  <span className="flex items-center">
                    <span className="font-medium">Score:</span>
                    <span className="ml-1">{paper.score.toFixed(3)}</span>
                  </span>
                )}

                {paper.related_ids && paper.related_ids.length > 0 && (
                  <span className="flex items-center">
                    <Network className="w-3 h-3 mr-1" />
                    <span>{paper.related_ids.length} related</span>
                  </span>
                )}
              </div>
            </div>

            <div className="ml-4 flex-shrink-0">
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  window.open(`https://arxiv.org/abs/${paper.id}`, '_blank')
                }}
                className="p-2 text-secondary-400 hover:text-primary-600 transition-colors"
                title="View on arXiv"
              >
                <ExternalLink className="w-4 h-4" />
              </button>
            </div>
          </div>

          {paper.related_ids && paper.related_ids.length > 0 && selectedPaper === paper.id && (
            <div className="mt-4 pt-4 border-t border-secondary-200">
              <h4 className="text-sm font-medium text-secondary-700 mb-2">Related Papers:</h4>
              <div className="flex flex-wrap gap-2">
                {paper.related_ids.slice(0, 5).map((relatedId) => (
                  <span
                    key={relatedId}
                    className="px-2 py-1 bg-secondary-100 text-secondary-700 text-xs rounded-md"
                  >
                    {relatedId}
                  </span>
                ))}
                {paper.related_ids.length > 5 && (
                  <span className="px-2 py-1 bg-secondary-100 text-secondary-500 text-xs rounded-md">
                    +{paper.related_ids.length - 5} more
                  </span>
                )}
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  )
}