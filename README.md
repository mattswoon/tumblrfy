# TUMBLRFY
Make your text more tumblr

# Usage

Run
`tumblrfy --ops operations -i input -o output`

## Operations
### bracket-number
```
tumblrfy --ops bracket-number -i input.txt

input.txt
-----------------
the number six is a small number
the number six thousand and eighty three is bigger

the number 1,179 has a comma
the number 1 789 378 uses spaces

this line has both the number eighty four and 3
------------------

output:
the number six (6) is a small number
the number six thousand and eighty three (6,083) is bigger

the number one thousand, one hundred and seventy nine (1,179) has a comma
the number one million, seven hundred and eighty nine thousand, three hundred and seventy eight (1,789,378) uses spaces

this line has both the number eighty four (84) and three (3)
```
