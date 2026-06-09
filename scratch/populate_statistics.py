import json
import re
import os

# 1. Define Statistics Syllabi
SUBJECT_SYLLABI = {
    "stamd11": {
        "title": "Elementary Statistics",
        "standard_questions": [
            ("Define Statistics and explain its scope and limitations in different fields.", "I"),
            ("Distinguish between primary and secondary data. Explain various methods of collecting primary data.", "I"),
            ("Discuss various types of scales of measurement: nominal, ordinal, interval, and ratio scales.", "I"),
            ("What is a questionnaire? State the main points to be considered in drafting a questionnaire.", "I"),
            ("Explain frequency distribution and cumulative frequency distributions with examples.", "II"),
            ("Describe graphical representation of data: histograms, frequency polygons, and ogives.", "II"),
            ("Define measures of central tendency. What are the characteristics of a good average?", "III"),
            ("Explain arithmetic mean, median, and mode, and write their relative merits and demerits.", "III"),
            ("State and prove the algebraic properties of the arithmetic mean.", "III"),
            ("Define partition values. Explain how quartiles, deciles, and percentiles are computed.", "III"),
            ("Define dispersion and write down various absolute and relative measures of dispersion.", "IV"),
            ("Define range, quartile deviation, and mean deviation, and compare their properties.", "IV"),
            ("What is skewness? Explain Karl Pearson's and Bowley's measures of skewness.", "V"),
            ("Define kurtosis. Differentiate between leptokurtic, mesokurtic, and platykurtic distributions.", "V"),
            ("Describe the stem-and-leaf display and box plot methods for exploratory data analysis.", "V")
        ]
    },
    "stamj11": {
        "title": "Descriptive Statistics",
        "standard_questions": [
            ("Define dispersion. Explain range, quartile deviation, mean deviation, and standard deviation.", "I"),
            ("State and prove that the root-mean-square deviation is minimum when taken about the arithmetic mean.", "I"),
            ("Define variance and coefficient of variation. Write their applications in comparing consistency.", "I"),
            ("What are moments? Distinguish between raw moments and central moments, and derive relations up to fourth order.", "II"),
            ("Define skewness and kurtosis. Explain how they are measured using Sheppard's corrected moments.", "II"),
            ("State and explain Bowley's coefficient of skewness with limits.", "II"),
            ("Define bivariate data and scatter diagrams. State properties of Karl Pearson's coefficient of correlation.", "III"),
            ("State and prove that Karl Pearson's correlation coefficient lies between -1 and +1.", "III"),
            ("Derive the equations of the two regression lines of Y on X and X on Y.", "IV"),
            ("Prove that the correlation coefficient is the geometric mean of the two regression coefficients.", "IV"),
            ("Define Spearman's rank correlation coefficient and derive its formula when ranks are not repeated.", "IV"),
            ("Show that correlation coefficient is independent of change of origin and scale.", "III"),
            ("State the properties of regression coefficients and show that if one is greater than unity, the other must be less than unity.", "IV"),
            ("Explain the concept of curve fitting. Describe the method of least squares for fitting a straight line.", "V"),
            ("Show how to fit a second-degree parabola to a set of bivariate data using least squares.", "V")
        ]
    },
    "stamn11": {
        "title": "Descriptive Statistics",
        "standard_questions": [
            ("Define dispersion. Explain range, quartile deviation, mean deviation, and standard deviation.", "I"),
            ("State and prove that the root-mean-square deviation is minimum when taken about the arithmetic mean.", "I"),
            ("Define variance and coefficient of variation. Write their applications in comparing consistency.", "I"),
            ("What are moments? Distinguish between raw moments and central moments, and derive relations up to fourth order.", "II"),
            ("Define skewness and kurtosis. Explain how they are measured using Sheppard's corrected moments.", "II"),
            ("State and explain Bowley's coefficient of skewness with limits.", "II"),
            ("Define bivariate data and scatter diagrams. State properties of Karl Pearson's coefficient of correlation.", "III"),
            ("State and prove that Karl Pearson's correlation coefficient lies between -1 and +1.", "III"),
            ("Derive the equations of the two regression lines of Y on X and X on Y.", "IV"),
            ("Prove that the correlation coefficient is the geometric mean of the two regression coefficients.", "IV"),
            ("Define Spearman's rank correlation coefficient and derive its formula when ranks are not repeated.", "IV"),
            ("Show that correlation coefficient is independent of change of origin and scale.", "III"),
            ("State the properties of regression coefficients and show that if one is greater than unity, the other must be less than unity.", "IV"),
            ("Explain the concept of curve fitting. Describe the method of least squares for fitting a straight line.", "V"),
            ("Show how to fit a second-degree parabola to a set of bivariate data using least squares.", "V")
        ]
    },
    "stamd21": {
        "title": "Inferential Statistics",
        "standard_questions": [
            ("Define parameter, statistic, and sampling distribution of a statistic.", "I"),
            ("Explain the concept of standard error and write its utility in statistical analysis.", "I"),
            ("Explain the terms: null hypothesis, alternative hypothesis, simple and composite hypotheses.", "II"),
            ("Distinguish between Type I and Type II errors. Define size and power of a test.", "II"),
            ("Describe the procedure of testing of hypothesis. What is critical region?", "II"),
            ("Explain the large sample test for testing the significance of a single mean.", "III"),
            ("Describe the t-test for testing the significance of the difference between two sample means.", "IV"),
            ("Explain the paired t-test for dependent samples with a real-life example.", "IV"),
            ("Describe the F-test for testing the equality of two population variances.", "IV"),
            ("Explain the chi-square test for goodness of fit and write its assumptions.", "V"),
            ("Explain the chi-square test for independence of attributes in a contingency table.", "V"),
            ("Explain the concept of interval estimation. How does it differ from point estimation?", "I"),
            ("Define confidence interval and confidence coefficient with a suitable example.", "I"),
            ("State the assumptions of Student's t-test and discuss its robustness.", "IV"),
            ("Describe how to test the significance of a single correlation coefficient in large samples.", "III")
        ]
    },
    "stamj21": {
        "title": "Introduction to Probability Theory",
        "standard_questions": [
            ("Define random experiment, sample space, mutually exclusive events, and collectively exhaustive events.", "I"),
            ("State classical, empirical, and axiomatic definitions of probability with limitations.", "I"),
            ("State and prove the addition theorem of probability for any two events.", "I"),
            ("Define conditional probability and prove the multiplication theorem of probability.", "I"),
            ("State and prove Bayes' theorem for conditional probability and write its applications.", "II"),
            ("Define random variable. Distinguish between discrete and continuous random variables.", "III"),
            ("Explain probability mass function (pmf) and probability density function (pdf) with properties.", "III"),
            ("Define cumulative distribution function (cdf) of a random variable and state its properties.", "III"),
            ("Define mathematical expectation of a random variable. Prove that $E(XY) = E(X)E(Y)$ for independent variables.", "IV"),
            ("Define Moment Generating Function (MGF) and Probability Generating Function (PGF) and write their properties.", "IV"),
            ("Establish the relationship between moments and moment generating function.", "IV"),
            ("State and prove Chebyshev's inequality and write its importance.", "V"),
            ("Explain the weak law of large numbers (WLLN) and the central limit theorem (CLT).", "V"),
            ("Define independent events. Prove that if A and B are independent, then A' and B' are also independent.", "I"),
            ("Find the MGF of a random variable X with pdf $f(x) = e^{-x}$ for $x > 0$.", "IV")
        ]
    },
    "stamn21": {
        "title": "Introduction to Probability Theory",
        "standard_questions": [
            ("Define random experiment, sample space, mutually exclusive events, and collectively exhaustive events.", "I"),
            ("State classical, empirical, and axiomatic definitions of probability with limitations.", "I"),
            ("State and prove the addition theorem of probability for any two events.", "I"),
            ("Define conditional probability and prove the multiplication theorem of probability.", "I"),
            ("State and prove Bayes' theorem for conditional probability and write its applications.", "II"),
            ("Define random variable. Distinguish between discrete and continuous random variables.", "III"),
            ("Explain probability mass function (pmf) and probability density function (pdf) with properties.", "III"),
            ("Define cumulative distribution function (cdf) of a random variable and state its properties.", "III"),
            ("Define mathematical expectation of a random variable. Prove that $E(XY) = E(X)E(Y)$ for independent variables.", "IV"),
            ("Define Moment Generating Function (MGF) and Probability Generating Function (PGF) and write their properties.", "IV"),
            ("Establish the relationship between moments and moment generating function.", "IV"),
            ("State and prove Chebyshev's inequality and write its importance.", "V"),
            ("Explain the weak law of large numbers (WLLN) and the central limit theorem (CLT).", "V"),
            ("Define independent events. Prove that if A and B are independent, then A' and B' are also independent.", "I"),
            ("Find the MGF of a random variable X with pdf $f(x) = e^{-x}$ for $x > 0$.", "IV")
        ]
    },
    "stamd31": {
        "title": "Basics of Sample Survey and Design of Experiment",
        "standard_questions": [
            ("Explain the difference between census and sample survey. Discuss the advantages of sampling.", "I"),
            ("Define sampling and non-sampling errors and explain how they can be controlled.", "I"),
            ("Explain simple random sampling. Distinguish between SRSWR and SRSWOR.", "II"),
            ("Describe stratified random sampling and discuss proportional and Neyman optimum allocations.", "II"),
            ("Explain systematic sampling and compare its efficiency with simple random sampling.", "II"),
            ("State the basic principles of design of experiments: replication, randomization, and local control.", "III"),
            ("Describe the analysis of variance (ANOVA) technique for one-way classified data.", "IV"),
            ("Describe the analysis of variance (ANOVA) technique for two-way classified data.", "IV"),
            ("Describe the layout, statistical model, and analysis of Completely Randomized Design (CRD).", "V"),
            ("Describe the layout, statistical model, and analysis of Randomized Block Design (RBD).", "V"),
            ("Explain the concept of local control and show how it increases the precision of an experiment.", "III"),
            ("Define a contrast and orthopedic contrasts in analysis of variance.", "IV"),
            ("Discuss the estimation of a single missing plot in a Randomized Block Design.", "V"),
            ("Explain the role of randomization in avoiding systematic bias in designs.", "III"),
            ("Compare the efficiencies of CRD and RBD.", "V")
        ]
    },
    "stamj31": {
        "title": "Basics of Probability Distribution",
        "standard_questions": [
            ("Define Bernoulli distribution and derive its mean and variance.", "I"),
            ("State the conditions under which Binomial distribution is applicable and derive its MGF.", "I"),
            ("Define Poisson distribution as a limiting case of Binomial distribution and derive its mean.", "I"),
            ("Define Geometric distribution. State and prove its memoryless property.", "II"),
            ("Define Negative Binomial distribution and write its relation to Geometric distribution.", "II"),
            ("Define Hypergeometric distribution and write its mean and variance.", "II"),
            ("Define Uniform (Rectangular) distribution and derive its mean and variance.", "III"),
            ("Define Normal distribution and state its chief properties. Show that mean, median, and mode coincide.", "IV"),
            ("Derive the Moment Generating Function of a normal distribution.", "IV"),
            ("Define Exponential distribution and derive its MGF and memoryless property.", "III"),
            ("Define Gamma distribution and derive its mean and variance.", "III"),
            ("Define Beta distribution of first and second kinds and write their properties.", "III"),
            ("Show that the odd-order moments of a normal distribution about its mean are zero.", "IV"),
            ("State and prove the additive property of independent Poisson random variables.", "I"),
            ("Discuss the significance of the normal curve as a model for physical measurements.", "IV")
        ]
    },
    "stamn31": {
        "title": "Basics of Probability Distribution",
        "standard_questions": [
            ("Define Bernoulli distribution and derive its mean and variance.", "I"),
            ("State the conditions under which Binomial distribution is applicable and derive its MGF.", "I"),
            ("Define Poisson distribution as a limiting case of Binomial distribution and derive its mean.", "I"),
            ("Define Geometric distribution. State and prove its memoryless property.", "II"),
            ("Define Negative Binomial distribution and write its relation to Geometric distribution.", "II"),
            ("Define Hypergeometric distribution and write its mean and variance.", "II"),
            ("Define Uniform (Rectangular) distribution and derive its mean and variance.", "III"),
            ("Define Normal distribution and state its chief properties. Show that mean, median, and mode coincide.", "IV"),
            ("Derive the Moment Generating Function of a normal distribution.", "IV"),
            ("Define Exponential distribution and derive its MGF and memoryless property.", "III"),
            ("Define Gamma distribution and derive its mean and variance.", "III"),
            ("Define Beta distribution of first and second kinds and write their properties.", "III"),
            ("Show that the odd-order moments of a normal distribution about its mean are zero.", "IV"),
            ("State and prove the additive property of independent Poisson random variables.", "I"),
            ("Discuss the significance of the normal curve as a model for physical measurements.", "IV")
        ]
    },
    "stamj32": {
        "title": "Sampling Distribution",
        "standard_questions": [
            ("Define Chi-square ($\chi^2$) statistic. Derive its probability density function.", "I"),
            ("State and prove the additive property of independent Chi-square random variables.", "I"),
            ("Define Student's t-statistic. Derive its pdf and write its properties.", "II"),
            ("Define Snedecor's F-statistic. Derive its pdf and write its relation to Chi-square.", "III"),
            ("Discuss the relationship between t, F, and Chi-square distributions.", "III"),
            ("Show that as degrees of freedom tend to infinity, Student's t-distribution tends to normal.", "II"),
            ("State Cochran's theorem on quadratic forms and its importance.", "IV"),
            ("Define standard error of sample mean and sample variance from a normal population.", "I"),
            ("Prove that the square of a t-distributed variable with $n$ degrees of freedom is F-distributed with $(1, n)$ degrees of freedom.", "III"),
            ("Derive the mean and variance of a Chi-square distribution.", "I"),
            ("Discuss the sampling distribution of the range and its applications.", "IV"),
            ("Explain the concept of order statistics and write the joint pdf of the minimum and maximum.", "V"),
            ("Derive the distribution of the $r$-th order statistic from a continuous population.", "V")
        ]
    },
    "stamj41": {
        "title": "Statistical Inference I",
        "standard_questions": [
            ("Explain the concept of point estimation. What are the criteria of a good estimator?", "I"),
            ("Define unbiasedness and consistency of an estimator. Give examples.", "I"),
            ("Define efficiency of an estimator and state the Cramer-Rao inequality.", "II"),
            ("Define sufficiency of an estimator. State and prove the Fisher-Neyman Factorization Theorem.", "III"),
            ("Explain the method of maximum likelihood estimation (MLE) and state its properties.", "IV"),
            ("Describe the method of moments for point estimation with an example.", "IV"),
            ("Explain the concept of interval estimation and define confidence intervals and confidence limits.", "V"),
            ("Derive the $95\%$ confidence interval for the mean of a normal population when variance is known.", "V"),
            ("Explain the minimum chi-square method of estimation.", "IV"),
            ("Discuss the Rao-Blackwell theorem and its application to UMVUE.", "III"),
            ("Show that maximum likelihood estimators are consistent and asymptotically normal.", "IV"),
            ("Define consistency and show that sample mean is consistent for population mean.", "I"),
            ("Explain the Cramer-Rao lower bound for variance of unbiased estimators.", "II"),
            ("Find the sufficient estimator for the parameter $\theta$ of a Poisson distribution.", "III"),
            ("Derive the confidence interval for the difference of two normal means when variances are unequal.", "V")
        ]
    },
    "stamn41": {
        "title": "Statistical Inference I",
        "standard_questions": [
            ("Explain the concept of point estimation. What are the criteria of a good estimator?", "I"),
            ("Define unbiasedness and consistency of an estimator. Give examples.", "I"),
            ("Define efficiency of an estimator and state the Cramer-Rao inequality.", "II"),
            ("Define sufficiency of an estimator. State and prove the Fisher-Neyman Factorization Theorem.", "III"),
            ("Explain the method of maximum likelihood estimation (MLE) and state its properties.", "IV"),
            ("Describe the method of moments for point estimation with an example.", "IV"),
            ("Explain the concept of interval estimation and define confidence intervals and confidence limits.", "V"),
            ("Derive the $95\%$ confidence interval for the mean of a normal population when variance is known.", "V"),
            ("Explain the minimum chi-square method of estimation.", "IV"),
            ("Discuss the Rao-Blackwell theorem and its application to UMVUE.", "III"),
            ("Show that maximum likelihood estimators are consistent and asymptotically normal.", "IV"),
            ("Define consistency and show that sample mean is consistent for population mean.", "I"),
            ("Explain the Cramer-Rao lower bound for variance of unbiased estimators.", "II"),
            ("Find the sufficient estimator for the parameter $\theta$ of a Poisson distribution.", "III"),
            ("Derive the confidence interval for the difference of two normal means when variances are unequal.", "V")
        ]
    },
    "stamj42": {
        "title": "Sample Surveys and Design of Experiment",
        "standard_questions": [
            ("Prove that in SRSWR, the sample mean is an unbiased estimator of population mean.", "I"),
            ("Prove that in SRSWOR, the sample mean is an unbiased estimator of population mean and find its variance.", "I"),
            ("Prove that stratified random sample mean is unbiased, and show that its variance under optimum allocation is less than under proportional.", "II"),
            ("Explain systematic sampling. Prove that systematic sample mean is unbiased.", "II"),
            ("Describe the Completely Randomized Design (CRD) and write its advantages and disadvantages.", "III"),
            ("Describe the Randomized Block Design (RBD) and discuss the estimation of one missing value.", "IV"),
            ("Describe the Latin Square Design (LSD). Write its layout and analysis.", "IV"),
            ("Compare the efficiencies of LSD, RBD, and CRD.", "IV"),
            ("What is a factorial experiment? Describe a $2^2$ factorial experiment and its main and interaction effects.", "V"),
            ("Explain the concept of confounding in factorial designs with an example.", "V"),
            ("Derive the formula for Neyman optimum allocation in stratified sampling.", "II"),
            ("Compare the variance of sample mean in systematic sampling with SRSWOR.", "II"),
            ("Explain the Yates' method of computing factorial effect totals.", "V"),
            ("Describe the split-plot design and its field applications.", "V"),
            ("Show that under SRSWOR, sample variance $s^2$ is unbiased for population variance $S^2$.", "I")
        ]
    },
    "stamj43": {
        "title": "Applied Statistics",
        "standard_questions": [
            ("Define index numbers. What are the problems in construction of index numbers?", "I"),
            ("Explain Laspeyres', Paasche's, and Fisher's ideal index numbers.", "I"),
            ("State and explain the Time Reversal Test and Factor Reversal Test for index numbers.", "I"),
            ("What is time series? Explain the components of a time series: trend, seasonal, cyclical, and irregular.", "II"),
            ("Describe the method of moving averages for determining trend in a time series.", "II"),
            ("Explain the method of least squares for fitting linear and quadratic trends to time series data.", "II"),
            ("Define vital statistics. Explain the measurement of mortality: CDR, SDR, and Infant Mortality Rate.", "III"),
            ("Explain fertility measurements: CBR, GFR, ASFR, and TFR.", "III"),
            ("Define Gross Reproduction Rate (GRR) and Net Reproduction Rate (NRR) and write their significance.", "III"),
            ("What is a Life Table? Describe its components and columns.", "IV"),
            ("Explain the construction of a complete life table from mortality data.", "IV"),
            ("Discuss the demand analysis. State the law of demand and explain price elasticity of demand.", "V"),
            ("Describe the method of family budget surveys for constructing consumer price index numbers.", "I"),
            ("Discuss the ratio-to-trend and link-relative methods of determining seasonal indices.", "II"),
            ("Show that Fisher's index number satisfies both Time Reversal and Factor Reversal tests.", "I")
        ]
    },
    "stamj51": {
        "title": "Operations Research",
        "standard_questions": [
            ("Define Operations Research and explain its applications in decision-making.", "I"),
            ("Formulate the general Linear Programming Problem (LPP) and solve a two-variable LPP graphically.", "I"),
            ("Describe the Simplex method for solving LPP. Explain slack, surplus, and artificial variables.", "II"),
            ("Explain Big-M (penalty) method for solving LPP.", "II"),
            ("State the concept of duality in linear programming and write the dual of a primal LPP.", "III"),
            ("Describe the Transportation Problem. Explain North-West Corner Rule, Least Cost Method, and Vogel's Approximation Method.", "IV"),
            ("Describe the Assignment Problem and explain the Hungarian Method for solving it.", "IV"),
            ("Explain the basic concepts of Queuing Theory and derive the steady-state solution of (M/M/1):(GD/infinity/infinity) queue.", "V"),
            ("Explain the concept of sensitivity analysis in linear programming.", "III"),
            ("Solve a $2 \times 2$ zero-sum game using graphical method.", "V"),
            ("Prove that the dual of the dual is the primal in LPP.", "III"),
            ("Discuss MODI (modified distribution) method for finding optimum transportation cost.", "IV"),
            ("Explain the traveling salesman problem as an assignment problem.", "IV"),
            ("Discuss the queuing parameters: queue length, waiting time in system, and server utilization.", "V")
        ]
    },
    "stamj52": {
        "title": "Numerical Methods",
        "standard_questions": [
            ("Explain the operators $\Delta$, $\nabla$, and $E$, and establish relations between them.", "I"),
            ("Derive Newton's forward and backward interpolation formulas.", "I"),
            ("Derive Lagrange's interpolation formula for unequal intervals.", "II"),
            ("Derive the general quadrature formula for numerical integration.", "III"),
            ("State and derive Trapezoidal rule and Simpson's one-third and three-eighths rules.", "III"),
            ("Describe Newton-Raphson method for finding real roots of algebraic equations.", "IV"),
            ("Explain the basic structure of a C program. Discuss data types and control structures in C.", "V"),
            ("Write a C program to compute the mean and standard deviation of a given array of numbers.", "V"),
            ("Write a C program to implement Simpson's one-third rule for numerical integration.", "V"),
            ("Write a C program to solve a system of linear equations using Gauss elimination.", "V"),
            ("Derive the error terms associated with Trapezoidal and Simpson's integration rules.", "III"),
            ("Explain the differences between Bisection, Regula-Falsi, and Newton-Raphson methods.", "IV"),
            ("Discuss Newton's divided difference interpolation formula.", "II"),
            ("Establish the relation $\Delta = E - 1$ and show how to use it to compute missing terms.", "I")
        ]
    },
    "stamj53": {
        "title": "Statistical Inference II",
        "standard_questions": [
            ("State the Neyman-Pearson fundamental lemma. Explain its use in finding Most Powerful (MP) tests.", "I"),
            ("Define Uniformly Most Powerful (UMP) test and UMP Unbiased (UMPU) test.", "I"),
            ("Explain Likelihood Ratio (LR) test and discuss its asymptotic properties.", "II"),
            ("Describe Wald's Sequential Probability Ratio Test (SPRT) and derive its decision boundaries.", "III"),
            ("Distinguish between parametric and non-parametric tests. Write their advantages.", "IV"),
            ("Explain the Sign test and Wilcoxon signed-rank test for paired observations.", "IV"),
            ("Describe the run test for randomness and median test for two independent samples.", "IV"),
            ("Describe the Kolmogorov-Smirnov one-sample and two-sample tests.", "V"),
            ("Derive the Operating Characteristic (OC) and Average Sample Number (ASN) functions of SPRT.", "III"),
            ("Find the MP test for testing $H_0: \theta = \theta_0$ vs $H_1: \theta = \theta_1$ in a normal population.", "I"),
            ("Explain how to perform a Likelihood Ratio test for the equality of several means.", "II"),
            ("Explain the Wilcoxon-Mann-Whitney U-test and discuss its parametric analogue.", "IV"),
            ("Explain the concept of randomized and non-randomized tests.", "I"),
            ("Derive the critical region for testing the parameter of an exponential distribution using NP lemma.", "I")
        ]
    },
    "stamj61": {
        "title": "Stochastic Processes",
        "standard_questions": [
            ("Define a stochastic process. Distinguish between discrete and continuous parameter processes.", "I"),
            ("Define a Markov chain. Explain transition probability matrix (tpm) and Chapman-Kolmogorov equations.", "II"),
            ("Classify states of a Markov chain: transient, recurrent, periodic, and absorbing states.", "III"),
            ("Define stationary distribution of a Markov chain and write the condition for its existence.", "III"),
            ("Describe the Poisson process. Derive its distribution and discuss its properties.", "IV"),
            ("Explain birth and death processes. Derive the differential-difference equations.", "V"),
            ("Discuss the pure birth process (Yule-Furry process) and obtain its probability distribution.", "V"),
            ("Explain the random walk model on a one-dimensional grid.", "I"),
            ("Define transient state and show that a state is transient if and only if the sum of transition probabilities converges.", "III"),
            ("Find the stationary distribution of a two-state Markov chain.", "III"),
            ("Explain the branching process and define the probability of extinction.", "V"),
            ("Discuss the relationship between Poisson process and exponential distribution.", "IV")
        ]
    },
    "stamj62": {
        "title": "Statistical Process Control and Reliability",
        "standard_questions": [
            ("Explain the concept of statistical quality control (SQC). Distinguish between assignable and chance causes of variation.", "I"),
            ("Describe the construction and working of control charts for variables: $\bar{X}$-chart and R-chart.", "II"),
            ("Describe the construction and working of control charts for attributes: p-chart and c-chart.", "II"),
            ("Explain the concept of acceptance sampling and describe single and double sampling plans.", "III"),
            ("Define reliability of a system. Explain hazard rate and mean time to failure (MTTF).", "IV"),
            ("Derive the reliability of a system when components are connected in series.", "V"),
            ("Derive the reliability of a system when components are connected in parallel.", "V"),
            ("Explain the concept of stand-by systems and obtain the reliability of a two-component stand-by system.", "V"),
            ("Describe the construction of an np-chart and u-chart.", "II"),
            ("Explain the Producer's risk and Consumer's risk in acceptance sampling.", "III"),
            ("State the exponential model of reliability and derive its hazard rate.", "IV"),
            ("Discuss the advantages of local control and local subgroups in quality control.", "I"),
            ("Derive the Operating Characteristic (OC) curve for a single sampling plan.", "III")
        ]
    },
    "stamj63": {
        "title": "Econometrics and Actuarial Statistics",
        "standard_questions": [
            ("Define econometrics. Explain the general linear regression model.", "I"),
            ("What is multicollinearity? Discuss its consequences and detection methods.", "II"),
            ("Explain heteroscedasticity and describe Goldfeld-Quandt and Park tests.", "III"),
            ("What is autocorrelation? Explain Durbin-Watson test.", "III"),
            ("Explain utility theory and its application in insurance.", "IV"),
            ("Define net premiums and write down the premium calculation principles.", "IV"),
            ("Describe the basic models in credibility theory.", "V"),
            ("Discuss the generalized least squares (GLS) estimation method.", "I"),
            ("Explain the consequence of heteroscedasticity on OLS estimators.", "III"),
            ("What is the difference between pure premium and gross premium in insurance?", "IV")
        ]
    },
    "stamj64": {
        "title": "Official and Vital Statistics",
        "standard_questions": [
            ("Describe the role of CSO (Central Statistical Office) and NSSO in the Indian statistical system.", "I"),
            ("Explain the population census method in India and its major stages.", "II"),
            ("Discuss vital statistics. Explain various registration systems of births and deaths.", "III"),
            ("What are the main functions of Ministry of Statistics and Programme Implementation (MoSPI)?", "I"),
            ("Describe the national income estimation in India and its main methods.", "IV"),
            ("Discuss agricultural statistics in India, focusing on crop acreage and yield estimation.", "V")
        ]
    }
}

# 2. Define get_custom_answer_key
def get_custom_answer_key(key, question):
    q_lower = question.lower()
    
    if "probability" in q_lower or "axioms" in q_lower or "bayes" in q_lower or "independent" in q_lower:
        return "1. **Axioms of Probability**:\n- Axiom 1: $P(A) \\ge 0$ for any event $A$.\n- Axiom 2: $P(S) = 1$ for the sample space $S$.\n- Axiom 3: For mutually exclusive events, $P(\\bigcup A_i) = \\sum P(A_i)$.\n2. **Bayes\\' Theorem**:\n$$P(B_i | A) = \\frac{P(B_i)P(A|B_i)}{\\sum_{j=1}^n P(B_j)P(A|B_j)}$$\n3. **Independent Events**:\nTwo events $A$ and $B$ are independent if $P(A \\cap B) = P(A)P(B)$."

    elif "mean" in q_lower or "median" in q_lower or "mode" in q_lower or "dispersion" in q_lower or "variance" in q_lower or "deviation" in q_lower:
        return "1. **Central Tendency**:\n- Arithmetic Mean: $\\bar{X} = \\frac{1}{N}\\sum X_i$. It is affected by extreme values.\n- Median: Middle value of sorted data. Not affected by extreme values.\n- Mode: Most frequent value.\n2. **Dispersion**:\n- Standard Deviation: $\\sigma = \\sqrt{\\frac{1}{N}\\sum (X_i - \\bar{X})^2}$. Measures absolute dispersion.\n- Coefficient of Variation: $CV = \\frac{\\sigma}{\\bar{X}} \\times 100\\%$. Measures relative dispersion."

    elif "correlation" or "regression" or "spearman" in q_lower:
        return "1. **Pearson Correlation Coefficient**:\n$$r = \\frac{\\sum(X-\\bar{X})(Y-\\bar{Y})}{\\sqrt{\\sum(X-\\bar{X})^2 \\sum(Y-\\bar{Y})^2}}$$\nIt lies between $-1$ and $+1$.\n2. **Regression Lines**:\n- Line of Y on X: $Y - \\bar{Y} = b_{yx}(X - \\bar{X})$ where $b_{yx} = r \\frac{\\sigma_y}{\\sigma_x}$.\n- Line of X on Y: $X - \\bar{X} = b_{xy}(Y - \\bar{Y})$ where $b_{xy} = r \\frac{\\sigma_x}{\\sigma_y}$."

    elif "sampling" in q_lower or "survey" in q_lower or "srswr" in q_lower or "srswor" in q_lower or "stratified" in q_lower:
        return "1. **SRSWOR vs SRSWR**:\n- In SRSWOR, variance of sample mean is: $Var(\\bar{y}_{wor}) = \\frac{S^2}{n}\\left(1 - \\frac{n}{N}\\right)$.\n- In SRSWR, variance is: $Var(\\bar{y}_{wr}) = \\frac{\\sigma^2}{n}$.\n2. **Stratified Sampling**:\nVariance is minimized under Neyman optimum allocation: $n_h \\propto N_h S_h$."

    elif "binomial" in q_lower or "poisson" in q_lower or "normal" in q_lower or "distribution" in q_lower:
        return "1. **Binomial Distribution**:\n$P(X=x) = \\binom{n}{x} p^x q^{n-x}$. Mean $= np$, Variance $= npq$.\n2. **Poisson Distribution**:\n$P(X=x) = \\frac{e^{-\\lambda}\\lambda^x}{x!}$. Mean $= \\text{Variance} = \\lambda$.\n3. **Normal Distribution**:\n$f(x) = \\frac{1}{\\sigma\\sqrt{2\\pi}}e^{-\\frac{1}{2}\\left(\\frac{x-\\mu}{\\sigma}\\right)^2}$. Symmetrical about $\\mu$."

    elif "test" in q_lower or "hypothesis" in q_lower or "np lemma" in q_lower or "neyman" in q_lower:
        return "1. **Neyman-Pearson Lemma**:\nTo test $H_0: \\theta = \\theta_0$ against $H_1: \\theta = \\theta_1$, the most powerful critical region $W$ is given by:\n$$\\frac{L(x|\\theta_1)}{L(x|\\theta_0)} \\ge k$$\n2. **Errors**:\n- Type I Error ($\\alpha$): Reject $H_0$ when it is true.\n- Type II Error ($\\beta$): Accept $H_0$ when it is false. Power $= 1 - \\beta$."

    elif "anova" in q_lower or "crd" in q_lower or "rbd" in q_lower or "lsd" in q_lower:
        return "1. **ANOVA Principles**:\nSplits total variation into components. $SS_{\\text{Total}} = SS_{\\text{Treatments}} + SS_{\\text{Error}}$.\n2. **Experimental Designs**:\n- CRD: One-way classification. Flexible but less precise.\n- RBD: Two-way classification using local control (blocks) to reduce error.\n- LSD: Three-way classification. Controls variation in two orthogonal directions."

    elif "index number" in q_lower or "laspeyres" in q_lower or "paasche" in q_lower or "fisher" in q_lower:
        return "1. **Index Numbers Formulas**:\n- Laspeyres: $I_L = \\frac{\\sum p_1 q_0}{\\sum p_0 q_0} \\times 100$\n- Paasche: $I_P = \\frac{\\sum p_1 q_1}{\\sum p_0 q_1} \\times 100$\n- Fisher: $I_F = \\sqrt{I_L \\times I_P}$\n2. **Tests**:\nFisher's Ideal Index satisfies both Time Reversal ($I_{01} \\times I_{10} = 1$) and Factor Reversal tests."

    elif "time series" in q_lower or "moving average" in q_lower or "trend" in q_lower:
        return "1. **Time Series Components**:\n$$Y_t = T_t \\times S_t \\times C_t \\times I_t \\quad \\text{(Multiplicative model)}$$\nwhere $T$ is trend, $S$ is seasonal, $C$ is cyclical, and $I$ is irregular.\n2. **Least Squares Trend Fitting**:\nFit line $Y = a + b X$ using normal equations:\n$$\\sum Y = n a + b \\sum X \\quad \\text{and} \\quad \\sum X Y = a \\sum X + b \\sum X^2$$"

    elif "simplex" in q_lower or "transportation" in q_lower or "assignment" in q_lower or "duality" in q_lower:
        return "1. **Simplex Algorithm**:\nIterative procedure to move from one basic feasible solution (BFS) to another along the edges of a convex polytope until an optimal solution is reached.\n2. **Duality Theorem**:\nEvery primal LPP has a corresponding dual LPP. The optimal objective value of the primal is equal to the optimal objective value of the dual."

    elif "stochastic" in q_lower or "markov" in q_lower or "transition probability" in q_lower:
        return "1. **Markov Chain**:\nStochastic process satisfying the Markov property: $P(X_{n+1} = j | X_n = i, ..., X_0 = i_0) = P(X_{n+1} = j | X_n = i) = p_{ij}$.\n2. **Stationary Distribution**:\nVector $\\pi$ satisfying $\\pi P = \\pi$ and $\\sum \\pi_i = 1$."

    elif "control chart" in q_lower or "quality" in q_lower or "reliability" in q_lower:
        return "1. **Control Limits (3-Sigma)**:\n$$UCL = \\mu + 3\\sigma, \\quad LCL = \\mu - 3\\sigma$$\n2. **Reliability**:\n- Series system: $R_s(t) = \\prod_{i=1}^n R_i(t)$.\n- Parallel system: $R_p(t) = 1 - \\prod_{i=1}^n (1 - R_i(t))$."

    return "1. **Core Statistical Analysis**:\nDefine the population parameters and formulate hypotheses. Compute the required sample statistics.\n2. **Probability Model**:\nSelect the appropriate probability distribution (binomial, normal, etc.) to evaluate expected frequencies.\n3. **Decision Rule**:\nCompare the computed test statistic (t, F, chi-square) with the critical value at the specified level of significance."

# 3. Token-splitting LaTeX Parser
def parse_tex_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace(r'\end{{parts}}', r'\end{parts}')
    content = content.replace(r'\begin{{parts}}', r'\begin{parts}')
    content = re.sub(r'(?m)^%.*$', '', content)
    
    doc_start = content.find(r'\begin{document}')
    idx = 0
    if doc_start != -1:
        idx = doc_start + len(r'\begin{document}')
    
    subcontent = content[idx:]
    pattern = r'(\\begin\{parts\}|\\end\{parts\}|\\item)'
    tokens = re.split(pattern, subcontent)
    
    stack = []
    current_items = []
    all_questions = []
    
    def clean_text(text):
        text = text.replace(r'\"{o}', 'ö').replace(r'\'e', 'é')
        text = re.sub(r'\\pts\{[^\}]*\}', '', text)
        text = re.sub(r'\\hfill', '', text)
        text = re.sub(r'\\s*\\(small|me|big)skip', '', text)
        text = re.sub(r'\\noindent', '', text)
        text = re.sub(r'\\rule\{[^\}]*\}\{[^\}]*\}', '', text)
        text = re.sub(r'\\textbf\{([^\}]*)\}', r'\1', text)
        text = re.sub(r'\\textit\{([^\}]*)\}', r'\1', text)
        text = re.sub(r'\\emph\{([^\}]*)\}', r'\1', text)
        text = text.replace('~', ' ')
        text = re.sub(r'\\\\(?:\[[^\]]*\])?', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    for token in tokens:
        if not token:
            continue
        token_strip = token.strip()
        if token_strip == r'\begin{parts}':
            stack.append(current_items)
            current_items = []
        elif token_strip == r'\end{parts}':
            if stack:
                parent_items = stack.pop()
                if parent_items:
                    last_parent = parent_items[-1]
                    sub_text = " " + " ".join(f"({idx+1}) {clean_text(item)}" for idx, item in enumerate(current_items))
                    parent_items[-1] = last_parent + sub_text
                    current_items = parent_items
                else:
                    for item in current_items:
                        cleaned = clean_text(item)
                        if len(cleaned) > 15:
                            all_questions.append(cleaned)
                    current_items = []
        elif token_strip == r'\item':
            current_items.append("")
        else:
            if current_items:
                current_items[-1] += " " + token
                
    for item in current_items:
        cleaned = clean_text(item)
        if len(cleaned) > 15:
            all_questions.append(cleaned)
            
    return all_questions

# 4. Map Filenames to Active Codes
def get_nep_mapping(code, filename):
    filename_upper = filename.upper()
    code_upper = code.upper()
    
    if code_upper == "BAS-101":
        return ["stamd11"], 1
    elif code_upper in ["STA-101", "STB-101"]:
        return ["stamj11", "stamn11"], 1
    elif code_upper == "BSC-07A":
        return ["stamj11", "stamn11"], 1
    elif code_upper in ["BAS-201", "STA-201", "STB-201"]:
        return ["stamj21", "stamn21"], 2
    elif code_upper == "BSC-08A":
        return ["stamj31", "stamn31"], 3
    elif code_upper == "STB-301":
        return ["stamj31", "stamn31"], 3
    elif code_upper == "STA-301":
        return ["stamj41", "stamn41"], 4
    elif code_upper == "BAS-301":
        return ["stamj43"], 4
    elif code_upper in ["BAS-401", "STA-401", "STB-401"]:
        return ["stamj42"], 4
    elif code_upper == "STA_STB-501":
        return ["stamj43"], 4
    elif code_upper == "STA_STB-502":
        return ["stamj53"], 5
    elif code_upper == "STA_STB-503":
        return ["stamj52"], 5
    elif code_upper == "STA_STB-504":
        return ["stamj51"], 5
    elif code_upper == "STA_STB-601":
        return ["stamj52"], 5
    elif code_upper == "STA_STB-602":
        return ["stamj63"], 6
    elif code_upper == "STA_STB-603":
        return ["stamj61"], 6
    elif code_upper == "STA_STB-604":
        return ["stamj62"], 6
    elif code_upper == "PAPER-VII":
        return ["stamj51"], 5
    elif code_upper == "PAPER-VIII":
        return ["stamj52"], 5
    elif code_upper == "PAPER-IX":
        return ["stamj53"], 5
    elif code_upper == "PAPER-X":
        return ["stamj52"], 5
    elif code_upper == "BSC-09A":
        return ["stamj53"], 5
    elif code_upper == "BSC-13A":
        return ["stamj41"], 4
        
    return ["stamj11", "stamn11"], 1

# 5. Populate Statistics Questions
def main():
    tex_dir = "aaa/STATISTIC/tex_files"
    if not os.path.exists(tex_dir):
        print(f"Directory not found: {tex_dir}")
        return

    # Extract all questions from files and group by active code
    subjects_raw_questions = {}
    for active_key in SUBJECT_SYLLABI.keys():
        subjects_raw_questions[active_key] = []

    files = [f for f in os.listdir(tex_dir) if f.endswith(".tex")]
    files.sort()

    nep_latex_data = []

    for file_name in files:
        filepath = os.path.join(tex_dir, file_name)
        code = file_name.split("_")[0]
        
        # We ignore BPT-201 because it's physics
        if code.upper() == "BPT-201":
            continue

        active_keys, sem = get_nep_mapping(code, file_name)
        
        # Build metadata list for js/nep-data.js
        # Extract subject
        subject_parts = file_name.split("_")[1:-2]
        subject = " ".join(subject_parts)
        # Add spaces between camelCase
        subject = re.sub(r'([a-z])([A-Z])', r'\1 \2', subject)
        
        # Extract year
        year_match = re.search(r'(\d{4}-\d{2}|\d{4}-\d{4})', file_name)
        year = year_match.group(1) if year_match else "2023-24"
        
        nep_code = " / ".join(k.upper() for k in active_keys)
        
        nep_latex_data.append({
            "code": code,
            "subject": subject,
            "semester": sem,
            "year": year,
            "department": "Statistics",
            "filePath": f"aaa/STATISTIC/tex_files/{file_name}",
            "fileName": file_name,
            "nepCode": nep_code,
            "oldCode": code
        })

        # Parse questions
        qs = parse_tex_file(filepath)
        for key in active_keys:
            if key in subjects_raw_questions:
                subjects_raw_questions[key].extend(qs)

    # Load existing exams database
    exams_js_path = "js/exams-data.js"
    with open(exams_js_path, "r", encoding="utf-8") as f:
        js_content = f.read()

    json_start = js_content.find("{")
    json_end = js_content.rfind("}")
    EXAMS = json.loads(js_content[json_start:json_end+1])

    print("Populating Statistics questions...")
    for unique_key, raw_qs in subjects_raw_questions.items():
        standard_qs = SUBJECT_SYLLABI[unique_key]["standard_questions"]
        title_text = SUBJECT_SYLLABI[unique_key]["title"]

        seen = set()
        final_questions = []

        # Deduplicate and filter parsed questions
        for q_text in raw_qs:
            q_norm = q_text.lower().strip()
            if q_norm not in seen and len(q_text) > 20:
                seen.add(q_norm)
                final_questions.append(q_text)

        # Pad with standard syllabus questions if fewer than 50
        std_idx = 0
        while len(final_questions) < 50 and std_idx < len(standard_qs):
            q_text, unit = standard_qs[std_idx]
            q_norm = q_text.lower().strip()
            if q_norm not in seen:
                seen.add(q_norm)
                final_questions.append((q_text, unit))
            std_idx += 1

        # Fallback padding if still fewer than 50
        fallback_idx = 1
        while len(final_questions) < 50:
            q_text = f"Discuss the theoretical frameworks, estimation techniques, and analytical applications of {title_text} (Part {fallback_idx})."
            final_questions.append((q_text, "V"))
            fallback_idx += 1

        # Slice to exactly 50
        final_questions = final_questions[:50]

        # Format questions object
        formatted_questions = []
        for idx, item in enumerate(final_questions):
            q_id = idx + 1
            if isinstance(item, tuple):
                q_text = item[0]
                unit = item[1]
            else:
                q_text = item
                # Uniformly assign units 10 per unit
                unit_num = (idx // 10) + 1
                unit_romans = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}
                unit = unit_romans.get(unit_num, "V")

            ans_key = get_custom_answer_key(unique_key, q_text)

            formatted_questions.append({
                "id": q_id,
                "unit": unit,
                "question": q_text,
                "answerKey": ans_key
            })

            # Inject into EXAMS database
            EXAMS[unique_key] = {
                "id": unique_key,
                "title": title_text,
                "module": unique_key.upper(),
                "duration": 60,
                "type": "theory",
                "comingSoon": False,
                "questions": formatted_questions
            }

    # Write unified exams data back to js/exams-data.js
    output_str = f"// Automatically generated exam data\nexport const EXAMS = {json.dumps(EXAMS, indent=2)};\n"
    with open(exams_js_path, "w", encoding="utf-8") as f:
        f.write(output_str)

    print("js/exams-data.js successfully populated with Statistics papers!")

    # Merge/append metadata to js/nep-data.js
    nep_data_path = "js/nep-data.js"
    with open(nep_data_path, "r", encoding="utf-8") as f:
        nep_js_content = f.read()

    # Find the starting and ending square brackets
    arr_start = nep_js_content.find("[")
    arr_end = nep_js_content.rfind("]")
    current_nep_data = json.loads(nep_js_content[arr_start:arr_end+1])

    # Remove any existing Statistics entries to prevent duplicates
    current_nep_data = [item for item in current_nep_data if item.get("department") != "Statistics"]
    
    # Append new entries
    current_nep_data.extend(nep_latex_data)

    # Sort array by department, then semester, then subject
    current_nep_data.sort(key=lambda x: (x.get("department", ""), x.get("semester", 1), x.get("subject", "")))

    updated_nep_js = f"// Automatically generated NEP Curriculum LaTeX PYQ data\nexport const NEP_LATEX_PYQ_DATA = {json.dumps(current_nep_data, indent=2)};\n"
    with open(nep_data_path, "w", encoding="utf-8") as f:
        f.write(updated_nep_js)

    print("js/nep-data.js successfully updated with Statistics mappings!")

if __name__ == "__main__":
    main()
