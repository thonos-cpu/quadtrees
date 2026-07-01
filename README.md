# 3D Spatial Indexing with an Octree + MinHash

A small spatial-search project built for a data-structures course. It indexes
3D points with an **octree** for fast range queries, and uses **MinHash + LSH**
to find textually similar items among the points a query returns.

The worked example treats coffee reviews as 3D points — `(rating, price,
review_date)` — and answers questions like *"show the reviews with rating
80–100, price 0–20, from this date range, then find ones with similar
descriptions."*

> The repo is named `quadtrees`, but the implementation is its 3D
> generalisation, an **octree** (each node splits into 8 octants, not 4).

## Files

| File | Role |
| --- | --- |
| `test.py` | Core library: the `point`, `Cuboid` and `Octree` classes (insert / delete / range query) plus cuboid helpers for plotting. |
| `data.py` | End-to-end pipeline: loads the CSV, builds the octree, runs a range query, then MinHash/LSH similarity search. |
| `user_gui.py` | A small Tkinter form for entering the query ranges. |
| `coffee_analysis.csv` | Sample dataset of coffee reviews. |

## Install & run

```bash
pip install pandas numpy plotly scikit-learn datasketch tkcalendar
python data.py        # opens the query form, then prints matching + similar reviews
```

## Using the octree directly

```python
from test import point, Cuboid, Octree

# A region covering rating 80-100, price 0-20, day-offset 0-2200
tree = Octree(1, Cuboid(80, 0, 0, 20, 20, 2200))

tree.insert(point(92, 7.5, 410, "bright, citrusy, clean finish"))
tree.insert(point(85, 4.0, 120, "nutty and mild"))

# Range query: [x_lo, x_hi], [y_lo, y_hi], [z_lo, z_hi]
hits = tree.query_by_range([90, 100], [0, 10], [0, 510])
for p in hits:
    print(p)
```

## How it works

1. **Octree** — points are inserted into a leaf until it exceeds its capacity,
   at which point the leaf subdivides into 8 octants and re-homes its points.
   Range queries prune whole sub-trees whose cuboid does not intersect the
   query box, so only relevant branches are visited.
2. **MinHash + LSH** — each review's text gets a MinHash signature; a
   `MinHashLSH` index then retrieves textually similar reviews among the
   octree's query results without comparing every pair.
