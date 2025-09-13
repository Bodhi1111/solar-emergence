# ADR-005: MLX Framework for M2 Max Optimization

## Status
Accepted

## Context
Machine learning inference needs to run efficiently on Mac M2 Max hardware. The framework must support transformer models, neural networks, and custom algorithms while maintaining the LOCAL_ONLY constraint.

## Decision
We will use Apple's MLX framework as the primary ML framework, with PyTorch as a fallback for operations not yet supported in MLX.

## Consequences

### Positive
- Optimized for Apple Silicon (M2 Max)
- Efficient memory usage with unified memory
- Hardware acceleration via Metal
- Growing ecosystem and support
- Native Mac performance

### Negative
- Newer framework with less documentation
- Smaller model ecosystem
- Some operations not yet implemented
- Limited community resources
- Potential API changes

## Implementation
- MLX for transformer models and core ML operations
- PyTorch with MPS backend for unsupported operations
- Custom Metal shaders for performance-critical code
- Model conversion pipeline from PyTorch to MLX
- Automatic fallback mechanism

## Alternatives Considered
1. **PyTorch Only**: Rejected - less optimized for M2
2. **TensorFlow**: Rejected - poor Mac support
3. **JAX**: Rejected - limited Mac acceleration
4. **Core ML**: Rejected - too restrictive for research

---
Date: 2025-09-12
Decided by: ML Infrastructure Team
Reviewed by: Technical Lead