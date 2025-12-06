#!/usr/bin/env python3
"""
🚀 SIMPLE WORKING AGENT
ਸਿੱਧਾ ਕੰਮ ਕਰਨ ਵਾਲਾ agent - ਬਿਨਾਂ ਕਿਸੇ ਮਸਲੇ ਦੇ!
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(__file__).parent.absolute()
sys.path.insert(0, str(WORKSPACE))

print("🔍 Loading video maker...")
from realistic_movie_maker import RealisticMovieMaker

class SimpleWorkingAgent:
    """Agent that actually works!"""
    
    def __init__(self):
        self.workspace = WORKSPACE
        self.maker = RealisticMovieMaker()
        
        # Different scenarios - 25+ diverse stories
        self.scenarios = [
            # SPIRITUAL (5)
            {
                "name": "morning_prayer",
                "story": """[SCENE 1: Dawn]
ਸੂਰਜ ਚੜ੍ਹਿਆ, ਘਰ ਵਿੱਚ ਰੌਸ਼ਨੀ ਆਈ। ਜਪੁਜੀ ਸਾਹਿਬ ਪੜ੍ਹਨੀ ਸ਼ੁਰੂ ਕੀਤੀ।
Sun rose, light filled the home. Started reading Japji Sahib.

[SCENE 2: Inner Peace]
ਮਨ ਸ਼ਾਂਤ ਹੋਇਆ, ਅੰਦਰ ਚੈਨ ਆਇਆ। ਵਾਹਿਗੁਰੂ ਦਾ ਨਾਮ ਜਪਿਆ।
Mind became calm, found inner peace. Recited Waheguru's name.

[SCENE 3: Gratitude]
ਸ਼ੁਕਰਾਨਾ ਕੀਤਾ, ਦਿਨ ਚੰਗਾ ਹੋਵੇ ਦੀ ਪ੍ਰਾਰਥਨਾ।
Gave thanks, prayed for a good day."""
            },
            {
                "name": "gurdwara_darshan",
                "story": """[SCENE 1: Holy Place]
ਗੁਰਦੁਆਰੇ ਪਹੁੰਚੇ, ਮਾਥਾ ਟੇਕਿਆ। ਗੁਰੂ ਗ੍ਰੰਥ ਸਾਹਿਬ ਦਾ ਦਰਸ਼ਨ।
Reached Gurdwara, bowed down. Had darshan of Guru Granth Sahib.

[SCENE 2: Kirtan]
ਮਧੁਰ ਕੀਰਤਨ, ਰਾਗੀ ਗਾ ਰਹੇ। ਸੰਗਤ ਧਿਆਨ ਵਿੱਚ।
Sweet kirtan, ragis singing. Sangat in meditation."""
            },
            {
                "name": "langar_seva",
                "story": """[SCENE 1: Kitchen]
ਲੰਗਰ ਹਾਲ ਵਿੱਚ ਸੇਵਾ ਕਰ ਰਹੇ। ਰੋਟੀਆਂ ਪਕਾ ਰਹੇ, ਸਬਜ਼ੀ ਬਣਾ ਰਹੇ।
Doing seva in langar hall. Making rotis, cooking vegetables.

[SCENE 2: Serving]
ਸੰਗਤ ਨੂੰ ਲੰਗਰ ਛਕਾ ਰਹੇ। ਵੰਡ ਛਕਣਾ, ਸਾਂਝ ਕਰਨੀ।
Serving langar to sangat. Sharing food, creating community."""
            },
            {
                "name": "path_sahib",
                "story": """[SCENE 1: Reading]
ਘਰ ਵਿੱਚ ਅਖੰਡ ਪਾਠ ਚੱਲ ਰਿਹਾ। ਪਰਿਵਾਰ ਸੁਣ ਰਿਹਾ।
Akhand Path going on at home. Family listening.

[SCENE 2: Blessing]
ਭੋਗ ਪਾਈ, ਕੜਾਹ ਪ੍ਰਸ਼ਾਦ ਵੰਡਿਆ। ਸਾਰਿਆਂ ਨੂੰ ਚੜ੍ਹਦੀ ਕਲਾ ਮਿਲੇ।
Completed bhog, distributed karah prasad. May all receive high spirits."""
            },
            {
                "name": "simran_time",
                "story": """[SCENE 1: Meditation]
ਸਵੇਰੇ ਅੰਮ੍ਰਿਤ ਵੇਲੇ ਸਿਮਰਨ ਕੀਤਾ। ਵਾਹਿਗੁਰੂ, ਵਾਹਿਗੁਰੂ।
Morning amrit vela simran. Waheguru, Waheguru.

[SCENE 2: Connection]
ਰੱਬ ਨਾਲ ਜੁੜੇ, ਆਤਮਾ ਖੁਸ਼ ਹੋਈ। ਮਨ ਨਿਰਮਲ ਹੋਇਆ।
Connected with God, soul became happy. Mind became pure."""
            },
            
            # FAMILY LIFE (5)
            {
                "name": "family_dinner",
                "story": """[SCENE 1: Together]
ਸ਼ਾਮ ਨੂੰ ਸਾਰਾ ਪਰਿਵਾਰ ਇਕੱਠਾ। ਮਾਂ ਨੇ ਖਾਣਾ ਬਣਾਇਆ।
Evening, whole family together. Mother cooked food.

[SCENE 2: Stories]
ਖਾਣਾ ਖਾ ਕੇ ਕਹਾਣੀਆਂ ਸੁਣੀਆਂ। ਦਾਦੀ ਪੁਰਾਣੇ ਕਿੱਸੇ ਸੁਣਾ ਰਹੀ।
After eating, listened to stories. Grandmother telling old tales."""
            },
            {
                "name": "kids_playing",
                "story": """[SCENE 1: Garden]
ਬੱਚੇ ਬਾਹਰ ਖੇਡ ਰਹੇ, ਹੱਸਦੇ ਕੁੱਦਦੇ। ਲੁਕਾ-ਛੁਪੀ ਖੇਡੀ।
Kids playing outside, laughing jumping. Playing hide and seek.

[SCENE 2: Joy]
ਮਾਂ ਬਾਪ ਦੇਖ ਕੇ ਖੁਸ਼। ਬੱਚਿਆਂ ਦੀ ਖੁਸ਼ੀ ਹੀ ਸਭ ਕੁੱਝ।
Parents watching happily. Children's happiness is everything."""
            },
            {
                "name": "wedding_celebration",
                "story": """[SCENE 1: Preparation]
ਵਿਆਹ ਦੀ ਤਿਆਰੀ ਚੱਲ ਰਹੀ। ਘਰ ਸਜਾਇਆ, ਲਾਈਟਾਂ ਲਗਾਈਆਂ।
Wedding preparation going on. Decorated house, put up lights.

[SCENE 2: Anand Karaj]
ਲਾਵਾਂ ਲਈਆਂ, ਨਵਾਂ ਜੋੜਾ ਬਣਿਆ। ਸਾਰੇ ਖੁਸ਼, ਮੁਬਾਰਕਾਂ ਦਿੱਤੀਆਂ।
Took lavaan, new couple formed. Everyone happy, gave congratulations."""
            },
            {
                "name": "birthday_party",
                "story": """[SCENE 1: Surprise]
ਜਨਮਦਿਨ ਦੀ ਸਰਪ੍ਰਾਇਜ਼ ਪਾਰਟੀ। ਕੇਕ, ਮੋਮਬੱਤੀਆਂ, ਗਿਫਟ।
Birthday surprise party. Cake, candles, gifts.

[SCENE 2: Wishes]
ਸਾਰੇ ਨੇ ਗਾਣਾ ਗਾਇਆ। ਖੁਸ਼ੀ ਤੇ ਪਿਆਰ ਦਾ ਮਾਹੌਲ।
Everyone sang song. Atmosphere of joy and love."""
            },
            {
                "name": "homework_help",
                "story": """[SCENE 1: Study Time]
ਬੱਚਾ ਹੋਮਵਰਕ ਕਰ ਰਿਹਾ। ਪਾਪਾ ਮਦਦ ਕਰ ਰਹੇ।
Child doing homework. Father helping.

[SCENE 2: Learning]
ਮੁਸ਼ਕਲ ਸਵਾਲ ਹੱਲ ਹੋਇਆ। ਬੱਚਾ ਸਮਝ ਗਿਆ, ਖੁਸ਼ ਹੋਇਆ।
Difficult question solved. Child understood, became happy."""
            },
            
            # VILLAGE LIFE (5)
            {
                "name": "farming_morning",
                "story": """[SCENE 1: Fields]
ਸਵੇਰੇ ਕਿਸਾਨ ਖੇਤ ਗਿਆ। ਟਰੈਕਟਰ ਚਲਾਇਆ, ਵਾਹੀ ਕੀਤੀ।
Morning farmer went to field. Drove tractor, did cultivation.

[SCENE 2: Harvest]
ਫਸਲ ਤਿਆਰ ਹੋਈ। ਮਿਹਨਤ ਦਾ ਫਲ ਮਿਲਣ ਵਾਲਾ।
Crop ready. About to get fruit of hard work."""
            },
            {
                "name": "village_well",
                "story": """[SCENE 1: Water]
ਪਿੰਡ ਦੇ ਖੂਹ ਤੇ ਔਰਤਾਂ ਪਾਣੀ ਲੈਣ ਆਈਆਂ। ਗੱਲਾਂ ਕਰਦੀਆਂ।
Women came to village well for water. Chatting.

[SCENE 2: Community]
ਪਿੰਡ ਦੀ ਸਾਂਝ, ਸਭ ਮਿਲ ਜੁਲ ਕੇ। ਸਾਧਾਰਨ ਜੀਵਨ, ਖੁਸ਼ੀਆਂ ਵਾਲਾ।
Village community, all together. Simple life, full of happiness."""
            },
            {
                "name": "cattle_care",
                "story": """[SCENE 1: Morning Care]
ਪਸ਼ੂਆਂ ਨੂੰ ਚਾਰਾ ਪਾਇਆ। ਗਾਵਾਂ ਦਾ ਦੁੱਧ ਦੁਹਿਆ।
Fed fodder to animals. Milked cows.

[SCENE 2: Connection]
ਪਿੰਡ ਦੀ ਜ਼ਿੰਦਗੀ ਕੁਦਰਤ ਨਾਲ ਜੁੜੀ। ਸਧਾਰਨ ਪਰ ਪਵਿੱਤਰ।
Village life connected with nature. Simple but pure."""
            },
            {
                "name": "harvest_festival",
                "story": """[SCENE 1: Celebration]
ਵਿਸਾਖੀ ਦਾ ਤਿਉਹਾਰ, ਪਿੰਡ ਸਜਿਆ। ਭੰਗੜਾ, ਗਿੱਧਾ ਪਾਇਆ।
Vaisakhi festival, village decorated. Did bhangra, giddha.

[SCENE 2: Prosperity]
ਫਸਲ ਕੱਟੀ, ਖੁਸ਼ੀਆਂ ਮਨਾਈਆਂ। ਕਿਸਾਨਾਂ ਦੇ ਚਿਹਰੇ ਖਿੜੇ।
Cut crop, celebrated happiness. Farmers' faces bloomed."""
            },
            {
                "name": "village_school",
                "story": """[SCENE 1: Education]
ਪਿੰਡ ਦੇ ਸਕੂਲ ਵਿੱਚ ਬੱਚੇ ਪੜ੍ਹਦੇ। ਮਾਸਟਰ ਜੀ ਸਿਖਾ ਰਹੇ।
Children studying in village school. Master ji teaching.

[SCENE 2: Dreams]
ਬੱਚਿਆਂ ਦੇ ਸੁਪਨੇ ਵੱਡੇ। ਪੜ੍ਹ ਕੇ ਕੁੱਝ ਬਣਨਗੇ।
Children's dreams big. Will become something by studying."""
            },
            
            # LEARNING (5)
            {
                "name": "science_experiment",
                "story": """[SCENE 1: Lab]
ਸਕੂਲ ਦੀ ਲੈਬ ਵਿੱਚ ਪ੍ਰਯੋਗ ਕਰ ਰਹੇ। ਰਸਾਇਣ ਮਿਲਾਏ, ਰਿਐਕਸ਼ਨ ਦੇਖਿਆ।
Doing experiment in school lab. Mixed chemicals, saw reaction.

[SCENE 2: Discovery]
ਵਿਗਿਆਨ ਦੀ ਸਮਝ ਵੱਧੀ। ਨਵੀਂ ਖੋਜ, ਨਵਾਂ ਗਿਆਨ।
Understanding of science increased. New discovery, new knowledge."""
            },
            {
                "name": "punjabi_lesson",
                "story": """[SCENE 1: Language]
ਪੰਜਾਬੀ ਦੀ ਕਲਾਸ, ਗੁਰਮੁਖੀ ਸਿੱਖ ਰਹੇ। ਪੈਂਤੀ, ਮੁਕਤਾ, ਦੁਲੈਂਕੜੀ।
Punjabi class, learning Gurmukhi. Penti, mukta, dulankari.

[SCENE 2: Heritage]
ਆਪਣੀ ਭਾਸ਼ਾ, ਆਪਣੀ ਪਛਾਣ। ਪੰਜਾਬੀਅਤ ਦਾ ਮਾਣ।
Our language, our identity. Pride of Punjabiyat."""
            },
            {
                "name": "coding_class",
                "story": """[SCENE 1: Computer]
ਕੰਪਿਊਟਰ ਕਲਾਸ ਵਿੱਚ ਕੋਡਿੰਗ ਸਿੱਖੀ। Python, JavaScript ਲਿਖਿਆ।
Learned coding in computer class. Wrote Python, JavaScript.

[SCENE 2: Future]
ਟੈਕਨੋਲੋਜੀ ਦਾ ਗਿਆਨ। ਆਉਣ ਵਾਲੇ ਕੱਲ੍ਹ ਲਈ ਤਿਆਰ।
Knowledge of technology. Ready for tomorrow."""
            },
            {
                "name": "music_practice",
                "story": """[SCENE 1: Harmonium]
ਹਾਰਮੋਨੀਅਮ ਵਜਾਉਣਾ ਸਿੱਖਿਆ। ਸੁਰ, ਤਾਲ, ਰਾਗ।
Learned to play harmonium. Sur, taal, raag.

[SCENE 2: Art]
ਸੰਗੀਤ ਦੀ ਕਲਾ, ਆਤਮਾ ਦਾ ਭੋਜਨ। ਰਿਆਜ਼ ਨਾਲ ਸਿੱਧੀ।
Art of music, food for soul. Perfection with practice."""
            },
            {
                "name": "history_lesson",
                "story": """[SCENE 1: Past]
ਇਤਿਹਾਸ ਦੀ ਕਲਾਸ। ਸਿੱਖ ਗੁਰੂਆਂ ਦੇ ਬਲਿਦਾਨ, ਪੰਜਾਬ ਦਾ ਇਤਿਹਾਸ।
History class. Sacrifices of Sikh Gurus, Punjab's history.

[SCENE 2: Lessons]
ਬੀਤੇ ਤੋਂ ਸਿੱਖਿਆ। ਇਤਿਹਾਸ ਸਾਨੂੰ ਸਿਖਾਉਂਦਾ।
Learned from past. History teaches us."""
            },
            
            # MODERN LIFE (5)
            {
                "name": "startup_idea",
                "story": """[SCENE 1: Innovation]
ਨੌਜਵਾਨਾਂ ਨੇ ਸਟਾਰਟਅਪ ਸ਼ੁਰੂ ਕੀਤਾ। ਨਵਾਂ ਆਈਡੀਆ, ਨਵਾਂ ਕਾਰੋਬਾਰ।
Youth started startup. New idea, new business.

[SCENE 2: Success]
ਮਿਹਨਤ ਰੰਗ ਲਿਆਈ। ਪੰਜਾਬ ਦਾ ਨਾਮ ਰੋਸ਼ਨ ਕੀਤਾ।
Hard work paid off. Made Punjab's name shine."""
            },
            {
                "name": "sports_training",
                "story": """[SCENE 1: Practice]
ਹਾਕੀ ਦੀ ਪ੍ਰੈਕਟਿਸ ਕਰ ਰਹੇ। ਪੰਜਾਬੀ ਖਿਡਾਰੀ ਮਿਹਨਤੀ।
Doing hockey practice. Punjabi players hardworking.

[SCENE 2: Champion]
ਟੂਰਨਾਮੈਂਟ ਜਿੱਤਿਆ। ਮਿੱਟੀ ਦਾ ਕਰਜ਼ ਉਤਾਰਿਆ।
Won tournament. Paid debt to motherland."""
            }
        ]
        
        self.recent_scenarios = []  # Track recent scenarios to avoid repetition
        self.max_recent = min(10, len(self.scenarios) // 2)  # Remember last 10 or half of total
        
        print(f"✅ Simple Agent ready with {len(self.scenarios)} scenarios")
    
    def create_one_video(self, scenario_index=None):
        """Create one video - with smart variety selection"""
        import random
        
        if scenario_index is None:
            # Get scenarios not used recently
            available = [s for s in self.scenarios if s['name'] not in self.recent_scenarios]
            
            # If all used, reset recent list
            if not available:
                self.recent_scenarios = []
                available = self.scenarios
            
            scenario = random.choice(available)
            
            # Track this scenario
            self.recent_scenarios.append(scenario['name'])
            if len(self.recent_scenarios) > self.max_recent:
                self.recent_scenarios.pop(0)  # Remove oldest
        else:
            scenario = self.scenarios[scenario_index % len(self.scenarios)]
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        video_name = f"training_{scenario['name']}_{timestamp}.mp4"
        
        print(f"\n{'='*60}")
        print(f"🎬 Creating: {scenario['name']}")
        print(f"{'='*60}")
        
        try:
            video_path = self.maker.create_movie(
                scenario['story'],
                video_name
            )
            
            # Check if video exists (handle both string and Path)
            if video_path:
                video_file = Path(video_path) if isinstance(video_path, str) else video_path
                
                # Also check with .mp4 extension if not present
                if not video_file.exists():
                    video_file = self.workspace / f"{video_name}.mp4"
                
                if video_file.exists():
                    size = video_file.stat().st_size / 1024  # KB
                    print(f"✅ Video created: {video_file.name}")
                    print(f"📊 Size: {size:.1f} KB")
                    print(f"📂 Location: {video_file}")
                    return True
                else:
                    print(f"⚠️ Video path returned but file not found")
                    print(f"   Expected: {video_file}")
                    # Check if any video was created
                    recent_videos = sorted(self.workspace.glob("*.mp4"), 
                                         key=lambda x: x.stat().st_mtime, reverse=True)
                    if recent_videos:
                        print(f"   Found recent video: {recent_videos[0].name}")
                        return True
                    return False
            else:
                print(f"❌ Video creation failed - no path returned")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def run_batch(self, num_videos=10, delay=5):
        """Create multiple videos"""
        print("\n" + "="*70)
        print(f"🚀 SIMPLE AGENT BATCH START")
        print(f"   Creating {num_videos} diverse videos")
        print("="*70)
        
        created = 0
        failed = 0
        
        for i in range(num_videos):
            print(f"\n📊 Progress: {i+1}/{num_videos}")
            
            success = self.create_one_video(i)
            
            if success:
                created += 1
            else:
                failed += 1
            
            if i < num_videos - 1:
                print(f"⏳ Waiting {delay} seconds...")
                time.sleep(delay)
        
        print("\n" + "="*70)
        print(f"✅ BATCH COMPLETE")
        print(f"   Created: {created}/{num_videos}")
        print(f"   Failed: {failed}")
        print("="*70)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Simple Working Agent')
    parser.add_argument('--videos', type=int, default=10,
                       help='Number of videos to create')
    parser.add_argument('--delay', type=int, default=5,
                       help='Delay between videos (seconds)')
    
    args = parser.parse_args()
    
    agent = SimpleWorkingAgent()
    agent.run_batch(num_videos=args.videos, delay=args.delay)


if __name__ == "__main__":
    main()
