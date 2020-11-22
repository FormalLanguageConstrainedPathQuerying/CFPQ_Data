Loads context-free grammar and outputs it in CNF.

Use the following input format:

- Line 0:

    ```
    a set of variable symbols delimited by spaces,
    the first one is the starting symbol
    ```

- Line 1:

    ```
    a set of terminal symbols delimited by spaces
    ```

- The rest of the lines are productions in the form:
    
    ```head -> body | body | ... | body```

    where each body can contain basic regular expression, allowed operators:
    
    - The concatenation, the default operator, which can by represented either by a space or a dot (.)
    
    - The union, represented by ```|``` 

    - The ```?``` quantifier
    
    - The kleene star, represented by ```*```
    
    Epsilon symbol should be represented by ```eps```


To start run:
```
python3 main.py grammar2cnf file PATH_TO_GRAMMAR --output PATH_TO_OUTPUT
```
