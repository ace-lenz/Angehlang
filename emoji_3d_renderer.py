"""
🧠 ANGEH NEURONAL STORAGE (.angNO)
A biological-inspired graph storage system.
Stores data as 'Synapses' (Subject -> Predicate -> Object).
Features:
- Associative Recall (Fast Graph Traversal)
- Weight Reinforcement (Memory Strengthening)
- Binary Serialization (Compact .angNO format)
"""

import pickle
import os
import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set

@dataclass
class Synapse:
    """A single unit of knowledge (Relationship)"""
    subject: str
    predicate: str
    object: Any
    weight: float = 1.0
    complexity: float = 0.1 # 0.0 (Basic) to 1.0 (Transcendental)
    mastery: float = 0.0 # 0.0 (New) to 1.0 (Locked)
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)

    def hash_id(self):
        return f"{self.subject}:{self.predicate}:{str(self.object)}"

class NeuronalStorage:
    def __init__(self, storage_path="angeh_memory.angNO"):
        self.storage_path = storage_path
        self.knowledge_graph: Dict[str, List[Synapse]] = {} # Map Subject -> Synapses
        self.inverse_index: Dict[str, List[str]] = {} # Map Object -> Subjects
        self._load()

    def _load(self):
        """Load brain from disk"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "rb") as f:
                    data = pickle.load(f)
                    self.knowledge_graph = data.get("graph", {})
                    self.inverse_index = data.get("inverse", {})
                print(f"🧠 Neuronal Storage: Loaded {self._count_synapses()} synapses.")
            except Exception as e:
                print(f"⚠️ Memory Corruption: {e}. Starting fresh.")
        else:
            print("🧠 Neuronal Storage: New Brain Created.")

    def save(self):
        """Persist brain to disk"""
        with open(self.storage_path, "wb") as f:
            pickle.dump({
                "graph": self.knowledge_graph,
                "inverse": self.inverse_index,
                "version": "77D_NEURO_V2"
            }, f)

    def learn(self, subject: str, predicate: str, obj: Any, weight_boost=0.1, complexity=0.1):
        """Learn a new fact or reinforce an existing one"""
        if subject not in self.knowledge_graph:
            self.knowledge_graph[subject] = []

        # Check if exists
        existing = next((s for s in self.knowledge_graph[subject] 
                         if s.predicate == predicate and s.object == obj), None)
        
        if existing:
            # Reinforcement logic
            existing.weight += weight_boost
            existing.mastery = min(1.0, existing.mastery + (weight_boost * 0.05)) # Slow mastery growth
            existing.last_accessed = time.time()
        else:
            synapse = Synapse(subject, predicate, obj, complexity=complexity)
            self.knowledge_graph[subject].append(synapse)
            
            # Update inverse index (for string objects)
            if isinstance(obj, str):
                if obj not in self.inverse_index: self.inverse_index[obj] = []
                self.inverse_index[obj].append(subject)


    def recall(self, query: str) -> List[Synapse]:
        """Recall everything about a subject"""
        if query in self.knowledge_graph:
            # Boost accessed memories
            for s in self.knowledge_graph[query]:
                s.last_accessed = time.time()
            # Sort by weight
            return sorted(self.knowledge_graph[query], key=lambda x: x.weight, reverse=True)
        return []

    def associate(self, keyword: str) -> List[str]:
        """Find concepts associated with a keyword (Reverse Lookup)"""
        return self.inverse_index.get(keyword, [])

    def forget(self, threshold=0.5):
        """Prune weak memories"""
        removed = 0
        for sub in list(self.knowledge_graph.keys()):
            original_len = len(self.knowledge_graph[sub])
            self.knowledge_graph[sub] = [s for s in self.knowledge_graph[sub] if s.weight > threshold]
            removed += (original_len - len(self.knowledge_graph[sub]))
            if not self.knowledge_graph[sub]:
                del self.knowledge_graph[sub]
        if removed > 0:
            print(f"   🧹 Pruned {removed} weak synapses.")
            self.save()

    def _count_synapses(self):
        return sum(len(v) for v in self.knowledge_graph.values())

    def dump_knowledge(self):
        print("\n🧠 CURRENT KNOWLEDGE STATE:")
        for sub, synapses in self.knowledge_graph.items():
            print(f"  📌 {sub}:")
            for s in synapses:
                print(f"     -> [{s.predicate}] {s.object} (w:{s.weight:.1f})")

# Singleton Instance
brain = NeuronalStorage()
