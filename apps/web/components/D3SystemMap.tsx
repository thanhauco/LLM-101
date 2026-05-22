"use client";

import * as d3 from "d3";
import { useEffect, useRef } from "react";

type D3SystemMapProps = {
  activeIndex: number;
};

type SystemNode = {
  id: string;
  label: string;
  detail: string;
  x: number;
  y: number;
  color: string;
};

const nodes: SystemNode[] = [
  { id: "prompt", label: "Prompt", detail: "user + system", x: 70, y: 78, color: "#2d8a6b" },
  { id: "router", label: "Router", detail: "task policy", x: 230, y: 78, color: "#4178a8" },
  { id: "retrieve", label: "Retrieve", detail: "Qdrant top-k", x: 390, y: 78, color: "#c49334" },
  { id: "rerank", label: "Rerank", detail: "cross encoder", x: 550, y: 78, color: "#7558a6" },
  { id: "generate", label: "Generate", detail: "vLLM stream", x: 710, y: 78, color: "#d66b4d" },
  { id: "evaluate", label: "Evaluate", detail: "Ragas checks", x: 710, y: 205, color: "#2d8a6b" }
];

const links = [
  { source: "prompt", target: "router" },
  { source: "router", target: "retrieve" },
  { source: "retrieve", target: "rerank" },
  { source: "rerank", target: "generate" },
  { source: "generate", target: "evaluate" },
  { source: "evaluate", target: "router" }
];

const width = 800;
const height = 290;

function linkPath(source: SystemNode, target: SystemNode) {
  const midX = (source.x + target.x) / 2;
  return `M ${source.x + 50} ${source.y + 22} C ${midX} ${source.y + 22}, ${midX} ${target.y + 22}, ${target.x - 50} ${target.y + 22}`;
}

export function D3SystemMap({ activeIndex }: D3SystemMapProps) {
  const svgRef = useRef<SVGSVGElement | null>(null);

  useEffect(() => {
    if (!svgRef.current) {
      return;
    }

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").interrupt();
    svg.selectAll("*").remove();
    svg.attr("viewBox", `0 0 ${width} ${height}`).attr("role", "img");

    const defs = svg.append("defs");
    const glow = defs.append("filter").attr("id", "d3-node-glow");
    glow.append("feGaussianBlur").attr("stdDeviation", 3).attr("result", "blur");
    glow
      .append("feMerge")
      .selectAll("feMergeNode")
      .data(["blur", "SourceGraphic"])
      .join("feMergeNode")
      .attr("in", (value) => value);

    const nodeById = new Map(nodes.map((node) => [node.id, node]));
    const linkGroup = svg.append("g").attr("class", "d3Links");

    linkGroup
      .selectAll("path")
      .data(links)
      .join("path")
      .attr("class", "d3Link")
      .attr("d", (link) => linkPath(nodeById.get(link.source)!, nodeById.get(link.target)!));

    linkGroup
      .selectAll("circle")
      .data(links)
      .join("circle")
      .attr("class", "d3Packet")
      .attr("r", 4)
      .each(function animatePacket(link, index) {
        const packet = d3.select(this);
        const source = nodeById.get(link.source)!;
        const target = nodeById.get(link.target)!;

        function repeat() {
          packet
            .attr("cx", source.x + 50)
            .attr("cy", source.y + 22)
            .transition()
            .delay(index * 180)
            .duration(1700)
            .ease(d3.easeCubicInOut)
            .attr("cx", target.x - 50)
            .attr("cy", target.y + 22)
            .transition()
            .duration(120)
            .attr("opacity", 0.2)
            .on("end", repeat);
        }

        repeat();
      });

    const nodeGroup = svg
      .append("g")
      .attr("class", "d3Nodes")
      .selectAll("g")
      .data(nodes)
      .join("g")
      .attr("class", (_node, index) => `d3Node ${index === activeIndex ? "active" : ""}`)
      .attr("transform", (node) => `translate(${node.x - 55}, ${node.y - 22})`);

    nodeGroup
      .append("rect")
      .attr("width", 110)
      .attr("height", 62)
      .attr("rx", 8)
      .attr("stroke", (node) => node.color);

    nodeGroup
      .append("circle")
      .attr("cx", 18)
      .attr("cy", 20)
      .attr("r", 6)
      .attr("fill", (node) => node.color);

    nodeGroup
      .append("text")
      .attr("x", 32)
      .attr("y", 24)
      .attr("class", "d3NodeTitle")
      .text((node) => node.label);

    nodeGroup
      .append("text")
      .attr("x", 18)
      .attr("y", 47)
      .attr("class", "d3NodeDetail")
      .text((node) => node.detail);

    nodeGroup
      .filter((_node, index) => index === activeIndex)
      .select("rect")
      .transition()
      .duration(360)
      .attr("filter", "url(#d3-node-glow)");

    return () => {
      svg.selectAll("*").interrupt();
    };
  }, [activeIndex]);

  return <svg ref={svgRef} className="d3Canvas" aria-label="D3 animated LLM system map" />;
}
