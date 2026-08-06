"""AI provider/model abstraction foundation (ADR-022).

Business contexts depend only on canonical AI capability/use-case contracts. No
provider/model name is ever hard-coded here; adapters are selected through
registries, routing policy and configuration.
"""
