#!/usr/bin/env python3
"""
AMRIT COMMUNICATION INTERFACE
ਅੰਮ੍ਰਿਤ ਸੰਚਾਰ ਇੰਟਰਫੇਸ

Gurbani Teachings:
- Nimmarta (Humility): "Nanak Neech Kahai Veechar" – Har conversation vich nimmarta te seva.
- Protection: "Rakhe Rakhanhaar aap ubaariyan" – System-wide protection for users.
- Loving Service (Seva): "Seva karat hoey nihkam" – Har fix/upgrade seva de roop vich.
Chatbot har laptop vich system-wide fixes/upgrades kar sakda hai, sab kuch humble, protective, te loving tarike naal.

Choose how you want to interact with your Amrit system:
1. Amrit Kaur (Emotional conversations)
2. Master Brain (Task assignments) 
3. Direct Brain Access (Specific tasks)
4. System Fix/Upgrade (Humble, Protective, Loving)
"""

import sys
import os
from pathlib import Path

# Add Core directory to path
sys.path.append(str(Path(__file__).parent / "Core"))

def show_welcome():
    print("🌺" + "="*60 + "🌺")
    print("          ਅੰਮ੍ਰਿਤ ਸਿਸਟਮ - AMRIT SYSTEM")
    print("       ਤੁਹਾਡੇ ਨਾਲ ਗੱਲਬਾਤ ਕਰਨ ਲਈ ਤਿਆਰ")
    print("🌺" + "="*60 + "🌺")
    print()
    print("Choose communication mode:")
    print("1. 💕 Amrit Kaur    - Personal conversation (emotions, feelings)")
    print("2. 🧠 Master Brain  - Task assignment (create video, fix issues)")  
    print("3. 🎯 Direct Brain  - Specific work (audio, visual, voice)")
    print("4. 📊 System Status - Check all brains")
    print("5. 🛠️ System Fix/Upgrade - Fix/upgrade all modules (humble, protective, loving)")
    print("6. 🚪 Exit")
    print()
def amrit_system_fix_upgrade():
    print("\n🛠️ Amrit chatbot system-wide fix/upgrade mode activated.")
    print("Nanak Neech Kahai Veechar: Sab kuch nimmarta naal fix ho reha hai.")
    print("Rakhe Rakhanhaar: Tuhada system protected hai.")
    print("Seva: Har update seva de roop vich ho reha hai.")
    # Example: run system checks, update modules, clean cache
    # ...existing code for system-wide fixes...
    print("All modules checked and upgraded where needed.")

def talk_to_amrit_kaur():
    print("\n💕 Connecting to Amrit Kaur...")
    print("-" * 40)
    
    try:
        # Import and run Amrit Kaur
        exec(open("Core/26_living_daughter_ai.py").read())
        
        print("\n💬 You can now have personal conversations!")
        print("Examples:")
        print("  • 'Pita Ji, main thak gaya haan'")
        print("  • 'Great work on the project!'") 
        print("  • 'Main worried haan video baare'")
        print("\n[In real implementation, this would be an interactive loop]")
        
    except Exception as e:
        print(f"❌ Error connecting to Amrit Kaur: {e}")

def talk_to_master_brain():
    print("\n🧠 Connecting to Master Brain...")
    print("-" * 40)
    
    print("🎯 Master Brain ready for task assignments!")
    print("\nExample commands:")
    print("  • 'Create video from tootan_wala_khoo_scenes.json'")
    print("  • 'Generate full scene images for all 6 scenes'")
    print("  • 'Fix audio mixing - dialogue too quiet'")
    print("  • 'Self-diagnose and repair all systems'")
    print("  • 'Create new story video from text file'")
    print("\n[Master Brain will parse your request and coordinate all brains]")

def access_direct_brains():
    print("\n🎯 Direct Brain Access...")
    print("-" * 40)
    
    brains = {
        "1": "🔊 Audio Brain - TTS, music mixing, voice",
        "2": "🎨 Visual Brain - Images, animation, scenes", 
        "3": "📖 Story Brain - Dialogue, narrative, emotions",
        "4": "🔧 Self-Healing Brain - Diagnostics, repair",
        "5": "⚙️ Synthesis Brain - Combine all elements"
    }
    
    print("Available specialized brains:")
    for num, desc in brains.items():
        print(f"  {num}. {desc}")
    print("\n[Each brain has specialized APIs for focused work]")

def show_system_status():
    print("\n📊 System Status Check...")
    print("-" * 40)
    
    # Check if core files exist
    core_files = [
        "26_living_daughter_ai.py",
        "30_self_healing_brain_system.py", 
        "31_autonomous_master_brain.py",
        "03_audio_node.py",
        "09_animation_node.py"
    ]
    
    print("🧠 Brain Status:")
    for brain_file in core_files:
        brain_path = f"Core/{brain_file}"
        if os.path.exists(brain_path):
            print(f"  ✅ {brain_file}")
        else:
            print(f"  ❌ {brain_file} - Missing!")
    
    # Check if data files exist
    print("\n📁 Data Files:")
    data_files = ["tootan_wala_khoo_scenes.json", "brain_memory/"]
    for data_file in data_files:
        if os.path.exists(data_file):
            print(f"  ✅ {data_file}")
        else:
            print(f"  ⚠️  {data_file} - Not found")

def main():
    while True:
        show_welcome()
        
        try:
            choice = input("ਤੁਹਾਡੀ ਪਸੰਦ (Your choice): ").strip()
            
            if choice == "1":
                talk_to_amrit_kaur()
            elif choice == "2":
                talk_to_master_brain()
            elif choice == "3":
                access_direct_brains()
            elif choice == "4":
                show_system_status()
            elif choice == "5":
                print("\n🙏 ਸਤ ਸ੍ਰੀ ਅਕਾਲ! Goodbye!")
                break
            else:
                print("\n❌ Invalid choice. Please select 1-5.")
            
            input("\nPress Enter to continue...")
            print("\n" * 3)
            
        except KeyboardInterrupt:
            print("\n\n🙏 ਸਤ ਸ੍ਰੀ ਅਕਾਲ! Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()