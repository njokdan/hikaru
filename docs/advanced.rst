*******************************************
Advanced Hikaru: Defining Your Own Classes
*******************************************

Hikaru supports the creation and integration of custom classes for a number of use cases. It can allow you to supply a custom class to an existing operation as well as creating instances of your custom class automatically when needed. Some use cases
are quite simple to implement, while others demand a bit more knowledge of Python dataclasses
to use properly. This section covers each of these use cases so that you can successfully 
create your own custom classes for use with Hikaru.

First Things First
##################

Regardless of your use case, there are a few basic requirements that you need to meet in order
for your classes to work properly within Hikaru:

1. First, the module that contains your custom classes **must** include a wildcard import of
   of all the classes in the model module upon which your custom class is based. So for example,
   if you wanted to create a subclass of ``Pod``, you will run into errors if the module that
   contains your ``Pod`` subclass has an import statement like the following:

    ``from hikaru.model.rel_1_21.v1 import Pod``

   Instead, you must import all of the symbols from that release/version:

    ``from hikaru.model.rel_1_21.v1 import *``

2. All of your custom classes must be defined at the top-level within your module, otherwise
   Hikaru won't be able to find them when needed.

3. All of your custom classes must be a subclass of either
   :ref:`HikaruDocumentBase<HikaruDocumentBase doc>` (in the case of top-level classes that
   represent an entire YAML document) or :ref:`HikaruBase<HikaruBase doc>` (in the case
   where a class represents an object that is contained within another Hikaru object).

How to Register Your Class
###########################

Hikaru provides the :ref:`register_version_kind_class()<register_version_kind_class doc>` function to enable you to associate a
:ref:`HikaruDocumentBase<HikaruDocumentBase doc>` subclass with a version/kind pair. You can also optionally specify a
particular release to register the class, otherwise it will be registered to the default
release for the calling thread.

When registering, you must supply the ``apiVersion`` and ``kind`` values that will serve as the
key for determining when to use  your custom class. If you're extending an existing class,
usually the best approach is to use the ``apiVersion`` and ``kind`` class attributes of the 
class you are subclassing. So for example, if you want to register your custom class ``MyPod``
that is a subclass of ``Pod``, you can use ``Pod's`` class attributes to supply the
``apiVersion`` and ``kind`` values:

.. code:: python

    register_version_kind_class(MyPod, Pod.apiVersion, Pod.kind)

Now, when Hikaru sees this particular combination of ``apiVersion`` and ``kind``, it will create
an instance of the ``MyPod`` class instead of the ``Pod`` class as before.

Use Case: Adding Only Methods to Hikaru Classes
################################################

If your use case involves only the addition of methods to existing Hikaru classes and not any
new instance attributes, you'll find this the most straightforward use case for creating custom
classes.

Simply create a subclass using an appropriate
:ref:`HikaruDocumentBase<HikaruDocumentBase doc>` subclass as a base (such as Pod or Deployment),
define the methods you wish, and then register this class using the
:ref:`register_version_kind_class()<register_version_kind_class doc>` function. Hikaru will then
create instances of this class whenever it sees the need for an instance that matches Pod's
``apiVersion`` and ``kind`` values.

As a simple example, here's a Pod subclass that provides a *create* method on the Pod class that takes the namespace 
as a parameter, and hides the actual create method name:

.. code:: python

    from hikaru import register_version_kind_class
    from hikaru.model.rel_1_21 import *

    class CRUDPod(Pod):
        def create_in_namespace(self, namespace: str):
            if self.metadata is None:
                self.metadata = ObjectMeta()
            self.metadata.namespace = namespace
            return self.createNamespacedPod(self.metadata.namespace)

    register_version_kind_class(CRUDPod, Pod.apiVersion, Pod.kind)

While registration of the class isn't needed to create and use the class in your code, Hikaru
will now create instances of CRUDPod whenever it needs to create a Pod, for example when
querying Kubernetes or loading YAML using :ref:`load_full_yaml()`.

Bear in mind that you can always add methods on subclasses of Hikaru objects.

Use Case: Adding Instance Attributes That Aren't Passed In
###########################################################

If your derived class requires additional instance data attributes whose values don't need
to be passed in when creating the new instance, then the proper approach is to implement the
``__post_init__()`` method. This method is established by the ``dataclasses`` machinery to
provide a hook where additional attributes can be specified but which won't be considered
as part of the set of fields for the dataclass.

As a simple example, suppose you wanted to add a local dict to your Pod subclass. You'd add
a ``__post_init__()`` method like the following:

.. code:: python

    from typing import Any
    from hikaru import register_version_kind_class
    from hikaru.model.rel_1_21 import *

    class DictPod(Pod):
        def __post_init__(self, client: Any = None):  # NOTE THE PARAMETERS!
            super(DictPod, self).__post_init__(client=client)  # NOTE CALL TO SUPER!
            self.my_dict = {}
            # and any other attributes you want to add

    register_version_kind_class(DictPod, Pod.apiVersion, Pod.kind)

The dataclass machinery ensures that ``__post_init__()`` is called after all work to set
up the instance is done in the generated ``__init__()`` method.

Two important aspects to note:

1. Every subclass of a :ref:`HikaruDocumentBase<HikaruDocumentBase doc>` subclass is passed
   a client object to the ``__post_init__()`` method. You must ensure that the signature on
   your method includes this argument, or there will be a runtime failure when trying to
   create an instance of your object. This is only required for HikaruDocumentBase subclasses;
   there's no argument passed into ``__post_init__()`` for HikaruBase subclasses.
2. Be sure to call ``super()`` passing this client object along to the parent class. Again,
   this is only for HikaruDocumentBase subclasses.

Use Case: Adding Instance Attributes That Are Passed In
########################################################

.. note::

    The next two use cases involve more direct use of Python dataclass features. If not familiar
    with them, the reader is advised to consult the Python documentation on the ``dataclasses``
    module to understand the constraints involved in dataclass use.

If you want additional instance attributes and want the caller to provide these to you, you can
use the special ``dataclasses`` field type ``InitVar`` to designate new fields that are only
part of the initialization process and are not stored as a dataclass field. This is the proper
way to add fields that must be passed in. The use of InitVar is important because, without it,
Hikaru will think that the additional field is part of the dataclass and that field will be
rendered in generated YAML, JSON, or Python dicts, which may prove to be a problem for the
consumer of these representations.

This is a bit more involved process, as it requires your new class to be made a dataclass, and
to provide suitable default values for the new fields. Hikaru will not be able to supply values
for these new fields as it won't know where to acquire the data, so you'll want to be sure they
have suitable defaults and also perhaps a means to mutate their value once the instance is 
created.

As an example, let's suppose we want a ``Pod`` subclass where we can optionally pass in several 
additional bits of information: two string values and a dict with some additional info. We
can create a new dataclass that makes provision for passing in this data like so:

.. code:: python

    from hikaru.model.rel_1_22 import *
    from dataclasses import dataclass, InitVar
    from typing import Any, Optional, Dict
    from hikaru import register_version_kind_class
    
    @dataclass
    class PodPlus(Pod):
        field1: InitVar[str] = 'wibble'  # defaults to 'wibble' if not provided
        field2: InitVar[Optional[Any]] = None
        my_dict: InitVar[Optional[Dict[str, str]]] = None
    
        def __post_init__(self, client: Any = None, field1=None, field2=None,
                          my_dict: InitVar[Dict[str, str]] = None):
            super(PodPlus, self).__post_init__(client=client)
            self.field1 = field1
            self.field2 = field2
            self.my_dict = my_dict if my_dict is not None else {}

    register_version_kind_class(PodPlus, Pod.apiVersion, Pod.kind)

Note that every field supplied either has a default or is optional with a default; this is because the parent
class already has a defaulted field and dataclasses that are subclasses can not have fields that don't have defaults
follow fields that do.

If you're familiar with dataclasses, you might wonder why the ``my_dict`` field doesn't use
a ``field()`` default specifier with a ``default_factory``. This is because ``default_factory``
can't be used with ``InitVar`` fields. This is why we create an empty dict in the 
``__post_init__()`` method instead of having the dataclass machinery do it for us.

Making a Class For a New Document Type
#######################################

Kubernetes provides a means to create your own controllers for common aggregations of basic
components, and also provides a means for objects known as 'operators' to be defined that allow
you to create YAML with new data and fields that those controllers can use. Using Hikaru
base classes and the class registration facility, you can get Hikaru to consume this YAML and
yield your own custom class instances, or model these operators directly in Python with the
same capabilities as existing Hikaru classes.

To create a class that supports a new YAML document type, you create a derived dataclass directly
from ``HikaruDocumentBase`` rather than one of its subclasses, and then provide it with all of
the fields required to hold the data for your operator. You **must** include ``apiVersion``
and ``kind`` fields in your class definition, but you do not need to implement a
``__post_init__()`` method unless you have other class attributes that you want to add that
aren't part of those that come from the official document definition.

As an example, let's suppose we have an operator that we want to define that will have a YAML
representation that looks like the following:

.. code:: yaml

    ---
    apiVersion: hikaru.v1
    kind: outer121
    metadata:
      name: custom-tester
      namespace: default
    inner:
      strField: gotta have it
      intField: 43
      optIntField: 121

Our outer object contains two other objects; one is a standard ``metadata`` object, and the other
has the key ``inner``, sort of like a ``spec`` object as in Pods or Deployments. You need to
model all objects that your aren't going to reuse from the existing set of Hikaru model objects.
Here is an example implementation of the classes that can consume this YAML:

.. code:: python

    from typing import Optional
    from dataclasses import dataclass
    from hikaru import HikaruBase, HikaruDocumentBase
    from hikaru.model.rel_1_21 import *

    @dataclass
    class Inner(HikaruBase):
        strField: str
        intField: int
        optStrField: Optional[str] = None
        optIntField: Optional[int] = None
    
    
    @dataclass
    class Outer(HikaruDocumentBase):
        apiVersion: str = 'hikaru.v1'
        kind: str = 'outer'
        metadata: Optional[ObjectMeta] = None
        inner: Optional[Inner] = None

    # we only register the subclass of HikaruDocumentBase
    register_version_kind_class(Outer, Outer.apiVersion, Outer.kind)

There are a few things to note here:

1. The ``Inner`` class is a subclass of ``HikaruBase``, not ``HikaruDocumentBase``. This is
   because it only appears as a component of a document class.
2. We can have fields without default values, but these must come before any fields with
   default values. Any fields that don't have a default value **must** be specified in the YAML
   and are treated as required parameters when creating such objects in Python.
3. We only register the top-level class, ``Outer``. It **must** have both ``apiVersion`` and
   ``kind`` attributes; if it doesn't, ``register_version_kind_class()`` will raise an
   exception.
4. We can mix existing Hikaru classes (here, ``ObjectMeta``) with our own custom classes.
5. As before, we can add methods or even ``__post_init__()`` implementations as described above.

.. note::

    A word on field names: Kubernetes YAML uses camel case for all field names in YAML objects,
    but uses PEP8 names within the Kubernetes Python client. In order to stay aligned with
    the YAML convention of camel case, Hikaru maintains camel case for the generated Python
    classes' field names, but will convert to PEP8 when needed. Conversion circumstances are
    sometimes subtle, and so to avoid the sudden appearance of a PEP8 name instead of camel
    case, it is best to always use camel case when defining your field names in custom
    classes such as the above.

Once registered, Hikaru will be able to create instances of the ``Outer`` class when parsing
YAML as in the example, and if asked to produce YAML from Python, it will generate appropriately
formatted YAML with the desired content. Processing with JSON and Python dicts will also
operate properly.

