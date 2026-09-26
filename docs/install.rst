.. _install:

Install
=======

.. only:: html

   :Release: |release|
   :Date: |today|

CFPQ_Data requires Python 3.11–3.13.  If you do not already
have a Python environment configured on your computer, please see the
instructions for installing the full `scientific Python stack
<https://scipy.org/install.html>`_.

Below we assume you have the default Python environment already configured on
your computer and you intend to install ``flpq_data`` inside of it.  If you want
to create and work with Python virtual environments, please follow instructions
on `venv <https://docs.python.org/3/library/venv.html>`_ and `virtual
environments <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_.

First, make sure you have the latest version of ``pip`` (the Python package manager)
installed. If you do not, refer to the `Pip documentation
<https://pip.pypa.io/en/stable/installing/>`_ and install ``pip`` first.

Install the released version
----------------------------

Install the current release of ``flpq_data`` with ``pip``::

    pip install cfpq-data

To upgrade to a newer release use the ``--upgrade`` flag::

    pip install --upgrade cfpq-data

If you do not have permission to install software systemwide, you can
install into your user directory using the ``--user`` flag::

    pip install --user cfpq-data

Alternatively, you can manually download ``flpq_data`` from
`GitHub <https://github.com/FormalLanguageConstrainedPathQuerying/CFPQ_Data/releases>`_  or
`PyPI <https://pypi.org/project/cfpq-data/>`_.
To install one of these versions, unpack it and run the following from the
top-level source directory using the Terminal::

    pip install .
