from app.core.agents.base_agent import BaseAgent


class ResearchAgent(BaseAgent):

    def run(self):

        prompt = f"""
        {self.state["system_prompt"]}

        User Question:
        {self.state["user_query"]}
        """

        self.state["agent_response"] = self.invoke_llm(prompt)

        return self.state