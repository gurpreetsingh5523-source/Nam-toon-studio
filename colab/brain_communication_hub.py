#!/usr/bin/env python3
"""
🧠 BRAIN COMMUNICATION HUB 🧠
============================

Real-time communication system where ALL brains:
1. Share their plans BEFORE starting work
2. Coordinate WHO does WHAT
3. Check each other's work
4. Report problems to Master Brain
5. Work as ONE unified system

ਸਾਰੇ ਦਿਮਾਗ ਇੱਕ ਦੂਜੇ ਨਾਲ ਗੱਲਬਾਤ ਕਰਦੇ ਨੇ!
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class BrainMessage:
    """Message that brains send to each other"""
    
    def __init__(
        self,
        from_brain: str,
        to_brain: str,
        message_type: str,
        content: Dict[str, Any],
        priority: str = "normal"
    ):
        self.from_brain = from_brain
        self.to_brain = to_brain  # "all" for broadcast
        self.message_type = message_type
        self.content = content
        self.priority = priority
        self.timestamp = datetime.now().isoformat()
        self.id = f"{from_brain}_{int(time.time() * 1000)}"


class BrainCommunicationHub:
    """
    Central hub where all brains communicate in real-time.
    
    Message Types:
    - PLAN: "I'm planning to do X"
    - REQUEST: "Can you help me with Y?"
    - RESPONSE: "Here's the result of Y"
    - COMPLAINT: "This doesn't look right!"
    - APPROVAL: "Looks good to me!"
    - COORDINATION: "Let's divide the work"
    """
    
    def __init__(self, quiet: bool = False):
        self.message_log = []
        self.brain_status = {}
        self.active_collaborations = {}
        self.quiet = quiet
        
        # Communication channels
        self.channels = {
            "visual_audio": [],      # Visual <-> Audio coordination
            "audio_voice": [],        # Audio <-> Voice coordination
            "visual_creative": [],    # Visual <-> Creative coordination
            "all_brains": []         # Broadcast channel
        }
        
        if not self.quiet:
            print("\n🧠 BRAIN COMMUNICATION HUB INITIALIZED")
            print("=" * 70)
            print("All brains can now:")
            print("  ✅ Share plans before starting")
            print("  ✅ Request help from each other")
            print("  ✅ Complain about inconsistencies")
            print("  ✅ Approve each other's work")
            print("  ✅ Coordinate task division")
            print("=" * 70)
    
    def send_message(self, message: BrainMessage) -> None:
        """Send message to another brain"""
        self.message_log.append(message)
        
        # Add to appropriate channel
        if message.to_brain == "all":
            self.channels["all_brains"].append(message)
        else:
            channel_key = self._get_channel_key(message.from_brain, message.to_brain)
            if channel_key in self.channels:
                self.channels[channel_key].append(message)
        
        # Display message (unless quiet)
        if not self.quiet:
            self._display_message(message)
    
    def broadcast(self, from_brain: str, message_type: str, content: Dict[str, Any]) -> None:
        """Broadcast message to all brains"""
        message = BrainMessage(
            from_brain=from_brain,
            to_brain="all",
            message_type=message_type,
            content=content,
            priority="high" if message_type == "COMPLAINT" else "normal"
        )
        self.send_message(message)
    
    def get_messages_for_brain(self, brain_name: str, unread_only: bool = True) -> List[BrainMessage]:
        """Get messages for a specific brain"""
        messages = []
        for msg in self.message_log:
            if msg.to_brain == brain_name or msg.to_brain == "all":
                messages.append(msg)
        return messages
    
    def _get_channel_key(self, brain1: str, brain2: str) -> str:
        """Get channel key for two brains"""
        brains = sorted([brain1, brain2])
        return f"{brains[0]}_{brains[1]}"
    
    def _display_message(self, msg: BrainMessage) -> None:
        """Display message in console"""
        icons = {
            "PLAN": "📋",
            "REQUEST": "🙏",
            "RESPONSE": "💬",
            "COMPLAINT": "⚠️",
            "APPROVAL": "✅",
            "COORDINATION": "🤝"
        }
        
        icon = icons.get(msg.message_type, "📨")
        
        if msg.message_type == "COMPLAINT":
            print(f"\n{icon} {msg.from_brain} → {msg.to_brain}: ⚠️  COMPLAINT")
            print(f"   Issue: {msg.content.get('issue', 'Unknown')}")
            print(f"   Details: {msg.content.get('details', '')}")
        elif msg.message_type == "PLAN":
            print(f"\n{icon} {msg.from_brain} → {msg.to_brain}: Planning")
            print(f"   Task: {msg.content.get('task', 'Unknown')}")
        elif msg.message_type == "REQUEST":
            print(f"\n{icon} {msg.from_brain} → {msg.to_brain}: Requesting help")
            print(f"   Need: {msg.content.get('need', 'Unknown')}")
        elif msg.message_type == "COORDINATION":
            print(f"\n{icon} {msg.from_brain} → {msg.to_brain}: Coordinating")
            print(f"   Plan: {msg.content.get('plan', 'Unknown')}")
        else:
            print(f"\n{icon} {msg.from_brain} → {msg.to_brain}: {msg.message_type}")
    
    def check_consistency(
        self,
        scene_data: Dict[str, Any],
        brain_outputs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Check if all brain outputs are consistent with each other.
        Each brain can complain about others!
        """
        
        if not self.quiet:
            print("\n" + "=" * 70)
            print("🔍 INTER-BRAIN CONSISTENCY CHECK")
            print("=" * 70)
        
        issues = []
        approvals = []
        
        # Visual Brain checks Audio Brain
        if "visual" in brain_outputs and "audio" in brain_outputs:
            visual_emotion = brain_outputs["visual"].get("emotion", "")
            audio_emotion = brain_outputs["audio"].get("emotion", "")
            
            if visual_emotion != audio_emotion:
                complaint = BrainMessage(
                    from_brain="visual_brain",
                    to_brain="audio_brain",
                    message_type="COMPLAINT",
                    content={
                        "issue": "Emotion mismatch",
                        "details": f"I see {visual_emotion} but you're playing {audio_emotion} music!",
                        "my_value": visual_emotion,
                        "your_value": audio_emotion
                    },
                    priority="high"
                )
                self.send_message(complaint)
                issues.append(complaint.content)
            else:
                approval = BrainMessage(
                    from_brain="visual_brain",
                    to_brain="audio_brain",
                    message_type="APPROVAL",
                    content={"aspect": "emotion", "value": visual_emotion}
                )
                self.send_message(approval)
                approvals.append("Visual-Audio emotion match ✅")
        
        # Audio Brain checks Visual Brain
        if "audio" in brain_outputs and "visual" in brain_outputs:
            audio_volume = brain_outputs["audio"].get("music_volume", 0.5)
            
            if audio_volume > 0.7:
                complaint = BrainMessage(
                    from_brain="audio_brain",
                    to_brain="visual_brain",
                    message_type="COMPLAINT",
                    content={
                        "issue": "Music too loud",
                        "details": f"My music at {audio_volume} might overpower your visuals!",
                        "suggestion": "Should I reduce to 0.5?"
                    }
                )
                self.send_message(complaint)
                issues.append(complaint.content)
        
        # Voice Brain checks Character consistency
        if "voice" in brain_outputs and "visual" in brain_outputs:
            voice_character = brain_outputs["voice"].get("character", "")
            visual_character = brain_outputs["visual"].get("character", "")
            
            if voice_character != visual_character:
                complaint = BrainMessage(
                    from_brain="voice_brain",
                    to_brain="visual_brain",
                    message_type="COMPLAINT",
                    content={
                        "issue": "Character mismatch",
                        "details": f"I'm voicing {voice_character} but you're showing {visual_character}!",
                        "my_value": voice_character,
                        "your_value": visual_character
                    },
                    priority="critical"
                )
                self.send_message(complaint)
                issues.append(complaint.content)
        
        # Creative Brain checks timing
        if "creative" in brain_outputs:
            dialogue_length = brain_outputs.get("voice", {}).get("duration", 3.0)
            visual_duration = brain_outputs.get("visual", {}).get("duration", 3.0)
            
            if abs(dialogue_length - visual_duration) > 0.5:
                complaint = BrainMessage(
                    from_brain="creative_brain",
                    to_brain="all",
                    message_type="COMPLAINT",
                    content={
                        "issue": "Timing mismatch",
                        "details": f"Voice is {dialogue_length}s but visual is {visual_duration}s!",
                        "suggestion": "Need to sync durations"
                    }
                )
                self.send_message(complaint)
                issues.append(complaint.content)
        
        # Summary
        if not self.quiet:
            print("\n" + "=" * 70)
            if issues:
                print(f"⚠️  Found {len(issues)} consistency issues:")
                for i, issue in enumerate(issues, 1):
                    print(f"   {i}. {issue.get('issue', 'Unknown')}")
            else:
                print("✅ All brains are in perfect harmony!")
            
            if approvals:
                print(f"\n✅ {len(approvals)} approvals:")
                for approval in approvals:
                    print(f"   • {approval}")
            
            print("=" * 70)
        
        return {
            "issues": issues,
            "approvals": approvals,
            "consistent": len(issues) == 0,
            "score": 1.0 - (len(issues) / max(len(brain_outputs), 1))
        }
    
    def coordinate_work_division(
        self,
        scene_data: Dict[str, Any]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Brains discuss and divide work BEFORE starting.
        """
        
        if not self.quiet:
            print("\n" + "=" * 70)
            print("🤝 BRAIN WORK COORDINATION SESSION")
            print("=" * 70)
        
        work_plan = {}
        
        # Visual Brain announces its plan
        visual_plan = {
            "task": "Generate scene colors and composition",
            "emotion": scene_data.get("emotion", "neutral"),
            "duration": 3.0,
            "needs_from_others": ["audio emotion", "character info"]
        }
        
        self.broadcast(
            "visual_brain",
            "PLAN",
            visual_plan
        )
        work_plan["visual"] = visual_plan
        
        # Audio Brain responds with its plan
        audio_plan = {
            "task": "Select music and ambient sounds",
            "emotion": scene_data.get("emotion", "neutral"),
            "duration": 3.0,
            "needs_from_others": ["scene location", "time of day"]
        }
        
        self.broadcast(
            "audio_brain",
            "PLAN",
            audio_plan
        )
        work_plan["audio"] = audio_plan
        
        # Voice Brain coordinates with both
        voice_plan = {
            "task": "Synthesize dialogue with Punjabi accent",
            "character": scene_data.get("characters", ["Narrator"])[0],
            "accent": scene_data.get("punjabi_accent", "Majhi"),
            "needs_from_others": ["scene duration", "background music volume"]
        }
        
        coordination_msg = BrainMessage(
            from_brain="voice_brain",
            to_brain="all",
            message_type="COORDINATION",
            content={
                "plan": "I'll wait for audio to set volume before generating voice",
                "reason": "Voice must be louder than music",
                "my_plan": voice_plan
            }
        )
        self.send_message(coordination_msg)
        work_plan["voice"] = voice_plan
        
        # Creative Brain coordinates timing
        creative_plan = {
            "task": "Coordinate timing and transitions",
            "will_ensure": [
                "All elements same duration",
                "Smooth transitions",
                "Proper pacing"
            ]
        }
        
        self.broadcast(
            "creative_brain",
            "COORDINATION",
            creative_plan
        )
        work_plan["creative"] = creative_plan
        
        print("\n✅ Work division agreed by all brains!")
        print("=" * 70)
        
        return work_plan
    
    def report_to_master(
        self,
        brain_name: str,
        status: str,
        details: Dict[str, Any]
    ) -> None:
        """Brain reports status to Master Brain"""
        
        report = BrainMessage(
            from_brain=brain_name,
            to_brain="master_brain",
            message_type="RESPONSE" if status == "complete" else "COMPLAINT",
            content={
                "status": status,
                "details": details,
                "timestamp": datetime.now().isoformat()
            }
        )
        
        self.send_message(report)
    
    def get_communication_report(self) -> str:
        """Get summary of all inter-brain communications"""
        
        report = []
        report.append("\n" + "=" * 70)
        report.append("📊 INTER-BRAIN COMMUNICATION REPORT")
        report.append("=" * 70)
        
        # Count message types
        msg_counts = {}
        for msg in self.message_log:
            msg_type = msg.message_type
            msg_counts[msg_type] = msg_counts.get(msg_type, 0) + 1
        
        report.append("\nMessage Statistics:")
        for msg_type, count in sorted(msg_counts.items()):
            icon = {"PLAN": "📋", "REQUEST": "🙏", "COMPLAINT": "⚠️", 
                   "APPROVAL": "✅", "COORDINATION": "🤝"}.get(msg_type, "📨")
            report.append(f"  {icon} {msg_type}: {count} messages")
        
        # Count complaints by brain
        complaints = [m for m in self.message_log if m.message_type == "COMPLAINT"]
        if complaints:
            report.append(f"\n⚠️  Total Complaints: {len(complaints)}")
            complaint_by_brain = {}
            for c in complaints:
                complaint_by_brain[c.from_brain] = complaint_by_brain.get(c.from_brain, 0) + 1
            
            report.append("Complaints by brain:")
            for brain, count in sorted(complaint_by_brain.items()):
                report.append(f"  • {brain}: {count} complaints")
        
        # Count approvals
        approvals = [m for m in self.message_log if m.message_type == "APPROVAL"]
        if approvals:
            report.append(f"\n✅ Total Approvals: {len(approvals)}")
        
        report.append("=" * 70)
        
        return "\n".join(report)


# Example usage
if __name__ == "__main__":
    hub = BrainCommunicationHub()
    
    # Test scene
    scene_data = {
        "scene_id": 0,
        "emotion": "happy",
        "characters": ["Kulwant Singh"],
        "location": "Village",
        "punjabi_accent": "Majhi"
    }
    
    # Coordinate work
    work_plan = hub.coordinate_work_division(scene_data)
    
    # Simulate brain outputs
    brain_outputs = {
        "visual": {
            "emotion": "happy",
            "character": "Kulwant Singh",
            "duration": 3.0,
            "colors": ["#FFD700", "#FFA500"]
        },
        "audio": {
            "emotion": "happy",
            "music_volume": 0.45,
            "music": "punjabi_folk_happy.mp3"
        },
        "voice": {
            "character": "Kulwant Singh",
            "duration": 3.2,  # Slightly off!
            "accent": "Majhi"
        },
        "creative": {
            "duration": 3.0,
            "transition": "fade"
        }
    }
    
    # Check consistency
    result = hub.check_consistency(scene_data, brain_outputs)
    
    # Get report
    print(hub.get_communication_report())
