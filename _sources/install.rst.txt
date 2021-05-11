.. _install:

Install
=======

.. only:: html

   :Release: |release|
   :Date: |today|

CFPQ_Data requires Python 3.7 or later.  If you do not already
have a Python environment configured on your computer, please see the
instructions for installing the full `scientific Python stack
<https://scipy.org/install.html>`_.

Below we assume you have the default Python environment already configured on
your computer and you intend to install ``cfpq_data`` inside of it.  If you want
to create and work with Python virtual environments, please follow instructions
on `venv <https://docs.python.org/3/library/venv.html>`_ and `virtual
environments <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_.

First, make sure you have the latest version of ``pip`` (the Python package manager)
installed. If you do not, refer to the `Pip documentation
<https://pip.pypa.io/en/stable/installing/>`_ and install ``pip`` first.

Install the released version
----------------------------

Install the current release of ``cfpq_data`` with ``pip``::

    pip install cfpq_data

To upgrade to a newer release use the ``--upgrade`` flag::

    pip install --upgrade cfpq_data

If you do not have permission to install software systemwide, you can
install into your user directory using the ``--user`` flag::

    pip install --user cfpq_data

Alternatively, you can manually download ``cfpq_data`` from
`GitHub <https://github.com/JetBrains-Research/CFPQ_Data/releases>`_  or
`PyPI <https://pypi.org/project/cfpq-data/>`_.
To install one of these versions, unpack it and run the following from the
top-level source directory using the Terminal::

    pip install .
