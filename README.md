# 🧩 Maze Game with Pathfinding Algorithms

## 📌 Introduction
This project was developed as part of the **Artificial Intelligence** course at HCMUTE.  
Its goal is to simulate various **pathfinding algorithms** in a maze environment, allowing learners to visually compare how each algorithm works and performs.

Implemented algorithms:
- DFS (Depth-First Search)  
- BFS (Breadth-First Search)  
- Hill Climbing  
- A* Search  
- Greedy Best-First Search  
- Uniform Cost Search (UCS)  
- Beam Search  

The graphical interface is built using **Pygame**, enabling users to create maps, add obstacles, and observe the behavior of different algorithms in real time.

---

## 🎯 Objectives
- Visualize common pathfinding algorithms in a maze.  
- Allow users to create custom maps with start, goal, and walls.  
- Provide an interactive interface for studying and comparing algorithm efficiency.  

---

## 🛠️ Tools & Technologies
- **Python**  
- **Pygame** (interactive graphical interface)  
- **NumPy** (data manipulation)  
- **Queue / PriorityQueue** (for BFS, UCS, A*, DFS, GREEDY, HILLCLIMBING, BEAM)  
- **Random, Copy** (maze generation and state handling)  

---

## 🚀 How to Run
1. Install Python 3.9+  
2. Install required libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

---

## 📖 Detailed Usage Guide

![Game Interface - Main View](images/image1.png)

### Main Menu
When you launch the application, you'll see the main menu with three options:
- **Start**: Begin the game with a default maze
- **Create Map**: Design your own custom maze
- **Exit**: Close the application

### Creating a Custom Map
If you select **Create Map**, you can design your own maze:

![Map Creation Features](images/image2.png)

1. **Select Region**: Press and drag your mouse to select a rectangular area for creating walls
2. **Set Start Position**: Press **1** to mark the starting position (where the player will begin)
3. **Set End Position**: Press **2** to mark the goal/end position (destination)
4. **Create Walls**: Press **3** to draw obstacles/walls in your selected region
5. **Delete Elements**: Press **4** to remove walls or other elements you've placed
6. **Start Game**: Press **S** to begin the game with your custom maze

### Game Controls

#### Navigation
- **Arrow Keys**: Move the player through the maze
- **Space**: Skip the player's turn

#### Algorithm Selection
During gameplay, you can activate multiple algorithms simultaneously by clicking on their checkboxes on the right panel. Each algorithm is represented by:
- **DFS** (Depth-First Search) - Red path
- **BFS** (Breadth-First Search) - Light blue path
- **Hill Climbing** - Dark cyan path
- **A* Search** - Teal path (heuristic-based)
- **Greedy Best-First Search** - Pink path
- **Uniform Cost Search (UCS)** - Dark gray path
- **Beam Search** - Purple path

#### Speed Control
- Adjust the speed slider at the bottom right to control how fast the algorithms and player move through the maze
- Drag the slider left (slower) or right (faster)

#### Activate All
- Click the **"Activate All"** checkbox to run all algorithms simultaneously and compare their performance

### After Algorithms Complete: Analyzing Results

After the algorithms finish running and reach the goal, you can analyze the results:

![Algorithm Step-by-Step Visualization](images/image3.png)

#### Viewing Final Paths
1. **Each algorithm's path is displayed in its unique color:**
   - Move the speed slider to the **rightmost** (fastest) position to let all algorithms finish
   - Once complete, all paths remain visible on the maze
   - The final path appears as a brighter/bolder line in each algorithm's color

2. **Comparing paths visually:**
   - Look at which algorithms took the most direct route
   - Observe which paths are longer or shorter
   - Note which algorithms overlapped their exploration (similar exploration patterns)

#### Reading Statistics on Right Panel
After completion, each algorithm shows:
- **Total Nodes Explored**: Number of cells examined (including backtracking)
- **Final Path Length**: Number of steps from start to goal
- **Algorithm Status**: Marked as complete if goal was found

#### Analyzing the Results

**Step 1: Compare Path Lengths**
- Look at the path length numbers on the right panel
- Shortest path = best solution
- Note which algorithms found the same (optimal) path

**Step 2: Evaluate Efficiency**
- Compare "Nodes Explored" vs "Path Length"
- A good algorithm finds short path with few explorations
- Calculate efficiency ratio: `Nodes Explored ÷ Path Length`
- Lower ratio = more efficient algorithm

**Step 3: Visual Pattern Analysis**
- **Wide exploration areas** = algorithm explored many cells
- **Narrow corridor of exploration** = algorithm went direct (uses heuristic well)
- **Multiple branching patterns** = algorithm tried different directions
- **Linear path to goal** = very efficient heuristic guidance

#### Detailed Review Steps

**To closely examine one algorithm's work:**
1. Reset/reload the maze
2. Disable all other algorithms
3. Enable only the target algorithm
4. Set speed to slowest (leftmost)
5. Watch it step-by-step and understand its decision-making

**To compare two algorithms directly:**
1. Run Algorithm A, note its path (screenshot helpful)
2. Reset/reload the same maze
3. Run Algorithm B, note its path
4. Compare the two paths side-by-side
5. Count steps and explorations for each

**To save/document results:**
- Take screenshots of each algorithm's path
- Write down the statistics:
  ```
  Algorithm: [Name]
  Nodes Explored: [Number]
  Path Length: [Number]
  Optimal: [Yes/No]
  ```
- Create a comparison table across all algorithms

### Understanding the Visual Display

**Color Codes:**
- **Blue square**: Player position
- **Red square**: Goal/End position
- **Gray squares**: Walls
- **Colored paths**: Each algorithm's explored path (different color per algorithm)
- **Visited nodes**: Lighter shading indicates cells explored by each algorithm

**Right Panel Information:**
- Shows each algorithm with its own checkbox
- Displays the number of steps/nodes explored by each algorithm
- Visual representation of the path taken by each algorithm
- Status indicator showing if the algorithm found the goal
- **After completion**: Shows final statistics for result analysis

### Interpreting Key Metrics

**Path Length**
- Number of steps the algorithm took from start to goal
- **Shorter = Better**
- Compare across algorithms to find the optimal path
- BFS, A*, and UCS should find the same shortest path in unweighted mazes

**Nodes Explored**
- Total number of cells the algorithm examined
- Includes cells that were not part of the final path
- **Lower = More Efficient**
- Heuristic-based algorithms (A*, Greedy) explore fewer nodes
- DFS/BFS explore more but may differ in pattern

**Efficiency Comparison**
- Calculate: `Nodes Explored / Path Length`
- Example: DFS explored 150 nodes, path is 20 steps = 7.5x ratio
- Compare ratios: Lower ratio = algorithm wasted less exploration

**Finding Quality (Optimality)**
- Did the algorithm find the **true shortest path**?
- BFS always finds shortest ✅
- A* finds shortest (if heuristic is admissible) ✅
- Greedy might find longer path ⚠️
- DFS may find longer path ⚠️

### Game Objective
Navigate your player from the start position to the goal position while observing how different pathfinding algorithms solve the same problem. Compare:
- **Efficiency**: Which algorithm uses the fewest steps?
- **Path Quality**: Does the algorithm find the optimal path?
- **Speed**: How fast does each algorithm explore the maze?

### Tips for Best Results
1. **Compare Algorithms**: Run multiple algorithms at once to see different approaches
2. **Custom Mazes**: Create interesting mazes with multiple possible paths to see how algorithms differ
3. **Adjust Speed**: Use the speed slider to follow the algorithm's decision-making process
4. **Study Behavior**: Observe how each algorithm explores differently:
   - DFS goes deep into one path
   - BFS explores evenly in all directions
   - A* and Greedy use heuristics to aim toward the goal
   - UCS considers path costs
   - Beam Search uses a limited frontier

### Step-by-Step Example: First Time Playing

**Scenario 1: Using the Default Maze**
1. Launch the application: `python main.py`
2. Click **"Start"** button on the main menu
3. Observe the default maze with start (blue), goal (red), and walls (gray)
4. Click checkboxes on the right panel to activate algorithms (start with 1-2 at a time)
5. Use the **speed slider** to slow down and watch how each algorithm explores
6. Compare the paths taken by different algorithms using the color legend
7. Note which algorithm finds the goal fastest and with the fewest steps

**Scenario 2: Creating Your Own Simple Maze**
1. From main menu, click **"Create Map"**
2. Drag mouse to select a region and press **3** to create walls (build an L-shaped or S-shaped maze)
3. Press **1** to set start position (top-left area)
4. Press **2** to set end position (bottom-right area)
5. Press **S** to start
6. Run algorithms and observe how they navigate your custom layout
7. Add more complexity: create multiple paths and see which algorithm finds the shortest one

**Scenario 3: Advanced Comparison Study**
1. Create a maze with multiple possible paths of different lengths
2. Activate all algorithms by clicking **"Activate All"** 
3. Slow down the speed to observe the exploration pattern
4. Note:
   - How many cells each algorithm explored (shown on right panel)
   - Which algorithms find the optimal (shortest) path
   - How the heuristic in A* and Greedy helps them explore fewer cells
5. Try the same maze with different start/end positions to see consistency
6. **After completion: Review Results**
   - Compare the final statistics (nodes explored, path length)
   - Create a table comparing all algorithms
   - Identify which was most efficient
   - Note any algorithms that failed or took longer paths

**Scenario 4: Results Analysis Checklist**
1. After all algorithms complete, check the right panel
2. Create a quick comparison:
   ```
   Algorithm | Nodes | Path | Optimal?
   ----------|-------|------|----------
   BFS       | 80    | 25   | Yes
   A*        | 65    | 25   | Yes
   Greedy    | 75    | 27   | No
   DFS       | 120   | 30   | No
   ```
3. Answer: Which was most efficient? Most optimal? Fastest to complete?
4. Draw conclusions about the maze difficulty and algorithm characteristics

### Detailed Algorithm Explanation

**DFS (Depth-First Search)**
- **How it works**: Goes as deep as possible into one path before backtracking
- **Color**: Red
- **Characteristics**:
  - Uses a stack internally
  - Non-optimal: may not find the shortest path
  - Memory efficient compared to BFS
  - Good for exploring all possibilities
- **Best for**: Puzzle solving, checking if a path exists
- **Watch for**: Lengthy detours before finding the goal

**BFS (Breadth-First Search)**
- **How it works**: Explores all neighbors at current depth before moving deeper
- **Color**: Light Blue
- **Characteristics**:
  - Uses a queue internally
  - **Optimal**: Always finds the shortest path
  - Explores level-by-level like ripples in water
  - More memory intensive than DFS
- **Best for**: Finding shortest paths in unweighted graphs
- **Watch for**: Systematic, even exploration pattern

**A* Search**
- **How it works**: Uses both actual cost and estimated cost to goal (heuristic)
- **Color**: Teal
- **Characteristics**:
  - **Optimal**: Finds best path when heuristic is admissible
  - Very efficient: explores fewer nodes than BFS
  - Uses: `f(n) = g(n) + h(n)` where g = cost so far, h = estimated cost to goal
  - Manhattan distance heuristic used in this project
- **Best for**: Real-world pathfinding (games, GPS navigation)
- **Watch for**: Direct movement toward goal with minimal backtracking

**Greedy Best-First Search**
- **How it works**: Always goes toward the node closest to the goal
- **Color**: Pink
- **Characteristics**:
  - **Not optimal**: May find suboptimal paths
  - Very fast: only considers heuristic value, not actual cost
  - Uses: `f(n) = h(n)` only
  - Can get trapped or take long routes
- **Best for**: Quick approximations, when speed > accuracy
- **Watch for**: May look smart but find longer paths than BFS

**Hill Climbing**
- **How it works**: Local search that always moves to better neighbors
- **Color**: Dark Cyan
- **Characteristics**:
  - **Not complete**: May fail to find path (gets stuck in local minima)
  - No backtracking capability
  - Very memory efficient
  - Gets stuck at dead ends or local optima
- **Best for**: Local optimization problems
- **Watch for**: Often fails; useful for comparison to show limitations

**Uniform Cost Search (UCS)**
- **How it works**: Expands nodes with lowest cumulative cost
- **Color**: Dark Gray
- **Characteristics**:
  - **Optimal**: Finds lowest-cost path
  - Like Dijkstra's algorithm
  - Uses priority queue (cost-based)
  - No heuristic guidance
- **Best for**: Weighted graphs with varying costs
- **Watch for**: More exploration than A* but guaranteed optimal

**Beam Search**
- **How it works**: Like BFS but keeps only k best nodes at each level
- **Color**: Purple
- **Characteristics**:
  - **Not complete**: May miss the goal if pruned early
  - Memory efficient compared to BFS
  - Practical compromise between A* and BFS
  - Can adjust beam width for different memory/quality trade-offs
- **Best for**: Memory-limited systems, quick good-enough solutions
- **Watch for**: May miss solutions if beam width too narrow

### Interactive Learning Exercises

**Exercise 1: Shortest Path Comparison**
- Objective: See which algorithm finds the true shortest path
- Steps:
  1. Create a simple maze with at least 2 different paths to the goal
  2. Run BFS and A* side by side
  3. Both should find equally short paths
  4. Now run Greedy - it might take a longer route
- Result: Understand optimality vs heuristics

**Exercise 2: Exploration Pattern**
- Objective: Visualize different search patterns
- Steps:
  1. Use default maze
  2. Set speed to slow (leftmost slider position)
  3. Enable only DFS, watch the deep exploration pattern
  4. Reset and enable only BFS, watch the wave-like pattern
  5. Enable A* and notice it aims toward the goal
- Result: Understand search strategy differences

**Exercise 3: Algorithm Limitations**
- Objective: See when algorithms fail
- Steps:
  1. Create a maze where Hill Climbing gets stuck
  2. Watch Hill Climbing fail at certain configurations
  3. See how other algorithms handle the same maze
- Result: Understand why different algorithms exist

**Exercise 4: Performance Metrics**
- Objective: Compare efficiency metrics
- Steps:
  1. Create the same maze for all tests
  2. Run each algorithm individually
  3. Note the "steps explored" count shown on right panel
  4. Create a comparison table of explored nodes vs path length
- Result: Understand time and space complexity trade-offs

---

## 📊 Algorithm Comparison

| Algorithm | Type | Optimality | Completeness | Remarks |
|-----------|------|-----------|--------------|---------|
| DFS | Uninformed | ❌ No | ✅ Yes | Explores deeply, can get stuck in long paths |
| BFS | Uninformed | ✅ Yes | ✅ Yes | Finds shortest path, explores level by level |
| A* | Informed | ✅ Yes | ✅ Yes | Uses heuristic + cost, very efficient |
| Greedy | Informed | ❌ No | ✅ Yes | Fast but not always optimal |
| Hill Climbing | Local | ❌ No | ❌ No | Can get stuck in local maxima |
| UCS | Cost-based | ✅ Yes | ✅ Yes | Considers path costs uniformly |
| Beam Search | Limited | ❌ No | ❌ No | Practical compromise between memory and quality |

---

## 🐛 Troubleshooting

**Issue**: Pygame window doesn't open
- **Solution**: Ensure Pygame is properly installed with `pip install -r requirements.txt`

**Issue**: Images not loading
- **Solution**: Make sure the `images/` folder contains all required PNG files (dfs.png, bfs.png, astar.png, etc.)

**Issue**: Algorithm not finding path
- **Solution**: Check that start and end positions are properly set and not blocked by walls

**Issue**: Performance is slow
- **Solution**: Reduce the maze size or use the speed slider to adjust animation speed

**Issue**: Can't create a custom map
- **Ensure**:
  1. You've selected "Create Map" from the menu
  2. You're dragging the mouse to select regions
  3. You're pressing the correct keys (1=start, 2=end, 3=wall, 4=delete)
  4. The region is properly selected before creating walls

**Issue**: Algorithms running too fast to see
- **Solution**: Move the speed slider all the way to the left for slowest animation speed

**Issue**: Algorithm seems stuck or not moving
- **Solution**: 
  1. Make sure start and end positions are set (different colors should appear)
  2. Try resetting with a new maze
  3. Check if walls completely block all paths

### Performance Tips
- For slower computers, reduce the number of simultaneous algorithms
- Use lower speed settings to reduce rendering load
- Create simpler mazes (smaller size) for testing
- Close other applications to free up system resources

---

## 📝 Project Structure
```
├── main.py              # Main game application and algorithm implementations
├── test.py              # Unit tests for algorithms
├── requirements.txt     # Python dependencies
├── images/              # Game sprites and icons
│   ├── bg.png          # Background image
│   ├── wall.png        # Wall texture
│   ├── finish.png      # Goal marker
│   ├── player.png      # Player sprite
│   ├── dfs.png         # DFS algorithm icon
│   ├── bfs.png         # BFS algorithm icon
│   ├── astar.png       # A* algorithm icon
│   ├── greedy.png      # Greedy algorithm icon
│   ├── hillclimbing.png # Hill Climbing algorithm icon
│   ├── ucs.png         # UCS algorithm icon
│   └── beam.png        # Beam Search algorithm icon
└── README.md           # This file
```

---

## 🎓 Learning Outcomes
By using this application, you'll understand:
- How different pathfinding algorithms work in practice
- The trade-offs between optimality, completeness, and efficiency
- How heuristics improve search performance
- Real-world applications of pathfinding in AI and game development
- Visual debugging and algorithm tracing

---

## 📚 References
- Breadth-First Search (BFS): Classic uninformed search algorithm
- Depth-First Search (DFS): Explores as far as possible along each branch
- A* Algorithm: Combines actual cost and heuristic estimate
- Greedy Best-First: Uses only heuristic without actual cost
- Uniform Cost Search: Expands lowest-cost paths first
- Hill Climbing: Local search that improves iteratively
- Beam Search: Limited memory variant of best-first search

---

## 🔗 Common Scenarios & How to Handle Them

### Scenario: Comparing BFS vs A* Performance
1. Load default maze or create a simple one
2. Note the start and end positions
3. Run only BFS - count the explored nodes shown on right
4. Reset the maze (create new/reload)
5. Run only A* - compare explored nodes count
6. A* should explore fewer nodes due to heuristic guidance
7. **Check results**: Compare the statistics panels
   - Path length should be identical (both optimal)
   - A* nodes explored should be ≤ BFS nodes explored
   - Document the efficiency improvement

### Scenario: Understanding Why DFS Can Fail
1. Create a maze where DFS might take a very long path
2. Run DFS alone
3. Watch it explore deeply in wrong directions
4. Reset and run BFS for comparison
5. See how BFS finds the goal faster despite exploring similar areas first
6. **After completion**: Compare path lengths
   - DFS path will likely be longer
   - BFS path will be shorter
   - Understand why: DFS has no goal awareness

### Scenario: Optimal Path Verification
1. Create a simple maze manually
2. Visually identify the shortest path
3. Run BFS (guaranteed to find shortest)
4. Run A* (should match BFS for unweighted maze)
5. Run Greedy (might differ)
6. Verify the paths shown match your expectations
7. **After completion**: Check if all optimal-guaranteeing algorithms found the same path
   - BFS and A* should match
   - Greedy might be longer
   - Record the differences

### Scenario: Teaching Others
1. Start with BFS only - show the wave-like exploration
2. Add DFS to show the deep-first pattern
3. Add A* to show heuristic-guided search
4. Run all together and let viewers see different approaches
5. **Review together**: Look at the final results
   - Point out differences in paths
   - Discuss exploration patterns
   - Highlight algorithm characteristics
6. Compare the statistics and discuss why they differ

### Scenario: Detailed Performance Analysis
1. Create a test maze
2. Run Algorithm A, screenshot the results
3. Reset maze (same layout)
4. Run Algorithm B, screenshot the results
5. Run Algorithm C, screenshot the results
6. **Analyze side-by-side**:
   - Create a comparison table with all results
   - Calculate efficiency (nodes/path)
   - Rank algorithms by efficiency
   - Identify which are optimal and which are not
7. Draw conclusions about performance differences

---

## 💡 Key Insights to Gain

1. **Uninformed Search (DFS, BFS)**
   - Work without knowledge of target location
   - BFS guarantees shortest path but uses more memory
   - DFS uses less memory but may find longer paths

2. **Informed Search (A*, Greedy)**
   - Use heuristic function to guide search
   - A* is optimal when heuristic is admissible
   - Greedy is faster but may miss optimal solution

3. **Cost-Based Search (UCS)**
   - Important when edges have different weights
   - In this maze (unweighted), similar to BFS
   - Would differ significantly with weighted edges

4. **Practical Considerations**
   - Real-world often prefers A* or Greedy for speed
   - BFS when guarantee of optimality is critical
   - Memory constraints might force Beam Search or DFS

5. **Heuristic Quality**
   - Good heuristic = fewer nodes explored = faster
   - Manhattan distance is good for grid-based mazes
   - Watch how A* exploits the heuristic vs greedy

---

## 🎮 Advanced Features Explained

### Speed Slider
- **Far Left (Slowest)**: 1 step per several frames - great for learning
- **Middle**: Comfortable observation speed
- **Far Right (Fastest)**: Algorithms run as fast as possible
- **Pro Tip**: Start slow to understand, speed up for testing multiple mazes

### Algorithm Checkboxes
- **Individual**: Run one at a time for focused analysis
- **Multiple**: Run 2-3 to compare specific algorithms
- **Activate All**: Run all 7 simultaneously to see complete picture
- **Note**: Performance depends on computer speed

### Statistics Panel (Right Side)
- **Algorithm Name**: Which algorithm is running
- **Nodes Explored**: Total cells examined (not including final path)
- **Path Length**: Steps from start to goal
- **Execution Status**: Showing if algorithm is active/completed

### Visualization Colors
- Used for quick visual comparison
- Each algorithm has distinct color to prevent confusion
- Lighter shades show exploration area
- Brighter colors show final path taken

---

## 📊 Expected Results by Algorithm

### In a Simple Rectangular Maze
- **DFS**: Variable performance, depends on wall placement
- **BFS**: Optimal, systematic exploration
- **A***: Very efficient, similar steps to BFS
- **Greedy**: Fast, may take longer path
- **Hill Climbing**: Often fails or gets stuck
- **UCS**: Similar to BFS in unweighted maze
- **Beam Search**: Decent, faster than BFS with beam width limit

### In a Complex Multi-Path Maze
- Differences become more obvious
- Heuristic-based algorithms (A*, Greedy) stand out
- BFS still optimal but explores more
- DFS performance becomes very variable

### In Open Spaces with Few Walls
- All algorithms become more similar
- Pathfinding becomes trivial
- Best for testing very different algorithms only

---

## 🎓 Questions to Ask While Using

1. **Why does [algorithm X] explore so many cells?**
   - Consider whether it uses heuristics
   - Check if it's prioritizing by cost, heuristic, or order

2. **Why does [algorithm X] find a longer path?**
   - It may not guarantee optimality
   - Check its optimality property in the comparison table

3. **Can [algorithm X] get stuck?**
   - Check completeness property
   - Test in a complex maze

4. **Which algorithm should I use for [application]?**
   - Game pathfinding: A* or Greedy
   - Route planning with costs: UCS
   - Simple shortest path: BFS
   - Limited memory: Beam Search or DFS

5. **How would this change with weighted edges?**
   - Imagine different edge costs
   - Consider which algorithms account for costs
   - UCS and A* become more valuable

---

## 📄 License & Credits
Developed as part of the **Artificial Intelligence** course at HCMUTE.
[📋 View License](LICENSE)
For questions or improvements, feel free to contribute!

