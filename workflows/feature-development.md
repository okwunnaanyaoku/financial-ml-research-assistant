---
name: feature-development
description: Feature development workflow using appropriate development agents
---

# Feature Development Workflow

**Feature Request**: $ARGUMENTS

This command orchestrates a systematic approach to feature development using our development agent team.

## Phase 1: Requirements Analysis (System Architect)
```
Use system-architect agent to:
- Analyze the feature request: "$ARGUMENTS"
- Define functional and non-functional requirements
- Identify system boundaries and integration points
- Assess impact on existing architecture
- Document technical specifications and acceptance criteria
```

## Phase 2: Architecture Design (System Architect)
```
Use system-architect agent to:
- Design the feature architecture and components
- Define APIs, data models, and service interfaces
- Plan database schema changes if needed
- Identify dependencies and integration patterns
- Create technical design documentation
```

## Phase 3: Security Review (Security Specialist)
```
Use security-specialist agent to:
- Review feature design for security implications
- Identify potential security vulnerabilities
- Recommend authentication and authorization patterns
- Define data protection and privacy requirements
- Document security considerations and mitigations
```

## Phase 4: Performance Planning (Performance Optimizer)
```
Use performance-optimizer agent to:
- Analyze performance requirements for the feature
- Identify potential bottlenecks and optimization opportunities
- Plan caching strategies and database optimization
- Define performance metrics and monitoring
- Document performance considerations
```

## Phase 5: Implementation Planning (Backend/Frontend Developer)
```
Use appropriate developer agent to:
- Break down feature into development tasks
- Estimate development effort and timeline
- Plan implementation phases and milestones
- Identify required libraries and dependencies
- Create development task breakdown
```

## Phase 6: Database Design (Backend Developer)
```
Use backend-developer agent if database changes needed:
- Design database schema modifications
- Plan migration scripts and data transformations
- Ensure data integrity and consistency
- Optimize database queries and indexes
- Document database changes
```

## Phase 7: API Design (Backend Developer)
```
Use backend-developer agent for API development:
- Design RESTful APIs and endpoints
- Define request/response schemas
- Implement API validation and error handling
- Create API documentation and examples
- Ensure API security and rate limiting
```

## Phase 8: Frontend Implementation (Frontend Developer)
```
Use frontend-developer agent for UI development:
- Implement user interface components
- Integrate with backend APIs
- Ensure responsive design and accessibility
- Implement client-side validation and error handling
- Create interactive user experiences
```

## Phase 9: Backend Implementation (Backend Developer)
```
Use backend-developer agent for server-side logic:
- Implement business logic and data processing
- Integrate with external services and APIs
- Implement background jobs and scheduled tasks
- Ensure scalability and error handling
- Create comprehensive unit tests
```

## Phase 10: Integration Testing (QA Engineer)
```
Use qa-engineer agent to:
- Create comprehensive test plans for the feature
- Test integration between frontend and backend
- Validate API contracts and data flow
- Test edge cases and error scenarios
- Document test results and coverage
```

## Phase 11: Code Review (Code Reviewer)
```
Use code-reviewer agent to:
- Review all implementation code for quality
- Ensure adherence to coding standards and best practices
- Verify security measures are properly implemented
- Check for performance considerations
- Approve code for deployment
```

## Phase 12: Performance Testing (Performance Optimizer)
```
Use performance-optimizer agent to:
- Execute performance tests on the new feature
- Measure response times and resource utilization
- Identify and resolve performance bottlenecks
- Validate performance meets requirements
- Document performance benchmarks
```

## Phase 13: Security Testing (Security Specialist)
```
Use security-specialist agent to:
- Perform security testing on the feature
- Validate authentication and authorization
- Test for common vulnerabilities (OWASP Top 10)
- Ensure data protection measures are working
- Document security test results
```

## Phase 14: User Acceptance Testing (QA Engineer)
```
Use qa-engineer agent to:
- Coordinate user acceptance testing
- Validate feature meets business requirements
- Test user workflows and scenarios
- Gather and document user feedback
- Ensure feature is ready for production
```

## Phase 15: Documentation (Documentation Agent)
```
Use documentation agent to:
- Create user documentation and guides
- Update technical documentation
- Create API documentation if applicable
- Update system architecture diagrams
- Create deployment and maintenance guides
```

## Phase 16: Deployment Planning (DevOps Engineer)
```
Use devops-engineer agent to:
- Plan feature deployment strategy
- Prepare deployment scripts and configurations
- Set up monitoring and alerting for the feature
- Plan feature flags and gradual rollout
- Create rollback procedures
```

## Feature Complexity Workflows

### Simple Features (UI Changes, Basic CRUD)
- Skip detailed architecture review
- Streamlined implementation with basic testing
- Direct deployment after code review

### Medium Features (New Components, API Changes)
- Standard workflow with emphasis on integration testing
- Performance review for API changes
- Staged deployment with monitoring

### Complex Features (Multi-system Integration)
- Full workflow with detailed architecture design
- Extensive security and performance reviews
- Gradual rollout with feature flags

## Quality Gates

### Before Implementation
- Requirements are clearly defined and approved
- Architecture design is complete and reviewed
- Security and performance considerations are documented

### Before Testing
- Implementation is complete and code reviewed
- Unit tests pass with adequate coverage
- Integration points are validated

### Before Deployment
- All testing phases are complete
- Performance benchmarks are met
- Security requirements are satisfied
- Documentation is complete

## Communication Protocol

Each agent should document:
1. **Current Status**: What phase of development is active
2. **Progress**: What has been completed and what's in progress
3. **Dependencies**: What's needed from other agents or systems
4. **Risks**: Any potential issues or blockers identified
5. **Next Steps**: What needs to happen next

## Success Criteria

Feature development is considered complete when:
- ✅ All functional requirements are implemented
- ✅ Non-functional requirements are met
- ✅ All tests pass including integration and performance tests
- ✅ Security requirements are satisfied
- ✅ Code quality standards are maintained
- ✅ Documentation is complete and accurate
- ✅ Feature is successfully deployed to production
- ✅ User acceptance criteria are met

Use this workflow to ensure systematic and thorough feature development.