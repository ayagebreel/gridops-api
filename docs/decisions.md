# Architecture Decisions

## Work Order Status Transitions

The system supports the following statuses:

- open
- assigned
- in_progress
- closed
- cancelled

## Allowed Transitions

| From | To |
|---|---|
| open | assigned |
| open | cancelled |
| assigned | in_progress |
| assigned | cancelled |
| in_progress | closed |

## Decision: Closed Orders Cannot Be Reopened

A closed work order represents a completed maintenance
operation.

If a new problem occurs after closure, a new fault
and work order should be created.

This preserves the history of maintenance operations
and avoids changing previously completed records.

Cancelled work orders are also terminal.