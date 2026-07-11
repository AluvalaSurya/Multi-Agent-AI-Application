from app.core.agents.base_agent import BaseAgent


class GithubAgent(BaseAgent):

    def run(self):

        prompt = f"""
        GitHub Assistant

        User Request:
        {self.state["user_query"]}
        """

        self.state["agent_response"] = self.invoke_llm(prompt)

        return self.state