Sepehr Akbari<br>
James Rocco Project '25<br>
Jun 20th, 2025

# Report: Week 4

### Week 3-6 goals (per proposal):

- Development of models outlined in Technical Approach
- Drafting introduction and initial findings of paper

### **Accomplishments**

**Data Cleaning:**

- Last week, I collected a lot of data from different sources, and made two data frames, one containing information on states and their demographics, births, and education related data, and the other containing information on 66 closed higher education institutions in the US, their demographics, characteristics, and their financial data. This week I merged these two data frames, and after some minor data preparations, I was able to create a comprehensive data frame ready for analysis and modeling.
- I constructed a pipeline, involving scaling and encoding variables. This allows us to easily apply the same transformations to new versions of our data frame in the period of our modeling and analysis.

**Modeling & Analysis:**

The initial goal of this week was to perform the following analyses:

- **Principle Component Analysis (PCA):** 
    - I performed PCA on the data frame, we found the first 5 principle components to explain about 75% of the variance in the data. Furthermore 95% of the variance can be explained by just 15 components.
    - I explored the eigenvalues, and found the 2 largest ones to be explaining a lot of the data, which is a good sign that PCA is a successful tool to reduce the dimensionality of our data.

- **Clustering (k-means):**
    - I performed k-means clustering on the data frame. First, to determine the optimal number of clusters, I used the elbow method. The relation between inertia and number of clusters was unexpected and could not clearly indicate the optimal number of clusters. I had to manually take action to reduce the dimensionality of the data frame, which helped me settle on an optimal number of clusters easier.
    - I performed clustering once with PCA components, and once with T-SNE components.

- **Linear Discriminant Analysis (LDA):**
    - To perform LDA, I constructed a new `reason` variable, which contains data from 4 different columns in the data frame, and indicates the reason for closure of the institution.
    - I performed LDA and got very good results. It was able to classify the institutions very clearly.
    - I also performed LDA based on the number of clusters we found in the previous step, and it was able to classify the institutions very well. However, setting the target as the reason for closure, would provide much better understanding of the data.

**Latent Dirichlet Allocation (LDA):**

- I made a new data frame, of one news article per institution to perform topic analysis on using LDA.
- The goal is to explore the topics to understand the reasons for closure of institutions, one level beyond just data.
- There is still some work to be done to perfect our model, yet even the initial results are looking to be an interesting addition to our analysis.
