from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from ai_sql_genrator.tools.custom_tool import SQLiteQueryTool

@CrewBase
class AiSqlGenrator():
    """AiSqlGenerator crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Agent Definitions
    @agent
    def question_parser(self) -> Agent:
        return Agent(
            config=self.agents_config['question_parser'],
            verbose=True
        )

    @agent
    def sql_validator(self) -> Agent:
        return Agent(
            config=self.agents_config['sql_validator'],
            tools=[SQLiteQueryTool()],
            verbose=True
        )

    @agent
    def answer_synthesizer(self) -> Agent:
        return Agent(
            config=self.agents_config['answer_synthesizer'],
            verbose=True
        )

    # Task Definitions
    @task
    def parse_question(self) -> Task:
        return Task(
            config=self.tasks_config['parse_question']
        )

    @task
    def validate_sql(self) -> Task:
        return Task(
            config=self.tasks_config['validate_sql']
        )

    @task
    def summarize_answer(self) -> Task:
        return Task(
            config=self.tasks_config['summarize_answer'],
            output_file='final_answer.md'
        )

    # Crew Definition
    @crew
    def crew(self) -> Crew:
        """Creates the AiSqlGenerator Crew"""

        return Crew(
            agents=self.agents,  # Automatically includes all decorated agents
            tasks=self.tasks,    # Automatically includes all decorated tasks
            process=Process.sequential,
            verbose=True,
            planning=True
        )