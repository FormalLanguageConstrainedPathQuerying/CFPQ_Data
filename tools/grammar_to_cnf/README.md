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
    
    **head -> body<sub>1</sub> | body<sub>2</sub> | ... | body<sub>n</sub>**

    where each body can contain basic regular expression, allowed operators:
    
    - The concatenation, the default operator, which can by represented either by a space or a dot (.)
    
    - The union, represented either by +
    
    - The kleene star, represented by *


To start run:
```
pip3 install -r requirements.txt
python3 grammar_to_pyformlang.py PATH_TO_GRAMMAR -o PATH_TO_OUTPUT
```