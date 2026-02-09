"""
Google ADK Multi-Agent Template — Sequential Pipeline with Parallel Fan-Out

This template demonstrates:
  - SequentialAgent for ordered pipelines
  - ParallelAgent for concurrent work
  - State sharing via output_key
  - AgentTool for on-demand specialist invocation
"""

from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LlmAgent
from google.adk.tools import AgentTool

MODEL = "gemini-2.5-flash"


# --- Specialist Agents ---

research_agent = LlmAgent(
    name="Researcher",
    model=MODEL,
    description="Researches a topic and provides key findings.",
    instruction="""You are a research specialist. Given a topic, provide 3-5 key findings
with brief explanations. Be factual and concise.""",
    output_key="research_findings",
)

data_agent = LlmAgent(
    name="DataAnalyst",
    model=MODEL,
    description="Analyzes data and provides statistical insights.",
    instruction="""You are a data analysis specialist. Given a topic, provide
relevant statistics, trends, and quantitative insights.""",
    output_key="data_insights",
)

writer_agent = LlmAgent(
    name="Writer",
    model=MODEL,
    description="Writes polished content from research and data.",
    instruction="""You are a professional writer. Using the research findings
from {research_findings} and data insights from {data_insights},
write a well-structured, engaging summary. Include an introduction,
key points, and conclusion.""",
    output_key="final_report",
)


# --- Pipeline: Parallel research + data, then sequential writing ---

parallel_gather = ParallelAgent(
    name="GatherInfo",
    sub_agents=[research_agent, data_agent],
)

root_agent = SequentialAgent(
    name="ReportPipeline",
    description="Generates comprehensive reports by researching, analyzing data, and writing.",
    sub_agents=[parallel_gather, writer_agent],
)


# --- Alternative: Coordinator with AgentTool pattern ---
# Uncomment below if you want LLM-driven orchestration instead of fixed pipeline.

# root_agent = LlmAgent(
#     name="Coordinator",
#     model=MODEL,
#     description="Coordinates research and writing tasks.",
#     instruction="""You are a project coordinator. When asked to create a report:
# 1. Use the researcher tool to gather findings
# 2. Use the data analyst tool for statistics
# 3. Use the writer tool to create the final report
# Combine all results into a coherent response.""",
#     tools=[
#         AgentTool(agent=research_agent),
#         AgentTool(agent=data_agent),
#         AgentTool(agent=writer_agent),
#     ],
# )
