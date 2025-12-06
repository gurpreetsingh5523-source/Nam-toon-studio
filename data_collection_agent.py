#!/usr/bin/env python3
"""
🔗 DATA COLLECTION AGENT
Collects training data from user interactions
ਡਾਟਾ ਇਕੱਠਾ ਕਰਨ ਵਾਲਾ ਏਜੰਟ
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(__file__).parent.absolute()
sys.path.insert(0, str(WORKSPACE))

from integrated_smart_video_maker import IntegratedSmartVideoMaker


class DataCollectionAgent:
    """
    Agent to collect training data from users
    ਯੂਜ਼ਰਾਂ ਤੋਂ ਟ੍ਰੇਨਿੰਗ ਡਾਟਾ ਇਕੱਠਾ ਕਰਦਾ ਹੈ
    """
    
    def __init__(self, workspace=None):
        self.workspace = Path(workspace or WORKSPACE)
        self.video_maker = IntegratedSmartVideoMaker(self.workspace)
        self.data_dir = self.workspace / "training_data"
        self.data_dir.mkdir(exist_ok=True)
        
        self.collected_data_file = self.data_dir / "collected_training_data.json"
        self.collected_data = self._load_data()
        
        print("✅ Data Collection Agent initialized")
    
    def _load_data(self):
        """Load collected data"""
        if self.collected_data_file.exists():
            with open(self.collected_data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "collections": [],
            "total_samples": 0,
            "categories": {}
        }
    
    def _save_data(self):
        """Save collected data"""
        with open(self.collected_data_file, 'w', encoding='utf-8') as f:
            json.dump(self.collected_data, f, indent=2, ensure_ascii=False)
    
    def collect_punjabi_stories(self, num_stories=10):
        """
        Interactive collection of Punjabi stories
        ਪੰਜਾਬੀ ਕਹਾਣੀਆਂ ਇਕੱਠੀਆਂ ਕਰੋ
        """
        print("\n" + "="*70)
        print("📚 PUNJABI STORY COLLECTION")
        print("="*70)
        print(f"\nWe need {num_stories} Punjabi stories for training!")
        print("ਸਾਨੂੰ ਸਿਖਲਾਈ ਲਈ ਪੰਜਾਬੀ ਕਹਾਣੀਆਂ ਦੀ ਲੋੜ ਹੈ!")
        print("\nExamples:")
        print("- ਪਿੰਡ ਦੀ ਕਹਾਣੀ (Village story)")
        print("- ਗੁਰੂ ਦੀ ਸਿੱਖਿਆ (Guru's teaching)")
        print("- ਪਰਿਵਾਰ ਦੀ ਗੱਲ (Family story)")
        
        collection_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        stories = []
        
        for i in range(num_stories):
            print(f"\n{'='*70}")
            print(f"📝 Story {i+1}/{num_stories}")
            print(f"{'='*70}")
            
            try:
                # Get category
                print("\nCategory:")
                print("1. Village/ਪਿੰਡ  2. Family/ਪਰਿਵਾਰ  3. Guru/ਗੁਰੂ")
                print("4. History/ਇਤਿਹਾਸ  5. Other/ਹੋਰ")
                category_num = input("➤ Select (1-5): ").strip()
                
                categories = {
                    "1": "village", "2": "family", "3": "guru",
                    "4": "history", "5": "other"
                }
                category = categories.get(category_num, "other")
                
                # Get story
                print("\nEnter story (Punjabi/English, press Enter twice when done):")
                story_lines = []
                while True:
                    line = input()
                    if not line and story_lines:  # Empty line and we have content
                        break
                    if line:
                        story_lines.append(line)
                
                story_text = "\n".join(story_lines)
                
                if not story_text:
                    print("⏭️  Story skipped (empty)")
                    continue
                
                # Get quality expectations
                print("\nWhat should the video focus on?")
                print("1. Realistic characters  2. Beautiful background")
                print("3. Smooth animation  4. All of above")
                focus_num = input("➤ Select (1-4): ").strip()
                
                focus_map = {
                    "1": ["realistic_characters"],
                    "2": ["beautiful_background"],
                    "3": ["smooth_animation"],
                    "4": ["realistic_characters", "beautiful_background", "smooth_animation"]
                }
                focus = focus_map.get(focus_num, ["all"])
                
                # Save story data
                story_data = {
                    "id": f"story_{collection_id}_{i+1}",
                    "timestamp": datetime.now().isoformat(),
                    "category": category,
                    "text": story_text,
                    "quality_focus": focus,
                    "language": "punjabi" if any(c > '\u0a00' and c < '\u0a7f' for c in story_text) else "english"
                }
                
                stories.append(story_data)
                
                # Update category count
                if category not in self.collected_data['categories']:
                    self.collected_data['categories'][category] = 0
                self.collected_data['categories'][category] += 1
                
                print(f"✅ Story {i+1} collected!")
                
                # Ask if user wants to create video from this
                create = input("\nCreate video from this story? (y/n): ").strip().lower()
                if create == 'y':
                    output_path = self.data_dir / f"sample_{story_data['id']}.mp4"
                    self.video_maker.create_video(
                        text=story_text,
                        output_path=str(output_path),
                        add_voice=True,
                        add_music=True,
                        ask_feedback=True
                    )
                
            except KeyboardInterrupt:
                print("\n\n⏹️  Collection stopped by user")
                break
            except Exception as e:
                print(f"❌ Error collecting story: {e}")
        
        # Save collection
        if stories:
            collection = {
                "collection_id": collection_id,
                "timestamp": datetime.now().isoformat(),
                "stories": stories,
                "total": len(stories)
            }
            
            self.collected_data['collections'].append(collection)
            self.collected_data['total_samples'] += len(stories)
            self._save_data()
            
            print(f"\n✅ Collected {len(stories)} stories!")
            print(f"📁 Saved to: {self.collected_data_file}")
    
    def collect_feedback_patterns(self):
        """
        Collect common feedback patterns
        ਆਮ ਫੀਡਬੈਕ ਪੈਟਰਨ ਇਕੱਠੇ ਕਰੋ
        """
        print("\n" + "="*70)
        print("💬 FEEDBACK PATTERN COLLECTION")
        print("="*70)
        print("\nWhat feedback do users commonly give?")
        print("ਯੂਜ਼ਰ ਆਮ ਤੌਰ 'ਤੇ ਕੀ ਫੀਡਬੈਕ ਦਿੰਦੇ ਹਨ?")
        
        patterns = []
        
        print("\nCommon complaints (enter one per line, empty line to finish):")
        print("Example: 'Too cartoonish', 'Characters not realistic'")
        
        while True:
            complaint = input("➤ Complaint: ").strip()
            if not complaint:
                break
            patterns.append({
                "type": "negative",
                "text": complaint,
                "timestamp": datetime.now().isoformat()
            })
        
        print("\nCommon praises (enter one per line, empty line to finish):")
        print("Example: 'Voice is good', 'Animation is smooth'")
        
        while True:
            praise = input("➤ Praise: ").strip()
            if not praise:
                break
            patterns.append({
                "type": "positive",
                "text": praise,
                "timestamp": datetime.now().isoformat()
            })
        
        if patterns:
            # Save patterns
            patterns_file = self.data_dir / "feedback_patterns.json"
            with open(patterns_file, 'w', encoding='utf-8') as f:
                json.dump(patterns, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Collected {len(patterns)} feedback patterns!")
            print(f"📁 Saved to: {patterns_file}")
    
    def show_collected_data_stats(self):
        """Show statistics of collected data"""
        print("\n" + "="*70)
        print("📊 COLLECTED DATA STATISTICS")
        print("="*70)
        
        print(f"\n📈 OVERALL:")
        print(f"   Total collections: {len(self.collected_data['collections'])}")
        print(f"   Total samples: {self.collected_data['total_samples']}")
        
        if self.collected_data['categories']:
            print(f"\n📂 BY CATEGORY:")
            for category, count in self.collected_data['categories'].items():
                print(f"   {category}: {count} stories")
        
        # Show recent collections
        if self.collected_data['collections']:
            print(f"\n📅 RECENT COLLECTIONS:")
            for collection in self.collected_data['collections'][-3:]:
                print(f"   {collection['collection_id']}: {collection['total']} stories")
    
    def export_for_training(self):
        """
        Export collected data in training format
        ਟ੍ਰੇਨਿੰਗ ਫਾਰਮੈਟ ਵਿੱਚ ਐਕਸਪੋਰਟ ਕਰੋ
        """
        print("\n" + "="*70)
        print("💾 EXPORTING DATA FOR TRAINING")
        print("="*70)
        
        if not self.collected_data['collections']:
            print("❌ No data to export")
            return
        
        # Create training format
        training_data = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "total_samples": self.collected_data['total_samples'],
                "categories": self.collected_data['categories']
            },
            "samples": []
        }
        
        # Convert all stories to training format
        for collection in self.collected_data['collections']:
            for story in collection['stories']:
                training_sample = {
                    "input": story['text'],
                    "category": story['category'],
                    "quality_requirements": story['quality_focus'],
                    "expected_output": {
                        "video_type": "realistic",
                        "language": story['language'],
                        "style": "punjabi_cultural"
                    }
                }
                training_data['samples'].append(training_sample)
        
        # Save
        output_file = self.data_dir / "training_dataset.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Exported {len(training_data['samples'])} samples")
        print(f"📁 Saved to: {output_file}")
        print("\n💡 This file can be used to train AI models!")


def main():
    """Main function"""
    print("\n" + "="*70)
    print("🔗 DATA COLLECTION AGENT")
    print("   Collect training data for AI improvement")
    print("="*70)
    
    agent = DataCollectionAgent()
    
    print("\nWhat would you like to do?")
    print("1. Collect Punjabi stories")
    print("2. Collect feedback patterns")
    print("3. Show statistics")
    print("4. Export for training")
    print("5. Exit")
    
    while True:
        try:
            choice = input("\n➤ Select (1-5): ").strip()
            
            if choice == '1':
                num = input("How many stories? (default 10): ").strip()
                num = int(num) if num.isdigit() else 10
                agent.collect_punjabi_stories(num_stories=num)
            
            elif choice == '2':
                agent.collect_feedback_patterns()
            
            elif choice == '3':
                agent.show_collected_data_stats()
            
            elif choice == '4':
                agent.export_for_training()
            
            elif choice == '5':
                print("👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid choice")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == '__main__':
    main()
