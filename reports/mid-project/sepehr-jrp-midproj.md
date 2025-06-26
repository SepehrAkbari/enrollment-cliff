Sepehr Akbari<br>
James Rocco Project '25<br>
Jun 27th, 2025

# Mid-Project Report

### Mid-Project Report: Analyzing Higher Education Institution Closures

#### Hook: The Silent Crisis in Higher Education

Imagine a future where hundreds of colleges across the United States vanish, leaving students, faculty, and communities in disarray. This isn’t science fiction—it’s a looming reality driven by demographic shifts, financial strain, and the aftermath of global crises like COVID-19. Drawing inspiration from Nathan D. Grawe’s seminal work, *Demographics and the Demand for Higher Education* (2018), this project dives into the factors behind college closures, blending data-driven analysis with insights from recent literature to uncover why some institutions thrive while others fade.

#### Project Overview

This mid-project report synthesizes preliminary findings from a comprehensive analysis of higher education institution closures in the U.S. Using a dataset of 58 closed colleges (sourced from IPEDS, NTSE, and DataUSA, accessed May–June 2025), the study employs k-means clustering, t-SNE, PCA, and LDA to identify patterns in closures. Additionally, a literature review draws on key works to contextualize these findings within broader trends, such as the enrollment cliff and shifting educational priorities.

#### Preliminary Findings
1. **Clustering Insights**:
   - K-means clustering with 7 clusters reveals distinct groups, potentially tied to institutional size, endowment levels, and regional demographics. Feature importance analysis highlights `endowmentMedian` and `totalEnrollment` as top drivers, with per-college explanations showing colleges like “Alderson Broaddus University” clustered due to low endowments.
   - T-SNE visualizations suggest non-linear groupings, with some outliers possibly linked to unique closure reasons.

2. **Dimensionality Reduction**:
   - PCA indicates that approximately 10–20 components capture 95% of the variance, with eigenvalues pointing to state-level metrics (e.g., `statePopulationMedian`) and financial health as key factors.
   - LDA, applied to a new `reasonClosure` column combining four closure reasons (e.g., “03” for financial and mutual benefit), yields higher-dimensional results, suggesting complex interactions between reasons like financial distress and enrollment drops.

3. **Topic Analysis with LDA**:
   - Preliminary LDA on textual data (e.g., institutional descriptions or reason narratives) identifies dominant themes: financial instability, demographic decline, and pandemic-related disruptions. These align with Grawe’s predictions of reduced demand due to shrinking youth populations.

4. **Literature Context**:
   - Grawe (2018) frames closures as a response to demographic shifts, a trend echoed by Carey (2022), who notes a shift toward job-oriented programs amid declining enrollment.
   - Lo and Yong (2021) highlight COVID-19’s impact on admissions, while Burns et al. (2022) detail student outcomes post-closure, underscoring the human cost.
   - Schuette (2023) and Campion (2020, 2022) offer strategies like retention and outreach, contrasting with Busch’s (2017) critique of neoliberal education models.

#### Challenges and Next Steps
- **Data Gaps**: Missing `endowmentMedian` values (imputed with -1) may skew clustering; further validation is needed.
- **Interpretability**: Overlapping labels in visualizations (58 colleges) require refinement, possibly with interactive tools.
- **Future Work**: Expand LDA with more textual data, validate clusters against financial health grades (Doyle, 2024), and integrate geographic risk models (O’Neil, 2020) to predict future closures.

#### Conclusion
This project lays a foundation for understanding college closures through Grawe’s demographic lens, revealing financial and enrollment pressures as central themes. As the analysis deepens, it promises to guide policy and institutional strategies to navigate this crisis. Stay tuned for a final report that could reshape how we view the future of higher education.

#### Literature Review (Preliminary)
- **Demographic Drivers**: Grawe (2018) argues that declining birth rates will reduce college demand, a hypothesis supported by Dorn et al. (2020) and Seybold (2024), though the latter challenges its inevitability.
- **Economic and Policy Responses**: Carey (2022) and Schuette (2023) advocate for job-oriented shifts and retention strategies, while Busch (2017) critiques this neoliberal pivot, suggesting a need for broader educational value.
- **Crisis Impacts**: Lo (2021) and Burns (2022) link COVID-19 and closures to student well-being, with U.S. data (2024) emphasizing education exports as an economic buffer.
- **Strategic Adaptations**: Campion (2020, 2022) and Harrison (2017) propose retention and widening participation, offering actionable insights beyond mere survival.

This draft reflects early insights, with the bibliography (`references.bib`) providing a robust foundation for further exploration. Feedback from my advisor will refine this into a cohesive narrative.