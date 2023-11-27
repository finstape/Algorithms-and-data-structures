# Algorithms-and-data-structures
Materials for the practicum for "Algorithms and data structures" course at SpbU 3rd semester

## Dataset generation

A. Generate a dataset with the following sets of properties:

1. Full name - Ivanov Ivan Ivanovich
2. Phone number - “+79001234567”
3. Work address - University emb., 7
4. Position - Manager
5. Salary - 50,000 rubles

B. Additional information on each property (St. Petersburg):

1. Full name - dictionary by full name.
2. Phone number - the ability to configure the dataset itself. For example,
so that there are more Megafon numbers than MTS, and the rest equally
and the ability to configure the probability of the internal regional
code of the service provider (Megafon, MTS, etc.)
3. The work address is a ”Dictionary" by which the street will be generated +
set a certain (real) interval of house numbers
4. Position - A ”Dictionary” according to which a position will be generated in
a certain proportion, which can be changed in the future (General
Director - 1%, Chief - 5%, Service personnel (Security Guard,
Cleaner, Commandant, etc.) - 20%, Accountant - 10%, Manager - 20%,
The main professions of your company (Programmers, Engineers,
Doctors, etc.) - 40% and the Secretary - 4%)
5. Salary - average in this specialty in the city and do
the probability that will make how many people get part time.
(Manager - 50,000 rubles, Manager - 25,000 rubles)

C. Limitations of the dataset:

1. The total number of rows in the dataset is at least 50,000.
2. Full name - the dictionary should consist only of Slavic full names
3. Phone number - all operators and variations of regional codes by
St. Petersburg.
4. The minimum number of people at the address is 50 people.
5. A set of professions - at least 10
6. Salary - varieties according to the formula = (A set of professions + (A set
of professions/2))
Example if we have 15 professions, then variations on S/N should be,
15+(15/2) = 23. since we round up the quotient to an integer.

## Dataset depersonalization

Part of the user:

1) The program must read the input file (the final file of the 1st laboratory work)
2) The program is divided by functionality.  
  a) Depersonalization of the input dataset.  
  b) Calculating the K-anonymity of the input dataset.
4) The user has the opportunity to specify Quasi-identifiers in K-anonymity.

Part of the programmer:

4) At your choice, we depersonalize the date set according to these methods (combining is welcome, but the main thing is to prove the effectiveness of this combination of methods):  
  a) Local generalization  
  b) Aggregation  
  c) Perturbation  
  d) Micro-aggregation  
  e) Mixing  
  f) Creating aliases  
  g) Masking  
  h) Local suppression  
  i) Removing attributes  
  j) Decomposition method  
5) Using the K-anonymity method, calculate K for an impersonal set.
6) Output 5 "bad" values of K-anonymity (if there are fewer of them, then all possible). The data of the variable K is output as a percentage of the entire set. 
7) The number of unique rows in the data set, according to quasi-indicators. Output unique strings if the variable K=1. 
8) Output an acceptable K-anonymity value for the data set:  
  a) up to 51000 records - K>=10  
  b) up to 105,000 records - K>=7  
  c) up to 260000 records - K>=5  
9) Evaluate the usefulness of the data by comparing the depersonalized set with the original set

## Hash functions research

The purpose of the work is to decrypt a data set encrypted using a hash function using an input modifier – salt, and also to analyze the solution of a similar problem under different conditions.

The procedure for performing laboratory work:

1. To study the features of encryption of phone numbers.
2. Write a program to de-identify the dataset.
3. Test the program on the issued version.
4. Test with at least 3 more different hash functions that encrypt the original depersonalized set.
5. Write what causes the decryption speed to change. The effect of the type of salt, the length of the salt and the hash function on the speed of decryption of the dataset.
6. Write a report.
