# Project Highlights

1. Dynamically add tools and sub-agents since the mapping is externalized using `registry.yaml` and not tightly coupled in the code.  
   Any sub-agent or tool can be enabled, disabled, or reordered without changing the code—only by modifying the registry configuration.

2. Every agent inside the system has its own configuration, allowing separate LLMs and providers per agent.  
   This helps in optimizing performance and reducing costs.

3. Agent, tool, and sub-agent builders are developed as a separate library and are not tightly coupled with the application code.  
   This makes the components reusable across multiple projects.

4. Used **UV** as the package and project manager for better dependency management and clean shipping.

---

# Scope to Expand

1. Agent Builder and Agent Registry can be moved as an installable library and included as a dependency in any new project.

2. A Bedrock-based project initializer can be developed to create a starter workspace for new projects with:
   - Required dependencies
   - Standard folder structure
   - Sample agent and registry configuration
