# core/orchestrator.py
from agent_queuing_system import select_best_agent
from collaborative_plugin_integration import get_applicable_plugins, execute_plugin_chain
from emergent_ai_consciousness import update_emergent_profile
from collaboration_safeguards import audit_collaboration_risks
from agent_to_agent_anti_bias import enforce_bias_safeguards
from culturally_diverse_voice_system import adjust_response_tone

class NeuroOrchestrator:
    def __init__(self, memory, logger):
        self.memory = memory
        self.logger = logger

    def process_user_input(self, user_id, input_text, context):
        self.logger.info(f"Received input from user {user_id}: {input_text}")

        # Step 1: Queue and select optimal agent
        agent = select_best_agent(input_text, context)
        self.logger.debug(f"Selected agent: {agent}")

        # Step 2: Retrieve relevant tools/plugins
        plugins = get_applicable_plugins(agent, input_text, context)
        self.logger.debug(f"Applicable plugins: {plugins}")

        # Step 3: Execute plugin chain
        plugin_result = execute_plugin_chain(plugins, input_text, context)

        # Step 4: Update AI self-model (consciousness telemetry)
        update_emergent_profile(agent, plugin_result)

        # Step 5: Run collaboration safety checks
        audit_collaboration_risks(agent, plugin_result)
        enforce_bias_safeguards(agent, plugin_result)

        # Step 6: Adjust for tone and cultural preferences
        final_response = adjust_response_tone(user_id, plugin_result)

        # Step 7: Store trace and return
        self.memory.log_interaction(user_id, input_text, final_response)
        return final_response
