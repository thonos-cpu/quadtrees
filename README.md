🌟 3D Spatial Indexing with Octree & MinHash 🌟
Welcome to the 3D Spatial Indexing project! This repository contains Python code to manage 3D point data using an Octree data structure and perform similarity search using MinHash. The project is perfect for scenarios requiring spatial queries, fast indexing, and similarity-based retrieval of large sets of 3D data.

📂 Project Overview
This repository is composed of three primary files:

data.py - Handles data processing, MinHash creation, similarity searches, and octree construction.
test.py - Defines the Point, Cuboid, and Octree classes, including methods for spatial querying and cuboid visualization.
user_gui.py - Contains code for user interface input handling, where users can define query ranges for finding similar reviews and points.
⚙️ Key Components
1. Octree Data Structure (Spatial Partitioning)
The Octree class efficiently manages 3D data by partitioning space into smaller cuboids. It supports operations like:

Insert Points into the tree
Subdivide the space into smaller cuboids when a cuboid's capacity is reached
Query points in a specific range (in the X, Y, and Z axes)
Delete points from the tree

2. MinHash for Similarity Search
MinHash is used to perform approximate similarity searches on text data. Using Locality Sensitive Hashing (LSH), the code can quickly find similar reviews based on their combined descriptions.

3. Data Processing & Visualization
Data Preprocessing: The dataset is cleaned, with the reviews processed and transformed into numerical data for spatial indexing.
Visualization: 3D points and cuboids can be visualized using Plotly for spatial analysis.

🚀 Getting Started
🛠 Installation
To run this project locally, you’ll need Python installed. You can install the required dependencies using the following commands:

bash
# Clone the repository
git clone https://github.com/thonos-cpu/quadtrees.git

# Navigate to the project directory
cd quadtrees

# Install dependencies
pip install -r requirements.txt
The requirements.txt file contains all necessary dependencies, including:

pandas for data manipulation
datasketch for MinHash and LSH functionality
plotly for 3D plotting
sklearn for PCA
matplotlib for additional plotting (in test.py)

⚡ Run the Code
To run the program and visualize the results:

Ensure that the data (coffee_analysis.csv) is available in the correct location.
Execute the main script:
bash
python data.py

🏗️ File Breakdown
📁 data.py - Data Preprocessing & MinHash Similarity
Imports: Libraries like pandas, datasketch, plotly, etc.
Data Loading: Loads a CSV file containing reviews and preprocesses the data.
MinHash Creation: Uses MinHash to generate signatures of the combined review descriptions.
LSH Indexing: Creates an LSH index to retrieve similar reviews.
Octree Construction: Constructs an octree and inserts points based on review data (rating, price, etc.).
User Queries: Handles queries based on user inputs (ranges for rating, price, and review date).
📁 test.py - Defining Octree, Point, and Cuboid Classes
Point Class: Represents a 3D point with x, y, z coordinates and optional description t.
Cuboid Class: Represents 3D cuboids used in the octree for spatial partitioning.
Octree Class: Manages 3D points by subdividing space into smaller cuboids and supports insert, query, and delete operations.
Cuboid Visualization: Includes functionality to visualize cuboids in 3D using Plotly.
Recursive Collection: Gathers all cuboids recursively for visualization.

📁 user_gui.py - User Input Handling
User Interface: Collects inputs for querying the octree and similarity searches.
Query Range Inputs: Allows the user to define minimum and maximum values for rating, price, and review date to perform spatial queries.

💡 How It Works
Data Ingestion: The data (e.g., reviews) is read from a CSV file.
Octree Construction: Points (based on review attributes like rating, price, and date) are inserted into the octree structure.
MinHash Indexing: Descriptions of reviews are processed using MinHash to create their signature. Similar reviews are indexed using LSH for efficient searching.
User Queries: Users can query the octree for points within a given range and find similar reviews based on the MinHash similarity.
Example Query
python
# Query for reviews with a rating between 80 and 100, price between 0 and 20 USD, and review date between 2017 and 2025
results = octree.query_by_range([80, 100], [0, 20], [0, 510])
Find Similar Reviews
python
similar_reviews = find_similar_reviews(index_to_query, lsh, results, n_similar=5)
📊 Data Visualization
Plot Points in 3D
The octree's points can be visualized using Plotly’s 3D scatter plots.
You can also visualize the cuboids by drawing lines around them.
Example of 3D plot:
python
fig = go.Figure(data=[points_trace] + lines)
fig.show()


🧠 What You’ll Learn
Spatial Partitioning with Octree: How to manage large 3D datasets efficiently.
Similarity Search with MinHash: Learn how to implement and use MinHash for quick approximate similarity searches.
Data Preprocessing and Querying: Get hands-on experience with cleaning and querying real-world data.
🚀 Contributing

We welcome contributions! To get involved:
Fork the repository.
Clone your fork locally.
Create a new branch for your changes.
Push your changes and submit a pull request.


Happy Coding! 🎉👨‍💻👩‍💻
