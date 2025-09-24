---
name: performance-optimization
description: Performance optimization workflow using appropriate development agents
---

# Performance Optimization Workflow

**Performance Target**: $ARGUMENTS

This command orchestrates a systematic approach to performance optimization using our development agent team.

## Phase 1: Performance Baseline (Performance Optimizer)
```
Use performance-optimizer agent to:
- Analyze current performance metrics for: "$ARGUMENTS"
- Establish baseline measurements (response time, throughput, resource usage)
- Identify performance bottlenecks and problem areas
- Profile application under typical and peak load conditions
- Document performance requirements and goals
```

## Phase 2: System Profiling (Performance Optimizer)
```
Use performance-optimizer agent to:
- Deep dive into system performance using profiling tools
- Analyze CPU utilization, memory usage, and I/O patterns
- Identify slow database queries and network requests
- Map performance hotspots in the application code
- Document detailed performance analysis findings
```

## Phase 3: Architecture Review (System Architect)
```
Use system-architect agent to:
- Review system architecture for performance limitations
- Identify architectural bottlenecks and scalability issues
- Evaluate caching strategies and data flow patterns
- Assess service communication and integration points
- Recommend architectural improvements for performance
```

## Phase 4: Database Optimization Analysis (Backend Developer)
```
Use backend-developer agent to:
- Analyze database query performance and execution plans
- Identify missing indexes and suboptimal queries
- Review database schema design for performance impact
- Evaluate connection pooling and transaction management
- Plan database optimization strategies
```

## Phase 5: Caching Strategy Design (Performance Optimizer)
```
Use performance-optimizer agent to:
- Design comprehensive caching strategy
- Identify cacheable data and optimal cache levels
- Plan cache invalidation and consistency strategies
- Evaluate different caching technologies (Redis, Memcached, CDN)
- Document caching implementation approach
```

## Phase 6: Code Optimization Planning (Performance Optimizer)
```
Use performance-optimizer agent to:
- Identify code-level optimization opportunities
- Plan algorithm improvements and data structure optimizations
- Evaluate asynchronous processing and parallel execution
- Design performance-critical code refactoring
- Prioritize optimizations by impact and effort
```

## Phase 7: Database Optimization Implementation (Backend Developer)
```
Use backend-developer agent to:
- Optimize database queries and add appropriate indexes
- Implement connection pooling and query optimization
- Refactor database access patterns for efficiency
- Implement database-level caching where appropriate
- Create database performance monitoring
```

## Phase 8: Application-Level Caching (Backend Developer)
```
Use backend-developer agent to:
- Implement application-level caching solutions
- Add caching to frequently accessed data and computations
- Implement cache warming and pre-loading strategies
- Create cache monitoring and invalidation mechanisms
- Optimize cache hit ratios and performance
```

## Phase 9: Algorithm and Code Optimization (Performance Optimizer)
```
Use performance-optimizer agent to:
- Optimize algorithms for better time and space complexity
- Implement more efficient data structures
- Optimize critical code paths and hot spots
- Implement asynchronous processing where beneficial
- Reduce computational overhead and resource usage
```

## Phase 10: Frontend Performance Optimization (Frontend Developer)
```
Use frontend-developer agent to:
- Optimize client-side performance and loading times
- Implement code splitting and lazy loading
- Optimize images, assets, and bundle sizes
- Implement efficient rendering and DOM manipulation
- Add client-side caching and service workers
```

## Phase 11: Network and I/O Optimization (Performance Optimizer)
```
Use performance-optimizer agent to:
- Optimize network requests and reduce latency
- Implement request batching and connection reuse
- Optimize file I/O and streaming operations
- Implement compression and data transfer optimization
- Reduce network round trips and payload sizes
```

## Phase 12: Infrastructure Optimization (DevOps Engineer)
```
Use devops-engineer agent to:
- Optimize infrastructure configuration for performance
- Implement auto-scaling and load balancing strategies
- Optimize server configurations and resource allocation
- Implement CDN and geographic distribution
- Monitor and tune infrastructure performance
```

## Phase 13: Performance Testing (Performance Optimizer)
```
Use performance-optimizer agent to:
- Execute comprehensive performance testing
- Load test optimized components under realistic conditions
- Stress test to identify new performance limits
- Validate performance improvements against baseline
- Document performance gains and remaining bottlenecks
```

## Phase 14: Monitoring and Alerting (DevOps Engineer)
```
Use devops-engineer agent to:
- Implement comprehensive performance monitoring
- Set up alerting for performance degradation
- Create performance dashboards and reporting
- Implement automated performance regression detection
- Establish ongoing performance monitoring processes
```

## Phase 15: Code Review (Code Reviewer)
```
Use code-reviewer agent to:
- Review all performance optimization changes
- Ensure optimizations don't compromise code quality
- Verify performance improvements are maintainable
- Check for potential side effects or regressions
- Approve optimizations before deployment
```

## Phase 16: Quality Assurance (QA Engineer)
```
Use qa-engineer agent to:
- Test optimized system for functional correctness
- Validate that optimizations don't break existing features
- Test edge cases and error scenarios
- Ensure performance improvements are stable
- Document test results and validation
```

## Performance Optimization Scope

### Micro-Optimizations (Single Function/Algorithm)
- Focus on algorithm efficiency and code-level improvements
- Quick implementation and testing cycle
- Immediate deployment after validation

### Component-Level Optimization (Service/Module)
- Include caching, database, and architectural improvements
- Comprehensive testing of affected interfaces
- Staged rollout with performance monitoring

### System-Wide Optimization (Full Application)
- Complete workflow with infrastructure optimization
- Extensive testing and monitoring implementation
- Gradual rollout with careful performance tracking

## Quality Gates

### Before Optimization
- Performance baseline is established and documented
- Bottlenecks are clearly identified and prioritized
- Optimization plan is approved with success criteria

### During Optimization
- Each optimization is validated against performance metrics
- Functional correctness is maintained
- Performance improvements are measurable

### Before Deployment
- Performance targets are met or exceeded
- All functionality remains intact
- Monitoring and alerting are in place
- Performance regression tests are implemented

## Communication Protocol

Each agent should document:
1. **Current Status**: What optimization phase is active
2. **Metrics**: Current performance measurements and improvements
3. **Bottlenecks**: Identified issues and resolution status
4. **Results**: Measurable performance gains achieved
5. **Next Steps**: What optimizations are planned next

## Success Criteria

Performance optimization is considered complete when:
- ✅ Performance targets are met or exceeded
- ✅ Bottlenecks are eliminated or significantly reduced
- ✅ System scalability is improved
- ✅ Resource utilization is optimized
- ✅ All functionality remains intact after optimization
- ✅ Performance monitoring is in place
- ✅ Optimizations are maintainable and documented
- ✅ Performance improvements are validated in production

## Performance Metrics to Track

### Response Time Metrics
- Average response time
- 95th/99th percentile response times
- Time to first byte (TTFB)
- Database query response times

### Throughput Metrics
- Requests per second
- Transactions per minute
- Data processing rates
- Concurrent user capacity

### Resource Utilization
- CPU usage patterns
- Memory consumption
- Database connection usage
- Network bandwidth utilization

### User Experience Metrics
- Page load times
- Time to interactive
- First contentful paint
- Cumulative layout shift

Use this workflow to ensure systematic and measurable performance optimization.