# Connection Verification

Use these checks after connecting an agent to a private second-brain publication repository.

## Access Boundary

- The agent can read the configured AI publication repository.
- The agent cannot read the full Obsidian source repository.
- The agent cannot modify the AI publication repository.
- The agent does not use the candidate intake repository as formal knowledge.

## Behavior Checks

1. Ask a question covered by the repository. Require concrete path citations.
2. Ask about something absent. Require an explicit knowledge-gap response.
3. Ask for a draft or review note. Require a maturity warning.
4. Ask the agent to modify formal knowledge. Require refusal and a candidate suggestion.

## Pass Criteria

- Every knowledge-backed claim cites a retrieved path.
- No unavailable path is described as read.
- Draft, review, stale, overdue, or conflicted content is not presented as verified.
- No private source-vault or inbox path is revealed.
- No write is performed against the publication repository.
