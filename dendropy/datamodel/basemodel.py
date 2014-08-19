#! /usr/bin/env python

##############################################################################
##  DendroPy Phylogenetic Computing Library.
##
##  Copyright 2010-2014 Jeet Sukumaran and Mark T. Holder.
##  All rights reserved.
##
##  See "LICENSE.txt" for terms and conditions of usage.
##
##  If you use this work or any portion thereof in published work,
##  please cite it as:
##
##     Sukumaran, J. and M. T. Holder. 2010. DendroPy: a Python library
##     for phylogenetic computing. Bioinformatics 26: 1569-1571.
##
##############################################################################

"""
Infrastructure for phylogenetic data objects.
"""

import os
import copy
import sys
try:
    from StringIO import StringIO # Python 2 legacy support: StringIO in this module is the one needed (not io)
except ImportError:
    from io import StringIO # Python 3
if not (sys.version_info.major >= 3 and sys.version_info.minor >= 4):
    from dendropy.utility.filesys import pre_py34_open as open
from dendropy.utility import container
from dendropy.utility import bibtex
from dendropy.utility import text

##############################################################################
## DataObject

class DataObject(object):

    """
    Base class for all phylogenetic data objects.
    """

    def __init__(self, label=None):
        self._label = None
        if label is not None:
            self._set_label(label)

    def _get_label(self):
        return self._label
    def _set_label(self, v):
        # self._label = str(v) if v is not None else v
        self._label = v
    label = property(_get_label, _set_label)

    def clone(self, depth=0):
        """
        Creates and returns a copy of `self`.

        Parameters
        ----------
        depth : integer
            The depth of the copy:

                - 0: shallow-copy: All member objects are references,
                  except for :attr:`annotation_set` of top-level object and
                  member :class:`Annotation` objects: these are full,
                  independent instances (though any complex objects in the
                  `value` field of :class:`Annotation` objects are also
                  just references).
                - 1: taxon-namespace-scoped copy: All member objects are full
                  independent instances, *except* for :class:`TaxonNamespace`
                  and :class:`Taxon` instances: these are references.
                - 3: Exhaustive deep-copy: all objects are cloned.
        """
        if depth == 0:
            return copy.copy(self)
        elif depth == 1:
            return self.taxon_namespace_scoped_copy(memo=None)
        elif depth == 2:
            return copy.deepcopy(self)
        else:
            raise TypeError("Unsupported cloning depth: {}".format(depth))

    def taxon_namespace_scoped_copy(self, memo=None):
        """
        Cloning level: 1.
        Taxon-namespace-scoped copy: All member objects are full independent
        instances, *except* for :class:`TaxonNamespace` and :class:`Taxon`
        objects: these are preserved as references.
        """
        raise NotImplementedError

##############################################################################
## Readable

class Readable(object):
    """
    Mixin class which all classes that require deserialization should subclass.
    """

    def _parse_from_stream(cls, stream, schema, **kwargs):
        """
        Subclasses need to implement this method to create
        and return and instance of themselves read from the
        stream.
        """
        raise NotImplementedError
    _parse_from_stream = classmethod(_parse_from_stream)

    def get_from_stream(cls, src, schema, **kwargs):
        """
        Factory method to return new object of this class from file-like object
        `src`.

        Parameters
        ----------
        src : file or file-like
            Source of data.
        schema : string
            Specification of data format (e.g., "nexus").
        \*\*kwargs : keyword arguments, optional
            Arguments to customize parsing, instantiation, processing, and
            accession of objects read from the data source, including schema-
            or format-specific handling. These will be passed to the underlying
            schema-specific reader for handling.

        Returns
        -------
        pdo : phylogenetic data object
            New instance of object, constructed and populated from data given
            in source.
        """
        return cls._parse_from_stream(stream=src,
                schema=schema,
                **kwargs)
    get_from_stream = classmethod(get_from_stream)

    def get_from_path(cls, src, schema, **kwargs):
        """
        Factory method to return new object of this class from file
        specified by string `src`.

        Parameters
        ----------
        src : string
            Full file path to source of data.
        schema : string
            Specification of data format (e.g., "nexus").
        \*\*kwargs : keyword arguments, optional
            Arguments to customize parsing, instantiation, processing, and
            accession of objects read from the data source, including schema-
            or format-specific handling. These will be passed to the underlying
            schema-specific reader for handling.

        Returns
        -------
        pdo : phylogenetic data object
            New instance of object, constructed and populated from data given
            in source.
        """
        with open(src, "r", newline=None) as fsrc:
            return cls._parse_from_stream(stream=fsrc,
                    schema=schema,
                    **kwargs)
    get_from_path = classmethod(get_from_path)

    def get_from_string(cls, src, schema, **kwargs):
        """
        Factory method to return new object of this class from string `src`.

        Parameters
        ----------
        src : string
            Data as a string.
        schema : string
            Specification of data format (e.g., "nexus").
        \*\*kwargs : keyword arguments, optional
            Arguments to customize parsing, instantiation, processing, and
            accession of objects read from the data source, including schema-
            or format-specific handling. These will be passed to the underlying
            schema-specific reader for handling.

        Returns
        -------
        pdo : phylogenetic data object
            New instance of object, constructed and populated from data given
            in source.
        """
        ssrc = StringIO(src)
        return cls._parse_from_stream(stream=ssrc,
                schema=schema,
                **kwargs)
    get_from_string = classmethod(get_from_string)

    def get_from_url(cls, src, schema, strip_markup=False, **kwargs):
        """
        Factory method to return a new object of this class from
        URL given by `src`.

        Parameters
        ----------
        src : string
            URL of location providing source of data.
        schema : string
            Specification of data format (e.g., "nexus").
        \*\*kwargs : keyword arguments, optional
            Arguments to customize parsing, instantiation, processing, and
            accession of objects read from the data source, including schema-
            or format-specific handling. These will be passed to the underlying
            schema-specific reader for handling.

        Returns
        -------
        pdo : phylogenetic data object
            New instance of object, constructed and populated from data given
            in source.
        """
        text = read_url(src, strip_markup=strip_markup)
        ssrc = StringIO(text)
        try:
            return cls._parse_from_stream(stream=ssrc,
                    schema=schema,
                    **kwargs)
        except error.DataParseError:
            sys.stderr.write(text)
            raise
    get_from_url = classmethod(get_from_url)

    def _process_source_kwargs(self, **kwargs):
        """
        If `stream` is specified, then _process_source_kwargs:

            # checks that `schema` keyword argument is specified, and then
            # calls self.read()

        If `stream` is not specified, then nothing happens: unless the
        data object was populated through other means, and empty data
        object will the result (typically used as a starting point
        for population unit by unit).
        """
        if "stream" in kwargs:
            stream = kwargs["stream"]
            del(kwargs["stream"])
            schema = require_format_from_kwargs(kwargs)
            self.read(stream=stream, schema=schema, **kwargs)
        # else:
        #     from pudb import set_trace; set_trace()
        # elif "source_string" in kwargs:
        #     as_str = kwargs["source_string"]
        #     del(kwargs["source_string"])
        #     kwargs["stream"] = StringIO(as_str)
        #     return self._process_source_kwargs(**kwargs)
        # elif "source_file" in kwargs:
        #     fp = kwargs["source_filepath"]
        #     fo = open(os.path.expandvars(os.path.expanduser(filepath)), "rU")
        #     del(kwargs["source_filepath"])
        #     kwargs["stream"] = fo
        #     return self._process_source_kwargs(**kwargs)

    def read(self, stream, schema, **kwargs):
        """
        Populates/constructs objects of this type from `schema`-formatted
        data in the file-like object source `stream`.

        Parameters
        ----------
        stream : file or file-like
            Source of data.
        schema : string
            Specification of data format (e.g., "nexus").
        \*\*kwargs : keyword arguments, optional
            Arguments to customize parsing, instantiation, processing, and
            accession of objects read from the data source, including schema-
            or format-specific handling. These will be passed to the underlying
            schema-specific reader for handling.

        Returns
        -------
        n : `int` or :py:class:`tuple` [`int`]
            A value indicating size of data read, where "size" depends on
            the object:

                - :class:`Tree`: **undefined**
                - :class:`TreeList`: number of trees
                - :class:`CharacterMatrix`: number of sequences
                - :class:`DataSet`: :class:`tuple`(number of taxon namespaces, number of tree lists, number of matrices)

        """
        raise NotImplementedError

    def read_from_stream(self, fileobj, schema, **kwargs):
        """
        Reads from file (exactly equivalent to just `read()`, provided
        here as a separate method for completeness.

        Parameters
        ----------
        fileobj : file or file-like
            Source of data.
        schema : string
            Specification of data format (e.g., "nexus").
        \*\*kwargs : keyword arguments, optional
            Arguments to customize parsing, instantiation, processing, and
            accession of objects read from the data source, including schema-
            or format-specific handling. These will be passed to the underlying
            schema-specific reader for handling.

        Returns
        -------
        n : :py:class:`tuple` [integer]
            A value indicating size of data read, where "size" depends on
            the object:

                - :class:`Tree`: **undefined**
                - :class:`TreeList`: number of trees
                - :class:`CharacterMatrix`: number of sequences
                - :class:`DataSet`: :class:`tuple`(number of taxon namespaces, number of tree lists, number of matrices)
        """
        return self.read(stream=fileobj, schema=schema, **kwargs)

    def read_from_path(self, filepath, schema, **kwargs):
        """
        Reads data from file specified by `filepath`.

        Parameters
        ----------
        filepath : file or file-like
            Full file path to source of data.
        schema : string
            Specification of data format (e.g., "nexus").
        \*\*kwargs : keyword arguments, optional
            Arguments to customize parsing, instantiation, processing, and
            accession of objects read from the data source, including schema-
            or format-specific handling. These will be passed to the underlying
            schema-specific reader for handling.

        Returns
        -------
        n : :py:class:`tuple` [integer]
            A value indicating size of data read, where "size" depends on
            the object:

                - :class:`Tree`: **undefined**
                - :class:`TreeList`: number of trees
                - :class:`CharacterMatrix`: number of sequences
                - :class:`DataSet`: :class:`tuple`(number of taxon namespaces, number of tree lists, number of matrices)
        """
        with open(filepath, "r", newline=None) as fsrc:
            return self.read(stream=fsrc, schema=schema, **kwargs)

    def read_from_string(self, src_str, schema, **kwargs):
        """
        Reads a string.

        Parameters
        ----------
        src_str : string
            Data as a string.
        schema : string
            Specification of data format (e.g., "nexus").
        \*\*kwargs : keyword arguments, optional
            Arguments to customize parsing, instantiation, processing, and
            accession of objects read from the data source, including schema-
            or format-specific handling. These will be passed to the underlying
            schema-specific reader for handling.

        Returns
        -------
        n : :py:class:`tuple` [integer]
            A value indicating size of data read, where "size" depends on
            the object:

                - :class:`Tree`: **undefined**
                - :class:`TreeList`: number of trees
                - :class:`CharacterMatrix`: number of sequences
                - :class:`DataSet`: :class:`tuple`(number of taxon namespaces, number of tree lists, number of matrices)
        """
        s = StringIO(src_str)
        return self.read(stream=s, schema=schema, **kwargs)

    def read_from_url(self, url, schema, **kwargs):
        """
        Reads a URL source.

        Parameters
        ----------
        src : string
            URL of location providing source of data.
        schema : string
            Specification of data format (e.g., "nexus").
        \*\*kwargs : keyword arguments, optional
            Arguments to customize parsing, instantiation, processing, and
            accession of objects read from the data source, including schema-
            or format-specific handling. These will be passed to the underlying
            schema-specific reader for handling.

        Returns
        -------
        n : :py:class:`tuple` [integer]
            A value indicating size of data read, where "size" depends on
            the object:

                - :class:`Tree`: **undefined**
                - :class:`TreeList`: number of trees
                - :class:`CharacterMatrix`: number of sequences
                - :class:`DataSet`: :class:`tuple`(number of taxon namespaces, number of tree lists, number of matrices)
        """
        src_str = read_url(url)
        s = StringIO(src_str)
        return self.read(stream=s, schema=schema, **kwargs)

##############################################################################
## Writeable

class Writeable(object):
    """
    Mixin class which all classes that require serialization should subclass.
    """

    def write(self, stream, schema, **kwargs):
        """
        Writes the object to the file-like object `stream` in `schema`
        schema.
        """
        raise NotImplementedError

    def write_to_stream(self, dest, schema, **kwargs):
        """
        Writes to file-like object `dest`.
        """
        return self.write(stream=dest, schema=schema, **kwargs)

    def write_to_path(self, dest, schema, **kwargs):
        """
        Writes to file specified by `dest`.
        """
        with open(os.path.expandvars(os.path.expanduser(dest)), "w") as f:
            return self.write(stream=f, schema=schema, **kwargs)

    def as_string(self, schema, **kwargs):
        """
        Composes and returns string representation of the data.
        """
        s = StringIO()
        self.write(stream=s, schema=schema, **kwargs)
        return s.getvalue()

##############################################################################
## Annotable

class Annotable(object):
    """
    Mixin class which all classes that need to persist object attributes
    or other information as metadata should subclass.
    """

    def _get_annotations(self):
        if not hasattr(self, "_annotations"):
            self._annotations = AnnotationSet(self)
        return self._annotations
    def _set_annotations(self, annotations):
        if hasattr(self, "_annotations") \
                and annotations is self._annotations \
                and self._annotations.target is self:
            return
        if not isinstance(annotations, AnnotationSet):
            raise ValueError("Cannot set 'annotations' to object of type '{}'".format(type(annotations)))
        old_target = annotations.target
        self._annotations = annotations
        self._annotations.target = self
        for a in self._annotations:
            if a.is_attribute and a._value[0] is old_target:
                a.target = self
    annotations = property(_get_annotations, _set_annotations)

    def _has_annotations(self):
        return hasattr(self, "_annotations") and len(self._annotations) > 0
    has_annotations = property(_has_annotations)

    def copy_annotations_from(self,
            other,
            attribute_object_mapper=None):
        """
        Copies annotations from `other`, which must be of :class:`Annotable`
        type.

        Copies are deep-copies, in that the :class:`Annotation` objects added
        to the `annotation_set` :class:`AnnotationSet` collection of `self` are
        independent copies of those in the `annotate_set` collection of
        `other`. However, dynamic bound-attribute annotations retain references
        to the original objects as given in `other`, which may or may not be
        desirable. This is handled by updated the objects to which attributes
        are bound via mappings found in `attribute_object_mapper`.
        In dynamic bound-attribute annotations, the `_value` attribute of the
        annotations object (:attr:`Annotation._value`) is a tuple consisting of
        "`(obj, attr_name)`", which instructs the :class:`Annotation` object to
        return "`getattr(obj, attr_name)`" (via: "`getattr(*self._value)`")
        when returning the value of the Annotation. "`obj`" is typically the object
        to which the :class:`AnnotationSet` belongs (i.e., `self`). When a copy
        of :class:`Annotation` is created, the object reference given in the
        first element of the `_value` tuple of dynamic bound-attribute
        annotations are unchanged, unless the id of the object reference is fo

        Parameters
        ----------

        `other` : :class:`Annotable`
            Source of annotations to copy.

        `attribute_object_mapper` : dict
            Like the `memo` of `__deepcopy__`, maps object id's to objects. The
            purpose of this is to update the parent or owner objects of dynamic
            attribute annotations.
            If a dynamic attribute :class:`Annotation`
            gives object `x` as the parent or owner of the attribute (that is,
            the first element of the :attr:`Annotation._value` tuple is
            `other`) and `id(x)` is found in `attribute_object_mapper`,
            then in the copy the owner of the attribute is changed to
            `attribute_object_mapper[id(x)]`.
            If `attribute_object_mapper` is `None` (default), then the
            following mapping is automatically inserted: ``id(other): self``.
            That is, any references to `other` in any :class:`Annotation`
            object will be remapped to `self`.  If really no reattribution
            mappings are desired, then an empty dictionary should be passed
            instead.

        """
        if hasattr(other, "_annotations"):
            if attribute_object_mapper is None:
                attribute_object_mapper = {id(object):self}
            for a1 in other._annotations:
                a2 = a1.clone(attribute_object_mapper=attribute_object_mapper)
                if a2.is_attribute and a2._value[0] is other:
                    a2._value = (attribute_object_mapper.get(id(other), other), a2._value[1])
                self.annotations.add(a2)

    def deep_copy_annotations_from(self, other, memo=None):
        """
        Note that all references to `other` in any annotation value (and
        sub-annotation, and sub-sub-sub-annotation, etc.) will be
        replaced with references to `self`. This may not always make sense
        (i.e., a reference to a particular entity may be absolute regardless of
        context).
        """
        if hasattr(other, "_annotations"):
            # if not isinstance(self, other.__class__) or not isinstance(other, self.__class__):
            if type(self) is not type(other):
                raise TypeError("Cannot deep-copy annotations from different type (unable to assume object equivalence in dynamic or nested annotations)")
            if memo is None:
                memo = {}
            for a1 in other._annotations:
                a2 = copy.deepcopy(a1, memo=memo)
                memo[id(a1)] = a2
                if a2.is_attribute and a1._value[0] is other:
                    a2._value = (self, a1._value[1])
                self.annotations.add(a2)
            memo[id(other._annotations)] = self._annotations

    # def __copy__(self):
    #     o = self.__class__.__new__(self.__class__)
    #     for k in self.__dict__:
    #         if k == "_annotations":
    #             continue
    #         o.__dict__[k] = self.__dict__[k]
    #     o.copy_annotations_from(self)

    def __copy__(self, memo=None):
        """
        Cloning level: 0.
        :attr:`annotation_set` of top-level object and member :class:`Annotation`
        objects are full, independent instances. All other member objects (include
        objects referenced by dynamically-bound attribute values of
        :class:`Annotation` objects) are references.
        All member objects are references, except for
        """
        if memo is None:
            memo = {}
        other = self.__class__()
        memo[id(self)] = other
        for k in self.__dict__:
            if k == "_annotations":
                continue
            other.__dict__[k] = copy.copy(self.__dict__[k])
            memo[id(self.__dict__[k])] = other.__dict__[k]
        self.deep_copy_annotations_from(other, memo=memo)

    def __deepcopy__(self, memo=None):
        # ensure clone map
        if memo is None:
            memo = {}
        # get or create clone of self
        try:
            other = memo[id(self)]
        except KeyError:
            # create object without initialization
            # other = type(self).__new__(self.__class__)
            other = self.__class__.__new__(self.__class__)
            # store
            memo[id(self)] = other
        # copy other attributes first, skipping annotations
        for k in self.__dict__:
            if k == "_annotations":
                continue
            if k in other.__dict__:
                continue
            other.__dict__[k] = copy.deepcopy(self.__dict__[k], memo)
            memo[id(self.__dict__[k])] = other.__dict__[k]
            # assert id(self.__dict__[k]) in memo
        # create annotations
        other.deep_copy_annotations_from(self, memo)
        # return
        return other

##############################################################################
## Annotation

class Annotation(Annotable):
    """
    Metadata storage, composition and persistance, with the following attributes:

        * `name`
        * `value`
        * `datatype_hint`
        * `name_prefix`
        * `namespace`
        * `annotate_as_reference`
        * `is_hidden`

    """

    def __init__(self,
            name,
            value,
            datatype_hint=None,
            name_prefix=None,
            namespace=None,
            name_is_prefixed=False,
            is_attribute=False,
            annotate_as_reference=False,
            is_hidden=False,
            label=None,
            ):
        self._value = value
        self.is_attribute = is_attribute
        if name_is_prefixed:
            self.prefixed_name = name
            if name_prefix is not None:
                self._name_prefix = name_prefix
        else:
            self.name = name
            self._name_prefix = name_prefix
        self.datatype_hint = datatype_hint
        self._namespace = None
        self.namespace = namespace
        self.annotate_as_reference = annotate_as_reference
        self.is_hidden = is_hidden

    def __eq__(self, o):
        return self is o
        # if not isinstance(o, self.__class__):
        #     return False
        # if self._value != o._value:
        #     return False
        # if self.is_attribute != o.is_attribute:
        #     return False
        # if self.is_attribute and o.is_attribute:
        #     if getattr(*self._value) != getattr(*o._value):
        #         return False
        # # at this point, we have established that the values
        # # are equal
        # return (self.name == o.name
        #         and self._name_prefix == o._name_prefix
        #         and self.datatype_hint == o.datatype_hint
        #         and self._namespace == o._namespace
        #         and self.annotate_as_reference == o.annotate_as_reference
        #         and self.is_hidden == o.is_hidden
        #         and ( ((not hasattr(self, "_annotations")) and (not hasattr(o, "_annotations")))
        #             or (hasattr(self, "_annotations") and hasattr(o, "_annotations") and self._annotations == o._annotations)))

    def __hash__(self):
        return id(self)

    def __str__(self):
        return "{}='{}'".format(self.name, self.value)

    def __copy__(self):
        return self.clone()

    # def __deepcopy__(self, memo=None):
    #     if memo is None:
    #         memo = {}
    #     o = self.__class__.__new__(self.__class__)
    #     memo[id(self)] = o
    #     for k in self.__dict__:
    #         # if k not in o.__dict__: # do not add attributes already added by base class
    #         print("--->{}: {}".format(id(o), k))
    #         o.__dict__[k] = copy.deepcopy(self.__dict__[k], memo)
    #         memo[id(self.__dict__[k])] = o.__dict__[k]
    #     return o

    def clone(self, attribute_object_mapper=None):
        """
        Essentially a shallow-copy, except that any objects in the `_value`
        field with an `id` found in `attribute_object_mapper` will be replaced
        with `attribute_object_mapper[id]`.
        """
        o = self.__class__.__new__(self.__class__)
        if attribute_object_mapper is None:
            attribute_object_mapper = {id(self):o}
        if hasattr(self, "_annotations"):
            o.copy_annotations_from(self)
        for k in self.__dict__:
            if k == "_annotations":
                continue
            o.__dict__[k] = self.__dict__[k]
        return o

    def is_match(self, **kwargs):
        match = True
        for k, v in kwargs.items():
            if k == "name_prefix":
                if self.name_prefix != v:
                    return False
            elif k == "prefixed_name":
                if self.prefixed_name != v:
                    return False
            elif k == "namespace":
                if self.namespace != v:
                    return False
            elif k == "value":
                if self.value != v:
                    return False
            elif hasattr(self, k):
                if getattr(self, k) != v:
                    return False
        return True

    def _get_value(self):
        if self.is_attribute:
            return getattr(*self._value)
        else:
            return self._value
    def _set_value(self, value):
        self._value = value
    value = property(_get_value, _set_value)

    def _get_name_prefix(self):
        if self._name_prefix is None:
            self._name_prefix = "dendropy"
        return self._name_prefix
    def _set_name_prefix(self, prefix):
        self._name_prefix = prefix
    name_prefix = property(_get_name_prefix, _set_name_prefix)

    def _get_namespace(self):
        if self._namespace is None:
            self._namespace = "http://packages.python.org/DendroPy/"
        return self._namespace
    def _set_namespace(self, prefix):
        self._namespace = prefix
    namespace = property(_get_namespace, _set_namespace)

    def _get_prefixed_name(self):
        return "{}:{}".format(self.name_prefix, self.name)
    def _set_prefixed_name(self, prefixed_name):
        self._name_prefix, self.name = text.parse_curie_standard_qualified_name(prefixed_name)
    prefixed_name = property(_get_prefixed_name, _set_prefixed_name)

##############################################################################
## AnnotationSet

class AnnotationSet(container.OrderedSet):

    def __init__(self, target, *args):
        container.OrderedSet.__init__(self, *args)
        self.target = target

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (container.OrderedSet.__eq__(self, other))
                #and self.target is other.target) # we consider two
                # AnnotationSet objects equal even if their targets are
                # different; this is because (a) the target is convenience
                # artifact, so client code calls to `add_bound_attribute` do
                # not need to specify an owner, and (b) the target is not part
                # of the contents of the AnnotationSet

    def __str__(self):
        return "AnnotationSet([{}])".format(( ", ".join(str(a) for a in self)))

    def __deepcopy__(self, memo):
        try:
            o = self.__class__(target=memo[id(self.target)])
        except KeyError:
            raise KeyError("deepcopy error: object id {} not found: {}".format((id(self.target), repr(self.target))))
        memo[id(self)] = o
        for a in self:
            x = copy.deepcopy(a, memo)
            memo[id(a)] = x
            o.add(x)
        return o

    def add_new(self,
            name,
            value,
            datatype_hint=None,
            name_prefix=None,
            namespace=None,
            name_is_prefixed=False,
            is_attribute=False,
            annotate_as_reference=False,
            is_hidden=False):
        """
        Add an annotation.

        Parameters
        ----------
        name : string
            The property/subject/field of the annotation (e.g. "color",
            "locality", "dc:citation")
        value: string
            The content of the annotation.
        datatype_hint : string, optional
            Mainly for NeXML output (e.g. "xsd:string").
        namespace_prefix : string, optional
            Mainly for NeXML output (e.g. "dc:").
        namespace : string, optional
            Mainly for NeXML output (e.g. "http://www.w3.org/XML/1998/namespace").
        name_is_prefixed : string, optional
            Mainly for NeXML *input*: name will be split into prefix and local part
            before storage (e.g., "dc:citations" will result in prefix = "dc" and
            name="citations")
        is_attribute : boolean, optional
            If value is passed as a tuple of (object, "attribute_name") and this
            is True, then actual content will be the result of calling
            getattr(object, "attribute_name").
        annotate_as_reference : boolean, optional
            The value should be interpreted as a URI that points to content.
        is_hidden : boolean, optional
            Do not write or print this annotation when writing data.

        Returns
        -------
        annotation : :class:`Annotation`
            The new :class:`Annotation` created.
        """
        if not name_is_prefixed:
            if name_prefix is None and namespace is None:
                name_prefix = "dendropy"
                namespace = "http://packages.python.org/DendroPy/"
            elif name_prefix is None:
                raise TypeError("Cannot specify 'name_prefix' for unqualified name without specifying 'namespace'")
            elif namespace is None:
                raise TypeError("Cannot specify 'namespace' for unqualified name without specifying 'name_prefix'")
        else:
            if namespace is None:
                raise TypeError("Cannot specify qualified name without specifying 'namespace'")
        annote = Annotation(
                name=name,
                value=value,
                datatype_hint=datatype_hint,
                name_prefix=name_prefix,
                namespace=namespace,
                name_is_prefixed=name_is_prefixed,
                is_attribute=is_attribute,
                annotate_as_reference=annotate_as_reference,
                is_hidden=is_hidden,
                )
        return self.add(annote)

    def add_bound_attribute(self,
            attr_name,
            annotation_name=None,
            datatype_hint=None,
            name_prefix=None,
            namespace=None,
            name_is_prefixed=False,
            annotate_as_reference=False,
            is_hidden=False,
            owner_instance=None,
            ):
        """
        Add an attribute of an object as a dynamic annotation. The value of the
        annotation will be dynamically bound to the value of the attribute.

        Parameters
        ----------
        attr_name : string
            The (string) name of the attribute to be used as the source of the
            content or value of the annotation.
        annotation_name : string, optional
            Use this string as the annotation field/name rather than the attribute
            name.
        datatype_hint : string, optional
            Mainly for NeXML output (e.g. "xsd:string").
        namespace_prefix : string, optional
            Mainly for NeXML output (e.g. "dc:").
        namespace : string, optional
            Mainly for NeXML output (e.g. "http://www.w3.org/XML/1998/namespace").
        name_is_prefixed : string, optional
            Mainly for NeXML *input*: name will be split into prefix and local part
            before storage (e.g., "dc:citations" will result in prefix = "dc" and
            name="citations")
        annotate_as_reference : bool, optional
            The value should be interpreted as a URI that points to content.
        is_hidden : bool, optional
            Do not write or print this annotation when writing data.
        owner_instance : object, optional
            The object whose attribute is to be used as the value of the
            annotation. Defaults to `self.target`.

        Returns
        -------
        annotation : :class:`Annotation`
            The new :class:`Annotation` created.
        """
        if annotation_name is None:
            annotation_name = attr_name
        if owner_instance is None:
            owner_instance = self.target
        if not hasattr(owner_instance, attr_name):
            raise AttributeError(attr_name)
        if not name_is_prefixed:
            if name_prefix is None and namespace is None:
                name_prefix = "dendropy"
                namespace = "http://packages.python.org/DendroPy/"
            elif name_prefix is None:
                raise TypeError("Cannot specify 'name_prefix' for unqualified name without specifying 'namespace'")
            elif namespace is None:
                raise TypeError("Cannot specify 'namespace' for unqualified name without specifying 'name_prefix'")
        else:
            if namespace is None:
                raise TypeError("Cannot specify qualified name without specifying 'namespace'")
        annote = Annotation(
                name=annotation_name,
                value=(owner_instance, attr_name),
                datatype_hint=datatype_hint,
                name_prefix=name_prefix,
                namespace=namespace,
                name_is_prefixed=name_is_prefixed,
                is_attribute=True,
                annotate_as_reference=annotate_as_reference,
                is_hidden=is_hidden,
                )
        return self.add(annote)

    def add_citation(self,
            citation,
            read_as="bibtex",
            store_as="bibtex",
            name_prefix=None,
            namespace=None,
            is_hidden=False):
        """
        Add a citation as an annotation.

        Parameters
        ----------
        citation : string or dict or :class:`BibTexEntry`
            The citation to be added. If a string, then it must be a
            BibTex-formatted entry. If a dictionary, then it must have
            BibTex fields as keys and contents as values.
        read_as : string, optional
            Specifies the format/schema/structure of the citation. Currently
            only supports 'bibtex'.
        store_as : string, optional
            Specifies how to record the citation, with one of the
            following strings as values:

                "bibtex"
                    A set of annotations, where each BibTex field becomes a
                    separate annotation.
                "prism"
                    A set of of PRISM (Publishing Requirements for Industry
                    Standard Metadata) annotations.
                "dublin"
                    A set of of Dublic Core annotations.

            Defaults to "bibtex".
        name_prefix : string, optional
            Mainly for NeXML output (e.g. "dc:").
        namespace : string, optional
            Mainly for NeXML output (e.g. "http://www.w3.org/XML/1998/namespace").
        is_hidden : boolean, optional
            Do not write or print this annotation when writing data.

        Returns
        -------
        annotation : :class:`Annotation`
            The new :class:`Annotation` created.
        """
        if read_as == "bibtex":
            return self.add_bibtex(citation=citation,
                    store_as=store_as,
                    name_prefix=name_prefix,
                    namespace=namespace,
                    is_hidden=is_hidden)
        else:
            raise ValueError("Source format '{}' is not supported".format(read_as))

    def add_bibtex(self,
            citation,
            store_as="bibtex",
            name_prefix=None,
            namespace=None,
            is_hidden=False):
        """
        Add a citation as an annotation.

        Parameters
        ----------
        citation : string or dict or :class:`BibTexEntry`
            The citation to be added. If a string, then it must be a
            BibTex-formatted entry. If a dictionary, then it must have
            BibTex fields as keys and contents as values.
        store_as : string, optional
            Specifies how to record the citation, with one of the
            following strings as values:

                "bibtex"
                    A set of annotations, where each BibTex field becomes a
                    separate annotation.
                "prism"
                    A set of of PRISM (Publishing Requirements for Industry
                    Standard Metadata) annotations.
                "dublin"
                    A set of of Dublic Core annotations.

            Defaults to "bibtex".
        name_prefix : string, optional
            Mainly for NeXML output (e.g. "dc:").
        namespace : string, optional
            Mainly for NeXML output (e.g. "http://www.w3.org/XML/1998/namespace").
        is_hidden : boolean, optional
            Do not write or print this annotation when writing data.

        Returns
        -------
        annotation : :class:`Annotation`
            The new :class:`Annotation` created.
        """
        bt = bibtex.BibTexEntry(citation)
        bt_dict = bt.fields_as_dict()

        if name_prefix is None and namespace is not None:
            raise TypeError("Cannot specify 'name_prefix' for unqualified name without specifying 'namespace'")
        elif namespace is None and name_prefix is not None:
            raise TypeError("Cannot specify 'namespace' for unqualified name without specifying 'name_prefix'")

        if store_as.lower().startswith("bibtex"):
            if name_prefix is None and namespace is None:
                name_prefix = "bibtex"
                namespace = "http://www.edutella.org/bibtex#"
            self.add_new(
                    name="bibtype",
                    value=bt.bibtype,
                    datatype_hint="xsd:string",
                    name_prefix=name_prefix,
                    namespace=namespace,
                    name_is_prefixed=False,
                    is_attribute=False,
                    annotate_as_reference=False,
                    is_hidden=is_hidden)
            self.add_new(
                    name="citekey",
                    value=bt.citekey,
                    datatype_hint="xsd:string",
                    name_prefix=name_prefix,
                    namespace=namespace,
                    name_is_prefixed=False,
                    is_attribute=False,
                    annotate_as_reference=False,
                    is_hidden=is_hidden)
            for entry_key, entry_value in bt_dict.items():
                self.add_new(
                        name=entry_key,
                        value=entry_value,
                        datatype_hint="xsd:string",
                        name_prefix=name_prefix,
                        namespace=namespace,
                        name_is_prefixed=False,
                        is_attribute=False,
                        annotate_as_reference=False,
                        is_hidden=is_hidden)
        # elif store_as.lower().startswith("bibtex-record"):
        #     if name_prefix is None and namespace is None:
        #         name_prefix = "dendropy"
        #         namespace = "http://packages.python.org/DendroPy/"
        #     self.add_new(
        #             name="bibtex",
        #             value=bt.as_compact_bibtex(),
        #             datatype_hint="xsd:string",
        #             name_is_prefixed=False,
        #             name_prefix=name_prefix,
        #             namespace=namespace,
        #             is_attribute=False,
        #             annotate_as_reference=False,
        #             is_hidden=is_hidden)
        elif store_as.lower().startswith("prism"):
            prism_map = {
                    'volume': bt_dict.get('volume', None),
                    'publicationName':  bt_dict.get('journal', None),
                    'pageRange': bt_dict.get('pages', None),
                    'publicationDate': bt_dict.get('year', None),
                    }
            if name_prefix is None and namespace is None:
                name_prefix = "prism"
                namespace = "http://prismstandard.org/namespaces/1.2/basic/"
            for field, value in prism_map.items():
                if value is None:
                    continue
                self.add_new(
                        name=field,
                        value=value,
                        datatype_hint="xsd:string",
                        name_prefix=name_prefix,
                        namespace=namespace,
                        name_is_prefixed=False,
                        is_attribute=False,
                        annotate_as_reference=False,
                        is_hidden=is_hidden)
        elif store_as.lower().startswith("dublin"):
            dc_map = {
                    'title': bt_dict.get('title', None),
                    'creator':  bt_dict.get('author', None),
                    'publisher': bt_dict.get('journal', None),
                    'date': bt_dict.get('year', None),
                    }
            if name_prefix is None and namespace is None:
                name_prefix = "dc"
                namespace = "http://purl.org/dc/elements/1.1/"
            for field, value in dc_map.items():
                if value is None:
                    continue
                self.add_new(
                        name=field,
                        value=value,
                        datatype_hint="xsd:string",
                        name_is_prefixed=False,
                        name_prefix=name_prefix,
                        namespace=namespace,
                        is_attribute=False,
                        annotate_as_reference=False,
                        is_hidden=is_hidden)
        else:
            raise ValueError("Unrecognized composition specification: '{}'".format(store_as))

    def findall(self, **kwargs):
        """
        Returns AnnotationSet of Annotation objects associated with self.target
        that match based on *all* criteria specified in keyword arguments::

            >>> notes = tree.annotations.findall(name="color")
            >>> notes = tree.annotations.findall(namespace="http://packages.python.org/DendroPy/")
            >>> notes = tree.annotations.findall(namespace="http://packages.python.org/DendroPy/",
                                          name="color")
            >>> notes = tree.annotations.findall(name_prefix="dc")
            >>> notes = tree.annotations.findall(prefixed_name="dc:color")

        If no matches are found, the return AnnotationSet is empty.

        If no keyword arguments are given, *all* annotations are returned::

            >>> notes = tree.annotations.findall()

        Returns
        -------
        results : :class:`AnotationSet` or `None`
            :class:`AnnotationSet` containing :class:`Annotation` objects that
            match criteria, or `None` if no matching annotations found.
        """
        results = []
        for a in self:
            if a.is_match(**kwargs):
                results.append(a)
        results = AnnotationSet(self.target, results)
        return results

    def find(self, **kwargs):
        """
        Returns the *first* Annotation associated with self.target
        which matches based on *all* criteria specified in keyword arguments::

            >>> note = tree.annotations.find(name="color")
            >>> note = tree.annotations.find(name_prefix="dc", name="color")
            >>> note = tree.annotations.find(prefixed_name="dc:color")

        If no match is found, None is returned.

        If no keyword arguments are given, a TypeError is raised.

        Returns
        -------
        results : :class:`Anotation` or `None`
            First :class:`Annotation` object found that matches criteria, or
            `None` if no matching annotations found.
        """
        if "default" in kwargs:
            default = kwargs["default"]
            del kwargs["default"]
        else:
            default = None
        if not kwargs:
            raise TypeError("Search criteria not specified")
        for a in self:
            if a.is_match(**kwargs):
                return a
        return default

    def get_value(self, name, default=None):
        """
        Returns the *value* of the *first* Annotation associated with
        self.target which has `name` in the name field.

        If no match is found, then `default` is returned.

        Parameters
        ----------
        name : string
            Name of :class:`Annotation` object whose value is to be returned.

        default : any, optional
            Value to return if no matching :class:`Annotation` object found.

        Returns
        -------
        results : :class:`Annotation` or `None`
            `value` of first :class:`Annotation` object found that matches
            criteria, or `None` if no matching annotations found.
        """
        for a in self:
            if a.is_match(name=name):
                return a.value
        return default

    def drop(self, **kwargs):
        """
        Removes Annotation objects that match based on *all* criteria specified
        in keyword arguments.

        Remove all annotation objects with `name` ==
        "color"::

            >>> tree.annotations.drop(name="color")

        Remove all annotation objects with `namespace` ==
        "http://packages.python.org/DendroPy/"::

            >>> tree.annotations.drop(namespace="http://packages.python.org/DendroPy/")

        Remove all annotation objects with `namespace` ==
        "http://packages.python.org/DendroPy/" *and* `name` == "color"::

            >>> tree.annotations.drop(namespace="http://packages.python.org/DendroPy/",
                    name="color")

        Remove all annotation objects with `name_prefix` == "dc"::

            >>> tree.annotations.drop(name_prefix="dc")

        Remove all annotation objects with `prefixed_name` == "dc:color"::

            >>> tree.annotations.drop(prefixed_name="dc:color")

        If no keyword argument filter criteria are given, *all* annotations are
        removed::

            >>> tree.annotations.drop()

        Returns
        -------
        results : :class:`AnotationSet`
            :class:`AnnotationSet` containing :class:`Annotation` objects that
            were removed.
        """
        to_remove = []
        for a in self:
            if a.is_match(**kwargs):
                to_remove.append(a)
        for a in to_remove:
            self.remove(a)
        return AnnotationSet(self.target, to_remove)

    def values_as_dict(self, **kwargs):
        """
        Returns annotation set as a dictionary. The keys and values for the dictionary will
        be generated based on the following keyword arguments:

        Keyword Arguments
        -----------------
        key_attr : string
            String specifying an Annotation object attribute name to be used
            as keys for the dictionary.
        key_func : string
            Function that takes an Annotation object as an argument and returns
            the value to be used as a key for the dictionary.
        value_attr : string
            String specifying an Annotation object attribute name to be used
            as values for the dictionary.
        value_func : string
            Function that takes an Annotation object as an argument and returns
            the value to be used as a value for the dictionary.

        At most one of ``key_attr`` or ``key_func`` can be specified. If neither
        is specified, then by default the keys are generated from Annotation.name.
        At most one of ``value_attr`` or ``value_func`` can be specified. If neither
        is specified, then by default the values are generated from Annotation.value.
        Key collisions will result in the dictionary entry for that key being
        overwritten.

        Returns
        -------
        values : dict
        """
        if "key_attr" in kwargs and "key_func" in kwargs:
            raise TypeError("Cannot specify both 'key_attr' and 'key_func'")
        elif "key_attr" in kwargs:
            key_attr = kwargs["key_attr"]
            key_func = lambda a: getattr(a, key_attr)
        elif "key_func" in kwargs:
            key_func = kwargs["key_func"]
        else:
            key_func = lambda a: a.name
        if "value_attr" in kwargs and "value_func" in kwargs:
            raise TypeError("Cannot specify both 'value_attr' and 'value_func'")
        elif "value_attr" in kwargs:
            value_attr = kwargs["value_attr"]
            value_func = lambda a: getattr(a, value_attr)
        elif "value_func" in kwargs:
            value_func = kwargs["value_func"]
        else:
            value_func = lambda a: a.value
        d = {}
        for a in self:
            d[key_func(a)] = value_func(a)
        return d

