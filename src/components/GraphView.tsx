import React, { useCallback, useMemo } from 'react'
import ReactFlow, {
  Node,
  Edge,
  addEdge,
  Connection,
  useNodesState,
  useEdgesState,
  Controls,
  Background,
  BackgroundVariant,
  NodeTypes,
} from 'reactflow'
import 'reactflow/dist/style.css'
import { GraphData, SearchResult } from '../types'
import PaperNode from './PaperNode'

interface GraphViewProps {
  graphData?: GraphData
  searchResults: SearchResult[]
  selectedPaper: string | null
  onPaperSelect: (paperId: string) => void
}

const nodeTypes: NodeTypes = {
  paper: PaperNode,
}

export default function GraphView({ 
  graphData, 
  searchResults, 
  selectedPaper, 
  onPaperSelect 
}: GraphViewProps) {
  const { nodes: initialNodes, edges: initialEdges } = useMemo(() => {
    if (!graphData) {
      return { nodes: [], edges: [] }
    }

    // Create a set of search result IDs for highlighting
    const searchResultIds = new Set(searchResults.map(r => r.id))

    // Convert graph nodes to ReactFlow nodes
    const nodes: Node[] = graphData.nodes.map((node, index) => ({
      id: node.id,
      type: 'paper',
      position: {
        x: Math.cos(index * 0.5) * 200 + 400,
        y: Math.sin(index * 0.5) * 200 + 300,
      },
      data: {
        title: node.title,
        authors: node.authors,
        centrality: node.centrality,
        isSearchResult: searchResultIds.has(node.id),
        isSelected: selectedPaper === node.id,
        onSelect: () => onPaperSelect(node.id),
      },
    }))

    // Convert graph edges to ReactFlow edges
    const edges: Edge[] = graphData.edges.map((edge) => ({
      id: `${edge.source}-${edge.target}`,
      source: edge.source,
      target: edge.target,
      style: {
        strokeWidth: Math.max(1, edge.weight * 4),
        stroke: edge.type === 'co_author' ? '#3b82f6' : '#6b7280',
      },
      animated: searchResultIds.has(edge.source) || searchResultIds.has(edge.target),
    }))

    return { nodes, edges }
  }, [graphData, searchResults, selectedPaper, onPaperSelect])

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes)
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges)

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  )

  // Update nodes when props change
  React.useEffect(() => {
    setNodes(initialNodes)
    setEdges(initialEdges)
  }, [initialNodes, initialEdges, setNodes, setEdges])

  if (!graphData || graphData.nodes.length === 0) {
    return (
      <div className="h-96 flex items-center justify-center text-secondary-500">
        <div className="text-center">
          <div className="w-16 h-16 bg-secondary-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </div>
          <p>No graph data available</p>
          <p className="text-sm mt-1">Papers will appear here once they're processed</p>
        </div>
      </div>
    )
  }

  return (
    <div className="h-96">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        fitView
        attributionPosition="bottom-left"
      >
        <Controls />
        <Background variant={BackgroundVariant.Dots} gap={12} size={1} />
      </ReactFlow>
    </div>
  )
}