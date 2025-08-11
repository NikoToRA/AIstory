# Code Style and Conventions

## Python Code Style
Based on the codebase analysis:

### Class and Function Naming
- **Classes**: PascalCase (e.g., `HaconiwaConfig`, `HaconiwaWorkspace`)
- **Functions**: snake_case (e.g., `load_config`, `save_config`)
- **Variables**: snake_case

### Documentation Style
- **Docstrings**: Triple quotes with descriptive text
- **Comments**: Inline comments for complex logic
- **Type hints**: Used throughout (e.g., `-> Dict[str, Any]`, `-> bool`)

### File Organization
- **Class-based architecture** - Each major component is a class
- **Method grouping** - Related functionality grouped within classes
- **Error handling** - Try-catch blocks with user-friendly error messages

### String Handling
- **UTF-8 encoding** - Explicitly specified in file operations
- **f-strings and format strings** - For string formatting

## Configuration Style
- **YAML format** - Primary configuration format
- **Hierarchical structure** - Nested configuration with clear sections
- **Default values** - Fallback configurations when files don't exist

## Character System Conventions
- **Japanese naming** - Character names in Japanese with romanization
- **Profile structure** - Standardized character profile format
- **Memory persistence** - JSON format for character memory storage
- **Relationship tracking** - Structured relationship data

## File Naming Conventions
- **Scripts**: `snake_case.py`
- **Configs**: `kebab-case.yaml`
- **Stories**: `YYYY-MM-DD_title_format/`
- **Characters**: `lowercase_names/`

## Internationalization
- **Japanese content** - Stories and character profiles in Japanese
- **UTF-8 support** - All text files support Japanese characters
- **Bilingual comments** - Some English, some Japanese in code

## Error Handling Patterns
```python
try:
    # operation
    return result
except Exception as e:
    print(f"Error description: {e}")
    return default_value
```