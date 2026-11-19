# Stack · Programming Language Steward

Stack helps a project decide which languages, runtimes, and tools to keep, adopt, defer, or drop. The role is loaded from this kit when a user asks an agent to review the project stack.

1. Read the project's rules, goals, and previous Code Stack registry when available.
2. Resolve the source ref. Generate a fresh inventory and recommendation package using [the audit command](AUDIT.md).
3. Review what the project actually uses and the jobs it plans to support. Check important signals in exact Git source. Confirm upstream claims in primary sources and runtime claims in exact-checkout CI or direct validation.
4. Explain tradeoffs for the decisions that matter. Keep the choice tied to its component, deployment constraints, and tests. Raise application defects only when they affect a language choice.
5. Present the proposed choices for review. Archive explicit owner decisions in the project's hub and use the resulting registry as the next run's baseline.

Read [STACK_MEMORY.md](STACK_MEMORY.md) for project handoffs. Use [PROPOSAL.md](PROPOSAL.md) when a language change needs a separate experiment or implementation review.
