import { memo } from "react";
import { Handle, Position } from "reactflow";

export interface PaperNodeData {
  title: string;
  size: number;
  isSearchResult: boolean;
  isSelected: boolean;
  isFaded?: boolean;
  showLabel?: boolean;
  onSelect: () => void;
}
interface PaperNodeProps { data: PaperNodeData }

function PaperNode({ data }: PaperNodeProps) {
  const { title, size, isSelected, isSearchResult, isFaded, showLabel, onSelect } = data;

  // slightly smaller + less zoom on select
  const d = Math.max(10, size) * (isSelected ? 1.15 : 1);
  const truncated = title.length > 28 ? title.slice(0, 28) + "…" : title;

  return (
    <div
      onClick={onSelect}
      className={["relative group select-none", isFaded ? "opacity-35" : "opacity-100"].join(" ")}
      style={{ width: d, height: d }}
    >
      <div
        className={[
          "rounded-full border-2 box-content cursor-pointer",
          isSelected
            ? "bg-[--accent] border-[--text]"
            : isSearchResult
              ? "bg-[--surface] border-[--accent]"
              : "bg-[--surface] border-[var(--border)]",
        ].join(" ")}
        style={{ width: d, height: d }}
        title={title}
      />

      {/* invisible, centred handles so edges attach to the middle */}
      <Handle
        type="source"
        position={Position.Top}
        style={{ left: "50%", top: "50%", transform: "translate(-50%, -50%)", width: 0, height: 0 }}
        className="!bg-transparent !border-0"
      />
      <Handle
        type="target"
        position={Position.Top}
        style={{ left: "50%", top: "50%", transform: "translate(-50%, -50%)", width: 0, height: 0 }}
        className="!bg-transparent !border-0"
      />

      {showLabel && (
        <div
          className="absolute left-1/2 -translate-x-1/2 -top-7 px-2 py-0.5 rounded border border-[var(--border)]
                     bg-[--surface] text-[--text] text-[10px] font-mono whitespace-nowrap z-10">
          {truncated}
        </div>
      )}
    </div>
  );
}

export default memo(PaperNode);
