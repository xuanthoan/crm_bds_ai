"""Framework-free shared primitives.

`shared_kernel` only accepts primitive/value abstractions approved by Architecture
review. It MUST NOT import web/ORM/broker frameworks and MUST NOT contain business
concepts (Customer, Lead, Product, ...). This is enforced by architecture tests.
"""
