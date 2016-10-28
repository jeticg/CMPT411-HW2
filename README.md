# CMPT411-HW2
Aufgaben 2 des CMPT411 im Herbst 2016

### How to Run The Programme

This programme is written in python. Here are some information on the
development environment:

    OS: macOS 10.12.1

    Python Version: Python 2.7.12 (default, Oct 11 2016, 05:24:00)
    [GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.38)] on darwin

To run the programme, simply pick a test file(for example, test1.txt), and use
the following command:

    python main.py test1.txt

The output will have two parts: information on reasoning process and final list
of conclusions. The conclusions will be printed out in the following format:

    ['t', '~r', '~w', '~s', 'q', 'p']

Whereas `~atom` means the negation of the `atom`.

### Logic of The Programme

The logic of this programme is simple. First given the input, we construct a
graph. Each sentence will have a conclusion and some antecedents, we build an
edge with positive weight from every positive antecedent to the sentence, and
an edge with negative weight from every negative antecedent to the sentence.

And finally, we maintain a list of all the sentences that can derive each atom.

Every time an atom is concluded, we remove the atom from all the sentences
that has it as a positive antecedent, and remove all the sentences that have it
as negative antecedent. The similar thing is done when an atom is failed.

The first phase we simply deduce all the truth we could. The way this programme
achieves this, is to go through all the sentences, and add all sentences with
conclusions only(no antecedents) to a queue. Then we go through the queue,
conclude these atoms, and when eliminating them from other sentences, check if
these sentences have any antecedent left after elimination, if no, add them to
the end of the queue; or, when eliminating sentences, if their conclusions have
no more sentences to deduce them, fail these atoms.

In this way, by the end of phase one, we will have all possible truth about the
atoms without failing those that have no sentences to make them true to start
with.

In phase two, we fail all atoms that only occured as antecedents of other
atoms. In the process, do the same elimination for them as phase one.

Now, the rest is simple, repeat the process just like in phase one, and we will
have all the facts.

In the actual code, instead of using a graph, I used 3 dicts and a list.

The list is for storing sentences, and the 3 dicts stores information of:

    `deduce[atom]`: a list of indices of all the sentences that have this
    `atom` as a positive antecedent. (What can this atom help deducing)

    `fail[atom]`: a list of indices of all the sentences that have this `atom`
    as a negative antecedent. (What can the failing of this atom help deducing)

    `depend[atom]`: a list of indices of all the sentences that have this
    `atom` as the conclusion. (What the truth of this atom depends on)

Using this data structure, for any atom, one can quickly find all its
references, so whenever we need to eliminate it from all references, or to
eliminate the sentences that is its reference, we can do it in `O(1)` time per
reference.

The overall complexity of the programme is `O(n)`, because all it does
technically, is to go through all sentences, and for each atom, eliminate all
its references. If the number of sentences is `m`, the maximum amount of atoms
in a sentence is `k`, then the time complexity would be `O(mk)`, which is
`O(n)` where `n` is the total length of input.

### Test Results

test1.txt:

    [p [q] [r]]
    [p [s] []]
    [q [] [s]]
    [r [] [t]]
    [t [] []]
    [s [w] []]

result:

    ['t', '~r', '~w', '~s', 'q', 'p']

test2.txt:

    [a [b] []]
    [b [] [h]]
    [c [d e] []]
    [e [] []]
    [d [f] [b]]
    [f [] [g h j]]
    [f [j] []]
    [g [] [j]]
    [h [e] []]
    [i [] [k]]
    [k [] [i]]

result:

    ['e', 'h', '~b', '~a', '~j', '~f', '~d', '~c', 'g']
    
