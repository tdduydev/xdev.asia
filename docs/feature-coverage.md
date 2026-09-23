# AI Studio feature coverage — 2026-09-23

Source: adjacent `xdev-ai-studio` checkout at `041daf6` plus current workspace
changes. Read-only source review; no changes were made to the product backend.

The landing page now links to 60 localized topic guides (120 articles). Topics
cover the current console and administration areas, including application
configuration, speech/image model selection, knowledge ingestion and retrieval,
external services, workflow node families, moderation extensions, evaluation,
publication, monitoring, identity, storage and instance operations.

This is a product documentation inventory, not proof that every integration has
been deployed or that all backend paths have passed acceptance testing. Provider,
sandbox, permission and deployment prerequisites are stated in the relevant guides.
Internal design-system screens and redirects are not advertised as user features.

## Source-to-guide map

Route families may be explained by several guides; screenshots show synthetic
data and illustrate the relevant interface. Configuration and evaluation guides
currently reuse their related editor/monitoring overview screenshots.

| Source page under `web/app` | Guide or scope |
| --- | --- |
| `(admin)/admin/flags` | admin (organisations, accounts, health, runtime, network, flags) |
| `(admin)/admin/health` | admin (organisations, accounts, health, runtime, network, flags) |
| `(admin)/admin/network` | admin (organisations, accounts, health, runtime, network, flags) |
| `(admin)/admin` | admin (organisations, accounts, health, runtime, network, flags) |
| `(admin)/admin/runtime` | admin (organisations, accounts, health, runtime, network, flags) |
| `(admin)/admin/tenants` | admin (organisations, accounts, health, runtime, network, flags) |
| `(admin)/admin/users` | admin (organisations, accounts, health, runtime, network, flags) |
| `(auth)/accept-invite` | account / identity / quickstart (sign-in and account prerequisites) |
| `(auth)/forgot-password` | account / identity / quickstart (sign-in and account prerequisites) |
| `(auth)/mfa` | account / identity / quickstart (sign-in and account prerequisites) |
| `(auth)/reset-password` | account / identity / quickstart (sign-in and account prerequisites) |
| `(auth)/signin` | account / identity / quickstart (sign-in and account prerequisites) |
| `(auth)/signup` | account / identity / quickstart (sign-in and account prerequisites) |
| `(auth)/verify-email` | account / identity / quickstart (sign-in and account prerequisites) |
| `(console)/account` | account |
| `(console)/apps/[id]/annotations` | annotations |
| `(console)/apps/[id]/api-access` | api |
| `(console)/apps/[id]/deploy` | publishing |
| `(console)/apps/[id]/logs` | logs |
| `(console)/apps/[id]/monitoring` | evaluations / monitoring |
| `(console)/apps/[id]` | quickstart / app-config |
| `(console)/apps/[id]/workflow` | workflows |
| `(console)/apps` | quickstart / app-config |
| `(console)/datasets/[id]/documents/[docId]` | knowledge / documents / sources / retrieval / pipelines / external-knowledge |
| `(console)/datasets/[id]` | knowledge / documents / sources / retrieval / pipelines / external-knowledge |
| `(console)/datasets/[id]/retrieval` | knowledge / documents / sources / retrieval / pipelines / external-knowledge |
| `(console)/datasets/[id]/settings` | knowledge / documents / sources / retrieval / pipelines / external-knowledge |
| `(console)/datasets/[id]/sources` | knowledge / documents / sources / retrieval / pipelines / external-knowledge |
| `(console)/datasets/connect` | knowledge / documents / sources / retrieval / pipelines / external-knowledge |
| `(console)/datasets/create` | knowledge / documents / sources / retrieval / pipelines / external-knowledge |
| `(console)/datasets` | knowledge / documents / sources / retrieval / pipelines / external-knowledge |
| `(console)/datasets/pipeline` | knowledge / documents / sources / retrieval / pipelines / external-knowledge |
| `(console)/integrations/data-source` | marketplace / models / sources / tools / extensions / triggers / security |
| `(console)/integrations/extension` | marketplace / models / sources / tools / extensions / triggers / security |
| `(console)/integrations/model-provider` | marketplace / models / sources / tools / extensions / triggers / security |
| `(console)/integrations` | marketplace / models / sources / tools / extensions / triggers / security |
| `(console)/integrations/tools/api` | marketplace / models / sources / tools / extensions / triggers / security |
| `(console)/integrations/tools/built-in` | marketplace / models / sources / tools / extensions / triggers / security |
| `(console)/integrations/tools/egress` | marketplace / models / sources / tools / extensions / triggers / security |
| `(console)/integrations/tools/mcp` | marketplace / models / sources / tools / extensions / triggers / security |
| `(console)/integrations/tools` | marketplace / models / sources / tools / extensions / triggers / security |
| `(console)/integrations/tools/workflow` | marketplace / models / sources / tools / extensions / triggers / security |
| `(console)/integrations/trigger` | marketplace / models / sources / tools / extensions / triggers / security |
| `(console)/marketplace` | marketplace |
| `(console)/memories` | memory |
| `(console)/monitoring` | monitoring |
| `(console)` | Navigation / guide entry point |
| `(console)/settings/branding` | settings |
| `(console)/settings/data-protection` | security |
| `(console)/settings/design-system` | Internal component catalog; not a user capability |
| `(console)/settings/external-knowledge` | external-knowledge |
| `(console)/settings/identity` | identity |
| `(console)/settings/roles` | roles |
| `(console)/settings/storage` | storage |
| `(console)/settings/training` | training |
| `(console)/settings/workspace` | workspace |
| `(console)/workflow/gates` | approvals |
| `(console)/workflow/triggers` | triggers |
| `(webapp)/s/[token]` | publishing (shared application) |

## Additional source handles

- `apps/[id]/features-panel.tsx`: speech, text-to-speech, image models, business processes and conversation settings.
- `apps/[id]/monitoring/evals-panel.tsx`: test datasets, run results and compatible-run comparisons.
- `apps/[id]/workflow/node-types.ts`: node inventory and code sandbox prerequisite.
- `datasets/[id]/retrieval-settings.tsx`: retrieval modes, Top K, thresholds and reranking.
- `integrations/extension/page.tsx`: HTTP moderation contract, not downloadable plugins.
- `settings/external-knowledge/page.tsx`: outbound retrieval versus imported data.
- `settings/storage/page.tsx`: storage state, quotas, orphan review and migration sequence.

All paths above are relative to `web/app/(console)/` in the product checkout.

## Detailed manual expansion

The eight navigation groups now include nested task guides for variables, speech,
versions, business processes, all 28 workflow node kinds, debugging, DSL import,
reusable graphs, webhook events, API/MCP/workflow tools, egress, document folders
and chunks, memory review and policy, training export, web sharing, messaging,
workspace members/keys/quotas, and six individual instance-administration areas.
Flags, tenant overview and network inspection are documented as read-only;
available runtime and account actions depend on instance-administrator access.

The product frontend logo component now uses the approved X + AI/STUDIO SVG,
including light/dark variants and the existing custom workspace-logo fallback.
Screenshots were recaptured from that frontend using synthetic API fixtures;
this does not establish backend integration acceptance. The guide index banner
was generated with the built-in imagegen tool; its prompt is stored in
`docs/brand/guide-banner-prompt.md`.

### Current guide inventory

| Guide | Parent | Title (English) |
| --- | --- | --- |
| quickstart | — | Create your first application |
| models | — | Connect AI models |
| knowledge | — | Build a knowledge base |
| sources | — | Connect data sources |
| tools | — | Give agents tools |
| workflows | — | Design visual workflows |
| approvals | — | Review approval requests |
| publishing | — | Publish and share |
| api | — | Use the application API and MCP |
| triggers | — | Automate with triggers |
| memory | — | Manage long-term memory |
| monitoring | — | Monitor usage and quality |
| workspace | — | Manage your workspace |
| security | — | Configure data protection |
| settings | — | Set up branding, storage and identity |
| training | — | Fine-tune a model |
| account | — | Manage your account |
| admin | — | Administer the instance |
| marketplace | — | Explore model providers |
| documents | — | Manage documents and chunks |
| retrieval | — | Test and tune retrieval |
| pipelines | — | Design knowledge ingestion pipelines |
| external-knowledge | — | Connect external knowledge |
| extensions | — | Use extension APIs for moderation |
| logs | — | Read logs and execution traces |
| annotations | — | Set up canned answers |
| roles | — | Create roles and assign permissions |
| storage | — | Manage S3 storage |
| identity | — | Configure single sign-on |
| app-config | — | Configure applications and multimodal features |
| evaluations | — | Evaluate and compare quality |
| inputs | app-config | Variables and input forms |
| speech-images | app-config | Speech and image generation |
| versions | publishing | Version history and restoration |
| workflow-debug | workflows | Run, trace and compare workflows |
| workflow-dsl | workflows | Import/export DSL and environment variables |
| workflow-library | workflows | Reuse snippets and edit the canvas |
| trigger-events | triggers | Webhooks, schedules and event retries |
| tool-api | tools | Configure API tools |
| tool-mcp | tools | Connect MCP servers |
| tool-workflow | tools | Use workflows as tools |
| egress | security | Manage outbound connections |
| document-folders | documents | Folders, filtering and moving documents |
| document-chunks | documents | Inspect and edit knowledge chunks |
| memory-review | memory | Review memories and their evidence |
| memory-settings | memory | Configure, retain and disable memory |
| training-export | training | Export training data |
| workspace-members | workspace | Invite members and control access |
| quotas | workspace | Token and request quotas |
| workspace-keys | api | Workspace API keys and MCP capabilities |
| admin-tenants | admin | Organisations and instance quotas |
| admin-users | admin | Instance accounts |
| admin-health | admin | Check service health |
| admin-runtime | admin | Change runtime settings |
| admin-network | admin | Network zones and destinations |
| admin-flags | admin | Control feature flags |
| business-processes | app-config | Design agent business processes |
| web-sharing | publishing | Web apps, embedding and chat experience |
| messaging-channels | publishing | Connect messaging channels |
| workflow-nodes | workflows | Workflow node reference |
