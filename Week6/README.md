# Course note.
## Index
- [Course note.](#course-note)
  - [Index](#index)
- [Code architecture and testing](#code-architecture-and-testing)
  - [What shall be tested?](#what-shall-be-tested)
  - [Diversity in individuals](#diversity-in-individuals)
  - [Questions when programming](#questions-when-programming)
- [Improved EV3 in solving Combinatorial energy minimization problem.](#improved-ev3-in-solving-combinatorial-energy-minimization-problem)
  - [Introduction & Goals](#introduction--goals)
  - [Sanity checks](#sanity-checks)
  - [Structures of EV3](#structures-of-ev3)
  - [Development steps of EV3](#development-steps-of-ev3)
  - [Results & Performance](#results--performance)
  - [References](#references)

# Code architecture and testing
- Testing and data reading and writing in a seperate way s.t. it can be flexible.
- Structuring the code would make the task easier and make testing easier later.

## What shall be tested?
1. Code itself
2. Algorithm correctness.
3. Perform comparative testing. Is the implementation better/worse than others?

## Diversity in individuals
1. Make more individual class
2. Or using isomorphism or class variations.
3. Add interface and use derived classes from individuals, from top level program we can treat these individuals all the same. Add methods into them, the mutation and crossOver methods.
4. These individuals classes has similar types, but might be with different data type which makes code more maintatinable and more extensible. Harvest the power of OOP.

5. You need to make sure that the quality of your code is fine. Proper result and comparison is needed!

6. Check for consistency, give more test patterns.

## Questions when programming
0. What is your way of prototyping a certain algorithm? How do you set up those varaibles needed? Procedures of testing when you are working your way through the algorithm? Can you give a demostration of your workflow?

1. How do you know which part of code needed to be modularized? Are there any general rules to follow? Any reference or textbook to follow? Design pattern approach?

2. How do you test a complex code? Printing out or are there other convenient stuff?
A:

4. How to debug a program from command pallette? Are there any tutorial of using parser any tutorial about it?
A:

5. Since most of the time spent on researching is reading other people's work. How to approach a new algorithm an algorithm you have never seen before?
A:

6. How to find the hyperparameter used in an EA algorithm?

# Improved EV3 in solving Combinatorial energy minimization problem.

## Introduction & Goals
>Goal: Find the arrangement using Improved EV3 algorithm s.t. the total energy of this arrangement shall be minimal. We only need to consider the interaction between the closest 2 particles.

1. Problem #1:
   - Add Combinatorial Integer representation type to EV3
   - Solve Imaginary 1-D universe energy minimization problem

2. Problem #2:
   - Upgrade EV3 real-number representation to handle multivariate problems, meaning that representation must handle problems with more than one variables(Requring a number of vectors)

3. For Problem #1

   1. Finite 1D discrete lattice with 3 types of particles
      - Lattice length is N
      - 3 particles types: Red Blue and Green(label as 0,1,2)

   2. Every point of lattice



## Sanity checks

## Structures of EV3

## Development steps of EV3

## Results & Performance

## References
