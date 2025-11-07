# 📊 PlantUML Diagrams - Visual Guide

This directory contains comprehensive PlantUML diagrams to help you understand the Hybrid Attack system visually.

---

## 📁 Available Diagrams

### 1. **flowChart.puml** - Main Hybrid Attack Flow
The big picture of how the hybrid attack works from start to finish.

**Shows:**
- ✅ Initial configuration setup
- ✅ Phase 1: Dictionary Attack flow
- ✅ Phase 2: Parallel Brute Force flow
- ✅ Decision points and branching
- ✅ Success and failure paths

**Best for:** Understanding the overall attack strategy

---

### 2. **classDiagram.puml** - System Architecture
Complete class structure showing all components and their relationships.

**Shows:**
- ✅ Main classes: `HybridConfig`, `AttackResult`, `HybridAttack`
- ✅ Attack strategies: `DictionaryAttack`, `BruteForceAttack`, `ParallelBruteForce`
- ✅ Worker classes and utilities
- ✅ Relationships between components
- ✅ Methods and attributes

**Best for:** Understanding code structure and design patterns

---

### 3. **dictionaryFlow.puml** - Dictionary Attack Detail
Deep dive into how the dictionary attack works step by step.

**Shows:**
- ✅ Dictionary loading process
- ✅ Password comparison loop
- ✅ Success and failure handling
- ✅ Verbose mode logging
- ✅ Result creation

**Best for:** Understanding the fast dictionary attack method

---

### 4. **parallelBruteForceFlow.puml** - Parallel Brute Force Detail
Deep dive into parallel brute force with multiple workers.

**Shows:**
- ✅ Work distribution among 4 workers
- ✅ Search space calculation
- ✅ Combination generation
- ✅ Worker synchronization
- ✅ Result collection

**Best for:** Understanding parallel processing and worker coordination

---

### 5. **sequenceDiagram.puml** - Interaction Flow
Shows how different components interact over time.

**Shows:**
- ✅ Message passing between components
- ✅ Time sequence of operations
- ✅ Dictionary attack → Brute force fallback
- ✅ Worker communication
- ✅ Result channel usage

**Best for:** Understanding component interactions and timing

---

### 6. **componentDiagram.puml** - System Architecture
High-level view of system components and dependencies.

**Shows:**
- ✅ User interface layer
- ✅ Attack strategy layer
- ✅ Core engine layer
- ✅ Worker pool layer
- ✅ Utility components
- ✅ Data storage

**Best for:** Understanding system organization and dependencies

---

## 🚀 How to View Diagrams

### Option 1: Online PlantUML Editor (Easiest)
1. Go to http://www.plantuml.com/plantuml/uml/
2. Copy and paste the content of any `.puml` file
3. Click "Submit" to see the diagram
4. Download as PNG/SVG if needed

### Option 2: VS Code Extension
1. Install "PlantUML" extension in VS Code
2. Open any `.puml` file
3. Press `Alt+D` (or `Cmd+D` on Mac) to preview
4. Or right-click → "Preview Current Diagram"

### Option 3: Command Line
```bash
# Install PlantUML
sudo apt-get install plantuml  # Ubuntu/Debian
brew install plantuml          # macOS

# Generate PNG images
plantuml flowChart.puml
plantuml classDiagram.puml
plantuml dictionaryFlow.puml
plantuml parallelBruteForceFlow.puml
plantuml sequenceDiagram.puml
plantuml componentDiagram.puml

# This creates PNG files for each diagram
```

### Option 4: Online with URL
```bash
# Each diagram can be viewed at:
http://www.plantuml.com/plantuml/proxy?src=<raw-github-url>
```

---

## 📖 Understanding Each Diagram Type

### Flowchart (Activity Diagram)
```
┌─────────┐
│  Start  │
└────┬────┘
     │
     ▼
┌─────────────┐     Yes    ┌─────────┐
│  Condition? │──────────→ │ Action  │
└─────────────┘            └─────────┘
     │ No
     ▼
┌─────────┐
│   End   │
└─────────┘
```
**Use for:** Step-by-step processes

### Class Diagram
```
┌──────────────────┐
│   ClassName      │
├──────────────────┤
│ - attribute      │
│ + method()       │
└──────────────────┘
        │
        ▼ (relationship)
┌──────────────────┐
│  AnotherClass    │
└──────────────────┘
```
**Use for:** Code structure and relationships

### Sequence Diagram
```
User    Main    Attack
 │       │        │
 │──msg──→        │
 │       │──call──→
 │       │←─return─
 │←result─        │
```
**Use for:** Time-based interactions

---

## 🎯 Quick Reference

### Main Flowchart Symbols
- **Rectangle**: Process/Action
- **Diamond**: Decision point
- **Oval**: Start/End
- **Fork/Join**: Parallel execution
- **Note**: Additional information

### Colors in Diagrams
- 🟢 **Green**: Success path
- 🔵 **Blue**: Brute force phase
- 🟡 **Yellow**: Warning/Not found
- 🔴 **Pink**: Error/Failure
- ⚪ **White**: Normal flow

---

## 📊 Diagram Comparison

| Diagram | What It Shows | Best For | Complexity |
|---------|---------------|----------|------------|
| Flow Chart | Overall process | Beginners | ⭐⭐ |
| Class Diagram | Code structure | Developers | ⭐⭐⭐⭐ |
| Dictionary Flow | Dict attack detail | Understanding speed | ⭐⭐ |
| Parallel Flow | Multi-threading | Advanced concepts | ⭐⭐⭐⭐⭐ |
| Sequence | Time-based flow | Interactions | ⭐⭐⭐ |
| Component | System architecture | Big picture | ⭐⭐⭐ |

---

## 🎓 Learning Path

### For Beginners:
1. Start with **flowChart.puml** (main overview)
2. Then **dictionaryFlow.puml** (simple attack)
3. Finally **componentDiagram.puml** (system view)

### For Intermediate:
1. **sequenceDiagram.puml** (interactions)
2. **parallelBruteForceFlow.puml** (parallel concepts)
3. **classDiagram.puml** (code structure)

### For Advanced:
1. All diagrams in order
2. Compare with actual code
3. Modify diagrams for experiments

---

## 🛠️ Customizing Diagrams

### Change Colors
```plantuml
skinparam backgroundColor #FFFFFF
skinparam classBackgroundColor #LIGHTBLUE
```

### Add Notes
```plantuml
note right
    Your explanation here
end note
```

### Modify Layout
```plantuml
left to right direction  ' Horizontal layout
top to bottom direction  ' Vertical layout (default)
```

---

## 💡 Key Concepts Visualized

### 1. Dictionary Attack (Fast Path)
```
Dictionary → Compare → Match? → Success (0.0001s)
                         ↓ No
                    Continue → Exhausted → Failed
```

### 2. Parallel Brute Force (Thorough Path)
```
Search Space ÷ 4 Workers
    ↓
Worker 1 (25%) ┐
Worker 2 (25%) ├→ First to find = Winner!
Worker 3 (25%) │
Worker 4 (25%) ┘
```

### 3. Hybrid Strategy
```
Try Dictionary (Fast)
    ↓ Success?
   Yes → Done! (Fast)
    ↓ No
Try Brute Force (Slow)
    ↓ Success?
   Yes → Done! (Slow but guaranteed)
```

---

## 🔍 Diagram Details

### Flow Chart Highlights
- **Green partition**: Dictionary attack (Phase 1)
- **Blue partition**: Brute force attack (Phase 2)
- **Fork/Join**: Shows parallel workers
- **Repeat loops**: Shows iteration

### Class Diagram Highlights
- **Solid lines**: Strong relationships
- **Dashed lines**: Dependencies
- **Triangles**: Inheritance/Implementation
- **Diamonds**: Composition/Aggregation

### Sequence Diagram Highlights
- **Vertical lines**: Object lifelines
- **Arrows**: Messages/Calls
- **Activation boxes**: Active processing
- **par/end**: Parallel execution

---

## 📝 Diagram Export Options

### PNG (Raster Image)
```bash
plantuml -tpng flowChart.puml
```
**Best for:** Presentations, documents

### SVG (Vector Image)
```bash
plantuml -tsvg flowChart.puml
```
**Best for:** Web, scaling without quality loss

### PDF
```bash
plantuml -tpdf flowChart.puml
```
**Best for:** Printing, academic papers

---

## 🎨 Color Scheme Reference

```plantuml
#PALEGREEN   - Success, found
#LIGHTBLUE   - Brute force phase
#LIGHTYELLOW - Warning, not found
#PINK        - Error, failure
#LIGHTGRAY   - Normal process
#FEFEFE      - Background
```

---

## 🚀 Quick Commands

```bash
# View all diagrams at once
for f in *.puml; do plantuml "$f"; done

# Export to specific format
plantuml -tsvg *.puml

# Watch for changes and auto-update
plantuml -tpng -w *.puml
```

---

## 📚 Additional Resources

### PlantUML Documentation
- Official site: https://plantuml.com/
- Language reference: https://plantuml.com/guide
- Real-world examples: https://real-world-plantuml.com/

### Diagram Best Practices
- Keep diagrams simple and focused
- Use consistent naming conventions
- Add notes for complex sections
- Use colors meaningfully
- Test with different viewers

---

## 🎯 Summary

You now have **6 comprehensive diagrams** that show:

1. ✅ **Overall flow** - How the attack progresses
2. ✅ **Code structure** - How classes are organized
3. ✅ **Dictionary details** - How fast attack works
4. ✅ **Parallel details** - How workers collaborate
5. ✅ **Interactions** - How components communicate
6. ✅ **Architecture** - How system is organized

**Pick the diagram that best fits your learning style!**

---

**Happy Learning!** 🎓📊

