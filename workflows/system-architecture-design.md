---
name: system-architecture-design
description: System architecture design workflow using appropriate development agents
---

# System Architecture Design Workflow

**Architecture Requirements**: $ARGUMENTS

This command orchestrates a systematic approach to system architecture design using our development agent team.

## Phase 1: Requirements Analysis (System Architect)
```
Use system-architect agent to:
- Analyze architecture requirements: "$ARGUMENTS"
- Define functional and non-functional requirements
- Identify system boundaries, constraints, and assumptions
- Analyze stakeholder needs and business objectives
- Document architectural drivers and quality attributes
```

## Phase 2: Domain Analysis (Domain Expert)
```
Use appropriate domain expert agent to:
- Analyze business domain and core concepts
- Identify domain entities, relationships, and workflows
- Define domain boundaries and bounded contexts
- Understand business rules and processes
- Document domain model and key abstractions
```

## Phase 3: Technology Assessment (System Architect)
```
Use system-architect agent to:
- Evaluate technology options and architectural patterns
- Assess existing systems and integration requirements
- Analyze scalability, performance, and reliability needs
- Consider security, compliance, and operational requirements
- Recommend technology stack and architectural approach
```

## Phase 4: Security Architecture Planning (Security Specialist)
```
Use security-specialist agent to:
- Define security requirements and threat model
- Design authentication and authorization architecture
- Plan data protection and encryption strategies
- Identify security controls and compliance needs
- Document security architecture and policies
```

## Phase 5: Performance Architecture Planning (Performance Optimizer)
```
Use performance-optimizer agent to:
- Define performance requirements and service levels
- Design for scalability and high availability
- Plan caching strategies and data distribution
- Identify performance bottlenecks and mitigation strategies
- Document performance architecture and monitoring needs
```

## Phase 6: System Decomposition (System Architect)
```
Use system-architect agent to:
- Decompose system into logical components and services
- Define component interfaces and communication patterns
- Design service boundaries and data ownership
- Plan microservices vs monolith architecture decisions
- Document system structure and component relationships
```

## Phase 7: Data Architecture Design (Backend Developer)
```
Use backend-developer agent to:
- Design data models and database schemas
- Plan data storage and persistence strategies
- Design data flow and integration patterns
- Consider data consistency and transaction requirements
- Document data architecture and governance policies
```

## Phase 8: API and Integration Design (System Architect)
```
Use system-architect agent to:
- Design APIs and service contracts
- Plan integration patterns and communication protocols
- Design event-driven architectures and messaging
- Plan external system integrations
- Document API specifications and integration guides
```

## Phase 9: Infrastructure Architecture (DevOps Engineer)
```
Use devops-engineer agent to:
- Design deployment and infrastructure architecture
- Plan containerization and orchestration strategies
- Design CI/CD pipelines and deployment processes
- Plan monitoring, logging, and observability
- Document infrastructure requirements and automation
```

## Phase 10: Frontend Architecture (Frontend Developer)
```
Use frontend-developer agent to:
- Design frontend application architecture
- Plan user interface frameworks and patterns
- Design client-server communication and state management
- Plan responsive design and progressive web app features
- Document frontend architecture and development guidelines
```

## Phase 11: Architecture Validation (System Architect)
```
Use system-architect agent to:
- Validate architecture against requirements and constraints
- Perform architecture trade-off analysis
- Identify architectural risks and mitigation strategies
- Create architecture decision records (ADRs)
- Validate architecture with stakeholders
```

## Phase 12: Prototype Development (Backend/Frontend Developer)
```
Use appropriate developer agents to:
- Build proof-of-concept prototypes for key components
- Validate architectural decisions with working code
- Test integration patterns and communication flows
- Validate performance and scalability assumptions
- Document prototype findings and recommendations
```

## Phase 13: Security Review (Security Specialist)
```
Use security-specialist agent to:
- Review complete architecture for security vulnerabilities
- Validate security controls and protection mechanisms
- Ensure compliance with security standards and regulations
- Identify security testing and validation requirements
- Approve security aspects of the architecture
```

## Phase 14: Performance Review (Performance Optimizer)
```
Use performance-optimizer agent to:
- Review architecture for performance and scalability
- Validate performance targets can be achieved
- Identify performance testing requirements
- Plan performance monitoring and optimization strategies
- Approve performance aspects of the architecture
```

## Phase 15: Implementation Planning (System Architect)
```
Use system-architect agent to:
- Create detailed implementation roadmap and phases
- Define development team structure and responsibilities
- Plan architectural governance and review processes
- Create technical debt management strategy
- Document implementation guidelines and standards
```

## Phase 16: Documentation and Communication (Documentation Agent)
```
Use documentation agent to:
- Create comprehensive architecture documentation
- Design architecture diagrams and visual models
- Create developer onboarding and reference guides
- Document architectural patterns and best practices
- Create stakeholder communication materials
```

## Architecture Complexity Levels

### Simple Architecture (Single Application)
- Focus on component design and data modeling
- Streamlined security and performance planning
- Basic infrastructure and deployment planning

### Medium Architecture (Multi-Service System)
- Include detailed service boundaries and APIs
- Comprehensive security and performance design
- Advanced infrastructure and integration planning

### Complex Architecture (Distributed Enterprise System)
- Full workflow with detailed domain analysis
- Extensive security, performance, and compliance planning
- Enterprise-level infrastructure and governance

## Quality Gates

### Requirements Phase
- All functional and non-functional requirements are clearly defined
- Stakeholder needs and business objectives are understood
- Architectural drivers and constraints are documented

### Design Phase
- Architecture satisfies all requirements and constraints
- Security and performance requirements are addressed
- Technology choices are justified and documented

### Validation Phase
- Architecture has been validated through prototypes
- All architectural risks have been identified and mitigated
- Stakeholders approve the architectural approach

### Implementation Readiness
- Implementation plan is detailed and realistic
- Development teams understand their responsibilities
- Architectural governance processes are established

## Communication Protocol

Each agent should document:
1. **Current Status**: What architecture phase is active
2. **Decisions**: Key architectural decisions made and rationale
3. **Risks**: Identified risks and mitigation strategies
4. **Dependencies**: Dependencies on other teams or systems
5. **Next Steps**: What needs to be designed or validated next

## Success Criteria

System architecture design is considered complete when:
- ✅ All requirements are addressed by the architecture
- ✅ Architecture is validated through analysis and prototypes
- ✅ Security and performance requirements are satisfied
- ✅ Technology choices are appropriate and justified
- ✅ Implementation plan is detailed and realistic
- ✅ Architecture is well-documented and communicated
- ✅ Stakeholders approve the architectural approach
- ✅ Development teams are ready to implement

## Architecture Documentation Deliverables

### High-Level Documentation
- Architecture overview and system context
- Key architectural decisions and rationale
- Quality attributes and trade-offs
- Architectural principles and patterns

### Detailed Design Documentation
- Component and service specifications
- Data models and API contracts
- Security architecture and policies
- Infrastructure and deployment guides

### Implementation Guidance
- Development standards and guidelines
- Architectural governance processes
- Technical debt management strategy
- Implementation roadmap and phases

## Architectural Principles

1. **Simplicity**: Keep the architecture as simple as possible while meeting requirements
2. **Modularity**: Design for loose coupling and high cohesion
3. **Scalability**: Plan for growth and changing requirements
4. **Security**: Build security in from the ground up
5. **Testability**: Design for easy testing and validation
6. **Maintainability**: Consider long-term maintenance and evolution
7. **Performance**: Meet performance requirements efficiently
8. **Resilience**: Design for failure and recovery

Use this workflow to ensure systematic and comprehensive system architecture design.