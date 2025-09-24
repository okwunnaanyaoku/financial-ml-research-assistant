---
name: code-refactoring
description: Code refactoring workflow using appropriate development agents
---

# Code Refactoring Workflow

**Refactoring Target**: $ARGUMENTS

This command orchestrates a systematic approach to code refactoring using our development agent team.

## Phase 1: Code Analysis (Code Refactoring Specialist)
```
Use code-refactoring-specialist agent to:
- Analyze the target code: "$ARGUMENTS"
- Identify code smells and technical debt
- Assess code complexity and maintainability metrics
- Document current architecture and dependencies
- Prioritize refactoring opportunities by impact and effort
```

## Phase 2: Performance Assessment (Performance Optimizer)
```
Use performance-optimizer agent to:
- Measure current performance benchmarks
- Identify performance bottlenecks in existing code
- Analyze resource utilization and efficiency
- Document performance baseline metrics
- Identify optimization opportunities during refactoring
```

## Phase 3: Security Review (Security Specialist)
```
Use security-specialist agent to:
- Review existing code for security vulnerabilities
- Identify security improvements needed during refactoring
- Ensure refactoring doesn't introduce security risks
- Document security considerations and requirements
- Plan security enhancements as part of refactoring
```

## Phase 4: Architecture Assessment (System Architect)
```
Use system-architect agent to:
- Evaluate current architecture and design patterns
- Identify architectural improvements and modernization opportunities
- Plan structural changes and component reorganization
- Ensure refactoring aligns with overall system architecture
- Document architectural goals for the refactoring
```

## Phase 5: Test Coverage Analysis (QA Engineer)
```
Use qa-engineer agent to:
- Analyze existing test coverage for target code
- Identify gaps in test coverage before refactoring
- Create comprehensive test plans for refactored code
- Ensure tests will catch regressions during refactoring
- Plan test improvements and additions
```

## Phase 6: Refactoring Planning (Code Refactoring Specialist)
```
Use code-refactoring-specialist agent to:
- Create detailed refactoring plan with phases
- Identify safe refactoring techniques to apply
- Plan incremental changes to minimize risk
- Define success criteria and quality metrics
- Create rollback strategy if issues arise
```

## Phase 7: Test Enhancement (QA Engineer)
```
Use qa-engineer agent to:
- Implement missing unit tests before refactoring
- Create integration tests for critical pathways
- Enhance test coverage to ensure safety net
- Implement automated regression testing
- Validate test suite catches existing behavior
```

## Phase 8: Incremental Refactoring (Code Refactoring Specialist)
```
Use code-refactoring-specialist agent to:
- Implement refactoring in small, safe increments
- Apply extract method, extract class, and other patterns
- Improve naming conventions and code clarity
- Eliminate code duplication and reduce complexity
- Ensure each increment is deployable and testable
```

## Phase 9: Performance Optimization (Performance Optimizer)
```
Use performance-optimizer agent to:
- Optimize algorithms and data structures during refactoring
- Implement caching and efficiency improvements
- Reduce memory usage and processing overhead
- Validate performance improvements with benchmarks
- Ensure optimizations don't compromise maintainability
```

## Phase 10: Code Review (Code Reviewer)
```
Use code-reviewer agent to:
- Review each refactoring increment for quality
- Ensure refactoring follows best practices and standards
- Verify code clarity and maintainability improvements
- Check for potential issues or regressions
- Approve incremental changes before proceeding
```

## Phase 11: Integration Testing (QA Engineer)
```
Use qa-engineer agent to:
- Test refactored code with comprehensive test suites
- Validate all existing functionality still works
- Test edge cases and error scenarios
- Ensure no regressions have been introduced
- Performance test to validate improvements
```

## Phase 12: Security Validation (Security Specialist)
```
Use security-specialist agent to:
- Validate refactored code maintains security standards
- Test that no new vulnerabilities were introduced
- Verify security improvements were properly implemented
- Update security documentation if needed
- Approve security aspects of refactoring
```

## Phase 13: Performance Validation (Performance Optimizer)
```
Use performance-optimizer agent to:
- Measure performance after refactoring completion
- Compare with baseline metrics to validate improvements
- Identify any performance regressions
- Fine-tune optimizations if needed
- Document performance gains achieved
```

## Phase 14: Documentation Update (Documentation Agent)
```
Use documentation agent to:
- Update technical documentation affected by refactoring
- Document new architecture and design patterns used
- Update code comments and inline documentation
- Create refactoring summary and lessons learned
- Update developer guides and best practices
```

## Phase 15: Deployment Planning (DevOps Engineer)
```
Use devops-engineer agent to:
- Plan deployment strategy for refactored code
- Ensure monitoring covers refactored components
- Prepare rollback procedures if issues arise
- Plan gradual rollout if risk is high
- Update deployment scripts and configurations
```

## Refactoring Scope Workflows

### Small Refactoring (Single Function/Class)
- Focus on code quality and readability improvements
- Streamlined testing with emphasis on unit tests
- Quick deployment after basic validation

### Medium Refactoring (Module/Component)
- Include performance and security reviews
- Comprehensive testing of affected interfaces
- Staged deployment with monitoring

### Large Refactoring (System-wide Changes)
- Full workflow with architectural review
- Extensive testing and validation phases
- Gradual rollout with careful monitoring

## Quality Gates

### Before Starting Refactoring
- Test coverage is adequate for safety net
- Performance baseline is established
- Refactoring plan is approved and detailed

### During Refactoring
- Each increment passes all tests
- Performance doesn't degrade unacceptably
- Code quality metrics show improvement

### Before Deployment
- All tests pass including new comprehensive tests
- Performance meets or exceeds baseline
- Security standards are maintained
- Code quality significantly improved

## Communication Protocol

Each agent should document:
1. **Current Status**: What phase of refactoring is active
2. **Metrics**: Current code quality, performance, and test metrics
3. **Issues**: Any problems or blockers encountered
4. **Improvements**: What improvements have been achieved
5. **Next Steps**: What needs to happen next

## Success Criteria

Code refactoring is considered complete when:
- ✅ Code quality metrics show significant improvement
- ✅ Technical debt is reduced measurably
- ✅ Performance is maintained or improved
- ✅ All tests pass with no regressions
- ✅ Code is more maintainable and readable
- ✅ Security standards are maintained or improved
- ✅ Documentation is updated accurately
- ✅ Refactored code is successfully deployed

## Refactoring Safety Principles

1. **Small Steps**: Make incremental changes that can be easily reversed
2. **Test First**: Ensure comprehensive test coverage before starting
3. **Measure Twice**: Validate improvements with metrics and benchmarks
4. **Document Changes**: Keep detailed records of what was changed and why
5. **Seek Review**: Get multiple eyes on significant changes
6. **Monitor Production**: Watch carefully after deployment for issues

Use this workflow to ensure systematic and safe code refactoring.