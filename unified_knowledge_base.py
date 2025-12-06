#!/usr/bin/env python3
"""
📚🔗 UNIFIED KNOWLEDGE BASE
Unifies all knowledge sources with love
"""

import json
from pathlib import Path
from typing import Dict, List, Any


class UnifiedKnowledgeBase:
    """Unifies all knowledge from brain files, memory, and improvements"""
    
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.unified_knowledge = {}
        self._load_all_knowledge()
    
    def _load_all_knowledge(self):
        """Load knowledge from all sources"""
        print("📚 LOADING ALL KNOWLEDGE WITH LOVE...")
        
        # Load brain files
        for brain_file in self.workspace.glob('brain_*.txt'):
            try:
                with open(brain_file, 'r', encoding='utf-8') as f:
                    self.unified_knowledge[brain_file.stem] = {
                        'type': 'brain',
                        'content': f.read(),
                        'size': brain_file.stat().st_size
                    }
                print(f"   ✅ {brain_file.stem}")
            except Exception as e:
                print(f"   ⚠️  {brain_file.stem}: {e}")
        
        # Load memory files
        memory_files = ['ai_memory.json', 'ai_improvements.json']
        for mem_file in memory_files:
            mem_path = self.workspace / mem_file
            if mem_path.exists():
                try:
                    with open(mem_path, 'r') as f:
                        self.unified_knowledge[mem_file] = {
                            'type': 'memory',
                            'content': json.load(f)
                        }
                    print(f"   ✅ {mem_file}")
                except Exception as e:
                    print(f"   ⚠️  {mem_file}: {e}")
    
    def query_knowledge(self, topic: str) -> Dict[str, Any]:
        """Query unified knowledge"""
        relevant = {}
        for key, data in self.unified_knowledge.items():
            if topic.lower() in str(data).lower():
                relevant[key] = data
        return relevant


if __name__ == "__main__":
    kb = UnifiedKnowledgeBase(Path(__file__).parent)
    print(f"\n✅ Loaded {len(kb.unified_knowledge)} knowledge sources!")
