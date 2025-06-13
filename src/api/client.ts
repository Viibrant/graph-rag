import { SearchResult, GraphData, PaperStatus } from '../types'

const API_BASE = '/api'

export async function searchPapers(query: string, topK: number = 10): Promise<SearchResult[]> {
  const response = await fetch(`${API_BASE}/search?query=${encodeURIComponent(query)}&top_k=${topK}`)
  if (!response.ok) {
    throw new Error('Search failed')
  }
  return response.json()
}

export async function getGraphData(): Promise<GraphData> {
  const response = await fetch(`${API_BASE}/graph`)
  if (!response.ok) {
    throw new Error('Failed to fetch graph data')
  }
  return response.json()
}

export async function getPaperStatus(paperIds: string[]): Promise<PaperStatus[]> {
  const params = paperIds.map(id => `paper_id=${encodeURIComponent(id)}`).join('&')
  const response = await fetch(`${API_BASE}/status?${params}`)
  if (!response.ok) {
    throw new Error('Failed to fetch paper status')
  }
  return response.json()
}

export async function runPipeline(query: string) {
  const response = await fetch(`${API_BASE}/pipeline?query=${encodeURIComponent(query)}`)
  if (!response.ok) {
    throw new Error('Pipeline failed')
  }
  return response.json()
}