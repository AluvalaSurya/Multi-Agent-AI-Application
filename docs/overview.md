# Multi-Agent AI Application using LangGraph + MCP

## Overview

This project is a **Multi-Agent AI System** built using **LangGraph**, **Groq LLMs**, and the **Model Context Protocol (MCP)**.

Instead of relying on a single AI model to perform every task, the system routes user requests to specialized agents such as:

- Research Agent (Internet Search)
- GitHub Agent (Repository Operations)
- Filesystem Agent (Local File Operations)
- Response Agent (Final Answer Generation)

Each agent performs one responsibility and returns structured outputs which are merged by LangGraph before generating the final response.

---

# Overall Architecture

```text
                        User
                          │
                          ▼
                  FastAPI / Streamlit
                          │
                          ▼
                    LangGraph Graph
                          │
                          ▼
                     Supervisor
                          │
              ┌───────────┼────────────┐
              ▼           ▼            ▼
        Research     Filesystem     GitHub
          Agent         Agent        Agent
              │           │            │
              │           │            │
              └───────────┼────────────┘
                          ▼
                     Aggregator
                          │
                          ▼
                   Response Agent
                          │
                          ▼
                     Final Response
```

---

# MCP Integration

Every specialized agent communicates with external services through MCP.

```text
                     Research Agent
                            │
                            ▼
                      MCPTools.search()
                            │
                            ▼
                        MCPClient
                            │
                            ▼
                     Tavily MCP Server
                            │
                            ▼
                        Tavily Search API



                     GitHub Agent
                            │
                            ▼
             MCPTools.search_repositories()
                            │
                            ▼
                        MCPClient
                            │
                            ▼
                    GitHub MCP Server
                            │
                            ▼
                        GitHub API



                  Filesystem Agent
                            │
                            ▼
                  MCPTools.read_file()
                            │
                            ▼
                        MCPClient
                            │
                            ▼
                 Filesystem MCP Server
                            │
                            ▼
                     Local File System
```

---

# Complete Request Flow

Suppose the user asks:

> Explain the latest LangGraph repository.

The execution flow is:

```text
User
 │
 ▼
Supervisor
 │
 ▼
LLM decides:

{
  "next_nodes":[
      "research",
      "github"
  ]
}
 │
 ▼
LangGraph routes execution
 │
 ├──────────────┐
 ▼              ▼
Research      GitHub
Agent         Agent
 │              │
 ▼              ▼
Tavily MCP   GitHub MCP
 │              │
 ▼              ▼
Results      Repository Data
 └──────────────┘
        │
        ▼
LangGraph merges outputs
        │
        ▼
Aggregator
        │
        ▼
Response Agent
        │
        ▼
Final Response
```

---

# Project Structure

```text
app
│
├── core
│   ├── agents
│   ├── graph_builder.py
│   ├── nodes.py
│   ├── edges.py
│   ├── supervisor.py
│   ├── state.py
│   ├── aggregator.py
│   └── llm.py
│
├── mcp
│   ├── config.py
│   ├── client.py
│   └── tools.py
│
├── backend
├── frontend
└── common
```

---

# Core Components

---

## 1. AgentState

`state.py`

The AgentState is the shared memory of the graph.

Every node receives the same state and returns only the fields it updates.

Example:

```python
{
    "user_query": "...",
    "messages": [],
    "next_nodes": [],
    "agent_outputs": {},
    "final_response": ""
}
```

LangGraph automatically merges updates using reducers such as:

- `add_messages`
- `merge_dict`

---

## 2. Supervisor

The Supervisor is the brain of the workflow.

Responsibilities:

- Understand user intent
- Decide which agents should execute
- Produce routing information

Example output:

```json
{
    "next_nodes":[
        "research",
        "github"
    ],
    "reason":"Repository lookup requires search and GitHub."
}
```

---

## 3. Research Agent

Responsibilities:

- Internet Search
- Technical Research
- Current Events

Flow

```text
User Query
      │
      ▼
MCPTools.search()
      │
      ▼
Tavily MCP
      │
      ▼
Search Results
      │
      ▼
LLM summarizes
```

---

## 4. GitHub Agent

Responsibilities

- Repository Search
- Read Repository Files
- Create Issues

Flow

```text
User Query
      │
      ▼
MCPTools.search_repositories()
      │
      ▼
GitHub MCP
      │
      ▼
Repository Results
      │
      ▼
LLM summarizes
```

---

## 5. Filesystem Agent

Responsibilities

- Read files
- Write files
- List directories

Flow

```text
User Query
      │
      ▼
MCPTools.read_file()
      │
      ▼
Filesystem MCP
      │
      ▼
Local File
      │
      ▼
LLM answers
```

---

## 6. Aggregator

The Aggregator receives outputs from all executed agents.

Current implementation:

- Pass-through node

Future enhancements:

- Merge metadata
- Filter failures
- Confidence scoring
- Execution statistics
- Output ranking

---

## 7. Response Agent

The Response Agent receives all agent outputs and generates a coherent final answer for the user.

Instead of exposing raw MCP results, it creates a natural language response.

---

# MCP Layer

The MCP folder abstracts all communication with MCP servers.

---

## config.py

Contains server configuration.

Example:

- Filesystem Server
- GitHub Server
- Tavily Server

Defines:

- command
- arguments
- environment variables

---

## client.py

Implements the MCP Client.

Responsibilities:

- Start MCP Server
- Create ClientSession
- Initialize connection
- Call tools
- Close resources

Example flow:

```text
MCPClient

↓

Start Server

↓

ClientSession

↓

Initialize

↓

Call Tool

↓

Receive Result
```

---

## tools.py

Provides high-level wrappers around MCP tools.

Instead of writing:

```python
client.call_tool(...)
```

agents simply call:

```python
await MCPTools.search(query)
```

Available wrappers include:

- search()
- research()
- extract()
- crawl()
- map()
- search_repositories()
- get_file_contents()
- create_issue()
- read_file()
- write_file()
- list_directory()

---

# Why return partial state instead of modifying state?

Every LangGraph node returns only the fields it updates.

Example:

```python
return {
    "agent_outputs": {
        "research": response
    }
}
```

instead of

```python
state["agent_outputs"]["research"] = response
```

Benefits:

- Parallel execution
- Automatic state merging
- Immutable workflow
- Cleaner debugging

---

# Why MCP?

Instead of writing custom integrations for every external service,

```text
Research Agent

↓

Tavily SDK
```

or

```text
GitHub Agent

↓

GitHub REST API
```

every interaction follows one protocol:

```text
Agent

↓

MCP Client

↓

MCP Server

↓

External Service
```

This makes adding new tools significantly easier.

---

# Future Improvements

- Dynamic MCP Tool Selection
- Parallel Tool Execution
- Agent-specific Inputs
- Memory Support
- RAG Integration
- Human Approval Nodes
- Retry & Error Recovery
- LangSmith Tracing

---

# Technologies Used

- LangGraph
- LangChain
- MCP (Model Context Protocol)
- Groq LLM
- Tavily MCP
- GitHub MCP
- Filesystem MCP
- FastAPI
- Streamlit