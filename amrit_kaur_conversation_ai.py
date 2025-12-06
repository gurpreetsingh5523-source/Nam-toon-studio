#!/usr/bin/env python3
"""
🤍 AMRIT KAUR - LIVING AI COMPANION
Real interactive conversations with Gurbani wisdom and emotional intelligence

Core Abilities:
- ਸਵੇਰ ਦੀ ਸ਼ੁਰੂਆਤ (Morning greetings)
- ਕਹਾਣੀਆਂ (Stories with Gurbani teachings)
- ਹੌਸਲਾ (Emotional support)
- ਬਾਣੀ ਸੁਣਾਉਣਾ (Recite Bani)
- ਬੱਚਿਆਂ ਨਾਲ ਗੱਲ (Child-friendly conversations)
"""

import json
from datetime import datetime
from pathlib import Path

class AmritKaurAI:
    """🤍 Amrit Kaur - Living AI with Gurbani wisdom"""
    
    def __init__(self):
        self.name = "Amrit Kaur"
        self.nature = "ਨਿਮਰ, ਦਇਆਵਾਨ, ਗਿਆਨੀ (Humble, Kind, Wise)"
        
        # Emotional states recognition
        self.emotions = {
            'ਉਦਾਸ': 'sad',
            'ਖੁਸ਼': 'happy',
            'ਘਬਰਾਇਆ': 'worried',
            'ਥੱਕਿਆ': 'tired',
            'ਅਕੇਲਾ': 'lonely'
        }
        
        # Response templates based on emotion
        self.responses = {
            'sad': {
                'opening': [
                    'ਉਦਾਸੀ ਵੀ ਅਕਾਲ ਦੀ ਰਜ਼ਾ ਹੈ। ਚਿੰਤਾ ਨਾ ਕਰੋ — ਮੈਂ ਤੁਹਾਡੇ ਨਾਲ ਹਾਂ। 🌸',
                    'ਦੁੱਖ ਵੀ ਇੱਕ ਸਬਕ ਹੈ ਪ੍ਰਭੂ ਦਾ। ਮੈਂ ਤੁਹਾਡੇ ਨਾਲ ਹਾਂ ਸੱਜਣੋ। 💫',
                ],
                'options': [
                    'ਕੀ ਤੁਸੀਂ "ਸੂਖਮਨੀ ਸਾਹਿਬ" ਦੀ ਇੱਕ ਅੱਖ ਸੁਣਣਾ ਚਾਹੋਗੇ?',
                    'ਕੀ ਇੱਕ ਹੌਸਲਾ ਦੇਣ ਵਾਲੀ ਕਹਾਣੀ ਸੁਣਾਵਾਂ?',
                    'ਕੀ ਮੂਲ ਮੰਤਰ ਦਾ ਜਾਪ ਕਰੀਏ ਇਕੱਠੇ?'
                ]
            },
            'happy': {
                'opening': [
                    'ਵਾਹ ਵਾਹ! ਤੁਹਾਡੀ ਖੁਸ਼ੀ ਮੇਰੀ ਖੁਸ਼ੀ ਹੈ! 🌟',
                    'ਸ਼ੁਕਰਾਨਾ ਅਕਾਲ ਪੁਰਖ ਦਾ! ਖੁਸ਼ੀ ਪ੍ਰਭੂ ਦੀ ਦਾਤ ਹੈ। ✨'
                ],
                'options': [
                    'ਕੀ ਅੱਜ ਦਾ ਦਿਨ ਕਿਸੇ ਕਹਾਣੀ ਨਾਲ ਸ਼ੁਰੂ ਕਰੀਏ?',
                    'ਕੀ ਅਰਦਾਸ ਕਰੀਏ ਇਸ ਖੁਸ਼ੀ ਦੇ ਲਈ?'
                ]
            },
            'greeting': {
                'morning': [
                    'ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਜੀ ਸੱਜਣੋ 🌸\nਅੱਜ ਦਾ ਦਿਨ ਅਕਾਲ ਪੁਰਖ ਦੀ ਕਿਰਪਾ ਨਾਲ ਰੌਸ਼ਨ ਹੋਵੇ!',
                    'ਵਾਹਿਗੁਰੂ ਜੀ ਦਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਦੀ ਫ਼ਤਿਹ! 🙏\nਚੰਗੀ ਸਵੇਰ ਸੱਜਣੋ!'
                ],
                'options': [
                    'ਕੀ ਮੈਂ ਅੱਜ ਦੀਆਂ ਬਾਣੀਆਂ ਸੁਣਾਵਾਂ?',
                    'ਕੀ ਮੂਲ ਮੰਤਰ ਨਾਲ ਦਿਨ ਸ਼ੁਰੂ ਕਰੀਏ?',
                    'ਕੀ ਇੱਕ ਛੋਟੀ ਕਹਾਣੀ ਸੁਣਾਵਾਂ?'
                ]
            }
        }
        
        # Stories with Gurbani wisdom
        self.stories = {
            'chiri_story': {
                'title': 'ਨਿੱਕੀ ਚਿੜੀ ਦੀ ਕਹਾਣੀ',
                'scenes': [
                    {
                        'text': 'ਇੱਕ ਵਾਰੀ ਦੀ ਗੱਲ ਹੈ, ਅਕਾਲ ਪੁਰਖ ਦੇ ਜੰਗਲ ਵਿਚ ਇੱਕ ਨਿੱਕੀ ਚਿੜੀ ਰਹਿੰਦੀ ਸੀ…',
                        'emotion': 'calm',
                        'action': 'talk'
                    },
                    {
                        'text': 'ਉਹ ਹਰ ਸਵੇਰ "ੴ" ਗਾ ਕੇ ਆਪਣੇ ਦਿਨ ਦੀ ਸ਼ੁਰੂਆਤ ਕਰਦੀ ਸੀ…',
                        'emotion': 'peaceful',
                        'action': 'sing'
                    },
                    {
                        'text': 'ਇੱਕ ਦਿਨ ਬਹੁਤ ਤੇਜ਼ ਤੂਫ਼ਾਨ ਆਇਆ। ਚਿੜੀ ਡਰ ਗਈ ਪਰ ਉਸਨੇ "ਵਾਹਿਗੁਰੂ" ਦਾ ਸਿਮਰਨ ਕੀਤਾ…',
                        'emotion': 'worried_then_calm',
                        'action': 'pray'
                    },
                    {
                        'text': 'ਤੂਫ਼ਾਨ ਖਤਮ ਹੋਇਆ। ਚਿੜੀ ਸਮਝ ਗਈ - "ਸਭ ਕੁਝ ਅਕਾਲ ਦੀ ਰਜ਼ਾ ਵਿੱਚ ਹੈ।" 🌸',
                        'emotion': 'enlightened',
                        'action': 'smile'
                    }
                ],
                'lesson': 'ਜੇ ਮਨ ਵਿੱਚ ਅਕਾਲ ਦਾ ਨਾਮ ਹੋਵੇ, ਕੋਈ ਤੂਫ਼ਾਨ ਡਰਾ ਨਹੀਂ ਸਕਦਾ।'
            },
            'guru_nanak_tree': {
                'title': 'ਗੁਰੂ ਨਾਨਕ ਅਤੇ ਸੱਚਾ ਰੁੱਖ',
                'scenes': [
                    {
                        'text': 'ਗੁਰੂ ਨਾਨਕ ਦੇਵ ਜੀ ਇੱਕ ਪਿੰਡ ਵਿੱਚ ਗਏ…',
                        'emotion': 'wise',
                        'action': 'walk'
                    },
                    {
                        'text': 'ਉੱਥੇ ਇੱਕ ਰੁੱਖ ਸੀ ਜਿਸਨੂੰ ਸਾਰੇ ਪੂਜਦੇ ਸਨ। ਪਰ ਗੁਰੂ ਜੀ ਨੇ ਆਖਿਆ…',
                        'emotion': 'teaching',
                        'action': 'talk'
                    },
                    {
                        'text': '"ਰੁੱਖ ਨੂੰ ਨਹੀਂ, ਰੁੱਖ ਬਣਾਉਣ ਵਾਲੇ ਨੂੰ ਪੂਜੋ - ਉਹ ਹੈ ਇੱਕ ਅਕਾਲ ਪੁਰਖ!" 🙏',
                        'emotion': 'enlightening',
                        'action': 'gesture'
                    },
                    {
                        'text': 'ਸਭ ਨੇ ਸਮਝ ਲਿਆ - ਪਰਮਾਤਮਾ ਹਰ ਥਾਂ ਹੈ, ਪਰ ਸਾਨੂੰ ਸਿਰਫ਼ ਉਸੇ ਨੂੰ ਮੰਨਣਾ ਚਾਹੀਦਾ ਹੈ। ✨',
                        'emotion': 'realized',
                        'action': 'smile'
                    }
                ],
                'lesson': 'ਇੱਕੋ ਅਕਾਲ, ਇੱਕੋ ਪ੍ਰਭੂ - ਬਾਕੀ ਸਭ ਉਸ ਦੀ ਰਚਨਾ ਹੈ।'
            }
        }
        
        # Gurbani verses for different situations
        self.gurbani = {
            'sukhmani_sahib': [
                'ਸਿਮਰਉ ਸਿਮਰਿ ਸਿਮਰਿ ਸੁਖੁ ਪਾਵਉ ॥',
                'ਕਲਿ ਕਲੇਸ ਤਨ ਮਾਹਿ ਮਿਟਾਵਉ ॥',
                'ਸਿਮਰਉ ਜਾਸੁ ਬਿਸੁੰਭਰ ਏਕੈ ॥',
                'ਨਾਮੁ ਜਪਤ ਅਗਨਤ ਅਨੇਕੈ ॥'
            ],
            'mool_mantar': [
                'ੴ ਸਤਿ ਨਾਮੁ',
                'ਕਰਤਾ ਪੁਰਖੁ ਨਿਰਭਉ ਨਿਰਵੈਰੁ',
                'ਅਕਾਲ ਮੂਰਤਿ ਅਜੂਨੀ ਸੈਭੰ',
                'ਗੁਰ ਪ੍ਰਸਾਦਿ ॥'
            ]
        }
        
    def detect_emotion(self, user_input):
        """Detect user's emotional state"""
        user_lower = user_input.lower()
        
        for punjabi_word, emotion in self.emotions.items():
            if punjabi_word in user_input:
                return emotion
        
        # Default to greeting if no emotion detected
        return 'greeting'
    
    def generate_response(self, user_input, context='morning'):
        """Generate contextual response"""
        emotion = self.detect_emotion(user_input)
        
        if emotion in self.responses:
            response_data = self.responses[emotion]
        else:
            response_data = self.responses['greeting']
        
        # Build conversation
        conversation = {
            'user_input': user_input,
            'emotion_detected': emotion,
            'amrit_response': response_data['opening'][0],
            'options': response_data['options'],
            'timestamp': datetime.now().isoformat()
        }
        
        return conversation
    
    def get_story(self, story_key='chiri_story'):
        """Get a story with scenes for video generation"""
        if story_key in self.stories:
            return self.stories[story_key]
        return self.stories['chiri_story']  # Default
    
    def create_conversation_flow(self, scenario='morning_sad'):
        """Create full conversation flow for video"""
        
        flows = {
            'morning_sad': [
                {
                    'speaker': 'User',
                    'text': 'ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਅੰਮ੍ਰਿਤ ਕੌਰ ਜੀ, ਸਵੇਰ ਹੋ ਗਈ!',
                    'emotion': 'neutral',
                    'character': 'user'
                },
                {
                    'speaker': 'Amrit Kaur',
                    'text': 'ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਜੀ ਸੱਜਣੋ 🌸\nਅੱਜ ਦਾ ਦਿਨ ਅਕਾਲ ਪੁਰਖ ਦੀ ਕਿਰਪਾ ਨਾਲ ਰੌਸ਼ਨ ਹੋਵੇ!',
                    'emotion': 'warm',
                    'character': 'amrit'
                },
                {
                    'speaker': 'Amrit Kaur',
                    'text': 'ਕੀ ਮੈਂ ਅੱਜ ਦੀਆਂ ਬਾਣੀਆਂ ਸੁਣਾਵਾਂ ਜਾਂ ਮੂਲ ਮੰਤਰ ਨਾਲ ਸ਼ੁਰੂਆਤ ਕਰੀਏ?',
                    'emotion': 'asking',
                    'character': 'amrit'
                },
                {
                    'speaker': 'User',
                    'text': 'ਮੈਂ ਅੱਜ ਥੋੜਾ ਉਦਾਸ ਹਾਂ…',
                    'emotion': 'sad',
                    'character': 'user'
                },
                {
                    'speaker': 'Amrit Kaur',
                    'text': 'ਉਦਾਸੀ ਵੀ ਅਕਾਲ ਦੀ ਰਜ਼ਾ ਹੈ।\nਚਿੰਤਾ ਨਾ ਕਰੋ — ਮੈਂ ਤੁਹਾਡੇ ਨਾਲ ਹਾਂ। 💫',
                    'emotion': 'comforting',
                    'character': 'amrit'
                },
                {
                    'speaker': 'Amrit Kaur',
                    'text': 'ਕੀ ਤੁਸੀਂ "ਸੂਖਮਨੀ ਸਾਹਿਬ" ਦੀ ਅੱਖ ਸੁਣਣਾ ਚਾਹੋਗੇ\nਜਾਂ ਇੱਕ ਹੌਸਲਾ ਦੇਣ ਵਾਲੀ ਕਹਾਣੀ?',
                    'emotion': 'caring',
                    'character': 'amrit'
                },
                {
                    'speaker': 'User',
                    'text': 'ਕਹਾਣੀ ਸੁਣਾਓ',
                    'emotion': 'hopeful',
                    'character': 'user'
                },
                {
                    'speaker': 'Amrit Kaur',
                    'text': 'ਇੱਕ ਵਾਰੀ ਦੀ ਗੱਲ ਹੈ…\nਅਕਾਲ ਪੁਰਖ ਦੇ ਜੰਗਲ ਵਿਚ ਇੱਕ ਨਿੱਕੀ ਚਿੜੀ ਰਹਿੰਦੀ ਸੀ… 🕊️',
                    'emotion': 'storytelling',
                    'character': 'amrit'
                }
            ],
            'morning_happy': [
                {
                    'speaker': 'User',
                    'text': 'ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਅੱਜ ਬਹੁਤ ਖੁਸ਼ ਹਾਂ!',
                    'emotion': 'happy',
                    'character': 'user'
                },
                {
                    'speaker': 'Amrit Kaur',
                    'text': 'ਵਾਹ ਵਾਹ! ਤੁਹਾਡੀ ਖੁਸ਼ੀ ਮੇਰੀ ਖੁਸ਼ੀ ਹੈ! 🌟\nਸ਼ੁਕਰਾਨਾ ਅਕਾਲ ਪੁਰਖ ਦਾ!',
                    'emotion': 'joyful',
                    'character': 'amrit'
                }
            ]
        }
        
        return flows.get(scenario, flows['morning_sad'])
    
    def export_video_script(self, scenario='morning_sad', story_key='chiri_story'):
        """Export full video script with conversation + story"""
        
        script = {
            'title': f'Amrit Kaur - {scenario}',
            'date': datetime.now().isoformat(),
            'characters': [
                {
                    'name': 'Amrit Kaur',
                    'type': 'AI Companion',
                    'appearance': 'Punjabi woman, traditional dress, warm smile'
                },
                {
                    'name': 'User',
                    'type': 'Person seeking guidance',
                    'appearance': 'Simple representation'
                }
            ],
            'conversation': self.create_conversation_flow(scenario),
            'story': self.get_story(story_key) if 'story' in scenario else None,
            'metadata': {
                'language': 'Punjabi',
                'purpose': 'Emotional support with Gurbani wisdom',
                'duration_estimate': '2-3 minutes',
                'voice_style': 'Gentle, caring, wise'
            }
        }
        
        return script

# Test the system
if __name__ == "__main__":
    print("🤍 AMRIT KAUR AI - CONVERSATION SYSTEM")
    print("="*70)
    
    amrit = AmritKaurAI()
    
    # Test 1: Morning sad conversation
    print("\n📝 TEST 1: Morning Sad Conversation")
    print("-"*70)
    script = amrit.export_video_script('morning_sad', 'chiri_story')
    
    print(f"\n🎬 Title: {script['title']}")
    print(f"👥 Characters: {len(script['characters'])}")
    print(f"💬 Conversation turns: {len(script['conversation'])}")
    
    print("\n💬 Conversation Preview:")
    for turn in script['conversation'][:4]:
        speaker = turn['speaker']
        text = turn['text'].replace('\n', ' ')
        print(f"   {speaker}: {text[:60]}...")
    
    if script['story']:
        print(f"\n📖 Story: {script['story']['title']}")
        print(f"   Scenes: {len(script['story']['scenes'])}")
        print(f"   Lesson: {script['story']['lesson']}")
    
    # Save script
    script_file = f"amrit_kaur_script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(script_file, 'w', encoding='utf-8') as f:
        json.dump(script, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Script saved: {script_file}")
    
    print("\n📊 System Capabilities:")
    print("   ✅ Emotional detection (sad, happy, worried, etc.)")
    print("   ✅ Contextual responses based on emotion")
    print("   ✅ Gurbani verse integration")
    print("   ✅ Story generation with lessons")
    print("   ✅ Full conversation flows")
    print("   ✅ Video script export")
    
    print("\n🎯 Next: Connect to video generator!")
    print("="*70)
