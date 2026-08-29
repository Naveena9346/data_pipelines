from collections import defaultdict, deque
from typing import List, Dict, Any, Tuple
from app.schemas.pipeline import PipelineNodeBase, PipelineEdgeBase
from app.core.exceptions import DAGCycleError, ValidationError


class DAGCompiler:
    """DAG Graph Compiler: Validates directed acyclic topology using Kahn's Algorithm."""

    @staticmethod
    def compile_and_toposort(nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> List[str]:
        if not nodes:
            raise ValidationError("Pipeline DAG must contain at least one node.")

        node_keys = {n["node_key"] for n in nodes}
        in_degree = {k: 0 for k in node_keys}
        adj_list = defaultdict(list)

        for edge in edges:
            src = edge["source_node_key"]
            tgt = edge["target_node_key"]

            if src not in node_keys:
                raise ValidationError(f"Invalid edge: source node key '{src}' does not exist in DAG.")
            if tgt not in node_keys:
                raise ValidationError(f"Invalid edge: target node key '{tgt}' does not exist in DAG.")

            adj_list[src].append(tgt)
            in_degree[tgt] += 1

        # Kahn's algorithm
        queue = deque([k for k in node_keys if in_degree[k] == 0])
        topological_order = []

        while queue:
            curr = queue.popleft()
            topological_order.append(curr)

            for neighbor in adj_list[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(topological_order) != len(node_keys):
            raise DAGCycleError("Cyclic dependency detected! DAG contains one or more closed execution loops.")

        return topological_order
