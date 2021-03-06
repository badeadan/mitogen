
Mitogen Compared To
-------------------

This provides a little free-text summary of conceptual differences between
Mitogen and other tools, along with some basic perceptual metrics (project
maturity/age, quality of tests, function matrix)


Ansible
#######

Ansible_ is a complete provisioning system, Mitogen is a small component of such a system.

You should use Ansible if ...

You should not use Ansible if ...


.. _Ansible: https://docs.ansible.com/ansible/latest/index.html
.. _ansible.src: https://github.com/ansible/ansible/

Baker
#####

    Baker_ lets you easily add a command line interface to your Python
    functions using a simple decorator, to create scripts with "sub-commands",
    similar to Django's ``manage.py``, ``svn``, ``hg``, etc.

- Unmaintained since 2015
- No obvious remote execution functionality

.. _Baker: https://bitbucket.org/mchaput/baker

Chopsticks
##########

Chopsticks_ also supports recursion! but the recursively executed instance has no special knowledge of its identity in a tree structure, and little support for functions running in the master to directly invoke functions in a recursive context.. effectively each recursion produces a new master, from which function calls must be made.

executing functions from __main__ entails picking just that function and deps
out of the main module, not transferring the module intact. that approach works
but it's much messier than just arranging for __main__ to be imported and
executed through the import mechanism.

supports sudo but no support for require_tty or typing a sudo password. also supports SSH and Docker.

good set of tests

real PEP-302 module loader, but doesn't try to cope with master also relying on
a PEP-302 module loader (e.g. py2exe).

Based on the tox configuration Python 2.7, and 3.3 to 3.6 are supported.

I/O multiplexer in the master, but not in children.

As with Execnet it includes its own serialization - pencode_ supports

- most Python primitive types (``bytes``/``str``/``unicode``, ``list``, ``tuple`` ...)
- identity references
- self referencing (recursive) data srtuctures

pencode lacks support for arbitrary classes. Byte strings require special
treatment if they contain non-ascii characters. Some primitive types
(e.g. ``complex``) are not handled. This would be straightforwar to address.
Values are length-prefixed with a 32 bit unsigned integer, meaning values
are limited to 4 billion bytes or items in length.

design is reminiscent of Mitogen in places (Tunnel is practically identical to
Mitogen's Stream), and closer to Execnet elsewhere (lack of uniformity,
tendency to prefer logic expressed in if/else special case soup rather than the
type system, though some of that is due to supporting Python 3, so not judging
too harshly!)

Chopsticks has its own `Chopsticks vs`_ comparisons.

You should use Chopsticks if you need Python 3 support.

.. _Chopsticks: https://chopsticks.readthedocs.io/en/stable/
.. _Chopsticks.src: https://github.com/lordmauve/chopsticks/
.. _Chopsticks vs: https://chopsticks.readthedocs.io/en/stable/intro.html#chopsticks-vs
.. _pencode: https://github.com/lordmauve/chopsticks/blob/master/doc/pencode.rst
.. _pencode.src: https://github.com/lordmauve/chopsticks/blob/master/chopsticks/pencode.py

Disco
#####

    Disco_ is a lightweight, open-source framework for distributed computing
    based on the MapReduce paradigm.

- An Erlang core, with Python bindings
- Wire format is pickle, according to `Execnet vs NLTK for distributed NLTK`_

.. _Disco: http://discoproject.org/
.. _Execnet vs NLTK for distributed NLTK: https://streamhacker.com/2009/12/14/execnet-disco-distributed-nltk/

Execnet
#######

Execnet_

- Parent and children may use threads, gevent, or eventlet, Mitogen only supports threads.
- No recursion
- Similar Channel abstraction but better developed.. includes waiting for remote to close its end
- Heavier emphasis on passing chunks of Python source code around, modules are loaded one-at-a-time with no dependency resolution mechanism
- Built-in unidirectional rsync-alike, compared to Mitogen's SSH emulation which allows use of real rsync in any supported mode
- no support for sudo, but supports connecting to vagrant
- works with read-only filesystem
- includes its own serialization_ independent of the standard library

      The obj and all contained objects must be of a builtin python type
      (so nested dicts, sets, etc. are all ok but not user-level instances).

- Known uses include `pytest-xdist`_, and `Distributed NLTK`_

You should use Execnet if you value code maturity more than featureset.

.. _Execnet: https://codespeak.net/execnet/
.. _serialization: https://codespeak.net/execnet/basics.html#dumps-loads
.. _pytest-xdist: https://pypi.python.org/pypi/pytest-xdist
.. _Distributed NLTK: https://streamhacker.com/2009/12/14/execnet-disco-distributed-nltk/

Fabric
######

Fabric_ allows execution of shell snippets on remote machines, Python functions run
locally, any remote interaction is fundamentally done via shell, with all the
limitations that entails. prefers to depend on SSH features (e.g. tunnelling)
than reinvent them

You should use Fabric if you enjoy being woken at 4am to pages about broken
shell snippets.

.. _fabric: http://www.fabfile.org/

Invoke
######

Invoke_

Python 2.6+, 3.3+

Basically a Fabric-alike

.. _invoke: http://www.pyinvoke.org/

Multiprocessing
###############

multiprocessing_ was added to the stdlib in Python 2.6.

    multiprocessing is a package that supports spawning processes using an
    API similar to the threading module. The multiprocessing package offers
    both local and remote concurrency

There is a backport_ for Python 2.4 & 2.5, but it is not pure Python.
pymultiprocessing_ appears to be a pure Python implementation.
An ecosystem_ of packages has built up around multiprocessing.

The `programming guidelines`_ section notes

- Arguments to proxies must be picklable. On Windows this also applies to
  ``multiprocessing.Process.__init__()`` arguments.
- Callers should beware replacing ``sys.stdin``, because
  ``multiprocessing.Process._bootstrap()``
  will close it and open /dev/null instead

.. _programming guidelines: https://docs.python.org/2/library/multiprocessing.html#programming-guidelines
.. _backport: https://pypi.python.org/pypi/multiprocessing
.. _pymultiprocessing: https://pypi.python.org/pypi/pymultiprocessing
.. _ecosystem: https://pypi.python.org/pypi?%3Aaction=search&term=multiprocessing&submit=search

Paver
#####

Paver_

More or less another task execution framework / make-alike, doesn't really deal
with remote execution at all.

.. _Paver: https://github.com/paver/paver/

Plumbum
#######

Plumbum_

Shell-only

Basically syntax sugar for running shell commands. Nicer than raw shell
(depending on your opinions of operating overloading), but it's still shell.

.. _Plumbum: https://pypi.python.org/pypi/plumbum

Pyro4
#####

Pyro4_
...

.. _Pyro4: https://pythonhosted.org/Pyro4/

RPyC
####

RPyC_

- supports transparent object proxies similar to Pyro (with all the pain and suffering hidden network IO entails)
- significantly more 'frameworkey' feel
- runs multiplexer in a thread too?
- bootstrap over SSH only, no recursion and no sudo
- requires a writable filesystem

.. _RPyC: https://rpyc.readthedocs.io/en/latest/

Salt
####

Salt_

- no crappy deps

You should use Salt if you enjoy firefighting endless implementation bugs,
otherwise you should prefer Ansible.

.. _Salt: https://docs.saltstack.com/en/latest/topics/
.. _Salt.src: https://github.com/saltstack/salt
