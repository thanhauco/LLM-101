"use client";

import * as d3 from "d3";
import { useEffect, useMemo, useRef } from "react";

type D3MetricsChartProps = {
  contextTokens: number;
  feedCount: number;
};

const width = 800;
const height = 290;
const margin = { top: 30, right: 30, bottom: 46, left: 46 };

export function D3MetricsChart({ contextTokens, feedCount }: D3MetricsChartProps) {
  const svgRef = useRef<SVGSVGElement | null>(null);
  const samples = useMemo(() => {
    const contextLift = Math.min(14, Math.round(contextTokens / 18));
    return [38, 44, 41, 48, 45, 52, 49, 55, 51, 58, 54, 61].map((value, index) => ({
      label: `${index + 1}`,
      tokensPerSecond: value + contextLift + (index % 3) * feedCount,
      latency: 1.8 - index * 0.045 + feedCount * 0.01
    }));
  }, [contextTokens, feedCount]);

  useEffect(() => {
    if (!svgRef.current) {
      return;
    }

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").interrupt();
    svg.selectAll("*").remove();
    svg.attr("viewBox", `0 0 ${width} ${height}`).attr("role", "img");

    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;
    const x = d3.scalePoint(samples.map((sample) => sample.label), [0, innerWidth]).padding(0.5);
    const y = d3
      .scaleLinear()
      .domain([0, d3.max(samples, (sample) => sample.tokensPerSecond) ?? 80])
      .nice()
      .range([innerHeight, 0]);

    const chart = svg.append("g").attr("transform", `translate(${margin.left}, ${margin.top})`);

    chart
      .append("g")
      .attr("class", "d3GridLines")
      .selectAll("line")
      .data(y.ticks(5))
      .join("line")
      .attr("x1", 0)
      .attr("x2", innerWidth)
      .attr("y1", (tick) => y(tick))
      .attr("y2", (tick) => y(tick));

    const area = d3
      .area<(typeof samples)[number]>()
      .x((sample) => x(sample.label) ?? 0)
      .y0(innerHeight)
      .y1((sample) => y(sample.tokensPerSecond))
      .curve(d3.curveCatmullRom.alpha(0.55));

    const line = d3
      .line<(typeof samples)[number]>()
      .x((sample) => x(sample.label) ?? 0)
      .y((sample) => y(sample.tokensPerSecond))
      .curve(d3.curveCatmullRom.alpha(0.55));

    chart
      .append("path")
      .datum(samples)
      .attr("class", "d3Area")
      .attr("d", area)
      .attr("opacity", 0)
      .transition()
      .duration(520)
      .attr("opacity", 1);

    const path = chart.append("path").datum(samples).attr("class", "d3Line").attr("d", line);
    const length = path.node()?.getTotalLength() ?? 0;
    path
      .attr("stroke-dasharray", length)
      .attr("stroke-dashoffset", length)
      .transition()
      .duration(900)
      .ease(d3.easeCubicOut)
      .attr("stroke-dashoffset", 0);

    chart
      .selectAll("circle")
      .data(samples)
      .join("circle")
      .attr("class", "d3Point")
      .attr("cx", (sample) => x(sample.label) ?? 0)
      .attr("cy", innerHeight)
      .attr("r", 0)
      .transition()
      .delay((_sample, index) => index * 55)
      .duration(420)
      .attr("cy", (sample) => y(sample.tokensPerSecond))
      .attr("r", 4);

    const barData = [
      { label: "latency", value: 72, color: "#d66b4d" },
      { label: "retrieval", value: 86, color: "#4178a8" },
      { label: "eval", value: 91, color: "#2d8a6b" }
    ];

    const barGroup = svg.append("g").attr("transform", "translate(48, 238)");
    barGroup
      .selectAll("rect")
      .data(barData)
      .join("rect")
      .attr("class", "d3Bar")
      .attr("x", (_bar, index) => index * 178)
      .attr("y", 0)
      .attr("width", 0)
      .attr("height", 12)
      .attr("rx", 6)
      .attr("fill", (bar) => bar.color)
      .transition()
      .duration(700)
      .delay((_bar, index) => index * 90)
      .attr("width", (bar) => bar.value * 1.35);

    barGroup
      .selectAll("text")
      .data(barData)
      .join("text")
      .attr("class", "d3BarLabel")
      .attr("x", (_bar, index) => index * 178)
      .attr("y", 30)
      .text((bar) => `${bar.label} ${bar.value}%`);

    svg
      .append("text")
      .attr("class", "d3ChartTitle")
      .attr("x", 46)
      .attr("y", 23)
      .text("token throughput and quality gates");

    return () => {
      svg.selectAll("*").interrupt();
    };
  }, [samples]);

  return <svg ref={svgRef} className="d3Canvas" aria-label="D3 animated telemetry chart" />;
}
