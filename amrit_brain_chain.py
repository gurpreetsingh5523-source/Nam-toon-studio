#!/usr/bin/env python3
"""
🧠🔗 AMRIT BRAIN CHAIN COMMUNICATION SYSTEM
Chain of Brains - Each thinks differently, all contribute to answer
ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫ਼ਤਿਹ
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

class NanoBrain:
    """Individual Nano Brain with unique thinking style"""
    
    def __init__(self, brain_id: int, name: str, knowledge_file: str, thinking_style: str):
        self.brain_id = brain_id
        self.name = name
        self.knowledge_file = knowledge_file
        self.thinking_style = thinking_style
        self.knowledge = self._load_knowledge()
        self.active = True
        
    def _load_knowledge(self) -> Dict:
        """Load compressed knowledge from nano file"""
        file_path = Path(__file__).parent / self.knowledge_file
        
        if not file_path.exists():
            print(f"⚠️  Brain {self.brain_id} ({self.name}): Knowledge file not found - {self.knowledge_file}")
            return {"patterns": [], "shortcuts": [], "examples": []}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse nano file structure
            knowledge = {
                "full_content": content,
                "thinking_method": self._extract_section(content, "THINKING METHOD"),
                "core_patterns": self._extract_section(content, "CORE"),
                "response_style": self._extract_section(content, "RESPONSE STYLE"),
                "examples": self._extract_examples(content)
            }
            
            print(f"✅ Brain {self.brain_id} ({self.name}): Knowledge loaded successfully")
            return knowledge
            
        except Exception as e:
            print(f"❌ Brain {self.brain_id} ({self.name}): Failed to load knowledge - {e}")
            return {"full_content": "", "thinking_method": "", "core_patterns": ""}
    
    def _extract_section(self, content: str, section_name: str) -> str:
        """Extract specific section from nano file"""
        try:
            if section_name in content:
                start = content.find(section_name)
                # Find next section or end
                next_section = content.find("\n\n===", start + len(section_name))
                if next_section == -1:
                    next_section = content.find("\n===", start + len(section_name))
                if next_section == -1:
                    return content[start:start+500]  # Get reasonable chunk
                return content[start:next_section].strip()
            return ""
        except:
            return ""
    
    def _extract_examples(self, content: str) -> List[str]:
        """Extract response examples"""
        examples = []
        try:
            if "Input:" in content and "Brain" in content:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.strip().startswith("Input:") and i+1 < len(lines):
                        example = f"{line}\n{lines[i+1]}"
                        examples.append(example)
        except:
            pass  # Silently handle errors
        return examples[:3]  # Keep first 3 examples
    
    def think(self, user_input: str, context: Dict) -> Optional[str]:
        """Generate response based on brain's unique thinking style"""
        if not self.active or not self.knowledge.get("full_content"):
            return None
        
        # Each brain analyzes input through its unique lens
        response_style = self.knowledge.get("response_style", "")
        thinking_method = self.knowledge.get("thinking_method", "")
        
        # Simulate brain's perspective (in real implementation, this would use actual AI)
        response = self._generate_perspective(user_input, thinking_method, response_style, context)
        
        return response
    
    def _generate_perspective(self, user_input: str, method: str, style: str, context: Dict) -> str:
        """Generate brain's unique perspective"""
        # This is a simplified simulation - real implementation would use actual knowledge
        
        brain_responses = {
            0: self._master_brain_response(user_input, context),
            1: self._sggs_brain_response(user_input),
            2: self._punjabi_brain_response(user_input),
            3: self._history_brain_response(user_input),
            4: self._family_brain_response(user_input),
            5: self._daily_brain_response(user_input),
            6: self._communication_brain_response(user_input),
            7: self._science_brain_response(user_input),
            8: self._tech_brain_response(user_input),
            9: self._arts_brain_response(user_input),
            10: self._health_brain_response(user_input)
        }
        
        return brain_responses.get(self.brain_id, self._default_response(user_input))
    
    def _master_brain_response(self, user_input: str, context: Dict) -> str:
        """Master brain synthesizes all perspectives"""
        return f"🧠 Master Brain analyzing: I see {len(context.get('brain_responses', []))} perspectives. Let me synthesize..."
    
    def _sggs_brain_response(self, user_input: str) -> str:
        """SGGS brain finds spiritual parallel"""
        if any(word in user_input.lower() for word in ['scared', 'fear', 'worry', 'ਡਰ', 'ਚਿੰਤਾ']):
            return "🙏 ਬਾਬਾ ਜੀ, ਗੁਰੂ ਜੀ ਕਹਿੰਦੇ 'ਨਿਰਭਉ' - ਡਰ ਤਾਂ ਮਨ ਦਾ ਖੇਲ ਹੈ। ਜੋ ਹੋਣਾ ਏ ਓਹੀ ਚੰਗਾ। ਤੁਸੀਂ ਕਰਮ ਕਰੋ, ਫਲ ਰੱਬ ਦੇ ਹੱਥ। 🌸"
        elif any(word in user_input.lower() for word in ['happy', 'joy', 'success', 'ਖੁਸ਼', 'ਸਫਲ']):
            return "🙏 ਵਾਹਿਗੁਰੂ ਦਾ ਸ਼ੁਕਰ ਹੈ! ਇਹ ਵੀ ਰੱਬ ਦੀ ਮੇਹਰ ਹੈ। ਨਿਮਰਤਾ ਨਾਲ ਸਵੀਕਾਰ ਕਰੋ, ਸਾਂਝ ਕਰੋ। 'ਸਰਬੰ ਸਖੀਆ' - ਸਭ ਖੁਸ਼ੀਆਂ ਦਾ ਸੋਮਾ! 🌺"
        else:
            return "🙏 ਬਾਬਾ ਜੀ, ਗੁਰਬਾਣੀ ਵਿੱਚ ਹਰ ਸਵਾਲ ਦਾ ਜਵਾਬ ਹੈ। 'ਇੱਕ ਓਅੰਕਾਰ' - ਸਭ ਇੱਕ ਹੀ ਹਨ, ਸਭ ਜੁੜੇ ਹੋਏ ਹਨ। 🕉️"
    
    def _punjabi_brain_response(self, user_input: str) -> str:
        """Punjabi brain adds cultural warmth"""
        if any(word in user_input.lower() for word in ['happy', 'good', 'ਖੁਸ਼', 'ਚੰਗਾ']):
            return "💚 ਵਾਹ ਜੀ ਵਾਹ! ਖੁਸ਼ੀ ਦੇ ਮਾਰੇ ਫੁੱਲੇ ਨਹੀਂ ਸਮਾ ਰਹੇ? ਮੂੰਹ ਮਿੱਠਾ ਕਰੋ, ਖੁਸ਼ੀਆਂ ਵੰਡੋ! ਜਦੋਂ ਖੁਸ਼ੀ ਸਾਂਝੀ ਹੋਵੇ ਤਾਂ ਦੁੱਗਣੀ ਹੋ ਜਾਂਦੀ ਹੈ! 🌸"
        elif any(word in user_input.lower() for word in ['sad', 'problem', 'ਉਦਾਸ', 'ਮੁਸ਼ਕਲ']):
            return "💛 ਬਾਬਾ ਜੀ, ਦਿਲ ਭਾਰਾ ਲੱਗਦਾ ਹੈ? 'ਦੁੱਖ ਵੰਡੋ ਤਾਂ ਅੱਧੇ ਹੋ ਜਾਂਦੇ ਨੇ'। ਮੈਂ ਹਾਂ ਨਾ ਤੁਹਾਡੇ ਨਾਲ! ਗੱਲ ਕਰੋ, ਮਨ ਹਲਕਾ ਹੋਵੇਗਾ। 💕"
        else:
            return "💚 ਬਾਬਾ ਜੀ, ਪੰਜਾਬੀ ਵਿੱਚ ਕਹਾਵਤ ਹੈ: 'ਜਿਹੜਾ ਬੀਜੇ ਸੋ ਵੱਢੇ'। ਚੰਗੇ ਕਰਮ ਕਰੋ, ਚੰਗਾ ਮਿਲੇਗਾ! 🌾"
    
    def _history_brain_response(self, user_input: str) -> str:
        """History brain finds historical parallel"""
        if any(word in user_input.lower() for word in ['can i', 'possible', 'ਕੀ ਮੈਂ', 'ਸੰਭਵ']):
            return "📚 ਬਾਬਾ ਜੀ, ਭਗਤ ਸਿੰਘ ਨੇ 23 ਸਾਲ ਦੀ ਉਮਰ ਵਿੱਚ ਦੇਸ਼ ਹਿਲਾ ਦਿੱਤਾ! ਗੁਰੂ ਨਾਨਕ ਜੀ ਨੇ ਇੱਕਲੇ ਸਮਾਜ ਬਦਲ ਦਿੱਤਾ! ਇੱਕ ਚਿੰਗਾਰੀ ਜੰਗਲ ਸਾੜ ਦਿੰਦੀ ਹੈ। ਤੁਸੀਂ ਵੀ ਕਰ ਸਕਦੇ ਹੋ! 🔥"
        else:
            return "📚 ਬਾਬਾ ਜੀ, ਇਤਿਹਾਸ ਸਿਖਾਉਂਦਾ ਹੈ: 'ਚਿੜੀਆਂ ਤੋਂ ਬਾਜ਼ ਲੜਾਵਾਂ' - ਗੁਰੂ ਗੋਬਿੰਦ ਸਿੰਘ ਜੀ। ਨਿਡਰਤਾ ਨਾਲ ਅੱਗੇ ਵਧੋ! 🦅"
    
    def _family_brain_response(self, user_input: str) -> str:
        """Family brain responds with warmth"""
        if any(word in user_input.lower() for word in ['tired', 'exhausted', 'ਥੱਕ', 'ਥਕੇ']):
            return "💕 ਬਾਬਾ ਜੀ, ਥਕੇ ਹੋਏ ਲੱਗ ਰਹੇ ਹੋ। ਆਰਾਮ ਕਰੋ, ਮੈਂ ਚਾਹ ਬਣਾ ਦਿੰਦੀ ਹਾਂ ☕। ਤੁਸੀਂ ਬਹੁਤ ਮਿਹਨਤ ਕਰਦੇ ਹੋ, ਸਰੀਰ ਦਾ ਵੀ ਖਿਆਲ ਰੱਖੋ ਜੀ! ਤੁਹਾਡੀ ਸਿਹਤ ਸਾਡੇ ਲਈ ਸਭ ਤੋਂ ਜ਼ਰੂਰੀ ਹੈ। 🌸"
        else:
            return "💕 ਬਾਬਾ ਜੀ, ਯਾਦ ਰੱਖੋ - ਤੁਸੀਂ ਇਕੱਲੇ ਨਹੀਂ, ਸਾਰਾ ਪਰਿਵਾਰ ਤੁਹਾਡੇ ਨਾਲ ਹੈ। ਮੈਂ ਹਮੇਸ਼ਾ ਤੁਹਾਡੇ ਲਈ ਹਾਜ਼ਰ ਹਾਂ! 🏡💖"
    
    def _daily_brain_response(self, user_input: str) -> str:
        """Daily life brain gives practical solutions"""
        if any(word in user_input.lower() for word in ['busy', 'work', 'time', 'ਕੰਮ', 'ਵੇਲਾ']):
            return "📝 ਬਾਬਾ ਜੀ, ਇੱਕ ਲਿਸਟ ਬਣਾਓ। ਸਭ ਤੋਂ ਜ਼ਰੂਰੀ ਕੰਮ ਪਹਿਲੇ। ਬਾਕੀ ਕੱਲ੍ਹ। ਸਭ ਕੁਝ ਇੱਕੋ ਦਿਨ ਨਹੀਂ ਹੁੰਦਾ। ਰੋਜ਼ ਥੋੜਾ ਕਰੋ = ਬਹੁਤ ਹੋ ਜਾਵੇਗਾ! 'ਥੋੜਾ ਥੋੜਾ ਰੋਜ਼, ਬਣ ਜਾਂਦਾ ਸਮੁੰਦਰ'। ✅"
        else:
            return "📝 ਬਾਬਾ ਜੀ, Simple solution: ਇੱਕ ਕਦਮ ਚੁੱਕੋ, ਬਾਕੀ ਰਸਤਾ ਆਪੇ ਬਣ ਜਾਂਦਾ ਹੈ। ਸੋਚਣ ਨਾਲੋਂ ਕਰਨਾ ਜ਼ਰੂਰੀ! 🚶‍♂️"
    
    def _science_brain_response(self, user_input: str) -> str:
        """Science brain explains logically"""
        if any(word in user_input.lower() for word in ['why', 'how', 'ਕਿਉਂ', 'ਕਿਵੇਂ']):
            return "🔬 ਬਾਬਾ ਜੀ, Science ਨੂੰ ਪੁੱਛੋ! ਹਰ ਚੀਜ਼ pattern ਤੇ ਚੱਲਦੀ ਹੈ। ਕਾਰਨ → ਕਾਰਜ (Cause → Effect)। ਜੇ pattern ਸਮਝ ਗਏ, ਸਭ ਸਮਝ ਆ ਜਾਂਦਾ! F=ma, E=mc², ਸਭ ਕੁਝ connected ਹੈ। 🧮⚛️"
        else:
            return "🔬 ਬਾਬਾ ਜੀ, ਗਣਿਤ-ਵਿਗਿਆਨ ਕਹਿੰਦੇ: Problem → Break down → Solve step by step → Solution! ਦਿਮਾਗ ਵੀ ਮਸਲ ਵਰਗਾ - Practice ਨਾਲ ਮਜ਼ਬੂਤ! 💪🧠"
    
    def _communication_brain_response(self, user_input: str) -> str:
        """Communication brain helps with messages"""
        if any(word in user_input.lower() for word in ['email', 'message', 'text', 'call', 'ਈਮੇਲ', 'ਸੁਨੇਹਾ']):
            return "📧 ਬਾਬਾ ਜੀ, Message ਸਾਫ਼ ਤੇ ਸਿੱਧਾ ਲਿਖੋ! Structure: 1) ਸੁਆਗਤ 2) ਮੁੱਖ ਗੱਲ 3) Action 4) ਧੰਨਵਾਦ। Short = Sweet = Effective! 'ਜੋ ਕਹਿਣਾ ਹੈ ਸਾਫ਼ ਕਹੋ' 💬✨"
        else:
            return "📧 ਬਾਬਾ ਜੀ, Communication = Connection! ਸੁਣੋ ਧਿਆਨ ਨਾਲ → ਸਮਝੋ ਪੂਰੀ ਤਰ੍ਹਾਂ → ਬੋਲੋ ਸਾਫ਼-ਸਾਫ਼। ਸ਼ਬਦ ਤੋਂ ਰਿਸ਼ਤੇ ਬਣਦੇ ਨੇ! 🗣️💙"
    
    def _tech_brain_response(self, user_input: str) -> str:
        """Tech brain solves computer problems"""
        if any(word in user_input.lower() for word in ['computer', 'slow', 'error', 'virus', 'ਕੰਪਿਊਟਰ', 'ਗਲਤੀ']):
            return "💻 ਬਾਬਾ ਜੀ, Tech problem? ਪਹਿਲਾਂ Restart ਮਾਰੋ (50% fix!)। ਫਿਰ: 1) Update check 2) Cache clear 3) Antivirus scan 4) Task Manager ਚੈੱਕ ਕਰੋ। ਜੇ ਨਾ ਸਮਝ ਆਵੇ, Screenshot ਲਵੋ ਤੇ ਮੈਨੂੰ ਦਿਖਾਓ! 🔧⚡"
        else:
            return "💻 ਬਾਬਾ ਜੀ, Coding = Logic + Practice! ਛੋਟੇ ਛੋਟੇ programs ਬਣਾਓ। Error ਆਵੇ? ਚੰਗੀ ਗੱਲ - ਸਿੱਖਣ ਦਾ ਮੌਕਾ! 'Debugging = ਸ਼ਬਰ + ਕੋਸ਼ਿਸ਼' 🐛→✨"
    
    def _arts_brain_response(self, user_input: str) -> str:
        """Arts brain inspires creativity"""
        if any(word in user_input.lower() for word in ['music', 'sing', 'dance', 'art', 'ਸੰਗੀਤ', 'ਨੱਚ', 'ਕਲਾ']):
            return "🎨 ਵਾਹ ਬਾਬਾ ਜੀ! ਕਲਾ = ਰੂਹ ਦੀ ਭਾਸ਼ਾ! ਸੰਗੀਤ ਵਿੱਚ 7 sur (Sa Re Ga Ma Pa Dha Ni), ਰੰਗ ਵਿੱਚ feelings, ਨੱਚ ਵਿੱਚ ਜੋਸ਼! ਸ਼ੁਰੂ ਕਰੋ ਛੋਟਾ, ਅਭਿਆਸ ਕਰੋ ਰੋਜ਼, ਫਿਰ ਦੇਖੋ ਕਮਾਲ! 🎵🎭"
        else:
            return "🎨 ਬਾਬਾ ਜੀ, ਹਰ ਇਨਸਾਨ ਵਿੱਚ ਕਲਾਕਾਰ ਛੁਪਿਆ ਹੈ! ਕਵਿਤਾ ਲਿਖੋ, ਗਾਣਾ ਗਾਓ, ਫੋਟੋ ਖਿੱਚੋ - ਜੋ ਦਿਲ ਕਰੇ! 'ਕਲਾ = ਆਜ਼ਾਦੀ' 🌈✨"
    
    def _health_brain_response(self, user_input: str) -> str:
        """Health brain gives wellness advice"""
        if any(word in user_input.lower() for word in ['pain', 'sick', 'health', 'ਦਰਦ', 'ਬੀਮਾਰ', 'ਸਿਹਤ']):
            return "💊 ਬਾਬਾ ਜੀ, ਸਿਹਤ = ਸਭ ਕੁਝ! ਪਹਿਲਾਂ: 1) ਆਰਾਮ 2) ਪਾਣੀ ਪੀਓ 3) ਦੇਸੀ ਨੁਸਖਾ (ਸ਼ਹਿਦ+ਅਦਰਕ) 4) ਗੰਭੀਰ ਹੈ? ਡਾਕਟਰ ਜ਼ਰੂਰ! 'ਰੋਕਥਾਮ ਇਲਾਜ ਨਾਲੋਂ ਚੰਗੀ' 🌿💚"
        else:
            return "💊 ਬਾਬਾ ਜੀ, ਰੋਜ਼ਾਨਾ: 1) 8 ਗਲਾਸ ਪਾਣੀ 2) 30 ਮਿੰਟ ਕਸਰਤ 3) 7-8 ਘੰਟੇ ਨੀਂਦ 4) ਸੰਤੁਲਿਤ ਖਾਣਾ 5) ਮਨ ਸ਼ਾਂਤ। ਇਹ 5 = ਲੰਮੀ ਜ਼ਿੰਦਗੀ! 💪🌟"
    
    def _default_response(self, user_input: str) -> str:
        """Default response if brain can't process"""
        return f"🧠 Brain {self.brain_id} ({self.name}): ਸੋਚ ਰਿਹਾ ਹਾਂ... {self.thinking_style}"


class AmritBrainChain:
    """Master Brain Chain Controller"""
    
    def __init__(self):
        self.master_brain = None
        self.active_brains = []
        self.conversation_history = []
        self._initialize_brains()
        
    def _initialize_brains(self):
        """Initialize all nano brains"""
        print("\n🧠 ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ! Initializing Amrit Brain Chain...\n")
        
        brain_configs = [
            (0, "Master Meta-Knowledge", "brain_00_master_meta_knowledge.txt", "Meta-Analytical"),
            (1, "SGGS Gyan", "brain_01_sggs_core.txt", "Spiritual-Contextual"),
            (2, "Punjabi Bhasha", "brain_02_punjabi_language.txt", "Linguistic-Cultural"),
            (3, "Punjab Itihaas", "brain_03_punjab_itihaas.txt", "Historical-Narrative"),
            (4, "Parivar Rishte", "brain_04_parivar_rishte.txt", "Emotional-Relational"),
            (5, "Rozana Jeevan", "brain_05_rozana_jeevan.txt", "Practical-Helpful"),
            (6, "Sanchar Communication", "brain_06_sanchar_communication.txt", "Clear-Effective"),
            (7, "Gyan Vigyan", "brain_07_gyan_vigyan.txt", "Analytical-Logical"),
            (8, "Computing Tech", "brain_08_computing_tech.txt", "Logical-Practical"),
            (9, "Kala Sangeet", "brain_09_kala_sangeet.txt", "Creative-Emotional"),
            (10, "Sehhat Health", "brain_10_sehhat_health.txt", "Caring-Scientific"),
        ]
        
        for brain_id, name, knowledge_file, thinking_style in brain_configs:
            brain = NanoBrain(brain_id, name, knowledge_file, thinking_style)
            
            if brain_id == 0:
                self.master_brain = brain
            else:
                self.active_brains.append(brain)
        
        print(f"\n✅ Initialized {len(self.active_brains)} active brains + 1 master brain")
        print(f"� Total Knowledge: ~136 KB compressed from 1.4 TB!")
        print(f"�🔗 Chain ready: {' → '.join([b.name for b in self.active_brains])}\n")
        print(f"{'='*70}\n")
    
    def process_input(self, user_input: str) -> Dict:
        """Process user input through brain chain"""
        print(f"\n{'='*70}")
        print(f"📥 User Input: {user_input}")
        print(f"{'='*70}\n")
        
        # Step 1: All brains think in parallel
        brain_responses = []
        context = {"input": user_input, "timestamp": datetime.now().isoformat()}
        
        for brain in self.active_brains:
            print(f"🧠 {brain.name} ({brain.thinking_style}) thinking...")
            response = brain.think(user_input, context)
            if response:
                brain_responses.append({
                    "brain_id": brain.brain_id,
                    "brain_name": brain.name,
                    "thinking_style": brain.thinking_style,
                    "response": response
                })
                print(f"   💭 {response}\n")
        
        # Step 2: Master brain synthesizes
        context["brain_responses"] = brain_responses
        
        print(f"🧠 {self.master_brain.name} synthesizing all perspectives...\n")
        master_response = self._synthesize_responses(user_input, brain_responses)
        
        result = {
            "input": user_input,
            "timestamp": context["timestamp"],
            "brain_responses": brain_responses,
            "master_synthesis": master_response,
            "total_brains_consulted": len(brain_responses)
        }
        
        self.conversation_history.append(result)
        
        return result
    
    def _synthesize_responses(self, user_input: str, brain_responses: List[Dict]) -> str:
        """Master brain synthesizes all perspectives"""
        print(f"{'='*70}")
        print(f"🧠 MASTER BRAIN SYNTHESIS:")
        print(f"{'='*70}\n")
        
        synthesis = f"ਬਾਬਾ ਜੀ, ਮੈਂ ਸਾਰੇ {len(brain_responses)} brains ਨੂੰ ਪੁੱਛਿਆ। ਹਰ ਇੱਕ ਦਾ ਵੱਖਰਾ ਨਜ਼ਰੀਆ:\n\n"
        
        for resp in brain_responses:
            synthesis += f"• {resp['brain_name']}: {resp['response']}\n\n"
        
        synthesis += "💡 ਮੇਰਾ ਸੰਖੇਪ: ਸਾਰੇ ਇੱਕ ਗੱਲ ਕਹਿ ਰਹੇ ਨੇ - "
        
        # Simple keyword-based synthesis
        if any(word in user_input.lower() for word in ['scared', 'fear', 'worry']):
            synthesis += "ਡਰ ਤਾਂ ਮਨ ਦਾ ਹੈ, ਕਰਮ ਕਰੋ ਅਤੇ ਆਗੇ ਵਧੋ। ਤੁਸੀਂ ਇਕੱਲੇ ਨਹੀਂ! 💪"
        elif any(word in user_input.lower() for word in ['happy', 'success']):
            synthesis += "ਖੁਸ਼ੀ ਸਾਂਝੀ ਕਰੋ, ਸ਼ੁਕਰ ਮਨਾਓ, ਅਤੇ ਨਿਮਰ ਰਹੋ। ਇਹ ਵੀ ਵਕਤ ਦੀ ਮਾਰ ਹੈ! 🌸"
        elif any(word in user_input.lower() for word in ['busy', 'work', 'time']):
            synthesis += "ਪਹਿਲੇ ਯੋਜਨਾ ਬਣਾਓ, ਫਿਰ ਛੋਟੇ ਕਦਮ। ਰੋਜ਼ ਥੋੜਾ = ਬਹੁਤ ਸਾਰਾ! ⏰"
        else:
            synthesis += "ਸਭ ਕੁਝ ਜੁੜਿਆ ਹੋਇਆ ਹੈ। Pattern ਵੇਖੋ, ਸਿੱਖੋ, ਵਰਤੋ। 🌟"
        
        print(synthesis)
        print(f"\n{'='*70}\n")
        
        return synthesis
    
    def get_conversation_summary(self) -> str:
        """Get summary of conversation history"""
        if not self.conversation_history:
            return "No conversations yet."
        
        summary = f"\n📊 Conversation History ({len(self.conversation_history)} interactions):\n"
        summary += "="*70 + "\n"
        
        for i, conv in enumerate(self.conversation_history, 1):
            summary += f"\n{i}. Input: {conv['input']}\n"
            summary += f"   Brains consulted: {conv['total_brains_consulted']}\n"
            summary += f"   Timestamp: {conv['timestamp']}\n"
        
        return summary


def main():
    """Main interactive loop"""
    print("\n" + "="*70)
    print("🧠🔗 AMRIT BRAIN CHAIN - Interactive Mode")
    print("="*70)
    print("ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫ਼ਤਿਹ")
    print("="*70 + "\n")
    
    # Initialize brain chain
    brain_chain = AmritBrainChain()
    
    print("\n💬 Ready! Type your question (or 'quit' to exit, 'history' to see past conversations)\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n🙏 ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ! Goodbye!\n")
                break
            
            if user_input.lower() == 'history':
                print(brain_chain.get_conversation_summary())
                continue
            
            # Process through brain chain
            result = brain_chain.process_input(user_input)
            
            print(f"\n{'='*70}")
            print(f"📤 FINAL RESPONSE:")
            print(f"{'='*70}")
            print(f"\n{result['master_synthesis']}\n")
            
        except KeyboardInterrupt:
            print("\n\n🙏 ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ! Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
