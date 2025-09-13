# ADR-004: Neo4j for Dynamic Knowledge Graph with PostgreSQL Pattern Storage

## Status
Accepted

## Context
Discovered patterns need to be stored, related, and queried efficiently. The system must support dynamic schema evolution as new pattern types emerge, while maintaining fast similarity searches and graph traversals.

## Decision
We will use Neo4j for the knowledge graph (entities and relationships) and PostgreSQL with pgvector for pattern embeddings and similarity search, both running in local Docker containers.

## Consequences

### Positive
- Natural graph representation of relationships
- Efficient graph traversal algorithms
- Dynamic schema evolution supported
- Fast vector similarity search
- ACID compliance for data integrity

### Negative
- Two database systems to maintain
- Additional memory overhead
- Synchronization complexity between stores
- Docker requirement for deployment
- Learning curve for Cypher query language

## Implementation
- Neo4j for entities, relationships, and graph queries
- PostgreSQL + pgvector for pattern embeddings
- Event-driven synchronization between stores
- GraphQL API for unified querying
- Automatic backup and recovery system

## Alternatives Considered
1. **Single Graph Database**: Rejected - poor vector search performance
2. **Single Vector Database**: Rejected - weak relationship modeling
3. **Document Store**: Rejected - inefficient for graph operations
4. **In-Memory Only**: Rejected - data loss risk, size limitations

---
Date: 2025-09-12
Decided by: Data Architecture Team
Reviewed by: Technical Lead