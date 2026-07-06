issue With Undo It Should Completely undo whatever i did with tool not one by one 

I used lambda because my slot needs arguments. The lambda delays the function call until the signal is emitted; otherwise, Python would call the function immediately while setting up the connection.

self.do_something → the function (can be called later)
self.do_something() → the result of calling the function now

print(2 + 3)
Python doesn't call print and somehow wait to compute 2 + 3 later.
It first computes:

temp = 2 + 3
print(temp)

The same evaluation rule applies here:

button.clicked.connect(self.do_something())

becomes

temp = self.do_something()      # executes now
button.clicked.connect(temp)

What Qt wants is a callable—something it can save and invoke later.

When you write

button.clicked.connect(self.do_something)

you're passing the function itself.

Qt stores it internally:

clicked signal
    │
    └──► self.do_something

Later, when the button is clicked, Qt says:

"I have a function stored. I'll call it now."

When you need arguments:

button.clicked.connect(
    lambda: self.do_something("Hello", 42)
)

Qt stores the lambda instead:

clicked signal
    │
    └──► lambda
            │
            └──► self.do_something("Hello", 42)

The lambda doesn't execute until Qt calls it after the signal is emitted.


As Qt Only Wants like i have a function stored so will call it. 
but beacuase you are giving me arguments that i dont know to handle . 
so that is why i will wrap the function call with argument so that qt call directly call that lambda which will remove that issue qt 

Qt expects a callable that it can invoke when the signal is emitted. If I need to pass my own arguments to the function, I wrap the call in a lambda. Qt calls the lambda, and the lambda then calls my function with the required arguments.