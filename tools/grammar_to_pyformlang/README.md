Loads CFG to pyformlang. 

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

    ```
    head -> body
    ```

    where body can contain regular expression.

To start run:
```
pip3 install -r requirements.txt
python3 grammar_to_pyformlang.py PATH_TO_GRAMMAR
```