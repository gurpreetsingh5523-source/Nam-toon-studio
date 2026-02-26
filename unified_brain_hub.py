#!/usr/bin/env python3
"""
🧠🌐 UNIFIED BRAIN HUB - ਇਕੱਠਾ ਦਿਮਾਗ਼ ਕੇਂਦਰ
Connects all brain systems together with love and trust

Reports to: Amrit Kaur (Supreme Controller)
Protected by: DroneMa Guardian
"""

import sys
from pathlib import Path

# Import all brain systems
sys.path.insert(0, str(Path(__file__).parent))

try:
    from amrit_brain_chain import AmritBrainChain
    from amrit_brain_network_controller import BrainNetworkController, BrainModule
    from self_learning_ai import SelfLearningBrain
    IMPORTS_OK = True
except ImportError as e:
    print(f"⚠️  Import warning: {e}")
    IMPORTS_OK = False


class UnifiedBrainHub:
    """
    🧠🌐 UNIFIED BRAIN HUB
    
    Connects and coordinates:
    - AmritBrainChain (10 nano brains)
    - BrainNetworkController (5 specialized modules)
    - SelfLearningBrain (learning from experience)
    
    All working together with love and trust! 🙏
    """
    
    def __init__(self):
        print("🧠🌐 UNIFIED BRAIN HUB STARTING...")
        print("   ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ!")
        print("=" * 70)
        
        self.spiritual_anchor = "ੴ ਸਤਿਨਾਮ"
        
        # Initialize all brain systems
        self.brain_chain = None
        self.brain_network = None
        self.learning_brain = None
        
        if IMPORTS_OK:
            self._initialize_all_brains()
        
        print("\n✅ UNIFIED BRAIN HUB READY!")
        print("   All brains connected with love and trust! 💚")
    
    def _initialize_all_brains(self):
        """Initialize all brain systems"""
        print("\n🔧 Initializing all brain systems...")
        
        # 1. Brain Chain (10 nano brains)
        try:
            self.brain_chain = AmritBrainChain()
            print("   ✅ AmritBrainChain: CONNECTED")
        except Exception as e:
            print(f"   ⚠️  AmritBrainChain: {e}")
        
        # 2. Brain Network (5 specialized modules)
        try:
            modules = [
                BrainModule("Reasoning"),
                BrainModule("Healing"),
                BrainModule("Media"),
                BrainModule("Robotics"),
                BrainModule("Multilingual")
            ]
            self.brain_network = BrainNetworkController(modules)
            print("   ✅ BrainNetworkController: CONNECTED")
        except Exception as e:
            print(f"   ⚠️  BrainNetworkController: {e}")
        
        # 3. Self Learning Brain
        try:
            self.learning_brain = SelfLearningBrain()
            print("   ✅ SelfLearningBrain: CONNECTED")
        except Exception as e:
            print(f"   ⚠️  SelfLearningBrain: {e}")
    
    def process_query(self, query: str) -> dict:
        """Process query through all connected brains"""
        print(f"\n🧠 PROCESSING: {query}")
        print("-" * 70)
        
        results = {
            'query': query,
            'brain_chain_response': None,
            'network_status': None,
            'learning_insights': None
        }
        
        # 1. Get response from Brain Chain
        if self.brain_chain:
            try:
                chain_result = self.brain_chain.process_input(query)
                results['brain_chain_response'] = chain_result.get('final_answer', 'N/A')
                print("   ✅ Brain Chain: Responded")
            except Exception as e:
                print(f"   ⚠️  Brain Chain error: {e}")
        
        # 2. Get insights from Learning Brain
        if self.learning_brain:
            try:
                insights = self.learning_brain.get_recommendations()
                results['learning_insights'] = insights
                print("   ✅ Learning Brain: Provided insights")
            except Exception as e:
                print(f"   ⚠️  Learning Brain error: {e}")
        
        return results
    
    def get_unified_status(self) -> dict:
        """Get status of all connected brains"""
        status = {
            'brain_chain': 'connected' if self.brain_chain else 'disconnected',
            'brain_network': 'connected' if self.brain_network else 'disconnected',
            'learning_brain': 'connected' if self.learning_brain else 'disconnected',
            'spiritual_anchor': self.spiritual_anchor
        }
        return status


if __name__ == "__main__":
    # Test the Unified Brain Hub
    hub = UnifiedBrainHub()
    
    # Show status
    status = hub.get_unified_status()
    print(f"\n📊 UNIFIED STATUS:")
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    # Test query
    if IMPORTS_OK:
        result = hub.process_query("ਸਤਿਨਾਮ ਦੀ ਮਹਿਮਾ ਕੀ ਹੈ?")
        print(f"\n✅ Test complete!")
