# Project Guidelines and Design Patterns

## Design Patterns

### 1. Configuration-Driven Architecture
- **Pattern**: All system behavior controlled via YAML/JSON configuration
- **Implementation**: `haconiwa.yaml` for CLI, `story-world/claude.md` for AI behavior
- **Benefits**: Easy to modify system behavior without code changes

### 2. Character-as-Code Pattern
- **Pattern**: AI characters defined as structured data with behavior rules
- **Files**: `profile.txt` (personality), `memory.json` (experiences), relationship data
- **Evolution**: Characters grow through accumulated experiences and interactions

### 3. Event-Driven Story Generation
- **Trigger**: GitHub Issues with specific labels
- **Processing**: Automated via GitHub Actions
- **Output**: Structured story files with metadata

### 4. Hierarchical Organization Model
- **Structure**: Nations → Cities → Companies → Rooms
- **Purpose**: Complex environment management for development workspaces
- **Implementation**: Reflected in configuration and workspace creation

## Development Guidelines

### Character Development Rules
1. **Personality Consistency**: Characters must maintain core personality traits
2. **Memory Persistence**: All interactions must be recorded and influence future behavior
3. **Relationship Evolution**: Character relationships should evolve naturally over time
4. **Japanese Cultural Context**: Stories should reflect Japanese high school setting

### Technical Guidelines
1. **UTF-8 First**: All text processing must handle Japanese characters
2. **Error Resilience**: System should gracefully handle missing files/data
3. **Modular Design**: Each component should be independently testable
4. **Configuration Over Code**: Prefer YAML/JSON configuration over hardcoded behavior

### Story Generation Principles
1. **Three-Act Structure**: 起承転結 (ki-sho-ten-ketsu) narrative structure
2. **Character Dynamics**: Focus on Chappie (energetic) vs Gemmy (rule-focused) interactions
3. **Comedy Timing**: Build tension then release through character quirks
4. **Emotional Growth**: Each story should contribute to character development

### Security Considerations
- **No Personal Data**: Never store real personal information
- **API Key Protection**: Anthropic API keys secured via GitHub Secrets
- **File Access Controls**: Restricted write permissions per `story-world/claude.md`
- **Safe Defaults**: Fallback to safe behavior when configuration is missing

### Performance Patterns
- **Lazy Loading**: Configuration loaded only when needed
- **Caching**: Character memory cached to reduce file I/O
- **Async Processing**: GitHub Actions run asynchronously
- **Resource Limits**: Text generation bounded by character limits

### Quality Assurance Patterns
- **Manual Testing Scripts**: `manual_test.py`, `character_growth_demo.py`
- **Metadata Tracking**: Every story includes creation metadata
- **Version Control**: All changes tracked via Git
- **Rollback Capability**: Character memory can be restored from previous states