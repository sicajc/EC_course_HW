# K-means
## Method1
1. (Naive) approach of finding every possible outcome in search space of <br /> $repr = [c_1,c_2,c_3,c_4,c_5....]$
Finding clusters in such way is not practical when size of search space is large.

## Method2
1. Modify the vector Representations s.t. the serach space is shrunk.
2. Each individual is now a multi-dimensional vector.
3. Mutation -> CrossOver -> Fitness Calculation.
4. Fitness function is k-means equation $Q = \Sigma \Sigma u_i ||x_k - v_i||^2$
5. Cons: Expensive calculation occurs when finding distance between each data points.

# Fuzzy Clustering
1. Traditional methods might run into problem due to noise presented within the dataSets s.t. it cannot find the cluster.
2. In Fuzzy set, 1 individual can partially belong to a certain group.
3. Doing so tiny pepper noise would not be distinguish into another group.
4. What elements are on the boundary of the clusters? Very hard problem to solve.
5. One ca acutllay allow the partition matrix to have fuzzy Partition matrix structure.

# Fuzzy C-mean clustering
1. We need an auxiliary function to construct the partition matrix. The choice of relation might differs.
2. Doing so can easily identify borders & marginal regions, making it able to handle with noisy data.
3. Fuzzy partition matrix can be calculated in EA.


# Fuzzy graph partitioning.
1. We can try to apply EA algorithm to this.

## EA algorithm excels
1. As long as data representation and mutationRate can be chosen, most problem can be conquered by EA.
2. It enables you to generate clusters on a 2-D mesh graph.
3. Fuzzy set theory and clustering is good at dealing with some problems.

## Girvan-NewMan community structure algorithm
1. Based on weight betweeness metrics and assume that clusters are delineated by regions.
2. Connecting the clusters with high connectivities. Also it is easy to implement.
3. Straightforward implementation cost $\Omicron (N^3)$ which is not good at all.
4. Clever way of implementing this can prevent this expensive cost.


# Hybridize
1. With hybrid algorithm we can tailor the problem to specific sets. We are be able to extract huge performance from it. Because EA takes too much time, so we need to hybridize each steps of flow with other algorithms to speed up each sections.

# Memetic algorithm
1. Adaptive memetic algorithm is useful.