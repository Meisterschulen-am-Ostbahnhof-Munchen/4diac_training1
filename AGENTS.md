# Agents & Skills

This document describes the available agents, subagents, and skills configured for this workspace.

## Available Skills

Skills are specialized instructions, scripts, and resources that extend the capabilities of the agent for specific tasks.



### [iec61499-creator](.agents/skills/iec61499-creator/SKILL.md)
Use this skill to create, edit, structure, and validate IEC 61499 library elements (Basic FBs, Composite FBs, Service Interface FBs, Adapters, Subapps, Devices, Resources, Systems, DataTypes) against standard schemas.


---

## Available Subagents

Subagents can be invoked to perform tasks in separate contexts, helping organize work or delegate tasks.

* **research**: A read-only subagent for exploring the codebase and reading files. Best used when a task requires many search and read operations that would clutter the main context.
* **self**: A subagent inheriting the full configuration, tools, and system prompts of the parent agent, capable of executing write operations and running commands.
