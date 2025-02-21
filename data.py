import pandas as pd
from datetime import datetime
from test import *
from datasketch import MinHash, MinHashLSH
from sklearn.decomposition import PCA
import time
import plotly.graph_objects as go

def create_minhash(text, num_perm=128):
    minhash = MinHash(num_perm=num_perm)
    for word in text.split():
        minhash.update(word.encode('utf8'))
    return minhash


def find_similar_reviews(index, lsh_index, results, n_similar=5):
    query_minhash = results[index].minhash 
    similar_indices = lsh_index.query(query_minhash) 
    similar_reviews = [results[int(idx)].combined_desc for idx in similar_indices]
    return similar_reviews[:n_similar]


df = pd.read_csv("C:/Users/tasis/Desktop/sxoli/code/quad-trees/coffee_analysis.csv")

for _ in range(20):    
    df = df._append(df.tail(1000), ignore_index=True)
print(df.shape) 

df['combined_desc'] = df['desc_1'] + " " + df['desc_2'] + " " + df['desc_3']
df['review_date'] = pd.to_datetime(df['review_date'], format='%B %Y')
df = df[df['loc_country'] == 'United States']
#convert 'review_date' to days since 01/01/2017
base_date = datetime(2017, 1, 1)
df['review_date'] = (df['review_date'] - base_date).dt.days






#create point objects and insert them into the Octree
points =[point(row['rating'], row['100g_USD'], row['review_date'], row['combined_desc']) for _, row in df.iloc[:].iterrows()]

boundary = Cuboid(80, 0, 0, 100, 20, 2200) #all of our sample ratings are above 80 so no need to create larger cuboid, same with rating. goes up to 20
octree = Octree(1, boundary) #1 is the maximum allowed point per octree

for p in points:
    octree.insert(p)

from user_gui import *

start_time = time.time()  #start timer to calculate the milliseconds needed for our program to do the query and find the n-similar reviews

results = octree.query_by_range([rating_min, rating_max], [usd_min, usd_max], [start_days, end_days]) #we do a query on user-given values


for result in results:
    result.combined_desc = result.t.lower()  #convert the combined_desc to lowercase
    result.minhash = create_minhash(result.t)

lsh = MinHashLSH(threshold=0.1, num_perm=128) 
for idx, result in enumerate(results):
    lsh.insert(str(idx), result.minhash)
end_time = time.time()

minhash_vectors = np.array([np.array(result.minhash.hashvalues) for  result in results])


if results:
    print("Points found within the range:")
    for point in results:
        print(point) #print all points that lie between the user-given range
else:
    print("No points found within the specified range.")


index_to_query = 0
similar_reviews = find_similar_reviews(index_to_query, lsh, results, n_similar=3) #based on the results, find the n_similar - similar reviews

#print similar reviews with two empty lines between them
print("Similar Reviews:\n")
for review in similar_reviews:
    print(review)
    print("\n\n")


#cuboids = []
#collect_cuboids(octree, cuboids)


 #Plot points
#points_trace = go.Scatter3d(
#    x=[p.x for p in results],
#    y=[p.y for p in results],
#    z=[p.z for p in results],
#    mode='markers',
#    marker=dict(size=2, color='red'),
#    name='Points'
#)
#
#print(f"Number of points: {len(results)}")
#print(f"Number of cuboids: {len(cuboids)}")
#
## Plot cuboids
#lines = []
#for cuboid in cuboids:
#    cuboid_lines = draw_cuboid(cuboid)
#    for line in cuboid_lines:
#        if line[0] and line[1] and line[2]:  # Ensure all axes have data
#            lines.append(go.Scatter3d(
#                x=line[0], y=line[1], z=line[2],
#                mode='lines',
#                line=dict(color='#0000FF', width=2),  # Use a hex code for color
#                showlegend=False
#))
#
#
#
#
#
#fig = go.Figure(data=[points_trace] + lines)
# #Set figure layout
#fig.update_layout(
#    scene=dict(
#        xaxis=dict(range=[80, 100]),
#        yaxis=dict(range=[0, 20]),
#        zaxis=dict(range=[0, 510]),
#    ),
#    title="Octree Visualization"
#)
#
elapsed_time = end_time - start_time
print(elapsed_time * 1000, " ms")
#
#fig.show()

