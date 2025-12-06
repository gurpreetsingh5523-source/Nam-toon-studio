#!/usr/bin/env python3
"""
🤖 RAHBAR AI DEVELOPER - VIDEO QUALITY CHECKER
Checks if video matches script, dialogues, story, and emotions

Analysis:
- Dialogue accuracy
- Story flow
- Emotional consistency
- Character expressions
- Gurbani context
- Technical quality
"""

import cv2
import json
from pathlib import Path
from datetime import datetime

class RahbarVideoAnalyzer:
    """🤖 Rahbar AI - Video Quality Analysis"""
    
    def __init__(self):
        self.name = "Rahbar AI Developer"
        self.analysis = {
            'dialogue_accuracy': 0,
            'story_flow': 0,
            'emotional_consistency': 0,
            'technical_quality': 0,
            'gurbani_context': 0,
            'overall_score': 0,
            'issues': [],
            'suggestions': []
        }
    
    def analyze_video(self, video_file, script_file=None):
        """Analyze video against script"""
        
        print("🤖 RAHBAR AI DEVELOPER - VIDEO ANALYSIS")
        print("="*70)
        print(f"📹 Video: {video_file}")
        
        if not Path(video_file).exists():
            print(f"❌ Video file not found: {video_file}")
            return None
        
        # Load video
        cap = cv2.VideoCapture(video_file)
        if not cap.isOpened():
            print(f"❌ Cannot open video: {video_file}")
            return None
        
        # Video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = frame_count / fps if fps > 0 else 0
        
        print(f"\n📊 Technical Specs:")
        print(f"   Resolution: {width}x{height}")
        print(f"   FPS: {fps}")
        print(f"   Frames: {frame_count}")
        print(f"   Duration: {duration:.1f}s")
        
        # Load script if available
        script = None
        if script_file and Path(script_file).exists():
            with open(script_file, 'r', encoding='utf-8') as f:
                script = json.load(f)
            print(f"📝 Script loaded: {script_file}")
        else:
            # Try to find matching script
            script_files = list(Path('.').glob('amrit_kaur_script_*.json'))
            if script_files:
                script_file = sorted(script_files)[-1]  # Most recent
                with open(script_file, 'r', encoding='utf-8') as f:
                    script = json.load(f)
                print(f"📝 Script auto-loaded: {script_file}")
        
        cap.release()
        
        # Analyze content
        print("\n🔍 Analyzing Content...")
        self.analyze_technical_quality(width, height, fps, frame_count, duration)
        
        if script:
            self.analyze_dialogue_story(script, duration)
            self.analyze_emotional_flow(script)
            self.analyze_gurbani_context(script)
        else:
            print("⚠️  No script found - limited analysis")
            self.analysis['suggestions'].append("Add script file for detailed analysis")
        
        # Calculate overall score
        self.calculate_overall_score()
        
        # Generate report
        self.generate_report(video_file, script)
        
        return self.analysis
    
    def analyze_technical_quality(self, width, height, fps, frames, duration):
        """Analyze technical aspects"""
        score = 10
        issues = []
        
        # Resolution check
        if width >= 1920 and height >= 1080:
            score += 20
        elif width >= 1280 and height >= 720:
            score += 15
            issues.append("Resolution could be higher (recommended: 1920x1080)")
        else:
            score += 5
            issues.append("Low resolution - upgrade to at least 1280x720")
        
        # FPS check
        if fps >= 30:
            score += 20
        elif fps >= 24:
            score += 15
            issues.append("FPS below 30 - consider 30 FPS for smoother playback")
        else:
            score += 5
            issues.append("Low FPS - minimum 24 FPS recommended")
        
        # Duration check
        if 20 <= duration <= 180:  # 20s to 3 minutes
            score += 10
        elif duration < 20:
            score += 5
            issues.append("Video is short - consider longer content for engagement")
        else:
            score += 8
        
        self.analysis['technical_quality'] = score
        self.analysis['issues'].extend(issues)
        
        print(f"   ✅ Technical Quality: {score}/50")
    
    def analyze_dialogue_story(self, script, duration):
        """Analyze dialogue and story flow"""
        score = 10
        issues = []
        suggestions = []
        
        conversation = script.get('conversation', [])
        expected_turns = len(conversation)
        
        print(f"\n📖 Story Analysis:")
        print(f"   Conversation turns: {expected_turns}")
        
        # Check if duration matches content
        expected_duration = expected_turns * 3  # 3 seconds per turn
        actual_duration = duration
        
        if abs(expected_duration - actual_duration) <= 5:
            score += 15
            print(f"   ✅ Duration matches content ({actual_duration:.1f}s)")
        else:
            score += 8
            issues.append(f"Duration mismatch: expected ~{expected_duration}s, got {actual_duration:.1f}s")
            print(f"   ⚠️  Duration: expected ~{expected_duration}s, got {actual_duration:.1f}s")
        
        # Check dialogue flow
        speakers = [turn['speaker'] for turn in conversation]
        has_both_speakers = 'Amrit Kaur' in speakers and 'User' in speakers
        
        if has_both_speakers:
            score += 15
            print(f"   ✅ Both characters present in dialogue")
        else:
            score += 5
            issues.append("Missing character dialogue - both Amrit Kaur and User should speak")
        
        # Check for story content
        story = script.get('story')
        if story:
            score += 10
            print(f"   ✅ Story included: {story.get('title', 'Unknown')}")
            suggestions.append("Consider showing story scenes visually")
        else:
            score += 5
            suggestions.append("Add story element for deeper engagement")
        
        self.analysis['dialogue_accuracy'] = score
        self.analysis['issues'].extend(issues)
        self.analysis['suggestions'].extend(suggestions)
        
        print(f"   📊 Dialogue & Story Score: {score}/50")
    
    def analyze_emotional_flow(self, script):
        """Analyze emotional consistency"""
        score = 10
        issues = []
        suggestions = []
        
        conversation = script.get('conversation', [])
        emotions = [turn.get('emotion', 'neutral') for turn in conversation]
        
        print(f"\n💭 Emotional Analysis:")
        print(f"   Emotions detected: {len(set(emotions))} unique")
        
        # Check for emotional variety
        unique_emotions = set(emotions)
        if len(unique_emotions) >= 4:
            score += 15
            print(f"   ✅ Good emotional variety: {', '.join(unique_emotions)}")
        elif len(unique_emotions) >= 2:
            score += 10
            suggestions.append("Add more emotional variety for engagement")
        else:
            score += 5
            issues.append("Limited emotional range - add more expressions")
        
        # Check for emotional progression (sad → comforting → hopeful)
        emotion_list = list(emotions)
        has_progression = False
        
        if 'sad' in emotion_list and 'comforting' in emotion_list:
            score += 10
            has_progression = True
            print(f"   ✅ Emotional progression: sad → comforting")
        
        if 'hopeful' in emotion_list or 'storytelling' in emotion_list:
            score += 5
            has_progression = True
            print(f"   ✅ Positive resolution detected")
        
        if not has_progression:
            suggestions.append("Add emotional progression (problem → support → resolution)")
        
        self.analysis['emotional_consistency'] = score
        self.analysis['issues'].extend(issues)
        self.analysis['suggestions'].extend(suggestions)
        
        print(f"   📊 Emotional Flow Score: {score}/40")
    
    def analyze_gurbani_context(self, script):
        """Analyze Gurbani wisdom integration"""
        score = 10
        issues = []
        suggestions = []
        
        print(f"\n🙏 Gurbani Context Analysis:")
        
        conversation = script.get('conversation', [])
        all_text = ' '.join([turn.get('text', '') for turn in conversation])
        
        # Check for Gurbani elements
        gurbani_elements = {
            'ੴ': 'Ik Onkar',
            'ਅਕਾਲ': 'Akal/Timeless',
            'ਵਾਹਿਗੁਰੂ': 'Waheguru',
            'ਗੁਰੂ': 'Guru',
            'ਸ੍ਰੀ ਅਕਾਲ': 'Sat Sri Akal',
            'ਖਾਲਸਾ': 'Khalsa',
            'ਸਤਿ': 'Truth/Sat',
            'ਪ੍ਰਭੂ': 'God/Prabhu',
            'ਸਿਮਰਨ': 'Remembrance'
        }
        
        found_elements = []
        for element, name in gurbani_elements.items():
            if element in all_text:
                found_elements.append(name)
        
        if len(found_elements) >= 3:
            score += 20
            print(f"   ✅ Rich Gurbani context: {len(found_elements)} elements")
            print(f"      Found: {', '.join(found_elements)}")
        elif len(found_elements) >= 1:
            score += 10
            print(f"   ✓ Some Gurbani elements: {', '.join(found_elements)}")
            suggestions.append("Add more Gurbani references for authenticity")
        else:
            score += 0
            issues.append("No Gurbani elements detected - add spiritual context")
        
        # Check for story with lesson
        story = script.get('story')
        if story and 'lesson' in story:
            score += 10
            lesson = story['lesson']
            print(f"   ✅ Moral lesson included")
            print(f"      {lesson}")
        else:
            suggestions.append("Add moral/spiritual lesson from Gurbani teachings")
        
        self.analysis['gurbani_context'] = score
        self.analysis['issues'].extend(issues)
        self.analysis['suggestions'].extend(suggestions)
        
        print(f"   📊 Gurbani Context Score: {score}/40")
    
    def calculate_overall_score(self):
        """Calculate overall quality score"""
        total = (
            self.analysis['technical_quality'] +
            self.analysis['dialogue_accuracy'] +
            self.analysis['emotional_consistency'] +
            self.analysis['gurbani_context']
        )
        
        # Convert to 10 scale
        self.analysis['overall_score'] = (total / 180) * 10
    
    def generate_report(self, video_file, script):
        """Generate detailed analysis report"""
        
        print("\n" + "="*70)
        print("📊 RAHBAR AI ANALYSIS REPORT")
        print("="*70)
        
        score = self.analysis['overall_score']
        
        # Overall rating
        if score >= 8.5:
            rating = "🌟 EXCELLENT"
            message = "Outstanding work! Video matches story perfectly!"
        elif score >= 7.0:
            rating = "✅ GOOD"
            message = "Video is good, minor improvements suggested"
        elif score >= 5.0:
            rating = "⚠️  NEEDS IMPROVEMENT"
            message = "Video needs work to match intended quality"
        else:
            rating = "❌ POOR"
            message = "Significant issues - rebuild recommended"
        
        print(f"\n{rating}")
        print(f"Overall Score: {score:.1f}/10")
        print(f"{message}")
        
        print(f"\n📊 Category Scores:")
        print(f"   Technical Quality: {self.analysis['technical_quality']}/50")
        print(f"   Dialogue & Story: {self.analysis['dialogue_accuracy']}/50")
        print(f"   Emotional Flow: {self.analysis['emotional_consistency']}/40")
        print(f"   Gurbani Context: {self.analysis['gurbani_context']}/40")
        
        if self.analysis['issues']:
            print(f"\n❌ Issues Found ({len(self.analysis['issues'])}):")
            for i, issue in enumerate(self.analysis['issues'], 1):
                print(f"   {i}. {issue}")
        
        if self.analysis['suggestions']:
            print(f"\n💡 Suggestions ({len(self.analysis['suggestions'])}):")
            for i, suggestion in enumerate(self.analysis['suggestions'], 1):
                print(f"   {i}. {suggestion}")
        
        # Story match analysis
        if script:
            print(f"\n📖 Story Match Analysis:")
            conversation = script.get('conversation', [])
            print(f"   Expected dialogue turns: {len(conversation)}")
            print(f"   Video should show:")
            for i, turn in enumerate(conversation[:3], 1):
                speaker = turn['speaker']
                text = turn['text'][:50] + "..." if len(turn['text']) > 50 else turn['text']
                emotion = turn.get('emotion', 'neutral')
                print(f"   {i}. {speaker} ({emotion}): {text}")
            if len(conversation) > 3:
                print(f"   ... and {len(conversation) - 3} more turns")
        
        print("\n" + "="*70)
        print("🤖 Rahbar AI Developer Analysis Complete")
        print("="*70)
        
        # Save report
        report_file = f"RAHBAR_VIDEO_ANALYSIS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        script_filename = script.get('title', 'Unknown') if script else None
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                'video_file': video_file,
                'script_analyzed': script_filename,
                'timestamp': datetime.now().isoformat(),
                'analysis': self.analysis
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Report saved: {report_file}")
        
        return self.analysis

# Run analysis
if __name__ == "__main__":
    import sys
    
    # Find latest Amrit Kaur video
    video_files = list(Path('.').glob('AMRIT_KAUR_*.mp4'))
    
    if not video_files:
        print("❌ No Amrit Kaur videos found")
        sys.exit(1)
    
    # Get most recent video
    latest_video = sorted(video_files, key=lambda x: x.stat().st_mtime)[-1]
    
    print(f"🎬 Analyzing latest video: {latest_video}")
    print()
    
    analyzer = RahbarVideoAnalyzer()
    result = analyzer.analyze_video(str(latest_video))
    
    if result:
        score = result['overall_score']
        print(f"\n🎯 Final Verdict: {score:.1f}/10")
        
        if score >= 7.0:
            print("✅ Video matches dialogues and story well!")
        else:
            print("⚠️  Video needs improvement to match script properly")
