# Story v2 — source-grounded feature coverage

The purchasing assistant is an illustrative workflow design, not an installed
business application. AI Gateway is a descriptive label for the provider runtime
and policy layer, not an independently deployed gateway product.

## Security and runtime evidence

Paths relative to adjacent `xdev-ai-studio` checkout, reviewed 2026-09-24:

- `api/src/hub/providers/runtime.py`: policy filters precede adapter calls;
  workspace/model-type fallback chain, credentials, retryable failures.
- `api/src/hub/iam/policies/provider.py`: provider eligibility by principal and data label.
- `api/src/hub/knowledge/retrieval.py`: sensitivity and department filters.
- `api/src/hub/knowledge/ner.py`: optional NER enhancement to PII rules;
  internal/external engine selection follows data policy; configured NER failure
  blocks rather than silently dropping the protection step.
- `api/src/hub/apps/turn.py` and `apps/prompt_pii.py`: chat masking follows the
  effective configured PII policy. This is not a guarantee of complete detection.
- `api/src/hub/knowledge/ocr.py`, `knowledge/pipeline.py`: OCR and
  configurable knowledge ingestion; retrieval/embedding choice still matters.
- `api/src/hub/egress/guard.py`: tool destination and label controls, auditing.
- `api/src/hub/workflow/nodes/sandbox.py`, `deploy/compose/docker-compose.prod.yml`:
  separate Code service; fail closed when unset. Isolation depends on deployment.
- `web/app/(console)/apps/[id]/workflow/node-types.ts`: 28 node kinds.
- Other user-facing features: route/source map in `docs/feature-coverage.md`.

Claims do not establish penetration testing, regulatory compliance or that every
optional service is configured on every installation. Internal-model routing does
not itself prove all installation traffic stays internal. The blocked illustration
is one policy outcome, not a universal ban on external models.

## Manual-to-scene map

The film explains every manual area at group level. Detailed per-field operations
remain in the 60-topic manual and original narrated tour.

| Manual guide | Story scene |
| --- | --- |
| quickstart | usecase |
| models | gateway |
| knowledge | ingestion |
| sources | ingestion |
| tools | integrations |
| workflows | custom |
| approvals | approval |
| publishing | publish |
| api | publish |
| triggers | publish |
| memory | memory |
| monitoring | quality |
| workspace | operations |
| security | security |
| settings | operations |
| training | quality |
| account | operations |
| admin | operations |
| marketplace | usecase |
| documents | ingestion |
| retrieval | knowledge |
| pipelines | ingestion |
| external-knowledge | knowledge |
| extensions | integrations |
| logs | quality |
| annotations | quality |
| roles | operations |
| storage | operations |
| identity | operations |
| app-config | usecase |
| evaluations | quality |
| inputs | usecase |
| speech-images | memory |
| versions | custom |
| workflow-debug | custom |
| workflow-dsl | custom |
| workflow-library | custom |
| trigger-events | publish |
| tool-api | integrations |
| tool-mcp | integrations |
| tool-workflow | integrations |
| egress | security |
| document-folders | ingestion |
| document-chunks | ingestion |
| memory-review | memory |
| memory-settings | memory |
| training-export | quality |
| workspace-members | operations |
| quotas | publish |
| workspace-keys | publish |
| admin-tenants | operations |
| admin-users | operations |
| admin-health | operations |
| admin-runtime | operations |
| admin-network | operations |
| admin-flags | operations |
| business-processes | usecase |
| web-sharing | publish |
| messaging-channels | publish |
| workflow-nodes | custom |
