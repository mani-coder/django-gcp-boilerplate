# Standard Library Imports
from collections import OrderedDict
from operator import attrgetter

# Third Party Library Imports
from six import with_metaclass


class EnumValue(object):
    """
    Class which is used as the value of the Enum.

    Potentially this can be extended and used as child classes can be created based on needs.
    """

    # Used for sorting the enums.
    counter = 0

    def __init__(self, value, verbose_name):
        self.value = value
        self.verbose_name = verbose_name
        EnumValue.counter += 1
        self._counter = EnumValue.counter


class EnumMeta(type):
    """
    Meta class for our Enum class.
    """

    def __init__(cls, name, bases, attrs):
        enum_values = {}  # will contain ENUM_NAME: (value, verbose_name)
        seen_values = set()
        for attr in attrs:
            enum_value = attrs[attr]
            if not isinstance(enum_value, EnumValue):
                # Simply ignore anything that is not an EnumValue instance
                continue

            if enum_value.value in seen_values:
                raise Exception(
                    "Multiple enum fields found with the value {} for enum {}. Check the enum definition again!".format(
                        enum_value.value, name
                    )
                )

            seen_values.add(enum_value.value)

            # store the attr-name in the enum for future reference.
            enum_value.__name__ = attr

            enum_values[attr] = enum_value
            setattr(cls, attr, enum_value.value)
        #
        # Enum models can be sub-class'd and so collect the enum values from the parent Enums and copy it over to
        # to the child class (i.e., the real Enum class for which we are doing this initialization.).
        #
        for base in bases:
            if cls.__name__ != "Enum" and base != Enum and issubclass(base, Enum):
                for attr, enum_value in base._enum_values.items():
                    setattr(cls, attr, enum_value.value)
                enum_values.update(base._enum_values)

        # Map of enum.__name__ to the EnumValue
        cls._enum_values = OrderedDict(
            ((enum.__name__, enum) for enum in sorted(enum_values.values(), key=attrgetter("_counter")))
        )

        # Map of value to the EnumValue
        cls._enum_value_by_value = OrderedDict(
            ((enum.value, enum) for enum in sorted(enum_values.values(), key=attrgetter("_counter")))
        )
        cls._values = list(map(attrgetter("value"), cls._enum_values.values()))

    def __iter__(self):
        for enum_value in self._enum_values.values():
            yield enum_value.value


class Enum(with_metaclass(EnumMeta, object)):
    """
    Enum class for defining the Enums.

    Usage:
        class TestEnum(Enum):
            A = EnumValue('a', 'verbose name a')
            B = EnumValue('b', 'verbose name b')
            C = EnumValue('c', 'verbose name c')

        TestEnum.A == 'a' # True
        TestEnum.values()
            returns ['a', 'b', 'c']

        TestEnum.validate_value("random") - raises ValueError
        TestEnum.validate_value(TestChoices.CHOICE1) - returns fine.
        TestEnum.verbose_name(TestChoices.CHOICE1)
            returns "verbose name a"

        TestEnum.verbose_name(TestChoices.CHOICE1)
            returns EnumValue('a', 'verbose name a')

        TestEnum.choices()
            return [('a', 'verbose name a'), ('b', 'verbose name b'), ('c', 'verbose name c')]

    IMPORTANT: only fields with an instance of EnumValue as their value are picked up.

    Sample: app.utils.tests.test_enums.SampleEnum
    """

    @classmethod
    def enum_values_it(cls):
        return cls._enum_values.values()

    @classmethod
    def values(cls):
        """
        Return list of all raw values in the string.

        :return: List of raw values.
        """
        return cls._values

    @classmethod
    def validate_value(cls, value):
        """
        Validate that the specified value is a valid Enum Value.

        :raise ValueError: If the value isn't valid one.
        """
        if value not in cls.values():
            raise ValueError("{} isn't a valid enum value for {} Enum.".format(value, cls.__name__))

    @classmethod
    def verbose_name(cls, value):
        """
        Return the verbose name for the given value. The value should be a valid value of the Enum.

        :param value: The raw enum value.
        :return: Verbose name.
        """
        return cls.enum_value(value).verbose_name

    @classmethod
    def enum_value(cls, value) -> EnumValue:
        """
        Returns the instance of EnumValue specified in the Enum.

        :param value: The raw enum value.
        :return: Instance of EnumValue used in the Enum.
        """
        cls.validate_value(value)
        return cls._enum_value_by_value[value]

    @classmethod
    def enum_name(cls, value):
        """
        Returns the name of the enum as defined in the Enum class.

        :param value: Enum original value.
        :return: Enum's string name.
        """
        cls.validate_value(value)
        return cls.enum_value(value).__name__

    @classmethod
    def choices(cls):
        """
        Return a list of tuples containing (name, verbose_name).

        :return: List of tuple(name, verbose_name).
        """
        return list(map(attrgetter("value", "verbose_name"), cls._enum_values.values()))
