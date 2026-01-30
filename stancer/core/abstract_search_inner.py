from typing import Generator
from typing import Type
from typing import TypeVar

from stancer.core.abstract_object import AbstractObject
from stancer.core.abstract_search import AbstractSearch
from stancer.core.inner_search_object import InnerSearchObject

SearchedObject = TypeVar('SearchedObject', bound=AbstractObject)


class AbstractSearchInner(AbstractSearch):
    def list_inner(
        self,
        inner_search_object: InnerSearchObject,
        searched_class: Type[SearchedObject],
        **kwargs,
    ) -> Generator[SearchedObject, None, None]:
        """
        List searched_class elements, linked to our instance.

        Args:
            inner_search_object (InnerSearchObject):
              An instance of InnerSearchObject with a custom uri.

            searched_class (AbstractObject): The class that will be listed

            limit: must be an integer between 1 and 100 and will limit the number of
                objects to be returned.
            start: must be an integer, will be used as a pagination cursor,
                starts at 0.
            kwargs: Arbitrary keyword argument.

        Returns:
            Generator.
        """
        if issubclass(searched_class, AbstractSearch):
            params = searched_class.get_param(**kwargs)
            return self._create_generator(inner_search_object, searched_class, **params)
        return self._create_generator(inner_search_object, searched_class)
