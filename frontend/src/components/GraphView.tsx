// frontend/src/components/GraphView.tsx
import { forceCenter, forceCollide, forceLink, forceManyBody, forceSimulation } from "d3-force";
import { useCallback, useEffect, useMemo } from "react";
import ReactFlow, {
  addEdge,
  Background,
  BackgroundVariant,
  type Connection,
  Controls,
  type Edge,
  type Node,
  type NodeTypes,
  ReactFlowProvider,
  useEdgesState,
  useNodesState,
  useReactFlow,
} from "reactflow";
import "reactflow/dist/style.css";
import type { GraphData, SearchResult } from "../types";
import PaperNode from "./PaperNode";

const NODE_TYPES: NodeTypes = Object.freeze({ paper: PaperNode });

interface GraphViewProps {
  graphData?: GraphData;
  searchResults: SearchResult[];
  selectedPaper: string | null;
  onPaperSelect: (paperId: string) => void;
  /** CSS height, e.g. "58vh" (default "62vh") */
  height?: string;
}

// smaller mapping so blobs don’t dominate
const sizeFromCentrality = (c?: number) => {
  const x = Math.max(0, c ?? 0);
  const d = 10 + 16 * Math.sqrt(x);       // was 12 + 20
  return Math.max(10, Math.min(28, d));   // cap 28 (was 34)
};

function synthFromResults(results: SearchResult[]): { nodes: Node[]; edges: Edge[] } {
  const nodes = new Map<string, Node>();
  const edges: Edge[] = [];
  for (const r of results) {
    nodes.set(r.id, {
      id: r.id,
      type: "paper",
      position: { x: 0, y: 0 },
      data: {
        title: r.title,
        size: sizeFromCentrality(r.score),
        isSearchResult: true,
        isSelected: false,
        isFaded: false,
        showLabel: false,
        onSelect: () => { },
      },
    });
  }
  for (const r of results) {
    for (const rel of r.related_ids ?? []) {
      if (!nodes.has(rel)) {
        nodes.set(rel, {
          id: rel,
          type: "paper",
          position: { x: 0, y: 0 },
          data: {
            title: rel,
            size: 10,
            isSearchResult: false,
            isSelected: false,
            isFaded: false,
            showLabel: false,
            onSelect: () => { },
          },
        });
      }
      edges.push({ id: `${r.id}-${rel}`, source: r.id, target: rel, style: { strokeWidth: 1.5, stroke: "var(--border)" } });
    }
  }
  return { nodes: Array.from(nodes.values()), edges };
}

function forceLayout(nodes: Node[], edges: Edge[]) {
  const diam = new Map(nodes.map((n) => [n.id, (n.data as any).size ?? 16]));
  const simNodes = nodes.map((n) => ({ id: n.id, x: Math.random() * 800, y: Math.random() * 500 }));
  const idx = new Map(simNodes.map((n) => [n.id, n]));
  const links = edges
    .filter((e) => idx.has(e.source) && idx.has(e.target))
    .map((e) => ({ source: idx.get(e.source)!, target: idx.get(e.target)!, distance: 110 }));

  const sim = forceSimulation(simNodes)
    .force("charge", forceManyBody().strength(-160))
    .force("link", forceLink(links).distance((d: any) => d.distance).strength(0.25))
    .force("collide", forceCollide((d: any) => (diam.get(d.id) ?? 16) / 2 + 6))
    .force("center", forceCenter(400, 240))
    .stop();

  for (let i = 0; i < 180; i++) sim.tick();

  const laid = nodes.map((n) => {
    const s = idx.get(n.id)!;
    return { ...n, position: { x: s.x ?? 0, y: s.y ?? 0 } };
  });
  return { nodes: laid, edges };
}

function GraphViewInner({ graphData, searchResults, selectedPaper, onPaperSelect, height = "62vh" }: GraphViewProps) {
  const { fitView } = useReactFlow();

  // base layout (data only)
  const { nodes: layoutNodes, edges: layoutEdges } = useMemo(() => {
    let baseNodes: Node[];
    let baseEdges: Edge[];

    if (graphData && graphData.edges?.length) {
      const hits = new Set(searchResults.map((r) => r.id));
      baseNodes = graphData.nodes.map((n) => ({
        id: n.id,
        type: "paper",
        position: { x: 0, y: 0 },
        data: {
          title: n.title,
          size: sizeFromCentrality(n.centrality),
          isSearchResult: hits.has(n.id),
          isSelected: false,
          isFaded: false,
          showLabel: false,
          onSelect: () => onPaperSelect(n.id),
        },
      }));
      baseEdges = graphData.edges
        .filter((e) => e.source !== e.target)
        .map((e) => ({
          id: `${e.source}-${e.target}`,
          source: e.source,
          target: e.target,
          style: { strokeWidth: Math.max(1, e.weight * 2), stroke: "var(--border)" },
        }));
    } else {
      const synth = synthFromResults(searchResults);
      baseNodes = synth.nodes.map((n) => ({
        ...n,
        data: { ...(n.data as any), onSelect: () => onPaperSelect(n.id), isSelected: false },
      }));
      baseEdges = synth.edges;
    }
    return forceLayout(baseNodes, baseEdges);
  }, [graphData, searchResults, onPaperSelect]);

  // selection-only styling (positions untouched)
  const styledNodes = useMemo(() => {
    if (!selectedPaper) return layoutNodes;
    const neigh = new Set<string>([selectedPaper]);
    for (const e of layoutEdges) {
      if (e.source === selectedPaper) neigh.add(String(e.target));
      if (e.target === selectedPaper) neigh.add(String(e.source));
    }
    return layoutNodes.map((n) => ({
      ...n,
      data: { ...(n.data as any), isSelected: n.id === selectedPaper, isFaded: !neigh.has(n.id), showLabel: n.id === selectedPaper },
    }));
  }, [layoutNodes, layoutEdges, selectedPaper]);

  const styledEdges = useMemo(() => {
    if (!selectedPaper) return layoutEdges;
    return layoutEdges.map((e) => ({
      ...e,
      style: {
        ...(e.style || {}),
        stroke: e.source === selectedPaper || e.target === selectedPaper ? "var(--accent)" : "var(--border)",
        strokeWidth: e.source === selectedPaper || e.target === selectedPaper ? 2.5 : 1.5,
      },
    }));
  }, [layoutEdges, selectedPaper]);

  const [nodes, setNodes, onNodesChange] = useNodesState(styledNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(styledEdges);

  const onConnect = useCallback((params: Connection) => setEdges((eds) => addEdge(params, eds)), [setEdges]);

  useEffect(() => {
    setNodes(styledNodes);
    setEdges(styledEdges);
    if (!selectedPaper) {
      const id = setTimeout(() => fitView({ padding: 0.1 }), 0);
      return () => clearTimeout(id);
    }
  }, [styledNodes, styledEdges, fitView, selectedPaper, setNodes, setEdges]);

  if (!nodes.length) {
    return (
      <div className="flex items-center justify-center text-[var(--muted)]" style={{ height }}>
        <div className="text-sm">No graph data — try another query.</div>
      </div>
    );
  }

  return (
    <div className="w-full h-full">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={NODE_TYPES}
        fitView
        proOptions={{ hideAttribution: true }}
        defaultEdgeOptions={{ type: "straight" }}
        minZoom={0.2}
        maxZoom={1.8}
      >
        <Controls position="bottom-left" />
        <Background variant={BackgroundVariant.Dots} gap={14} size={1} color="var(--grid)" />
      </ReactFlow>
    </div>
  );
}

export default function GraphViewWrapper(props: GraphViewProps) {
  return (
    <ReactFlowProvider>
      <div className="w-full h-full flex-1">
        <GraphViewInner {...props} />
      </div>
    </ReactFlowProvider>
  );
}
