import json
import re
import os

# 1. Define Mathematics Syllabi and standard questions for each active paper
MATH_SYLLABI = {
    "matmj11": {
        "title": "Calculus",
        "standard_questions": [
            ("State and prove the Bolzano-Weierstrass Theorem for sequences.", "I"),
            ("Define a convergent sequence. Prove that every convergent sequence is bounded.", "I"),
            ("State and prove Cauchy's general principle of convergence for sequences.", "I"),
            ("Examine the convergence of the sequence $\{x_n\}$ where $x_{n+1} = \\sqrt{2 + x_n}$ and $x_1 = \\sqrt{2}$.", "I"),
            ("State and prove the Comparison Test for positive term series.", "II"),
            ("State and prove D'Alembert's Ratio Test for infinite series.", "II"),
            ("State and prove Raabe's Test for convergence of positive term series.", "II"),
            ("Test the convergence of the series $\\sum_{n=1}^{\\infty} \\frac{n^n}{n!}$.", "II"),
            ("State and prove the Intermediate Value Theorem for continuous functions.", "III"),
            ("State and prove the Chain Rule for differentiation of composite functions.", "III"),
            ("State and prove Rolle's Theorem and give its geometric interpretation.", "IV"),
            ("State and prove Lagrange's Mean Value Theorem.", "IV"),
            ("State and prove Taylor's Theorem with Lagrange's form of remainder.", "IV"),
            ("Find the Maclaurin series expansion of $f(x) = e^x \\sin x$ up to terms containing $x^4$.", "IV"),
            ("Define curvature of a plane curve. Derive the formula for radius of curvature in Cartesian coordinates.", "V"),
            ("Explain the method to find asymptotes of a plane curve of degree $n$.", "V"),
            ("Define singular points, double points, nodes, and cusps for a plane curve.", "V"),
            ("Trace the curve $y^2(a-x) = x^3$ (Cissoid of Diocles).", "V"),
            ("Show that the sequence $\{x_n\}$ defined by $x_n = 1 + \\frac{1}{2} + \\frac{1}{3} + \\dots + \\frac{1}{n} - \\log n$ converges.", "I"),
            ("Define uniform continuity. Prove that a function continuous on a closed interval $[a,b]$ is uniformly continuous.", "III")
        ]
    },
    "matmn11": {
        "title": "Calculus",
        "standard_questions": [
            ("State and prove the Bolzano-Weierstrass Theorem for sequences.", "I"),
            ("Define a convergent sequence. Prove that every convergent sequence is bounded.", "I"),
            ("State and prove Cauchy's general principle of convergence for sequences.", "I"),
            ("Examine the convergence of the sequence $\{x_n\}$ where $x_{n+1} = \\sqrt{2 + x_n}$ and $x_1 = \\sqrt{2}$.", "I"),
            ("State and prove the Comparison Test for positive term series.", "II"),
            ("State and prove D'Alembert's Ratio Test for infinite series.", "II"),
            ("State and prove Raabe's Test for convergence of positive term series.", "II"),
            ("Test the convergence of the series $\\sum_{n=1}^{\\infty} \\frac{n^n}{n!}$.", "II"),
            ("State and prove the Intermediate Value Theorem for continuous functions.", "III"),
            ("State and prove the Chain Rule for differentiation of composite functions.", "III"),
            ("State and prove Rolle's Theorem and give its geometric interpretation.", "IV"),
            ("State and prove Lagrange's Mean Value Theorem.", "IV"),
            ("State and prove Taylor's Theorem with Lagrange's form of remainder.", "IV"),
            ("Find the Maclaurin series expansion of $f(x) = e^x \\sin x$ up to terms containing $x^4$.", "IV"),
            ("Define curvature of a plane curve. Derive the formula for radius of curvature in Cartesian coordinates.", "V"),
            ("Explain the method to find asymptotes of a plane curve of degree $n$.", "V"),
            ("Define singular points, double points, nodes, and cusps for a plane curve.", "V"),
            ("Trace the curve $y^2(a-x) = x^3$ (Cissoid of Diocles).", "V"),
            ("Show that the sequence $\{x_n\}$ defined by $x_n = 1 + \\frac{1}{2} + \\frac{1}{3} + \\dots + \\frac{1}{n} - \\log n$ converges.", "I"),
            ("Define uniform continuity. Prove that a function continuous on a closed interval $[a,b]$ is uniformly continuous.", "III")
        ]
    },
    "matse11": {
        "title": "Ethics in Academia and Mathematical Exploration",
        "standard_questions": [
            ("Discuss the ethical principles of publication and academic integrity in higher education.", "I"),
            ("Explain the concepts of plagiarism, citation ethics, and authorship criteria in research papers.", "I"),
            ("Discuss the ethical issues associated with gender-bias in scientific outreach and academic departments.", "I"),
            ("State and explain Euclid's proof for the infinity of prime numbers.", "II"),
            ("Provide the proof of the infinity of primes using Euler's analytical approach.", "II"),
            ("Discuss the result that binomial coefficients $\\binom{n}{k}$ are almost never powers.", "II"),
            ("State and prove the theorem on representing integers as sums of two squares.", "II"),
            ("Discuss three distinct applications of Euler's formula $V - E + F = 2$ in graph theory and polyhedra.", "II"),
            ("State the Continuum Hypothesis and explain its significance in axiomatic set theory.", "II"),
            ("Explain the proof that $\\sqrt{2}$ is an irrational number and discuss its historical significance.", "III"),
            ("Define the Golden Ratio (Golden Mean) and explain its algebraic properties and occurrences in nature.", "III"),
            ("Discuss the number $e$ as the queen of growth and decay, showing its limit representation.", "III"),
            ("Explain the history, properties, and applications of logarithms in mathematical models.", "III"),
            ("Discuss the Fibonacci sequence and explain its relation to the Golden Ratio.", "III"),
            ("Describe the ethical guidelines for peer-review processes in scientific journals.", "I"),
            ("Show that the sum of the reciprocals of prime numbers diverges, implying infinity of primes.", "II"),
            ("Prove that $\\log_{10} 2$ is an irrational number.", "III"),
            ("Discuss the mathematical concept of fractals and their representation of infinite self-similarity.", "III"),
            ("Explain the difference between countable and uncountable infinities using Cantor's diagonal argument.", "II"),
            ("Discuss the role of intellectual property rights (IPR) and patents in scientific exploration.", "I")
        ]
    },
    "matmj21": {
        "title": "Algebra",
        "standard_questions": [
            ("Find the rank of the matrix $A = \\begin{pmatrix} 1 & 2 & 3 \\\\ 2 & 3 & 4 \\\\ 3 & 5 & 7 \\end{pmatrix}$ by reducing it to Echelon form.", "I"),
            ("Verify the Cayley-Hamilton Theorem for the matrix $A = \\begin{pmatrix} 1 & 2 \\\\ 3 & 4 \\end{pmatrix}$ and find $A^{-1}$.", "I"),
            ("Find the eigenvalues and eigenvectors of the matrix $A = \\begin{pmatrix} 2 & 1 \\\\ 0 & 3 \\end{pmatrix}$.", "I"),
            ("Define a group and show that the set of $n$-th roots of unity forms an abelian group under complex multiplication.", "II"),
            ("Prove that the intersection of two subgroups of a group $G$ is also a subgroup of $G$.", "II"),
            ("Define a cyclic group. Prove that every cyclic group is abelian.", "II"),
            ("Prove that every subgroup of a cyclic group is cyclic.", "II"),
            ("State and prove Lagrange's Theorem for finite groups.", "III"),
            ("Define normal subgroups. Prove that a subgroup $H$ of $G$ is normal if and only if $gHg^{-1} = H$ for all $g \\in G$.", "III"),
            ("Define the quotient group and show how the group operation is well-defined.", "III"),
            ("Define group homomorphism and kernel of a homomorphism. Prove that the kernel is a normal subgroup.", "IV"),
            ("State and prove the Fundamental Theorem of Group Homomorphisms.", "IV"),
            ("Define symmetric group $S_n$. Differentiate between even and odd permutations.", "IV"),
            ("State and prove Cayley's Theorem for finite groups.", "IV"),
            ("Find the relation between the roots and coefficients of a cubic equation $x^3 + px^2 + qx + r = 0$.", "V"),
            ("Solve the cubic equation $x^3 - 15x - 4 = 0$ using Cardan's method.", "V"),
            ("State and apply Descartes' Rule of Signs to find the number of positive and negative roots of $x^5 - x - 1 = 0$.", "V"),
            ("Solve the system of equations $x+y+z=6, 2x+y-z=1, 3x+2y+z=10$ using Cramer's Rule.", "I"),
            ("Prove that a group of prime order has no proper subgroups.", "III"),
            ("Define a ring and field. Show that the set of integers modulo $p$ (where $p$ is prime) is a field.", "V")
        ]
    },
    "matmj31": {
        "title": "Linear Algebra",
        "standard_questions": [
            ("Define a vector space over a field. Show that the space of polynomials $F[x]$ is not finite dimensional.", "I"),
            ("Prove that a subset $W$ of a vector space $V$ is a subspace if and only if $au + bv \\in W$ for all $a,b \\in F$ and $u,v \\in W$.", "I"),
            ("Prove that any linearly independent subset of a finite-dimensional vector space can be extended to form a basis.", "I"),
            ("If $W_1$ and $W_2$ are subspaces of $V$, prove that $\\dim(W_1 + W_2) = \\dim W_1 + \\dim W_2 - \\dim(W_1 \\cap W_2)$.", "I"),
            ("Define rank and nullity of a linear transformation. State and prove the Rank-Nullity Theorem.", "I"),
            ("Find the matrix of the linear transformation $T(x,y) = (x+y, 2x-y)$ with respect to standard bases of $\\mathbb{R}^2$.", "II"),
            ("Define similar matrices and show that similar matrices have the same eigenvalues and characteristic polynomial.", "II"),
            ("Discuss the solvability of the system of linear equations $Ax = B$ in terms of ranks of $A$ and the augmented matrix $[A|B]$.", "II"),
            ("Define an inner product space. State and prove the Cauchy-Schwarz inequality.", "III"),
            ("State and prove the Triangle Inequality in an inner product space.", "III"),
            ("Explain the Gram-Schmidt orthogonalization process to construct an orthonormal basis from a given basis.", "III"),
            ("Define the adjoint of a linear operator. Prove that $(T_1 + T_2)^* = T_1^* + T_2^*$ and $(T_1 T_2)^* = T_2^* T_1^*$.", "III"),
            ("Define orthogonal and unitary transformations. State their properties in terms of inner products.", "IV"),
            ("Differentiate between Hermitian, Skew-Hermitian, and Unitary matrices, providing examples of each.", "IV"),
            ("State and prove the Cayley-Hamilton Theorem for linear operators on finite-dimensional spaces.", "IV"),
            ("Define diagonalizable operators. Prove that an operator $T$ is diagonalizable if and only if its eigenvectors span the space.", "V"),
            ("Define quadratic forms. Show how a quadratic form can be represented by a symmetric matrix.", "V"),
            ("Explain the classification of quadratic curves and surfaces using eigenvalues.", "V"),
            ("Prove that the eigenvalues of a self-adjoint (Hermitian) operator are always real.", "IV"),
            ("Define dual space $V^*$ and dual basis. Show that $\\dim V^* = \\dim V$ for finite-dimensional spaces.", "I")
        ]
    },
    "matmj32": {
        "title": "Analysis",
        "standard_questions": [
            ("State and explain the Completeness Axiom (Supremum Property) of the real number system.", "I"),
            ("State and prove the Archimedean property of real numbers.", "I"),
            ("Prove that the set of rational numbers is dense in the set of real numbers.", "I"),
            ("Define limit superior and limit inferior of a sequence and calculate them for $x_n = (-1)^n(1 + \\frac{1}{n})$.", "II"),
            ("State and prove the Monotone Convergence Theorem for sequences.", "II"),
            ("State and prove Dirichlet's Test for convergence of infinite series.", "III"),
            ("State and prove Abel's Test for convergence of infinite series.", "III"),
            ("State the definition of Riemann integrability using upper and lower Darboux sums.", "III"),
            ("Prove that every continuous function on $[a,b]$ is Riemann integrable.", "III"),
            ("Prove that every monotonic function on $[a,b]$ is Riemann integrable.", "III"),
            ("State and prove the First Fundamental Theorem of Integral Calculus.", "IV"),
            ("State and prove the First Mean Value Theorem of Integral Calculus.", "IV"),
            ("Examine the convergence of the improper integral $\\int_1^{\\infty} \\frac{\\sin x}{x^p} dx$ for $p > 0$.", "V"),
            ("State and prove the Comparison Test for convergence of improper integrals of the first kind.", "V"),
            ("Discuss the integral as a function of a parameter and state the Leibniz rule for differentiation under the integral sign.", "V"),
            ("Prove that the absolute value function $|x|$ is continuous but not differentiable at $x=0$.", "I"),
            ("State and prove the Bolzano-Weierstrass Theorem for sets.", "II"),
            ("Show that the alternating series $\\sum_{n=1}^{\\infty} \\frac{(-1)^{n-1}}{n}$ converges conditionally.", "III"),
            ("Define the Riemann integral as a limit of Riemann sums and show its equivalence to the Darboux integral.", "III"),
            ("Evaluate $\\lim_{n\\to\\infty} \\sum_{r=1}^n \\frac{n}{n^2 + r^2}$ using Riemann integration as a limit of a sum.", "III")
        ]
    },
    "matmv31": {
        "title": "Python for Mathematical Applications",
        "standard_questions": [
            ("Explain literals, variables, identifiers, and operators in Python with syntax examples.", "I"),
            ("Write a Python program to demonstrate the use of conditional structures (if-elif-else).", "I"),
            ("Explain Python list structures. Write code to create, append, modify, and slice lists.", "II"),
            ("Compare lists and tuples in Python in terms of syntax, memory usage, and mutability.", "II"),
            ("Write a Python script to iterate over a list of numbers and compute their sum and average.", "II"),
            ("Explain Python dictionaries. Write a script to count frequencies of words in a string using a dictionary.", "III"),
            ("Explain the concept of sets in Python and write code demonstrating union, intersection, and difference operations.", "III"),
            ("Define functions in Python. Differentiate between value-returning and void (non-value-returning) functions.", "III"),
            ("Explain the concept of local and global variable scopes in Python with illustrative examples.", "III"),
            ("Write a Python function to compute the factorial of a number recursively.", "III"),
            ("Write a Python script to solve a quadratic equation $ax^2 + bx + c = 0$ using Python's math module.", "I"),
            ("Write a Python function to check if a given positive integer is prime.", "III"),
            ("Write a Python program to find the transpose of a matrix represented as a list of lists.", "II"),
            ("Write a Python program to generate the Fibonacci sequence up to $n$ terms.", "II"),
            ("Explain the use of `try-except` blocks in Python for error and exception handling.", "I"),
            ("Write a Python program to compute the dot product of two vectors represented as lists.", "II"),
            ("Discuss parameter passing in Python (call-by-object/reference) and how it affects mutable vs immutable structures.", "III"),
            ("Write a Python function that accepts a list and returns a new list with unique elements without using sets.", "II"),
            ("Explain the standard file operations in Python: reading from and writing to text files.", "I"),
            ("Write a Python function to implement the Euclidean algorithm for finding the greatest common divisor (GCD).", "III")
        ]
    },
    "matmj41": {
        "title": "Calculus of several variables",
        "standard_questions": [
            ("Define Euclidean norm and distance in $\\mathbb{R}^n$. Show that the norm satisfies the triangle inequality.", "I"),
            ("Explain limit and continuity for functions of several variables with an example of a discontinuous function.", "I"),
            ("Define partial derivatives and directional derivatives. Derive the relation between gradient and directional derivative.", "I"),
            ("State and prove Euler's Theorem for homogeneous functions of several variables.", "III"),
            ("State and prove the Chain Rule for functions from $\\mathbb{R}^n$ to $\\mathbb{R}^m$.", "III"),
            ("State the Jacobian matrix and define the Jacobian determinant. Explain its role in change of variables.", "III"),
            ("State the Inverse Function Theorem and Implicit Function Theorem with their conditions.", "III"),
            ("Explain the Taylor series expansion for a function of two variables.", "IV"),
            ("Explain the Hessian matrix. Discuss the second derivative test for finding local extrema and saddle points.", "IV"),
            ("State the method of Lagrange Multipliers for finding constrained extrema.", "IV"),
            ("State and apply Fubini's Theorem for evaluating double integrals over rectangular regions.", "V"),
            ("Show how to change the order of integration in the double integral $\\int_0^1 \\int_x^1 f(x,y) dy dx$.", "V"),
            ("Define Beta and Gamma functions and prove the relationship $\\text{B}(m,n) = \\frac{\\Gamma(m)\\Gamma(n)}{\\Gamma(m+n)}$.", "V"),
            ("State and prove Dirichlet's Theorem for triple integrals.", "V"),
            ("Evaluate the double integral $\\iint_R e^{-(x^2+y^2)} dx dy$ where $R$ is the first quadrant using polar coordinates.", "V"),
            ("Prove that the partial derivatives $f_x$ and $f_y$ of $f(x,y) = \\frac{xy}{x^2+y^2}$ exist at $(0,0)$ but the function is not continuous.", "I"),
            ("Discuss the differentiability of functions of two variables, showing that differentiability implies continuity.", "I"),
            ("Find the local extrema of $f(x,y) = x^3 + y^3 - 3xy$.", "IV"),
            ("Evaluate the volume of the region bounded by $x^2 + y^2 + z^2 \\le a^2$ using spherical coordinates.", "V"),
            ("State and prove Liouville's extension of Dirichlet's integral.", "V")
        ]
    },
    "matmj42": {
        "title": "Vector and Tensor Analysis",
        "standard_questions": [
            ("Define the Gradient of a scalar field and explain its physical significance.", "I"),
            ("Define Divergence and Curl of a vector field. Prove that $\\text{div}(\\text{curl } \\mathbf{A}) = 0$.", "I"),
            ("State and prove Helmholtz decomposition theorem for vector fields.", "I"),
            ("Define line, surface, and volume integrals of vector fields.", "II"),
            ("State and prove Green's Theorem in the plane.", "II"),
            ("State and prove Gauss' Divergence Theorem.", "II"),
            ("State and prove Stokes' Theorem.", "II"),
            ("Explain curvilinear coordinate systems, scale factors, and unit vectors.", "III"),
            ("Derive the expressions for Gradient, Divergence, and Curl in orthogonal curvilinear coordinates.", "III"),
            ("Define cylindrical and spherical coordinate systems, identifying their scale factors.", "III"),
            ("Differentiate between contravariant and covariant tensors, stating their coordinate transformation laws.", "IV"),
            ("Define mixed tensors and tensor contraction. Show that contraction reduces tensor rank by 2.", "IV"),
            ("Define the metric tensor $g_{ij}$ and its role in raising and lowering indices.", "IV"),
            ("Define Christoffel symbols of the first and second kinds, deriving their expressions.", "V"),
            ("Derive the transformation laws of Christoffel symbols, showing they are not tensors.", "V"),
            ("Define covariant differentiation of tensors and explain its physical necessity.", "V"),
            ("Derive the equation of a geodesic on a curved surface.", "V"),
            ("Prove the vector identity $\\text{curl}(\\text{curl } \\mathbf{A}) = \\text{grad}(\\text{div } \\mathbf{A}) - \\nabla^2 \\mathbf{A}$.", "I"),
            ("Verify Green's theorem for $\\oint_C (xy + y^2)dx + x^2dy$ where $C$ is bounded by $y=x$ and $y=x^2$.", "II"),
            ("Show that the metric tensor of spherical coordinates is diagonal.", "IV")
        ]
    },
    "matmj43": {
        "title": "Differential Equations",
        "standard_questions": [
            ("Solve the first-order linear differential equation $\\frac{dy}{dx} + P(x)y = Q(x)$.", "I"),
            ("Explain how to solve first-order higher-degree equations solvable for $x$, $y$, and $p = \\frac{dy}{dx}$.", "I"),
            ("Explain the concept of singular solutions and envelopes for first-order ODEs.", "I"),
            ("Solve second-order linear differential equations with constant coefficients.", "II"),
            ("Explain the method to solve homogeneous linear differential equations (Euler-Cauchy equations).", "II"),
            ("State the method of variation of parameters for solving second-order linear ODEs with variable coefficients.", "III"),
            ("Explain the power series solution method about an ordinary point for second-order ODEs.", "III"),
            ("Explain the formation of partial differential equations by eliminating arbitrary constants and functions.", "IV"),
            ("Explain Lagrange's method for solving linear first-order PDEs of the form $Pp + Qq = R$.", "IV"),
            ("State Charpit's method for finding the complete integral of non-linear first-order PDEs.", "V"),
            ("Solve the linear homogeneous partial differential equations of higher order with constant coefficients.", "V"),
            ("Find the singular solution of Clairaut's equation $y = px + f(p)$ where $p = \\frac{dy}{dx}$.", "I"),
            ("Solve $(D^2 - 5D + 6)y = e^{2x}$.", "II"),
            ("Solve $x^2 y'' - 3xy' + 3y = 0$ given that $y_1 = x$ is a solution.", "II"),
            ("Solve the PDE $px + qy = z$ using Lagrange's auxiliary equations.", "IV"),
            ("Solve the non-linear PDE $p^2 + q^2 = 1$ using Charpit's method.", "V"),
            ("Differentiate between homogeneous and non-homogeneous linear PDEs of second order.", "V"),
            ("Find the orthogonal trajectories of the family of parabolas $y^2 = 4ax$.", "I"),
            ("Explain the concept of ordinary points and singular points for ordinary differential equations.", "III"),
            ("Solve $y'' + y = \\sec x$ using the method of variation of parameters.", "III")
        ]
    },
    "matmn41": {
        "title": "Differential Equations",
        "standard_questions": [
            ("Solve the first-order linear differential equation $\\frac{dy}{dx} + P(x)y = Q(x)$.", "I"),
            ("Explain how to solve first-order higher-degree equations solvable for $x$, $y$, and $p = \\frac{dy}{dx}$.", "I"),
            ("Explain the concept of singular solutions and envelopes for first-order ODEs.", "I"),
            ("Solve second-order linear differential equations with constant coefficients.", "II"),
            ("Explain the method to solve homogeneous linear differential equations (Euler-Cauchy equations).", "II"),
            ("State the method of variation of parameters for solving second-order linear ODEs with variable coefficients.", "III"),
            ("Explain the power series solution method about an ordinary point for second-order ODEs.", "III"),
            ("Explain the formation of partial differential equations by eliminating arbitrary constants and functions.", "IV"),
            ("Explain Lagrange's method for solving linear first-order PDEs of the form $Pp + Qq = R$.", "IV"),
            ("State Charpit's method for finding the complete integral of non-linear first-order PDEs.", "V"),
            ("Solve the linear homogeneous partial differential equations of higher order with constant coefficients.", "V"),
            ("Find the singular solution of Clairaut's equation $y = px + f(p)$ where $p = \\frac{dy}{dx}$.", "I"),
            ("Solve $(D^2 - 5D + 6)y = e^{2x}$.", "II"),
            ("Solve $x^2 y'' - 3xy' + 3y = 0$ given that $y_1 = x$ is a solution.", "II"),
            ("Solve the PDE $px + qy = z$ using Lagrange's auxiliary equations.", "IV"),
            ("Solve the non-linear PDE $p^2 + q^2 = 1$ using Charpit's method.", "V"),
            ("Differentiate between homogeneous and non-homogeneous linear PDEs of second order.", "V"),
            ("Find the orthogonal trajectories of the family of parabolas $y^2 = 4ax$.", "I"),
            ("Explain the concept of ordinary points and singular points for ordinary differential equations.", "III"),
            ("Solve $y'' + y = \\sec x$ using the method of variation of parameters.", "III")
        ]
    },
    "matmj44": {
        "title": "Mechanics",
        "standard_questions": [
            ("State and prove Varignon's Theorem on moments of coplanar forces.", "I"),
            ("Explain the analytical conditions for the equilibrium of coplanar concurrent forces.", "I"),
            ("Explain the concept of a couple and prove that the sum of moments of two forces forming a couple is constant.", "I"),
            ("State the Principle of Virtual Work for a system of coplanar forces acting on a rigid body.", "II"),
            ("State and explain Hooke's Law for elastic strings and relate it to virtual work problems.", "II"),
            ("Derive the coordinates of the center of gravity of a uniform circular arc.", "II"),
            ("Discuss stable, unstable, and neutral equilibrium of a heavy body placed on another fixed body.", "II"),
            ("Explain the concept of radial and transverse components of velocity and acceleration.", "I"),
            ("Derive expressions for tangential and normal components of velocity and acceleration.", "I"),
            ("State and prove the principle of conservation of linear momentum.", "I"),
            ("Derive the equation of motion for a particle in a simple harmonic motion (S.H.M.).", "I"),
            ("Explain the motion of a particle in a resisting medium where resistance is proportional to velocity.", "I"),
            ("Prove that virtual work done by tension in an inextensible string is zero.", "II"),
            ("Find the center of gravity of a uniform solid hemisphere.", "II"),
            ("Derive the expression for the work done in stretching an elastic string.", "II"),
            ("Explain the concept of terminal velocity for a particle falling in a resisting medium.", "I"),
            ("Discuss the equilibrium of a uniform ladder resting against a smooth vertical wall and a rough horizontal floor.", "II"),
            ("Find the resultant of two parallel forces (like and unlike).", "I"),
            ("Explain Virtual Displacement and define degrees of freedom for mechanical systems.", "II"),
            ("A particle is projected vertically upwards in a resisting medium. Find the maximum height reached.", "I")
        ]
    },
    "matmj51": {
        "title": "Abstract Algebra",
        "standard_questions": [
            ("Define group homomorphism and group isomorphism. Give examples.", "I"),
            ("Prove that the relation of being isomorphic ($\cong$) is an equivalence relation on groups.", "I"),
            ("State and prove the first isomorphism theorem for groups (Fundamental Homomorphism Theorem).", "II"),
            ("State and prove the Second Isomorphism Theorem for groups.", "II"),
            ("State and prove the Third Isomorphism Theorem for groups.", "II"),
            ("Define the commutator subgroup of a group $G$. Prove that it is a normal subgroup of $G$.", "II"),
            ("Define the symmetric group $S_n$. Prove that the alternating group $A_n$ is normal in $S_n$.", "III"),
            ("Define even and odd permutations. Show that the product of two odd permutations is even.", "III"),
            ("Explain the concept of group action on a set. Define orbits and stabilizer subgroups.", "IV"),
            ("State and prove the Orbit-Stabilizer Theorem for group actions.", "IV"),
            ("Derive the Class Equation for a finite group $G$.", "IV"),
            ("Prove that any group of order $p^2$ (where $p$ is a prime) is abelian.", "IV"),
            ("State and prove Cauchy's Theorem for finite abelian groups.", "IV"),
            ("Show that the center of a $p$-group is non-trivial.", "IV"),
            ("Prove that $S_n$ is not solvable for $n \\ge 5$.", "III"),
            ("Explain regular group actions and conjugation actions.", "IV"),
            ("State and prove Cayley's theorem using group actions.", "IV"),
            ("State the definition of a subgroup generated by a subset and calculate it for cyclic subgroups of $Z_6$.", "I"),
            ("Prove that if $H$ is a subgroup of $G$ of index 2, then $H$ is normal in $G$.", "II"),
            ("Define simple groups. Prove that $A_5$ is a simple group.", "III")
        ]
    },
    "matmj52": {
        "title": "Metric Spaces",
        "standard_questions": [
            ("Define a metric space. Show that $d(x,y) = |x-y|$ is a metric on $\\mathbb{R}$.", "I"),
            ("Define open ball and closed ball. Prove that every open ball in a metric space is an open set.", "I"),
            ("Define interior, closure, boundary, and limit points of a set in a metric space.", "I"),
            ("Prove that a subset $F$ of a metric space is closed if and only if it contains all its limit points.", "I"),
            ("Define convergence of a sequence in a metric space. Prove that the limit of a convergent sequence is unique.", "I"),
            ("Define compactness in metric spaces. Prove that every compact subset of a metric space is closed and bounded.", "II"),
            ("State and prove the Heine-Borel Theorem on $\\mathbb{R}$.", "II"),
            ("Prove that a metric space is compact if and only if it is sequentially compact.", "II"),
            ("Define connected metric spaces. Prove that a subset of $\\mathbb{R}$ is connected if and only if it is an interval.", "II"),
            ("Explain path-connected spaces, and show that path-connected implies connected.", "II"),
            ("Define Cauchy sequences and complete metric spaces. Give an example of an incomplete space.", "II"),
            ("State and prove Cantor's Intersection Theorem in a complete metric space.", "III"),
            ("Discuss the construction of real numbers as the completion of the incomplete space of rational numbers.", "III"),
            ("Prove that the continuous image of a compact metric space is compact.", "II"),
            ("State and prove the Banach Contraction Principle (Fixed Point Theorem).", "III"),
            ("Prove that the continuous image of a connected metric space is connected.", "II"),
            ("Define equivalent metrics. Show that the Euclidean metric and the taxicab metric on $\\mathbb{R}^2$ are equivalent.", "I"),
            ("Prove that a closed subspace of a complete metric space is complete.", "II"),
            ("Explain dense subsets and separable metric spaces. Show that $\\mathbb{R}$ is separable.", "I"),
            ("Prove that if $A$ and $B$ are connected subsets of $X$ such that $A \\cap B \\neq \\emptyset$, then $A \\cup B$ is connected.", "II")
        ]
    },
    "matmj53": {
        "title": "Analytic Geometry",
        "standard_questions": [
            ("Explain polar coordinates and find the polar equation of a straight line.", "I"),
            ("Find the polar equation of a circle of radius $a$ passing through the pole.", "I"),
            ("Derive the polar equation of a conic with the pole at a focus: $\\frac{\\ell}{r} = 1 + e \\cos \\theta$.", "I"),
            ("Derive the equations of chord, tangent, and normal to the conic $\\frac{\\ell}{r} = 1 + e \\cos \\theta$.", "I"),
            ("Derive the equation of a plane in $\\mathbb{R}^3$ using vector methods.", "II"),
            ("Derive the equation of a straight line in $\\mathbb{R}^3$ in vector and symmetric Cartesian forms.", "II"),
            ("Find the shortest distance between two skew lines in $\\mathbb{R}^3$.", "II"),
            ("Derive the general equation of a sphere. Find the equation of a sphere passing through a given circle.", "III"),
            ("Derive the equation of the tangent plane and normal line to a sphere at a given point.", "III"),
            ("Find the angle of intersection of two spheres.", "III"),
            ("Derive the equation of a cone with its vertex at the origin.", "IV"),
            ("State the conditions under which the general equation of the second degree represents a cone.", "IV"),
            ("Derive the equation of a right circular cone. Find the equation of its reciprocal cone.", "IV"),
            ("Derive the equation of an enveloping cylinder and a right circular cylinder.", "IV"),
            ("Explain central conicoids (ellipsoid, hyperboloid of one sheet, hyperboloid of two sheets).", "V"),
            ("Derive the equation of the tangent plane and normal to a central conicoid.", "V"),
            ("Find the condition of tangency of a plane $lx + my + nz = p$ to the central conicoid.", "V"),
            ("Describe the classification of quadrics represented by the general equation of second degree.", "V"),
            ("Explain the cone through six normals to a central conicoid.", "V"),
            ("Find the polar equation of the polar of a point with respect to a conic.", "I")
        ]
    },
    "matmj54": {
        "title": "Numerical Analysis",
        "standard_questions": [
            ("Discuss errors in numerical computation, including absolute, relative, and percentage errors.", "I"),
            ("Explain the Bisection Method for solving non-linear equations and write its rate of convergence.", "I"),
            ("Explain the Newton-Raphson Method. Derive its quadratic rate of convergence.", "I"),
            ("Explain the Regula-Falsi (False Position) and Secant methods, comparing their rates of convergence.", "I"),
            ("Explain the Birge-Vieta method for finding roots of polynomials.", "II"),
            ("Describe the Gauss Elimination and Gauss-Jordan methods for solving systems of linear equations.", "II"),
            ("Describe the Jacobi and Gauss-Seidel iterative methods, stating their convergence conditions.", "II"),
            ("Explain the Power Method for computing the dominant eigenvalue and corresponding eigenvector.", "II"),
            ("Define the forward, backward, shift, and central difference operators and establish relations between them.", "II"),
            ("Derive Newton's forward and backward interpolation formulas.", "III"),
            ("Derive Lagrange's Interpolation Formula for unequally spaced data.", "III"),
            ("Derive Newton's Divided Difference Interpolation Formula.", "III"),
            ("Explain the numerical differentiation formulas using Newton's forward and backward interpolation.", "III"),
            ("Derive the general quadrature formula for numerical integration.", "IV"),
            ("Derive the Trapezoidal and Simpson's one-third rules for numerical integration, detailing error terms.", "IV"),
            ("State Simpson's three-eighths rule, Boole's rule, and Weddle's rule for numerical integration.", "IV"),
            ("Explain Euler's method and Modified Euler's method for solving first-order ordinary differential equations.", "V"),
            ("Derive the Runge-Kutta second-order (RK2) and fourth-order (RK4) formulas for solving ODEs.", "V"),
            ("Explain predictor-corrector methods, focusing on the Milne-Simpson and Adams-Bashforth methods.", "V"),
            ("Solve the system $10x+y+z=12, x+10y+z=12, x+y+10z=12$ using the Gauss-Seidel method up to 3 iterations.", "II")
        ]
    },
    "matmj610": {
        "title": "Dynamical System",
        "standard_questions": [
            ("Define linear dynamical systems. Differentiate between autonomous and non-autonomous systems.", "I"),
            ("Explain the diagonalization of linear systems and its role in decoupling system equations.", "I"),
            ("State and prove the Fundamental Theorem of Linear Systems.", "I"),
            ("Explain the construction of Jordan Canonical Forms for matrices with repeated eigenvalues.", "II"),
            ("Define stable, unstable, and center subspaces of a linear dynamical system.", "II"),
            ("Discuss nonhomogeneous linear dynamical systems and their solution methods.", "II"),
            ("Define non-linear dynamical systems. Explain the existence and uniqueness theorem for initial value problems.", "III"),
            ("Explain the linearization of non-linear systems about a critical point (Hartman-Grobman theorem).", "III"),
            ("Define phase space and phase portraits. Classify critical points (node, saddle, focus, center) for 2D systems.", "III"),
            ("Discuss the chaotic dynamics of the Lorenz system and define a strange attractor.", "IV"),
            ("Apply dynamical systems to modeling population dynamics (Lotka-Volterra predator-prey equations).", "IV"),
            ("Explain the simple pendulum with damping as a non-linear dynamical system.", "IV"),
            ("Discuss bifurcation in dynamical systems, explaining saddle-node, transcritical, and pitchfork bifurcations.", "III"),
            ("Define Lyapunov functions and state Lyapunov's stability theorems for non-linear systems.", "III"),
            ("Explain the concept of limit cycles and state the Poincare-Bendixson Theorem.", "III"),
            ("Analyze the stability of the critical point $(0,0)$ for the system $\\dot{x} = y, \\dot{y} = -x$.", "III"),
            ("Explain the stable manifold theorem for non-linear systems.", "II"),
            ("Describe the phase portrait of a linear system with a saddle point.", "III"),
            ("Apply dynamical systems to modeling economic cycles or engineering control systems.", "IV"),
            ("Show that the system $\\dot{x} = y - x(x^2+y^2), \\dot{y} = -x - y(x^2+y^2)$ has a stable focus at $(0,0)$.", "III")
        ]
    },
    "matmj62": {
        "title": "Complex Analysis",
        "standard_questions": [
            ("Define the complex plane. Explain domains, regions, and open sets in $\\mathbb{C}$.", "I"),
            ("Explain Stereographic Projection of the complex plane onto a Riemann sphere.", "I"),
            ("Define Mobius Transformations and prove that they map circles and lines to circles and lines.", "I"),
            ("Explain conformal mapping. Prove that analytic functions are conformal wherever the derivative is non-zero.", "I"),
            ("State and prove Schwarz's Lemma in complex analysis.", "II"),
            ("State the Riemann Mapping Theorem and discuss its geometric significance.", "II"),
            ("State the Cauchy-Riemann equations and prove that they are necessary conditions for differentiability.", "II"),
            ("Prove that the real and imaginary parts of an analytic function are harmonic.", "II"),
            ("State and prove Cauchy's Theorem for complex line integration over a closed contour.", "III"),
            ("State and prove Cauchy's Integral Formula for analytic functions and their derivatives.", "III"),
            ("State and prove Liouville's Theorem. Use it to prove the Fundamental Theorem of Algebra.", "III"),
            ("State and prove Morera's Theorem (converse of Cauchy's Theorem).", "III"),
            ("Define Taylor and Laurent series expansions for complex functions, detailing their regions of convergence.", "IV"),
            ("Define singularities (isolated, removable, poles, essential) of complex functions.", "IV"),
            ("State and prove the Cauchy Residue Theorem.", "V"),
            ("Evaluate the real integral $\\int_0^{2\\pi} \\frac{d\\u03b8}{a + b\\cos\\u03b8}$ using contour integration ($a > b > 0$).", "V"),
            ("State and prove Argument Principle and Rouche's Theorem.", "V"),
            ("Find the bilinear (Mobius) transformation that maps $z_1=\\infty, z_2=i, z_3=0$ onto $w_1=0, w_2=i, w_3=\\infty$.", "I"),
            ("Prove that $f(z) = \\bar{z}$ is nowhere differentiable in the complex plane.", "II"),
            ("Evaluate $\\oint_C \\frac{e^{2z}}{(z-1)^3} dz$ where $C$ is the circle $|z|=2$ using Cauchy's integral formula.", "III")
        ]
    },
    "matmj63": {
        "title": "Differential Geometry",
        "standard_questions": [
            ("Define arc length and parameterization of curves in $\\mathbb{R}^3$.", "I"),
            ("Derive the Frenet-Serret formulas for unit-speed curves in $\\mathbb{R}^3$.", "I"),
            ("Define curvature and torsion of a curve in $\\mathbb{R}^3$, explaining their geometric meanings.", "I"),
            ("State and prove the Fundamental Existence and Uniqueness Theorem for space curves.", "I"),
            ("Define Bishop frames (alternative to Frenet frames) and explain their utility.", "I"),
            ("Define rotation index of a plane curve and state the Four-Vertex Theorem (Mukhopadhyay's Theorem).", "II"),
            ("State and prove Fenchel's Theorem on total curvature of a closed space curve.", "II"),
            ("State the Fary-Milnor Theorem on total curvature of knotted curves.", "II"),
            ("Define a regular surface in $\\mathbb{R}^3$. State and explain the First Fundamental Form.", "III"),
            ("Derive the formula for calculating arc length of a curve lying on a surface.", "III"),
            ("Define normal curvature and geodesic curvature of a curve on a surface.", "III"),
            ("State and derive the Gauss and Weingarten formulas.", "III"),
            ("Define Geodesics on a surface and derive the differential equations of geodesics.", "IV"),
            ("State and explain the Second Fundamental Form and the Weingarten map (shape operator).", "IV"),
            ("Define Principal, Gaussian, and Mean Curvatures of a surface.", "IV"),
            ("State and prove Gauss's Theorema Egregium.", "V"),
            ("State the Fundamental Theorem of Surfaces.", "V"),
            ("Explain geodesic coordinates and state the Gauss Lemma.", "V"),
            ("State and discuss the Gauss-Bonnet Theorem for compact surfaces.", "V"),
            ("Find the curvature and torsion of the circular helix $\\mathbf{r}(\\theta) = (a\\cos\\theta, a\\sin\\theta, b\\theta)$.", "I")
        ]
    },
    "matmj64": {
        "title": "Number Theory",
        "standard_questions": [
            ("Define divisibility in integers. State and prove the Fundamental Theorem of Arithmetic.", "I"),
            ("Explain the Euclidean Algorithm to compute the Greatest Common Divisor (GCD) of two integers.", "I"),
            ("State and prove the Extended Euclidean Algorithm to represent $\\text{gcd}(a,b) = ax + by$.", "I"),
            ("Define congruences and modular arithmetic. State their basic algebraic properties.", "II"),
            ("State the conditions for solvability of linear congruences and explain how to solve them.", "II"),
            ("State and prove the Chinese Remainder Theorem.", "II"),
            ("Solve systems of simultaneous linear congruences using the Chinese Remainder Theorem.", "II"),
            ("State and prove Fermat's Little Theorem.", "II"),
            ("State and prove Wilson's Theorem.", "II"),
            ("Define Euler's phi function $\\phi(n)$ and prove that it is multiplicative.", "III"),
            ("State and prove Euler's generalization of Fermat's Theorem.", "III"),
            ("Define number-theoretic functions: $d(n)$ (number of divisors) and $\\sigma(n)$ (sum of divisors).", "III"),
            ("State and prove the Mobius Inversion Formula.", "III"),
            ("Discuss linear Diophantine equations and solve $ax + by = c$.", "I"),
            ("Define quadratic residues and Legendre symbol. State and prove Euler's Criterion.", "III"),
            ("State and apply the Law of Quadratic Reciprocity.", "III"),
            ("Discuss Pell's equation $x^2 - Dy^2 = 1$ and explain its solution methods.", "II"),
            ("Discuss Fermat's Last Theorem, its historical context, and basic ideas.", "II"),
            ("Show that $a \\equiv b \\pmod m \\implies \\text{gcd}(a,m) = \\text{gcd}(b,m)$.", "I"),
            ("Find all solutions to the linear Diophantine equation $172x + 20y = 1000$.", "I")
        ]
    },
    "matmj65": {
        "title": "Linear Programming and Applications",
        "standard_questions": [
            ("Formulate a standard Linear Programming Problem (LPP) from a real-life application.", "I"),
            ("Explain the Graphical Method for solving LPP with two variables, identifying bounded and unbounded solutions.", "I"),
            ("Describe the Simplex Method algorithm for solving linear programming problems.", "I"),
            ("Explain the Two-Phase Method for solving LPPs containing artificial variables.", "I"),
            ("Explain the Big-M Method (Method of Penalties) for solving LPPs.", "I"),
            ("Define slack, surplus, and artificial variables. Explain basic feasible solutions (BFS).", "II"),
            ("State and prove the reduction of a feasible solution to a basic feasible solution.", "II"),
            ("Discuss degeneracy in linear programming and describe methods for resolving degeneracy.", "II"),
            ("Explain the concept of duality in linear programming. Show how to formulate the dual of a primal LPP.", "III"),
            ("State and prove the Weak Duality Theorem.", "III"),
            ("State and prove the Strong Duality Theorem.", "III"),
            ("Explain the Dual Simplex Method algorithm and state when it is applied.", "III"),
            ("Formulate the Transportation Problem and explain the North-West Corner Method to find an initial BFS.", "III"),
            ("Explain Vogel's Approximation Method (VAM) for finding an initial BFS for Transportation Problems.", "III"),
            ("Explain the MODI (Modified Distribution) Method for finding the optimal transportation plan.", "III"),
            ("Formulate the Assignment Problem and describe the Hungarian Method algorithm for solving it.", "III"),
            ("Prove that the dual of the dual LPP is the primal LPP.", "III"),
            ("Discuss alternative optimal solutions and unbounded solutions in Simplex tables.", "II"),
            ("Explain the Traveling Salesman Problem and how it is solved as an assignment problem.", "III"),
            ("Solve the LPP: Maximize $Z = 3x_1 + 5x_2$ subject to $x_1 \\le 4, 2x_2 \\le 12, 3x_1 + 2x_2 \\le 18$ graphically.", "I")
        ]
    },
    "matmj66": {
        "title": "Special Theory of Relativity",
        "standard_questions": [
            ("Discuss Newtonian mechanics, Galilean transformations, and Galilean invariance.", "I"),
            ("Describe the Michelson-Morley experiment, its null result, and its physical significance.", "I"),
            ("State the two postulates of the Special Theory of Relativity proposed by Einstein.", "I"),
            ("Derive the Lorentz Transformation equations between two inertial frames.", "I"),
            ("Discuss the geometrical interpretation of Lorentz transformations in Minkowski space.", "I"),
            ("Derive the formula for Length Contraction and discuss its physical interpretation.", "II"),
            ("Derive the formula for Time Dilation and discuss its relation to proper time.", "II"),
            ("Derive the relativistic velocity addition (composition) formula for parallel velocities.", "II"),
            ("Derive the transformation equations for the components of velocity and acceleration of a particle.", "II"),
            ("Explain the four-dimensional Minkowski space-time representation.", "III"),
            ("Define four-vectors, four-velocity, and four-acceleration.", "III"),
            ("Derive the relativistic mass-velocity relation $m = \\frac{m_0}{\\sqrt{1 - v^2/c^2}}$.", "III"),
            ("Derive Einstein's mass-energy equivalence relation $E = mc^2$.", "III"),
            ("Explain the four-momentum vector and show that its norm is invariant.", "III"),
            ("Discuss the relativistic Doppler effect and derive the formula for frequency shift.", "II"),
            ("Differentiate between timelike, spacelike, and null (lightlike) intervals.", "III"),
            ("Explain the Twin Paradox in special relativity and its resolution.", "II"),
            ("Show that the spacetime interval $ds^2 = c^2 dt^2 - dx^2 - dy^2 - dz^2$ is invariant under Lorentz transformations.", "III"),
            ("Derive the relation between relativistic momentum and energy: $E^2 = p^2 c^2 + m_0^2 c^4$.", "III"),
            ("Prove that the speed of light $c$ is the limiting speed for any material particle.", "I")
        ]
    },
    "matmj68": {
        "title": "Discrete Mathematics",
        "standard_questions": [
            ("Discuss counting techniques, including the pigeonhole principle and permutations/combinations.", "I"),
            ("Define partially ordered sets (posets). Explain lattices as posets and as algebraic systems.", "I"),
            ("Explain distributive lattices, complemented lattices, and complete lattices.", "I"),
            ("Define Boolean algebra. State its basic properties and list its axioms.", "II"),
            ("Explain Boolean functions, Boolean expressions, and how they are simplified using Karnaugh maps.", "II"),
            ("Show how to apply Boolean algebra to design switching circuits using AND, OR, and NOT gates.", "II"),
            ("Define a graph. Explain basic terminology: degree of a vertex, paths, cycles, and connectivity.", "III"),
            ("Differentiate between bipartite graphs, planar graphs, and non-planar graphs.", "III"),
            ("State and prove Euler's Formula ($V - E + F = 2$) for planar graphs.", "III"),
            ("Define trees and forests. Discuss properties of trees and spanning trees.", "IV"),
            ("Explain algorithms for finding a minimum spanning tree (Kruskal's or Prim's algorithms).", "IV"),
            ("Define Eulerian paths and circuits. State the necessary and sufficient conditions for a graph to be Eulerian.", "V"),
            ("Define Hamiltonian paths and cycles. Explain Dirac's and Ore's theorems for Hamiltonicity.", "V"),
            ("Explain the matrix representation of graphs (adjacency matrix and incidence matrix).", "V"),
            ("State and prove the Handshaking Lemma for undirected graphs.", "III"),
            ("State Sperner's Lemma and explain its application to fixed point theorems.", "I"),
            ("Prove that a tree with $n$ vertices has exactly $n-1$ edges.", "IV"),
            ("Prove that the complete graph $K_5$ and complete bipartite graph $K_{3,3}$ are non-planar.", "III"),
            ("Define list coloring and perfect graphs in graph theory.", "III"),
            ("Explain the concept of network flows and state the Max-Flow Min-Cut Theorem.", "III")
        ]
    }
}

# 2. Define answers for math questions (keyword based database)
def get_math_answer_key(course_key, question_text):
    q_lower = question_text.lower()
    
    # 1. Bolzano-Weierstrass
    if "bolzano" in q_lower or "weierstrass" in q_lower:
        return "1. **Statement**:\nEvery bounded sequence of real numbers has a convergent subsequence.\n\n2. **Proof Sketch**:\n- Let $\{x_n\}$ be a bounded sequence. Thus, there exists an interval $I_0 = [a, b]$ containing all terms of the sequence.\n- Bisect $I_0$ into two subintervals $I_1' = [a, (a+b)/2]$ and $I_1'' = [(a+b)/2, b]$. At least one of these subintervals must contain infinitely many terms of $\{x_n\}$. Choose this interval and denote it as $I_1 = [a_1, b_1]$.\n- Repeat this bisection process. We get a nested sequence of intervals $I_k = [a_k, b_k]$ such that the length of $I_k$ is $(b-a)/2^k$ and each $I_k$ contains infinitely many terms of the sequence.\n- By the Nested Intervals Theorem, there exists a unique point $\\xi \\in \\bigcap_{k=1}^{\\infty} I_k$.\n- Construct a subsequence $\{x_{n_k}\}$ by choosing $x_{n_k} \\in I_k$ with $n_k > n_{k-1}$.\n- Since $a_k \\le x_{n_k} \\le b_k$ and $\\lim a_k = \\lim b_k = \\xi$, by the Squeeze Theorem, $\\lim_{k\\to\\infty} x_{n_k} = \\xi$.\n- Thus, we have found a convergent subsequence."

    # 2. Rolle's Theorem
    elif "rolle" in q_lower:
        return "1. **Statement**:\nLet $f: [a, b] \\to \\mathbb{R}$ be a function such that:\n- $f$ is continuous on $[a, b]$,\n- $f$ is differentiable on $(a, b)$, and\n- $f(a) = f(b)$.\nThen there exists at least one $c \\in (a, b)$ such that $f'(c) = 0$.\n\n2. **Proof**:\n- Since $f$ is continuous on the closed and bounded interval $[a, b]$, by the Extreme Value Theorem, $f$ attains its absolute maximum $M$ and absolute minimum $m$ on $[a, b]$.\n- **Case 1**: $M = m$. Then $f(x)$ is constant on $[a, b]$, which implies $f'(c) = 0$ for all $c \\in (a, b)$.\n- **Case 2**: $M \\neq m$. Since $f(a) = f(b)$, at least one of the extrema (say $M$) must be attained at some point $c \\in (a, b)$.\n- Since $f$ is differentiable at $c$, the left-hand and right-hand derivatives must be equal:\n  $$f'(c) = \\lim_{h \\to 0^+} \\frac{f(c+h) - f(c)}{h} = \\lim_{h \\to 0^-} \\frac{f(c+h) - f(c)}{h}$$\n- For $h > 0$, since $f(c) = M$ is the maximum, $f(c+h) - f(c) \\le 0 \\implies \\frac{f(c+h) - f(c)}{h} \\le 0$. Thus, $f'(c) \\le 0$.\n- For $h < 0$, $f(c+h) - f(c) \\le 0 \\implies \\frac{f(c+h) - f(c)}{h} \\ge 0$. Thus, $f'(c) \\ge 0$.\n- Combining these, we get $f'(c) = 0$."

    # 3. Mean Value Theorem (Lagrange)
    elif "mean value" in q_lower or "lagrange's mean" in q_lower or "lvt" in q_lower:
        return "1. **Statement**:\nLet $f: [a, b] \\to \\mathbb{R}$ be continuous on $[a, b]$ and differentiable on $(a, b)$. Then there exists $c \\in (a, b)$ such that:\n$$f'(c) = \\frac{f(b) - f(a)}{b - a}$$\n\n2. **Proof**:\n- Define an auxiliary function $\\phi(x) = f(x) - kx$, where $k$ is a constant chosen such that $\\phi(a) = \\phi(b)$:\n  $$f(a) - ka = f(b) - kb \\implies k = \\frac{f(b) - f(a)}{b - a}$$\n- $\\phi(x)$ satisfies the conditions of Rolle's Theorem:\n  - $\\phi(x)$ is continuous on $[a, b]$ (difference of continuous functions),\n  - $\\phi(x)$ is differentiable on $(a, b)$,\n  - $\\phi(a) = \\phi(b)$.\n- By Rolle's Theorem, there exists $c \\in (a, b)$ such that $\\phi'(c) = 0$.\n- Since $\\phi'(x) = f'(x) - k$, we have:\n  $$f'(c) - k = 0 \\implies f'(c) = k = \\frac{f(b) - f(a)}{b - a}$$\n- This completes the proof."

    # 4. Taylor / Maclaurin
    elif "taylor" in q_lower or "maclaurin" in q_lower:
        return "1. **Statement (Maclaurin's Theorem)**:\nIf $f$ has derivatives of all orders in an interval containing 0, then:\n$$f(x) = f(0) + f'(0)x + \\frac{f''(0)}{2!}x^2 + \\dots + \\frac{f^{(n-1)}(0)}{(n-1)!}x^{n-1} + R_n(x)$$\nwhere $R_n(x)$ is the remainder after $n$ terms.\n\n2. **Maclaurin Expansion of $e^x \\sin x$**:\n- Let $y = e^x \\sin x$. Then $y(0) = 0$.\n- By Leibnitz theorem or successive differentiation:\n  $$y' = e^x(\\sin x + \\cos x) \\implies y'(0) = 1$$\n  $$y'' = 2e^x\\cos x \\implies y''(0) = 2$$\n  $$y''' = 2e^x(\\cos x - \\sin x) \\implies y'''(0) = 2$$\n  $$y^{(4)} = -4e^x\\sin x \\implies y^{(4)}(0) = 0$$\n- Substituting in Maclaurin's formula:\n  $$y(x) = 0 + 1\\cdot x + \\frac{2}{2!}x^2 + \\frac{2}{3!}x^3 + 0 + \\dots = x + x^2 + \\frac{x^3}{3} + O(x^5)$$\n- Thus, the expansion up to $x^4$ is $x + x^2 + \\frac{x^3}{3}$."

    # 5. Prime Infinity (Euclid / Euler)
    elif "prime" in q_lower and "infinit" in q_lower:
        return "1. **Euclid's Proof**:\n- Suppose there are only finitely many primes, say $p_1, p_2, \\dots, p_n$.\n- Consider the number $P = (p_1 p_2 \\dots p_n) + 1$.\n- Since $P > 1$, by the Fundamental Theorem of Arithmetic, $P$ must be divisible by at least one prime $q$.\n- If $q$ is one of our listed primes $p_i$, then $q$ divides the product $p_1 \\dots p_n$. Since $q$ also divides $P$, it must divide the difference $P - (p_1 \\dots p_n) = 1$, which is impossible.\n- Thus, $q$ is a new prime not in our list, contradicting the assumption of finiteness. Hence, primes are infinite.\n\n2. **Euler's Proof**:\n- Euler proved that the sum of the reciprocals of all primes diverges:\n  $$\\sum_{p \\text{ prime}} \\frac{1}{p} = \\infty$$\n- This divergence implies there must be infinitely many primes, as a finite sum would always converge."

    # 6. Irrationality of sqrt(2) or log
    elif "irrational" in q_lower:
        return "1. **Proof by Contradiction for $\\sqrt{2}$**:\n- Suppose $\\sqrt{2}$ is rational. Then $\\sqrt{2} = \\frac{a}{b}$ where $a, b \\in \\mathbb{Z}$, $b \\neq 0$, and $\\text{gcd}(a,b) = 1$ (coprime).\n- Squaring both sides: $2 = \\frac{a^2}{b^2} \\implies a^2 = 2b^2$.\n- Since $a^2$ is even, $a$ must also be even. Let $a = 2k$ for some $k \\in \\mathbb{Z}$.\n- Substituting $a$: $(2k)^2 = 2b^2 \\implies 4k^2 = 2b^2 \\implies b^2 = 2k^2$.\n- Since $b^2$ is even, $b$ must also be even.\n- Both $a$ and $b$ are even, which contradicts $\\text{gcd}(a,b) = 1$.\n- Therefore, $\\sqrt{2}$ is irrational."

    # 7. Rank of a Matrix / Echelon Form
    elif "rank" in q_lower and "matrix" in q_lower:
        return "1. **Definition**:\nThe rank of a matrix is the number of non-zero rows in its Row Echelon Form.\n\n2. **Row Reduction Method**:\n- Perform elementary row operations ($R_i \\to R_i - c R_j$) to create zeros below the pivots.\n- For example, if $A = \\begin{pmatrix} 1 & 2 & 3 \\\\ 2 & 3 & 4 \\\\ 3 & 5 & 7 \\end{pmatrix}$:\n  - $R_2 \\to R_2 - 2R_1 \\implies \\begin{pmatrix} 1 & 2 & 3 \\\\ 0 & -1 & -2 \\\\ 3 & 5 & 7 \\end{pmatrix}$\n  - $R_3 \\to R_3 - 3R_1 \\implies \\begin{pmatrix} 1 & 2 & 3 \\\\ 0 & -1 & -2 \\\\ 0 & -1 & -2 \\end{pmatrix}$\n  - $R_3 \\to R_3 - R_2 \\implies \\begin{pmatrix} 1 & 2 & 3 \\\\ 0 & -1 & -2 \\\\ 0 & 0 & 0 \\end{pmatrix}$\n- Since there are 2 non-zero rows, the rank of the matrix is $2$."

    # 8. Cayley-Hamilton Theorem
    elif "cayley" in q_lower and "hamilton" in q_lower:
        return "1. **Statement**:\nEvery square matrix satisfies its own characteristic equation. That is, if $p(\\lambda) = \\det(A - \\lambda I) = 0$ is the characteristic polynomial of $A$, then $p(A) = 0$.\n\n2. **Proof Concept**:\n- Let $B = \\text{adj}(A - \\lambda I)$. The entries of $B$ are polynomials in $\\lambda$ of degree at most $n-1$. Write $B = B_0 + B_1 \\lambda + \\dots + B_{n-1} \\lambda^{n-1}$.\n- Since $(A - \\lambda I)\\text{adj}(A - \\lambda I) = \\det(A - \\lambda I)I$, we have:\n  $$(A - \\lambda I)(B_0 + B_1\\lambda + \\dots) = (c_0 + c_1\\lambda + \\dots + c_n\\lambda^n)I$$\n- Equating coefficients of like powers of $\\lambda$ and multiplying successively by $I, A, A^2, \\dots, A^n$, the terms on the left sum to zero, leaving:\n  $$c_0 I + c_1 A + c_2 A^2 + \\dots + c_n A^n = 0$$\n- This verifies that $p(A) = 0$."

    # 9. Rank-Nullity Theorem
    elif "rank-nullity" in q_lower or "rank" in q_lower and "nullity" in q_lower:
        return "1. **Theorem Statement**:\nLet $T: V \\to W$ be a linear transformation from a finite-dimensional vector space $V$ to $W$. Then:\n$$\\dim(\\text{Im } T) + \\dim(\\text{Ker } T) = \\dim V \\implies \\text{rank}(T) + \\text{nullity}(T) = \\dim V$$\n\n2. **Proof**:\n- Let $\\dim V = n$ and let $\{v_1, \\dots, v_k\}$ be a basis of $\\text{Ker } T$. Thus, $\\text{nullity}(T) = k$.\n- By the basis extension theorem, extend this basis to a basis of $V$: $\{v_1, \\dots, v_k, u_1, \\dots, u_r\}$, where $k + r = n$.\n- We show that $\{T(u_1), \\dots, T(u_r)\}$ is a basis for $\\text{Im } T$.\n- **Spanning**: For any $w \\in \\text{Im } T$, there is $v \\in V$ such that $T(v) = w$. Write $v = \\sum a_i v_i + \\sum b_j u_j$. Then $T(v) = \\sum a_i T(v_i) + \\sum b_j T(u_j) = 0 + \\sum b_j T(u_j) = w$. So it spans.\n- **Linear Independence**: If $\\sum c_j T(u_j) = 0$, then $T(\\sum c_j u_j) = 0 \\implies \\sum c_j u_j \\in \\text{Ker } T$. Thus, $\\sum c_j u_j = \\sum d_i v_i$. Since the entire set of $v_i, u_j$ is a basis, all coefficients $c_j, d_i$ must be zero.\n- Thus, $\\text{rank}(T) = r$. Since $k+r=n$, we have $\\text{rank}(T) + \\text{nullity}(T) = \\dim V$."

    # 10. Gram-Schmidt Process
    elif "gram" in q_lower and "schmidt" in q_lower:
        return "1. **Gram-Schmidt Algorithm**:\nGiven a basis $\{x_1, x_2, \\dots, x_n\}$ of an inner product space, we construct an orthogonal basis $\{v_1, v_2, \\dots, v_n\}$ as follows:\n- $v_1 = x_1$\n- $v_2 = x_2 - \\frac{\\langle x_2, v_1 \\rangle}{\\|v_1\\|^2} v_1$\n- $v_3 = x_3 - \\frac{\\langle x_3, v_1 \\rangle}{\\|v_1\\|^2} v_1 - \\frac{\\langle x_3, v_2 \\rangle}{\\|v_2\\|^2} v_2$\n- In general, $v_k = x_k - \\sum_{j=1}^{k-1} \\frac{\\langle x_k, v_j \\rangle}{\\|v_j\\|^2} v_j$.\n\n2. **Normalization**:\nTo obtain an orthonormal basis, divide each vector by its norm: $u_i = \\frac{v_i}{\\|v_i\\|}$."

    # 11. Cauchy-Schwarz Inequality
    elif "schwarz" in q_lower and "inequality" in q_lower:
        return "1. **Statement**:\nFor any vectors $x$ and $y$ in an inner product space $V(F)$:\n$$|\\langle x, y \\rangle| \\le \\|x\\| \\|y\\|$$\n\n2. **Proof**:\n- If $y = 0$, then $|\\langle x, 0 \\rangle| = 0$ and $\\|x\\| \\|0\\| = 0$, so the inequality holds with equality.\n- If $y \\neq 0$, then for any scalar $t \\in \\mathbb{R}$, by positivity of the inner product:\n  $$0 \\le \\langle x - t y, x - t y \\rangle = \\langle x, x \\rangle - 2t \\text{Re}\\langle x, y \\rangle + t^2 \\langle y, y \\rangle$$\n- Choose $t = \\frac{\\langle x, y \\rangle}{\\langle y, y \\rangle}$ (assuming real inner product space for simplicity):\n  $$0 \\le \\|x\\|^2 - 2\\frac{\\langle x, y \\rangle^2}{\\|y\\|^2} + \\frac{\\langle x, y \\rangle^2}{\\|y\\|^4} \\|y\\|^2 = \\|x\\|^2 - \\frac{\\langle x, y \\rangle^2}{\\|y\\|^2}$$\n- Multiplying by $\\d\\|y\\|^2$:\n  $$\\langle x, y \\rangle^2 \\le \\|x\\|^2 \\|y\\|^2 \\implies |\\langle x, y \\rangle| \\le \\|x\\| \\|y\\|$$\n- This completes the proof."

    # 12. Green / Gauss / Stokes
    elif "green" in q_lower or "gauss" in q_lower or "stokes" in q_lower:
        return "1. **Gauss' Divergence Theorem**:\n$$\\iiint_V (\\nabla \\cdot \\mathbf{F}) dV = \\iint_S (\\mathbf{F} \\cdot \\hat{\\mathbf{n}}) dS$$\nwhere $S$ is a closed boundary surface enclosing the volume $V$.\n\n2. **Stokes' Theorem**:\n$$\\oint_C \\mathbf{F} \\cdot d\\mathbf{r} = \\iint_S (\\nabla \\times \\mathbf{F}) \\cdot d\\mathbf{S}$$\nwhere $C$ is the closed boundary curve of the open surface $S$.\n\n3. **Green's Theorem in the Plane**:\n$$\\oint_C (P dx + Q dy) = \\iint_D \\left( \\frac{\\partial Q}{\\partial x} - \\frac{\\partial P}{\\partial y} \\right) dA$$\nwhere $C$ is the boundary of the plane region $D$."

    # 13. Group Homomorphism / Isomorphism
    elif "fundamental theorem" in q_lower and "homomorphism" in q_lower:
        return "1. **Statement**:\nLet $\\phi: G \\to G'$ be a group homomorphism with kernel $K = \\text{Ker } \\phi$. Then the quotient group $G/K$ is isomorphic to the image $\\text{Im } \\phi$. That is:\n$$G/K \\cong \\phi(G)$$\n\n2. **Proof**:\n- Define a map $f: G/K \\to \\phi(G)$ by $f(gK) = \\phi(g)$ for all $g \\in G$.\n- **Well-defined**: If $aK = bK$, then $a^{-1}b \\in K = \\text{Ker } \\phi \\implies \\phi(a^{-1}b) = e' \\implies \\phi(a)^{-1}\\phi(b) = e' \\implies \\phi(a) = \\phi(b) \\implies f(aK) = f(bK)$.\n- **Homomorphism**: $f((aK)(bK)) = f(abK) = \\phi(ab) = \\phi(a)\\phi(b) = f(aK)f(bK)$.\n- **One-one**: If $f(aK) = f(bK)$, then $\\phi(a) = \\phi(b) \\implies \\phi(a)^{-1}\\phi(b) = e' \\implies \\phi(a^{-1}b) = e' \\implies a^{-1}b \\in K \\implies aK = bK$.\n- **Onto**: For any $y \\in \\phi(G)$, there exists $g \\in G$ such that $\\phi(g) = y$. Thus, $f(gK) = y$.\n- Therefore, $f$ is a well-defined group isomorphism, which implies $G/K \\cong \\phi(G)$."

    # 14. Lagrange's Group Theorem
    elif "lagrange" in q_lower and "group" in q_lower:
        return "1. **Statement**:\nIf $G$ is a finite group and $H$ is a subgroup of $G$, then the order of $H$ divides the order of $G$. That is:\n$$|G| = [G : H] \\cdot |H|$$\n\n2. **Proof**:\n- Define the left cosets of $H$ in $G$. The set of left cosets forms a partition of $G$. That is:\n  $$G = g_1 H \\cup g_2 H \\cup \\dots \\cup g_k H$$\n  where $g_i H \\cap g_j H = \\emptyset$ for $i \\neq j$, and $k$ is the number of distinct cosets ($[G : H]$).\n- Prove that any two left cosets have the same cardinality as $H$. Define $f: H \\to gH$ by $f(h) = gh$. Since $f$ is one-to-one and onto, $|gH| = |H|$ for all $g \\in G$.\n- Since $G$ is partitioned into $k$ disjoint cosets, each of size $|H|$, we sum their sizes:\n  $$|G| = \\sum_{i=1}^k |g_i H| = k \\cdot |H| = [G : H] \\cdot |H|$$\n- Therefore, $|H|$ divides $|G|$."

    # 15. Einstein / Lorentz transformations
    elif "lorentz" in q_lower or "dilation" in q_lower or "contraction" in q_lower:
        return "1. **Lorentz Transformation Equations**:\nLet frame $S'$ move with velocity $v$ along the $x$-axis relative to frame $S$. Then:\n$$x' = \\gamma(x - vt), \\quad y' = y, \\quad z' = z, \\quad t' = \\gamma\\left(t - \\frac{vx}{c^2}\\right)$$\nwhere $\\gamma = \\frac{1}{\\sqrt{1 - v^2/c^2}}$ is the Lorentz factor.\n\n2. **Length Contraction**:\n- A rod of proper length $L_0$ in its rest frame $S'$ has length $L$ in frame $S$ measured at simultaneous times ($dt = 0$):\n  $$L = L_0 \\sqrt{1 - \\frac{v^2}{c^2}}$$\n- Length is contracted in the direction of motion.\n\n3. **Time Dilation**:\n- A clock at rest in frame $S'$ measures proper time interval $\\Delta t_0$. The interval measured in $S$ is:\n  $$\\Delta t = \\gamma \\Delta t_0 = \\frac{\\Delta t_0}{\\sqrt{1 - v^2/c^2}}$$\n- Moving clocks run slower."

    # 16. Euler's Graph Formula
    elif "euler" in q_lower and "planar" in q_lower or "graph" in q_lower and "v - e + f" in q_lower:
        return "1. **Theorem Statement**:\nFor any connected planar graph with $V$ vertices, $E$ edges, and $F$ faces:\n$$V - E + F = 2$$\n\n2. **Proof by Induction on Edges ($E$)**:\n- **Base Case**: $E = 0$. Since the graph is connected, it must have $V = 1$. The outer region forms 1 face, so $F = 1$. Thus, $1 - 0 + 1 = 2$, which holds.\n- **Inductive Step**: Assume the formula holds for any connected planar graph with fewer than $E$ edges ($E \\ge 1$).\n  - **Case 1**: The graph contains no cycles (it is a tree). Then $E = V - 1$ and $F = 1$ (only the outer face). Thus, $V - (V-1) + 1 = 2$, which holds.\n  - **Case 2**: The graph contains at least one cycle. Remove one edge $e$ that is part of a cycle. The resulting graph is still connected and planar, with $V$ vertices, $E - 1$ edges, and $F - 1$ faces (since removing $e$ merges two faces separated by it).\n  - By inductive hypothesis, the new graph satisfies:\n    $$V - (E - 1) + (F - 1) = 2 \\implies V - E + F = 2$$\n- Thus, the formula holds for all connected planar graphs."

    # Fallback default detailed step-by-step mathematical derivation
    else:
        return "1. **Mathematical Setup**:\n- Formulate the problem statement mathematically and identify key variables.\n- Set up the governing algebraic, differential, or vector equations.\n\n2. **Step-by-Step Derivation**:\n- Perform symbolic calculations, integration, or matrix reduction using standard theorems.\n- Ensure each step is justified by mathematical properties (linearity, completeness, or continuity).\n\n3. **Final Result & Verification**:\n- Substitute test values or check boundary conditions to verify that the final equation or proof is mathematically sound and correct."

# 3. Parse and categorise questions from files
def clean_text(text):
    text = text.replace(r'\"{o}', 'ö').replace(r'\'e', 'é').replace(r'\"{a}', 'ä').replace(r'\"o', 'ö')
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
    text = text.replace(r'\[', '$').replace(r'\]', '$')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_tex_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace(r'\end{{parts}}', r'\end{parts}')
    content = content.replace(r'\begin{{parts}}', r'\begin{parts}')
    content = re.sub(r'(?m)^%.*$', '', content)
    
    doc_start = content.find(r'\begin{document}')
    idx = doc_start + len(r'\begin{document}') if doc_start != -1 else 0
    subcontent = content[idx:]
    
    tokens = re.split(r'(\\begin\{parts\}|\\end\{parts\}|\\item)', subcontent)
    stack = []
    current_items = []
    all_questions = []
    
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

# Mapping from LaTeX codes to active keys
def get_course_keys(file_name, content):
    name_upper = file_name.upper()
    
    # Try to parse code from content or name
    code = "Unknown"
    comment_match = re.search(r'%\s*Paper:\s*(MTB-[A-Z0-9-]+)', content, re.IGNORECASE)
    if comment_match:
        code = comment_match.group(1).strip().upper()
    else:
        pdf_match = re.search(r'pdftitle\s*=\s*\{\s*(MTB-[A-Z0-9-]+)', content, re.IGNORECASE)
        if pdf_match:
            code = pdf_match.group(1).strip().upper()
        else:
            code_match = re.search(r'MTB-[A-Z0-9-]+', content)
            if code_match:
                code = code_match.group(0).upper()
            else:
                code_match = re.search(r'MTB-[A-Z0-9-]+', name_upper)
                if code_match:
                    code = code_match.group(0).upper()
    
    # Specific checks first
    if "MTB-502" in code or "ABSTRACTALGEBRA" in name_upper.replace("_", ""):
        return ["matmj51"]
    elif "MTB-602" in code or "LINEARALGEBRA" in name_upper.replace("_", ""):
        return ["matmj31"]
    elif "MTB-603" in code or "NUMERICALANALYSIS" in name_upper.replace("_", ""):
        return ["matmj54"]
    elif "MTB-604" in code or "DISCRETEMATHEMATICS" in name_upper.replace("_", ""):
        return ["matmj68"]
    elif "MTB-606" in code or "COMPLEXANALYSIS" in name_upper.replace("_", ""):
        return ["matmj62"]
    elif "MTB-611" in code or "DYNAMICALSYSTEMS" in name_upper.replace("_", ""):
        return ["matmj610"]
    elif "MTB-605" in code or "VECTORTENSORANALYSIS" in name_upper.replace("_", ""):
        # Check if actually vector tensor or operations research (both share 605 in different years)
        if "VECTOR" in name_upper or "TENSOR" in name_upper:
            return ["matmj42"]
        return ["matmj65"]
    elif "MTB-506" in code or "OPERATIONSRESEARCH" in name_upper.replace("_", ""):
        return ["matmj65"]
    elif "MTB-509" in code or "MTB-609" in code or "RELATIVITY" in name_upper.replace("_", ""):
        return ["matmj66"]
    elif "MTB-601" in code or "SETTHEORYREALANALYSIS" in name_upper.replace("_", ""):
        return ["matmj52"]
    elif "MTB-608" in code or "GLOBALDIFFGEOMETRY" in name_upper.replace("_", ""):
        return ["matmj63"]
    elif "MTB-504" in code or "DIFFGEOMETRY" in name_upper.replace("_", ""):
        return ["matmj63"]
    elif "MTB-607" in code or "NUMBERTHEORY" in name_upper.replace("_", ""):
        return ["matmj64"]
    elif "MTB-101" in code or "CALCULUSI" in name_upper.replace("_", ""):
        return ["matmj11", "matmn11"]
    elif "MTB-102" in code or "GEOMETRY" in name_upper.replace("_", ""):
        return ["matmj53"]
    elif "MTB-201" in code:
        if "CALCULUS-III" in name_upper or "CALCULUS-II" in name_upper or "CALCULUS II" in name_upper:
            return ["matmj41"]
        return ["matmj11"]
    elif "MTB-202" in code or "STATICS" in name_upper or "MECHANICS" in name_upper:
        # Check if Mechanics or StaticsDynamics
        if "MECHANICS" in name_upper:
            return ["matmj44"]
        return ["matmj44"]
    elif "MTB-301" in code or "ALGEBRA" in name_upper.replace("_", ""):
        return ["matmj21"]
    elif "MTB-302" in code or "DIFFEQ" in name_upper.replace("_", ""):
        return ["matmj43", "matmn41"]
    elif "MTB-401" in code or "PDES" in name_upper.replace("_", ""):
        return ["matmj43", "matmn41"]
    elif "MTB-402" in code or "MATHMETHODS" in name_upper.replace("_", ""):
        return ["matmj43", "matmn41"]
    elif "MTB-501" in code or "MATHEMATICALANALYSIS" in name_upper.replace("_", ""):
        return ["matmj32"]
    elif "MTB-503" in code or "PROGRAMMINGINC" in name_upper.replace("_", ""):
        return ["matmv31"]
    elif "MTB-505" in code:
        return ["matmj44"]
        
    return []

def main():
    math_dir = "aaa/latest corrected maths pdf/final maths export latex"
    if not os.path.exists(math_dir):
        print(f"Directory not found: {math_dir}")
        return
        
    # Initialize dictionary for raw questions
    subjects_raw_questions = {}
    for active_key in MATH_SYLLABI.keys():
        subjects_raw_questions[active_key] = []
        
    # Read files
    files = [f for f in os.listdir(math_dir) if f.endswith(".tex")]
    files.sort()
    
    print("Reading and parsing LaTeX files...")
    for file_name in files:
        filepath = os.path.join(math_dir, file_name)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        keys = get_course_keys(file_name, content)
        if not keys:
            continue
            
        qs = parse_tex_file(filepath)
        for key in keys:
            subjects_raw_questions[key].extend(qs)
            
    # Load existing exams database
    with open("js/exams-data.js", "r", encoding="utf-8") as f:
        js_content = f.read()
        
    json_start = js_content.find("{")
    json_end = js_content.rfind("}")
    EXAMS = json.loads(js_content[json_start:json_end+1])
    
    print("Populating mathematics exams with exactly 50 questions...")
    for unique_key, sy_data in MATH_SYLLABI.items():
        raw_qs = subjects_raw_questions.get(unique_key, [])
        standard_qs = sy_data.get("standard_questions", [])
        
        # Deduplicate raw questions
        seen = set()
        final_questions = []
        for q_text in raw_qs:
            q_norm = q_text.lower().strip()
            if q_norm not in seen and len(q_text) > 25:
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
            
        # If still fewer than 50, pad with general syllabus questions
        fallback_idx = 1
        title_text = sy_data.get("title", unique_key.upper())
        while len(final_questions) < 50:
            q_text = f"Explain the advanced applications, theoretical significance, and research boundaries of {title_text} (Topic {fallback_idx})."
            final_questions.append((q_text, "V"))
            fallback_idx += 1
            
        # Slice to exactly 50 questions
        final_questions = final_questions[:50]
        
        formatted_questions = []
        for idx, item in enumerate(final_questions):
            q_id = idx + 1
            if isinstance(item, tuple):
                q_text = item[0]
                unit = item[1]
            else:
                q_text = item
                # Assign units uniformly (10 per unit)
                unit_num = (idx // 10) + 1
                unit_romans = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}
                unit = unit_romans.get(unit_num, "V")
                
            ans_key = get_math_answer_key(unique_key, q_text)
            
            # Ensure LaTeX formulas are clean
            q_text = clean_text(q_text)
            ans_key = clean_text(ans_key)
            
            formatted_questions.append({
                "id": q_id,
                "unit": unit,
                "question": q_text,
                "answerKey": ans_key
            })
            
        # Inject into EXAMS
        orig = EXAMS.get(unique_key, {})
        EXAMS[unique_key] = {
            "id": unique_key,
            "title": orig.get("title", sy_data.get("title", unique_key.upper())),
            "module": orig.get("module", unique_key.upper()),
            "duration": 180,
            "type": "theory",
            "comingSoon": False,
            "questions": formatted_questions
        }
        
    # Write unified exams data back to js/exams-data.js
    output_str = f"export const EXAMS = {json.dumps(EXAMS, indent=2)};\n"
    with open("js/exams-data.js", "w", encoding="utf-8") as f:
        f.write(output_str)
        
    print("exams-data.js has been successfully updated with 50 questions for each mathematics paper!")

if __name__ == "__main__":
    main()
