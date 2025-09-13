/**
 * BMAD Knowledge Loader - Utility for agents to access integrated knowledge
 * 
 * This module provides BMAD agents with easy access to the harvested and
 * validated knowledge from the Solar Emergence project corpus.
 */

const fs = require('fs');
const path = require('path');

class KnowledgeLoader {
    constructor() {
        this.contextPath = path.join(process.cwd(), '.bmad-core', 'context');
        this.memoryPath = path.join(process.cwd(), '.bmad-core', 'memory');
        this.specsPath = path.join(process.cwd(), 'specs');
        
        this._knowledgeContext = null;
        this._memoryState = null;
        this._knowledgeIndex = null;
    }

    /**
     * Load the complete knowledge context for Solar Emergence
     * @returns {Object} Complete knowledge context
     */
    loadKnowledgeContext() {
        if (!this._knowledgeContext) {
            try {
                const contextFile = path.join(this.contextPath, 'knowledge_context.json');
                this._knowledgeContext = JSON.parse(fs.readFileSync(contextFile, 'utf8'));
            } catch (error) {
                console.warn('⚠️  Could not load knowledge context:', error.message);
                this._knowledgeContext = { solar_emergence_knowledge: {} };
            }
        }
        return this._knowledgeContext;
    }

    /**
     * Load the current BMAD memory state
     * @returns {Object} Current memory state
     */
    loadMemoryState() {
        if (!this._memoryState) {
            try {
                const memoryFile = path.join(this.memoryPath, 'current_state.json');
                this._memoryState = JSON.parse(fs.readFileSync(memoryFile, 'utf8'));
            } catch (error) {
                console.warn('⚠️  Could not load memory state:', error.message);
                this._memoryState = {};
            }
        }
        return this._memoryState;
    }

    /**
     * Load the knowledge index for quick lookups
     * @returns {Object} Knowledge index
     */
    loadKnowledgeIndex() {
        if (!this._knowledgeIndex) {
            try {
                const indexFile = path.join(this.memoryPath, 'knowledge_index.json');
                this._knowledgeIndex = JSON.parse(fs.readFileSync(indexFile, 'utf8'));
            } catch (error) {
                console.warn('⚠️  Could not load knowledge index:', error.message);
                this._knowledgeIndex = { quick_access: {} };
            }
        }
        return this._knowledgeIndex;
    }

    /**
     * Get discovered patterns relevant to the current task
     * @param {string} category - Optional category filter
     * @returns {Array} Array of discovered patterns
     */
    getDiscoveredPatterns(category = null) {
        const context = this.loadKnowledgeContext();
        const patterns = context.solar_emergence_knowledge?.discovered_patterns || [];
        
        if (category) {
            return patterns.filter(pattern => 
                pattern.toLowerCase().includes(category.toLowerCase())
            );
        }
        
        return patterns;
    }

    /**
     * Get local processing algorithms that comply with constraints
     * @returns {Array} Array of local algorithms
     */
    getLocalAlgorithms() {
        const index = this.loadKnowledgeIndex();
        return index.quick_access?.local_processing_tools || [];
    }

    /**
     * Get fusion architectures for multimodal processing
     * @returns {Array} Array of fusion architectures
     */
    getFusionArchitectures() {
        const index = this.loadKnowledgeIndex();
        return index.quick_access?.fusion_architectures || [];
    }

    /**
     * Get pattern discovery techniques
     * @returns {Array} Array of pattern discovery techniques
     */
    getPatternDiscoveryTechniques() {
        const index = this.loadKnowledgeIndex();
        return index.quick_access?.pattern_discovery || [];
    }

    /**
     * Check if a technique complies with project constraints
     * @param {string} technique - Technique to check
     * @returns {boolean} True if compliant
     */
    isConstraintCompliant(technique) {
        const memory = this.loadMemoryState();
        const constraints = memory.constraints || {};
        
        const techniqueText = technique.toLowerCase();
        
        // Check for constraint violations
        if (constraints.local_only && techniqueText.includes('api')) {
            return false;
        }
        
        if (constraints.zero_cost && (techniqueText.includes('paid') || techniqueText.includes('subscription'))) {
            return false;
        }
        
        if (constraints.no_external_apis && (techniqueText.includes('openai') || techniqueText.includes('cloud'))) {
            return false;
        }
        
        return true;
    }

    /**
     * Get project core principles
     * @returns {Array} Array of core principles
     */
    getCorePronciples() {
        const context = this.loadKnowledgeContext();
        return context.solar_emergence_knowledge?.core_principles || [];
    }

    /**
     * Get current project status and next steps
     * @returns {Object} Project status information
     */
    getProjectStatus() {
        const memory = this.loadMemoryState();
        return {
            project: memory.project || 'Unknown',
            architecture: memory.architecture || 'Unknown',
            knowledge_stats: memory.current_knowledge || {},
            next_steps: memory.next_steps || [],
            available_tools: memory.available_tools || []
        };
    }

    /**
     * Search knowledge for specific terms
     * @param {string} searchTerm - Term to search for
     * @returns {Object} Search results categorized by type
     */
    searchKnowledge(searchTerm) {
        const context = this.loadKnowledgeContext();
        const knowledge = context.solar_emergence_knowledge || {};
        
        const results = {
            patterns: [],
            algorithms: [],
            architectures: [],
            techniques: []
        };
        
        const term = searchTerm.toLowerCase();
        
        // Search patterns
        (knowledge.discovered_patterns || []).forEach(pattern => {
            if (pattern.toLowerCase().includes(term)) {
                results.patterns.push(pattern);
            }
        });
        
        // Search algorithms
        (knowledge.applicable_algorithms || []).forEach(algorithm => {
            if (algorithm.toLowerCase().includes(term)) {
                results.algorithms.push(algorithm);
            }
        });
        
        // Search architectures
        (knowledge.local_architectures || []).forEach(architecture => {
            if (architecture.toLowerCase().includes(term)) {
                results.architectures.push(architecture);
            }
        });
        
        // Search techniques
        (knowledge.constraint_compliant_techniques || []).forEach(technique => {
            if (technique.toLowerCase().includes(term)) {
                results.techniques.push(technique);
            }
        });
        
        return results;
    }

    /**
     * Get knowledge summary statistics
     * @returns {Object} Summary statistics
     */
    getKnowledgeStats() {
        const context = this.loadKnowledgeContext();
        const memory = this.loadMemoryState();
        const knowledge = context.solar_emergence_knowledge || {};
        
        return {
            last_updated: knowledge.last_updated || 'Unknown',
            total_patterns: (knowledge.discovered_patterns || []).length,
            total_algorithms: (knowledge.applicable_algorithms || []).length,
            total_architectures: (knowledge.local_architectures || []).length,
            total_techniques: (knowledge.constraint_compliant_techniques || []).length,
            compliance_status: memory.current_knowledge?.compliance_enforced || false,
            core_principles_count: (knowledge.core_principles || []).length
        };
    }
}

// Export for use in BMAD agents
module.exports = { KnowledgeLoader };

// Example usage for agents:
/*
const { KnowledgeLoader } = require('./.bmad-core/utils/knowledge-loader.js');

// In your BMAD agent
const knowledgeLoader = new KnowledgeLoader();

// Get all local algorithms
const localAlgs = knowledgeLoader.getLocalAlgorithms();
console.log('Available local algorithms:', localAlgs);

// Search for specific knowledge
const whisperInfo = knowledgeLoader.searchKnowledge('whisper');
console.log('Whisper-related knowledge:', whisperInfo);

// Check constraint compliance
const isCompliant = knowledgeLoader.isConstraintCompliant('OpenAI API processing');
console.log('Is OpenAI compliant?', isCompliant); // Should be false

// Get project status
const status = knowledgeLoader.getProjectStatus();
console.log('Current project status:', status);
*/