from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from ai_sql_genrator.tools.current_date_tool import CurrentDateTool
from ai_sql_genrator.tools.custom_tool import SQLiteQueryTool
from ai_sql_genrator.tools.db_schema_reader_tool import DatabaseSchemaTool

@CrewBase
class AiSqlGenrator():
    """AiSqlGenerator crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Agent Definitions
    @agent
    def sql_parser_validator(self) -> Agent:
        return Agent(
            config=self.agents_config['sql_parser_validator'],
            tools=[CurrentDateTool(), SQLiteQueryTool(), DatabaseSchemaTool()],
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
    def parse_and_validate_sql(self) -> Task:
        return Task(
            config=self.tasks_config['parse_and_validate_sql']
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