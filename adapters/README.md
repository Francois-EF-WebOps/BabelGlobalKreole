# Integration contract

The initial interface is a versioned file bundle, not an assumed live API.

Portable formats: Markdown, JSON Schema, JSON/JSONL, YAML and documented CSV. HTTP APIs may be added when a real consumer and maintainable host exist.

Consumers declare supported framework/schema versions, record types/fields, domain, language/variety scope, handling of unknown/disputed/restricted/deprecated records, validation method, update cadence and rollback behaviour.

Consumers must not silently treat draft/proposed records as accepted. Unknown/restricted records cannot be presented as validated reusable content.

Planned adapters for LLM retrieval, translation, speech and publishing are contracts, not implemented integrations. Future APIs must document authentication, cost, rate limits, data handling, offline fallback and reproducible tests. No paid API is required for the core files.
