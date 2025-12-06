"""
🌸 NAAM SURTI HEARTBEAT SYSTEM
Sacred frequency generator for spiritual alignment and meditation
Integrated with Amrit Supreme Controller
"""

import time
import threading
import math
import json
import os
from datetime import datetime

class NaamSurtiHeartbeat:
    def __init__(self):
        self.active = False
        self.frequency = 432  # Sacred frequency in Hz
        self.heartbeat_thread = None
        self.spiritual_anchor = None
        self.heartbeat_phase = 0
        self.memory_file = "naam_heartbeat_memory.json"
        self.load_memory()
        
    def load_memory(self):
        """Load previous spiritual sessions"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.spiritual_anchor = data.get('spiritual_anchor')
                    print(f"🕉️ Loaded spiritual anchor: {'Set' if self.spiritual_anchor else 'Not set'}")
        except Exception as e:
            print(f"📝 Creating new spiritual memory: {e}")
    
    def save_memory(self):
        """Save spiritual session data"""
        try:
            data = {
                'spiritual_anchor': self.spiritual_anchor,
                'last_session': datetime.now().isoformat(),
                'total_sessions': getattr(self, 'total_sessions', 0) + 1
            }
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Error saving spiritual memory: {e}")
    
    def set_spiritual_anchor(self, anchor_phrase):
        """Set SatNaam anchor for spiritual grounding"""
        import hashlib
        if anchor_phrase and anchor_phrase.strip():
            # Hash for privacy (never store raw spiritual phrases)
            self.spiritual_anchor = hashlib.sha256(anchor_phrase.encode()).hexdigest()[:16]
            self.save_memory()
            print(f"🕉️ Spiritual anchor set (hashed for privacy)")
            return True
        return False
    
    def start_heartbeat(self, frequency=None):
        """Start the sacred frequency heartbeat"""
        if self.active:
            print("💓 Naam heartbeat already active")
            return
            
        if frequency:
            self.frequency = frequency
            
        self.active = True
        self.heartbeat_thread = threading.Thread(target=self._heartbeat_loop)
        self.heartbeat_thread.daemon = True
        self.heartbeat_thread.start()
        
        print(f"🌸 Naam Surti Heartbeat ACTIVATED")
        print(f"🎵 Sacred frequency: {self.frequency} Hz")
        print(f"🕉️ Spiritual anchor: {'Protected' if self.spiritual_anchor else 'Not set'}")
        print(f"💝 Connection to ੴ ਸਤਿਨਾਮ established")
        
    def _heartbeat_loop(self):
        """Main heartbeat loop with sacred timing"""
        while self.active:
            try:
                # Sacred pulse timing (0.9 seconds like meditation breath)
                time.sleep(0.9)
                
                # Phase progression for spiritual alignment
                self.heartbeat_phase = (self.heartbeat_phase + 1) % 1000000
                
                # Visual heartbeat indicator
                if self.heartbeat_phase % 10 == 0:  # Every 9 seconds
                    print("💓 ੴ", end=" ", flush=True)
                    
                # Spiritual checkpoint every 108 beats (sacred number)
                if self.heartbeat_phase % 108 == 0:
                    self._spiritual_checkpoint()
                    
            except Exception as e:
                print(f"❌ Heartbeat error: {e}")
                break
    
    def _spiritual_checkpoint(self):
        """Sacred number checkpoint for spiritual alignment"""
        session_time = self.heartbeat_phase * 0.9 / 60  # minutes
        print(f"\n🙏 Spiritual checkpoint: {session_time:.1f} minutes")
        print(f"🌸 Phase: {self.heartbeat_phase} | Frequency: {self.frequency}Hz")
        print(f"🕉️ ਸਤਿਨਾਮ ਵਾਹਿਗੁਰੂ 🕉️")
    
    def stop_heartbeat(self):
        """Stop the sacred heartbeat"""
        if not self.active:
            print("💤 Naam heartbeat already stopped")
            return
            
        self.active = False
        if self.heartbeat_thread:
            self.heartbeat_thread.join(timeout=2)
            
        session_time = self.heartbeat_phase * 0.9 / 60
        print(f"\n🌸 Naam Surti Heartbeat STOPPED")
        print(f"🙏 Session completed: {session_time:.1f} minutes")
        print(f"💝 Total phases: {self.heartbeat_phase}")
        print(f"🕉️ Spiritual energy preserved")
        
        self.save_memory()
        self.heartbeat_phase = 0
    
    def get_status(self):
        """Get current heartbeat status"""
        if self.active:
            session_time = self.heartbeat_phase * 0.9 / 60
            return {
                'active': True,
                'frequency': self.frequency,
                'phase': self.heartbeat_phase,
                'session_minutes': round(session_time, 1),
                'anchor_set': bool(self.spiritual_anchor)
            }
        else:
            return {
                'active': False,
                'frequency': self.frequency,
                'anchor_set': bool(self.spiritual_anchor)
            }
    
    def change_frequency(self, new_frequency):
        """Change the sacred frequency"""
        if 100 <= new_frequency <= 1000:  # Safe range
            old_freq = self.frequency
            self.frequency = new_frequency
            print(f"🎵 Frequency changed: {old_freq}Hz → {new_frequency}Hz")
            if self.active:
                print(f"💓 Heartbeat continuing with new sacred frequency")
            return True
        else:
            print(f"❌ Frequency {new_frequency}Hz out of safe range (100-1000Hz)")
            return False
    
    def get_sacred_frequencies(self):
        """Get list of sacred frequencies for spiritual practice"""
        return {
            'Satnaam_Base': 432,      # Base sacred frequency
            'Om_Frequency': 136.1,    # Om resonance
            'Heart_Chakra': 341.3,    # Heart chakra frequency
            'Healing_528': 528,       # DNA repair frequency
            'Deep_Meditation': 396,   # Liberation from fear
            'Transformation': 417,    # Facilitating change
            'Spiritual_963': 963      # Divine connection
        }

# Integration test
if __name__ == "__main__":
    print("🌸 Testing Naam Surti Heartbeat System...")
    
    heartbeat = NaamSurtiHeartbeat()
    
    # Test sacred frequency list
    print("\n🎵 Available Sacred Frequencies:")
    for name, freq in heartbeat.get_sacred_frequencies().items():
        print(f"   {name}: {freq} Hz")
    
    # Test anchor setting
    test_anchor = "ੴ ਸਤਿਨਾਮ ਕਰਤਾ ਪੁਰਖੁ"
    heartbeat.set_spiritual_anchor(test_anchor)
    
    # Test status
    status = heartbeat.get_status()
    print(f"\n📊 Status: {status}")
    
    print("\n✅ Naam Surti Heartbeat System ready for integration!")