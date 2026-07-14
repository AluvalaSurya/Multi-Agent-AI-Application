# 🏗️ Architecture

## Overview

This project implements a **Multi-Agent AI System** using **LangGraph** and **Model Context Protocol (MCP)**.

Instead of using a single LLM for every task, the application routes the user request to specialized AI agents based on the query. Each agent performs one responsibility and returns structured outputs that are combined into a final response.

The architecture follows a layered design:

```
                    User
                      │
                      ▼
             Frontend (Streamlit)
                      │
                      ▼
             Backend (FastAPI)
                      │
                      ▼
                LangGraph Graph
                      │
                      ▼
                 Supervisor Agent
                      │
      ┌───────────────┼────────────────┐
      ▼               ▼                ▼
Research Agent   GitHub Agent   Filesystem Agent
      │               │                │
      ▼               ▼                ▼
     MCP             MCP              MCP
      │               │                │
      ▼               ▼                ▼
 Tavily Server   GitHub Server   Filesystem Server
      │               │                │
      ▼               ▼                ▼
 External APIs / Resources / Local Files
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

# Project Layers

The application is divided into three major layers.

```
Frontend
     │
Backend API
     │
LangGraph Core
     │
MCP Layer
     │
External Services
```

---

# LangGraph Workflow

Every user request follows the same execution pipeline.

```
START
   │
   ▼
Supervisor
   │
   ├──────────────┐
   ▼              ▼
Research      GitHub
Agent         Agent
   │              │
   └──────┬───────┘
          ▼
     Filesystem
        (optional)
          │
          ▼
     Aggregator
          │
          ▼
   Response Agent
          │
          ▼
         END
```

The Supervisor decides which agents should execute based on the user query.

---

# Shared State

LangGraph uses a shared state (`AgentState`) that flows through every node.

```
AgentState
│
├── user_query
├── messages
├── next_nodes
├── routing_reason
├── routing_confidence
├── agent_outputs
└── final_response
```

Each node receives the same state and **returns only the fields it updates**.

Example:

```python
return {
    "agent_outputs": {
        "research": response
    }
}
```

LangGraph automatically merges updates using reducers (`merge_dict`, `add_messages`).

This enables safe parallel execution.

---

# Supervisor

The Supervisor is the decision-making component of the graph.

Responsibilities:

- Understand user intent
- Select the required agents
- Generate routing information
- Produce structured JSON output

Example:

```json
{
  "next_nodes": [
    "research",
    "github"
  ],
  "agent_inputs": {
    "github": {
      "owner": "langchain-ai",
      "repo": "langgraph"
    }
  },
  "reason": "Repository information requires GitHub search.",
  "confidence": 0.97
}
```

The Supervisor does **not** execute tools.

It only decides **who should execute**.

---

# Research Agent

Purpose:

- Internet Search
- Technical Research
- Current Events

Execution Flow:

```
User Query
     │
     ▼
MCPTools.search()
     │
     ▼
MCP Client
     │
     ▼
Tavily MCP Server
     │
     ▼
Tavily Search API
     │
     ▼
Search Results
     │
     ▼
LLM Summary
```

---

# GitHub Agent

Purpose:

- Search repositories
- Read repository files
- Create GitHub issues

Execution Flow

```
User Query
      │
      ▼
MCPTools.search_repositories()
      │
      ▼
MCP Client
      │
      ▼
GitHub MCP Server
      │
      ▼
GitHub API
      │
      ▼
Repository Results
      │
      ▼
LLM Summary
```

---

# Filesystem Agent

Purpose:

- Read files
- Write files
- List directories

Execution Flow

```
User Query
      │
      ▼
MCPTools.read_file()
      │
      ▼
MCP Client
      │
      ▼
Filesystem MCP Server
      │
      ▼
Local File
      │
      ▼
LLM Summary
```

---

# Response Agent

The Response Agent combines outputs from all executed agents and produces the final natural language answer.

Example:

```
Research Output
      │
GitHub Output
      │
Filesystem Output
      │
      ▼
Response Agent
      │
      ▼
Final Response
```

---

# Aggregator

The Aggregator is a synchronization point in the graph.

Current implementation:

- Pass-through node

Future responsibilities:

- Merge metadata
- Filter failed agent responses
- Track execution statistics
- Confidence scoring
- Ranking outputs

Currently LangGraph already merges state automatically using reducers, so the Aggregator simply forwards the merged state.

---

# MCP Architecture

The project uses the **Model Context Protocol (MCP)** to communicate with external tools.

```
Agent
   │
   ▼
MCPTools
   │
   ▼
MCPClient
   │
   ▼
ClientSession
   │
   ▼
MCP Server
   │
   ▼
External Service
```

The agents never communicate with external APIs directly.

---

# MCP Components

## config.py

Defines every available MCP server.

Example:

```
Filesystem
GitHub
Tavily
```

Each configuration contains:

- command
- arguments
- environment variables

---

## client.py

Implements the MCP client.

Responsibilities:

- Start MCP servers
- Create ClientSession
- Initialize the MCP protocol
- Execute tools
- Cleanly close connections

---

## tools.py

Provides Python wrappers over MCP tools.

Instead of writing:

```python
client.call_tool(...)
```

agents simply use:

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

# End-to-End Request Example

Suppose the user asks:

> Explain the latest LangGraph repository.

Execution flow:

```
User
 │
 ▼
Frontend
 │
 ▼
Backend API
 │
 ▼
GraphBuilder
 │
 ▼
Supervisor
 │
 ▼
Chooses:
Research + GitHub
 │
 ├───────────────┐
 ▼               ▼
Research      GitHub
Agent         Agent
 │               │
 ▼               ▼
Tavily MCP   GitHub MCP
 │               │
 ▼               ▼
Results      Repository Data
 └──────┬────────┘
        ▼
LangGraph merges outputs
        ▼
Aggregator
        ▼
Response Agent
        ▼
Final Answer
```

---

# Design Decisions

## Why LangGraph?

- Stateful execution
- Multi-agent orchestration
- Parallel execution
- Automatic state merging

---

## Why MCP?

Instead of implementing custom integrations for every external service:

```
Research Agent
     │
     ▼
Tavily SDK
```

or

```
GitHub Agent
     │
     ▼
GitHub REST API
```

every interaction follows the same protocol:

```
Agent
     │
     ▼
MCP Client
     │
     ▼
MCP Server
     │
     ▼
External Service
```

This makes adding new services straightforward.

---

## Why BaseAgent?

Common functionality is centralized.

Every specialized agent inherits:

- LLM initialization
- LLM invocation
- Common interface

reducing code duplication.

---

## Why Partial State Updates?

Nodes return only updated fields.

Example:

```python
return {
    "agent_outputs": {
        "research": response
    }
}
```

instead of modifying the shared state directly.

Benefits:

- Parallel execution
- Automatic reducer support
- Immutable workflow
- Easier debugging

---

# Future Improvements

- Dynamic MCP Tool Selection
- MCP Registry
- Agent-specific Inputs
- Memory Support
- RAG Integration
- Human-in-the-loop Approval
- Retry Policies
- LangSmith Tracing
- Streaming Responses
- Tool Selection using LLM