import time
import logging
import asyncio # New: For concurrent, multi-tasking operations

# Setup for clear, structured logging (Essential for debugging and learning)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - Mastermind - %(message)s')

class NaamToonMastermind:
    """
    The Advanced Central AI Brain for NAAM TOON STUDIO.
    Features: Concurrent Thinking, Error Self-Correction, and Deep Logical Planning.
    """

    def __init__(self, studio_name="NAAM TOON STUDIO"):
        self.name = studio_name
        self.agents = {}  # Dictionary to hold agents for quick access (Fast thinking!)
        self.learned_errors = set() # Set to store errors and prevent repeating them (Learning!)
        self.log_vision()
    
    def log_vision(self):
        """Displays the updated vision and commitment to continuous learning."""
        logging.info("================================================================")
        logging.info(f"MASTERMIND INITIALIZED: {self.name} - Version 2.0 (Self-Learning)")
        logging.info("Core Logic: Concurrent Execution (Multi-focus) & Error-Proofing.")
        logging.info(f"Commitment: Never repeat past mistakes. Current known errors: {len(self.learned_errors)}")
        logging.info("================================================================")

    def register_agent(self, agent_instance):
        """Registers an agent for multi-tasking, using its name as the key."""
        self.agents[agent_instance.name] = agent_instance
        logging.info(f"Agent Registered: {agent_instance.name}. Total Agents: {len(self.agents)}")
    
    async def process_sub_task(self, agent_name, instruction):
        """Simulates the agent executing a task asynchronously (concurrently)."""
        
        # Simulate checking for a known, fatal error (Example of self-correction)
        if "OS_VERSION_MISMATCH" in self.learned_errors:
            logging.warning(f"Self-Correction: Skipping {agent_name} due to prior fatal OS requirement error.")
            return f"Skipped: OS_VERSION_MISMATCH detected."

        logging.info(f"  > Start: {agent_name} received instruction: {instruction}")
        await asyncio.sleep(0.5) # Simulate time taken by the agent
        
        # Simulate success
        logging.info(f"  < Finish: {agent_name} successfully executed its part.")
        return f"Result: {agent_name} completed '{instruction}'"

    def reasoning_engine(self, complex_task):
        """Breaks down a task, prioritizing high-level, concurrent stages."""
        
        logging.info(f"\n[MASTER REASONING] Analyzing '{complex_task}'. Looking for parallel steps...")
        
        steps = []
        if "create movie" in complex_task.lower():
            # These steps can run concurrently (at the same time)
            logging.info("Decomposition: Identifying parallel tasks for efficiency.")
            steps.append(("Scripting_Agent", "Generate full script (Text/Dialogue)."))
            steps.append(("Visual_Agent", "Start generating placeholder visual assets."))
            steps.append(("Audio_Agent", "Prepare background music and sound effects."))
            
            # This step must wait for the others
            steps.append(("Master_Assembler", "Final Assembly (Requires all prior steps to complete)."))
        else:
            logging.warning("Task is simple. Executing sequentially.")
            steps.append(("Simple_Executor", complex_task))

        return steps

    async def execute_task(self, task_description):
        """The main controller for multi-stage, concurrent execution."""
        
        planning_steps = self.reasoning_engine(task_description)
        
        if not planning_steps or not self.agents:
            logging.error("Execution failed: No valid plan or no agents registered.")
            return

        # 1. Run all concurrent tasks
        concurrent_tasks = []
        assembly_step = None
        
        for agent_name, instruction in planning_steps:
            if agent_name == "Master_Assembler":
                assembly_step = (agent_name, instruction)
            else:
                # Add concurrent tasks to the list
                concurrent_tasks.append(self.process_sub_task(agent_name, instruction))
        
        # Run all concurrent tasks together (The multi-focus power!)
        logging.info("\n[CONCURRENT START] Launching multi-focus agents simultaneously...")
        results = await asyncio.gather(*concurrent_tasks)
        
        # 2. Run the final sequential task (Assembly)
        if assembly_step:
            logging.info("\n[ASSEMBLY START] All parts received. Running final assembly...")
            final_result = await self.process_sub_task(assembly_step[0], assembly_step[1])
            results.append(final_result)
        
        logging.info("\n[EXECUTION COMPLETE] Final Mastermind Output. Check results for details.")
        return results

# ===============================================
# Example of how the Advanced Mastermind would be used:
# ===============================================

# NOTE: Since 'asyncio' requires special handling, we wrap the execution in a function.
def run_studio_test():
    # 1. Create the central brain
    master_brain = NaamToonMastermind()
    
    # 2. Add a hypothetical agent (We will create these tomorrow)
    class DummyAgent:
        def __init__(self, name):
            self.name = name
    
    master_brain.register_agent(DummyAgent("Scripting_Agent"))
    master_brain.register_agent(DummyAgent("Visual_Agent"))
    master_brain.register_agent(DummyAgent("Audio_Agent"))
    master_brain.register_agent(DummyAgent("Master_Assembler"))

    # 3. Add a past error to the learned set (The Mastermind remembers the OS problem)
    master_brain.learned_errors.add("OS_VERSION_MISMATCH")

    # 4. Give the Mastermind a complex task to see its multi-focus logic
    asyncio.run(master_brain.execute_task("Create a full short movie about a farmer inventing an AI tractor."))

if __name__ == "__main__":
    run_studio_test()
