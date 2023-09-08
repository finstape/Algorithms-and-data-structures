# Algorithms-and-data-structures
Materials for the practicum for 'Algorithms and data structures' course at SpbU 3rd semester

## Dataset generation

A. Generate a dataset with the following sets of properties:

1. Full name - Ivanov Ivan Ivanovich
2. Phone number - “+79001234567”
3. Work address - University nab., 7
4. Position - Manager
5. S/P - 50,000 rubles

B. Additional information on each property (Saint Petersburg):

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
5. S / P - average in this specialty in the city and do
the probability that will make how many people get gender. bids.
(Manager - 50,000 rubles, Manager - 25,000 rubles)

C. Limitations of the dataset:

1. The total number of rows in the dataset is at least 50,000.
2. FULL name - the dictionary should consist only of Slavic full names
3. Phone number - all operators and variations of regional codes by
St. Petersburg.
4. The minimum number of people at the address is 50 people.
5. A set of professions - at least 10
6. S /N - varieties according to the formula = (A set of professions + (A set
of professions/2))
Example if we have 15 professions, then variations on S/N should be,
15+(15/2) = 23. since we round up the quotient to an integer.
