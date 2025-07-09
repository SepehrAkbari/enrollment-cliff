<style>body {text-align: justify}</style>

Sepehr Akbari<br>
James Rocco Project '25<br>
Jul 4th, 2025

# Report: Week 6

### Week 3-6 goals (per proposal):

- Development of models outlined in Technical Approach
- Drafting introduction and initial findings of paper

### **Accomplishments**

- **Fine-tuning LDA**: I spent some time fine-tuning the LDA model's parameters to improve topic coherence. All thats left to be done here is to add stop-words to the model, so that it produces more meaningful topics. This will be probably be done at the very end, when we are including the model in the paper.

- **Cluster Analysis**: I got the SHAP values for each feature in each cluster, which will be used to interpret them. I also made a spider plot for each to communicate the differences between them.

- **Feature Analysis**: I added two modules: (1) a module to calculate SHAP value of a feature across all clusters, and report its rank in the cluster, and (2) a module to calculate the median of the scaled values of each feature and reverse scale them to the make them interpretable. These will be useful to understand what kind of anomalies or outliers there are, and evaluate how the k-means is performing.

- **Adding Data**: I added data from IPEDS, for the number of degree-awarding institutions in each state and region, and the number of institutions that are closed, per year 2020-2023. I imputed these values for 2024 and 2025 as well.

- **Initial BHM**: Based on my understanding of the example in the book, I created an initial Bayesian Hierarchical Model (BHM). This was really just a starting point, and I will be working on it more over the next week.