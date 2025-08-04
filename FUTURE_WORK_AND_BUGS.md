# Future Work and Known Bugs

## 🚧 Planned Features & Enhancements

- **Add Elicitation Example**

  - Create a new prompt and workflow demonstrating elicitation (interactive, step-by-step information gathering)
  - Document usage and integration in the prompts guide

- **Integration**

  - Add support for external identity providers (LDAP, SSO)
  - Enable webhook notifications for high-privilege changes

## 🐞 Known Bugs & Issues

- **Prompts Not Showing in Inspector or Copilot**

  - Currently, registered prompts do not appear in the MCP Inspector or Copilot UI.
  - Workaround: Prompts are available via direct API/tool calls, but not discoverable in the UI.
  - Status: Needs investigation—likely a registration or metadata issue in the MCP server integration.

- **Randomized Permissions in Seeding**

  - The database seeding script assigns random permissions, which may lead to inconsistent demo results.
  - Consider using a deterministic or fixed seed for reproducible demos.

- **No Elicitation Example Yet**

  - The system currently lacks a prompt or workflow demonstrating elicitation (stepwise information gathering).

- **Prompt Parameter Validation**

  - Some prompts may not validate input parameters robustly (e.g., missing developer/resource names).

- **Prompt/Tool Error Handling**
  - Improve error messages and fallback behavior for failed tool or prompt invocations.
