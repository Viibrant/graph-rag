export interface SearchResult {
  id: string
  title: string
  authors: string[]
  score?: number
  related_ids?: string[]
}

export interface GraphNode {
  id: string
  title: string
  authors: string[]
  centrality: number
}

export interface GraphEdge {
  source: string
  target: string
  weight: number
  type: string
}

export interface GraphData {
  nodes: GraphNode[]
  edges: GraphEdge[]
}

export interface PaperStatus {
  id: string
  status: 'queued' | 'embedded' | 'seen' | 'error'
  in_graph: boolean
}

export interface SimNode {
  id: string;
  x: number;
  y: number;
}

export interface SimLink {
  source: SimNode;
  target: SimNode;
  distance: number;
}
