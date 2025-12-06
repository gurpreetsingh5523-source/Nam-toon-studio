#!/usr/bin/env python3
"""
📡 BRAIN COMMUNICATION PROTOCOL
Enables real-time brain-to-brain communication with love
"""

from typing import Dict, Any, List
from datetime import datetime


class BrainMessage:
    """Message between brains"""
    
    def __init__(self, sender: str, recipient: str, content: Any, msg_type: str = "info"):
        self.sender = sender
        self.recipient = recipient
        self.content = content
        self.msg_type = msg_type
        self.timestamp = datetime.now().isoformat()


class BrainCommunicationProtocol:
    """Protocol for brain-to-brain communication"""
    
    def __init__(self):
        self.message_queue = []
        self.registered_brains = {}
        print("📡 COMMUNICATION PROTOCOL READY!")
    
    def register_brain(self, brain_name: str, brain_instance: Any):
        """Register a brain for communication"""
        self.registered_brains[brain_name] = brain_instance
        print(f"   ✅ Registered: {brain_name}")
    
    def send_message(self, sender: str, recipient: str, content: Any):
        """Send message between brains"""
        msg = BrainMessage(sender, recipient, content)
        self.message_queue.append(msg)
        print(f"   📨 {sender} → {recipient}")
    
    def broadcast(self, sender: str, content: Any):
        """Broadcast to all brains"""
        for brain_name in self.registered_brains:
            if brain_name != sender:
                self.send_message(sender, brain_name, content)


if __name__ == "__main__":
    protocol = BrainCommunicationProtocol()
    protocol.register_brain("Brain1", None)
    protocol.register_brain("Brain2", None)
    protocol.send_message("Brain1", "Brain2", "Hello with love!")
    print("\n✅ Communication test complete!")
