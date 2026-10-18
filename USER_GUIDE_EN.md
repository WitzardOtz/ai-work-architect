# AWA: practical guide

[English](USER_GUIDE_EN.md) | [Italiano](USER_GUIDE_IT.md)

AWA helps an AI agent organize work: clarify the outcome, split it into verifiable tasks, choose available and permitted resources, check results, and preserve continuity in project files.

It is a skill with instructions, templates and supporting tools. The wizard is a conversation with the agent using the skill, not a separate application with its own screens. Actual capabilities depend on the environment, tools and permissions.

## 1. Install and start

Download or clone the repository and install its folder as `ai-work-architect` in the skills location supported by your AI environment. `SKILL.md` must be at the folder root. GitHub's automatic ZIP may extract as `ai-work-architect-main`; rename that folder if necessary.

Then tell the agent:

> Use AI Work Architect and help me configure it for first use.

AWA checks existing configuration. If absent, it guides your choice between local and shared memory and verifies accessible storage. Google Drive is optional. An environment without access to the selected memory must state that limitation instead of pretending it saved work.

Memory setup and company setup are independent: having a Vault does not mean your company's policies are already configured.

## 2. If you are the first person configuring the company

Say:

> Let's configure AWA for my company. Help me connect our existing documents and prepare context that colleagues can reuse.

AWA guides you through:

1. Identifying the organization and scope: the whole company, a team or a specific project.
2. Choosing a private profile location and the documents or links to consult. You can start without documents, explicitly leaving information to be verified.
3. Separating background context, procedures, mandatory policies and preferences. Extracted rules retain source references; assumptions do not become approved policies.
4. Reviewing inspected sources, missing access, rules, conflicts and unknown information.
5. Confirming which profile to use within the chosen scope and saving a private reference for resuming work.

The result may include a compact profile, a source index and a pointer from the project. Original documents remain in place; AWA retrieves only relevant material. Colleague reuse requires a shared reference reachable by recipients: a local path on your PC is insufficient.

### The message for colleagues

After the first reusable setup, AWA automatically prepares a message to copy to colleagues. It includes the actual profile reference, scope and instruction to connect it without rebuilding it. If the shared reference is missing, the message remains a draft and AWA explains what to complete. It neither sends the message nor grants access automatically.

Illustrative example, to complete with actual details:

> We have configured our company context for AWA. Install the skill if needed, then ask: "Connect the existing company profile at [shared link] for [company and scope]. Verify my access and the current version, show the applicable rules, and ask only for missing details about my role and project. Reuse the configured context."

## 3. If a colleague has already configured the company

Use their message and profile link. AWA checks your access, environment and version, clarifies your scope, and fills only missing details. The shared company profile is reused; your role, access and project binding remain separate from the first configurator's.

| Level | Contents |
|---|---|
| Company | Sources, policies, procedures, terminology and common preferences |
| User and environment | Role, actual access and available tools |
| Project | Objective, applicable constraints, plan, checkpoint and log |

Sharing a profile does not give everyone the same permissions. If a source is unreachable, AWA reports the limitation. It does not automatically copy the whole archive or the colleague's authorizations.

## 4. During work

AWA applies relevant constraints before selecting tools, environments and data paths. For example, when a confirmed rule prohibits sending confidential documents to external services, an external tool's technical availability does not make it usable for those documents.

For work spanning sessions, AWA keeps short tasks, a plan, checkpoint and log in project files. The checkpoint records completed/open work, changed files, decisions, checks actually run and their results, and the next concrete action. Start with [project-work.md](templates/project-work.md).

On resumption it checks the profile reference and version. If relevant changes or stale sources appear, it clarifies their effect before the affected action. This is an agent check during work; there is no service automatically notifying every user.

You can ask to update policies, switch organizations or return to personal mode. Disconnecting a profile does not automatically delete company documents or previous records.

## 5. Data locations and limitations

The public repository contains only the skill, instructions and generic templates. Filled company profiles, documents, personal configuration, events and caches remain outside the public package. The Vault is the compact execution record, not a copy of the company knowledge base.

The AI host must be authorized to process the material before it is opened. The profile guides the agent but does not replace permissions, network controls or infrastructure protection and does not certify compliance. Profile bindings are agent-managed: `awa_cli.py` manages the Vault but does not automatically load or enforce company policies.

Structure, references and publication have been verified. The company workflow still needs validation through real onboarding; improved decision efficacy has not been established. The [improvement protocol](references/controlled-improvement.md) supports evidence-based comparisons of variants.

## References

- [First-use setup](references/first-run-setup.md)
- [Company wizard and colleague instructions](references/organization-context-setup.md)
- [Company profile template](templates/organization-profile.md)
- [Source index](templates/organization-sources.md)
- [Changelog](CHANGELOG.md)
- [Apache License 2.0: English explanation](docs/LICENSE_EN.md), covering the AWA package rather than your private documents
