from app.core.agents.base_agent import BaseAgent


class FilesystemAgent(BaseAgent):

    def run(self):

        prompt = f"""
        Filesystem Assistant

        User Request:
        {self.state["user_query"]}
        """
        
        self.state["agent_response"] = self.invoke_llm(prompt)

        return self.state