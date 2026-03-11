from typing import Dict, List, Tuple

class PageParent:
    def __init__(self, page_id: str):
        self.page_id = page_id
    
    @property
    def data(self) -> Dict:
        return {
            "parent": {
                "type": "page_id",
                "page_id": self.page_id
            }
        }

class DatabaseParent:
    def __init__(self, database_id: str):
        self.database_id = database_id
    
    @property
    def data(self):
        return {
            "parent": {"database_id": self.database_id}
        }

class Cover:
    def __init__(self, url: str = None):
        self.url = url

    @property
    def data(self) -> Dict:
        if self.url is not None:
            return {
                "cover": {
                    "external": {"url": self.url}
                }
            }
        return {}

class Icon:
    def __init__(self, emoji: str = None, url: str = None):
        # assert emoji is None or url is None, "Set emoji or url, only one."
        self.emoji = emoji
        self.url = url

    @property
    def data(self) -> Dict:
        if self.emoji is not None:
            return {"icon": {"emoji": self.emoji}}
        elif self.url is not None:
            return {
                "icon": {
                    "external": {"url": self.url}
                }
            }
        return {}

class PageTitle:
    def __init__(self, title: str):
        self._title = title

    @property
    def data(self) -> List[Dict]:
        return [
            {
                "type": "text",
                "text": {
                    "content": self._title,
                    "link": None,
                }
            }
        ]

class DataProperty:
    def __init__(self, name: str, **kwargs):
        self.name = name

    @property
    def init_data(self) -> Dict: pass

    def update(self) -> None:
        pass

    @property
    def data(self) -> Dict:
        pass

class Text(DataProperty):
    def __init__(self, name: str, text: str= None):
        super().__init__(name=name)
        self._text = text

    @property
    def init_data(self) -> Dict:
        return {self.name: {"rich_text": {}}}

    def update(self, text: str) -> None:
        self._text = text

    @property
    def data(self) -> Dict:
        return {self.name: {"rich_text": [{"type": "text", "text": {"content": self._text}}]}}

class Number(DataProperty):
    def __init__(self, name: str, number: int = None, number_format: str = "number"):
        super().__init__(name=name)
        self._number = number
        self._number_format = number_format

    @property
    def init_data(self) -> Dict:
        return {self.name: {"number": {"format": self._number_format}}}
    
    def update(self, number: int) -> None:
        self._number = number

    @property
    def data(self) -> Dict:
        return {self.name: {"number": self._number}}

class Select(DataProperty):
    _prop_name = "select"
    def __init__(self, name: str, init_options: List[Tuple[str,str]] = [], options: List=None):
        super().__init__(name=name)
        self.init_options = init_options
        self._options = options

    @property
    def init_data(self) -> Dict:
        return {self.name: {self._prop_name: {"options": [{"name": n, "color": c} for n,c in self.init_options]}}}

    def update(self, options: List[str]) -> None:
        self._options = options

    @property
    def data(self) -> Dict:
        return {self.name: {self._prop_name: {"name": self._options}}}
#
class Status(Select):
    _prop_name = "status"
    def __init__(self, name: str, init_options: List[Tuple[str,str]] = [], options: List=None):
        super().__init__(name=name, init_options=init_options, options=options)

class MultiSelect(Select):
    _prop_name = "multi_select"
    def __init__(self, name: str, init_options: List[Tuple[str,str]] = [], options: List=None):
        super().__init__(name=name, init_options=init_options, options=options)

class Date(DataProperty):
    def __init__(self, name: str, start: str = None, end: str = None):
        super().__init__(name=name)
        self._start = start
        self._end = end

    @property
    def init_data(self) -> Dict:
        return {self.name: {"date": {}}}

    def update(self, start: str, end: str = None):
        self._start = start
        self._end = end

    @property
    def data(self) -> Dict:
        return {self.name: {"date": {"start": self._start, "end": self._end}}}


class People(DataProperty):
    def __init__(self, name: str, people: str = None):
        super().__init__(name=name)
        self._people = people

    @property
    def init_data(self) -> Dict:
        return {self.name: {"people": {}}}

    def update(self, people: str) -> None:
        self._people = people

    # TODO
    @property
    def data(self) -> Dict:
        pass

class File(DataProperty):
    def __init__(self, name: str, file: str = None):
        super().__init__(name=name)
        self._file = file

    @property
    def init_data(self) -> Dict:
        return {self.name: {"file": {}}}

    def update(self, file: str) -> None:
        self._file = file

    # TODO
    @property
    def data(self) -> Dict:
        pass

class Checkbox(DataProperty):
    def __init__(self, name: str, checked: bool = False):
        super().__init__(name=name)
        self._checked = checked

    @property
    def init_data(self) -> Dict:
        return {self.name: {"checkbox": {}}}

    def update(self ,checked: bool) -> None:
        self._checked = checked

    # TODO
    @property
    def data(self) -> Dict:
        pass

class Url(DataProperty):
    def __init__(self, name: str, url: str = {}):
        super().__init__(name=name)
        self._url = url

    @property
    def init_data(self) -> Dict:
        return {self.name: {"url": {}}}

    def update(self, url: str) -> None:
        self._url = url

    @property
    def data(self) -> Dict:
        return {self.name: {"url": self._url}}

class Email(DataProperty):
    def __init__(self, name: str, email: str = None):
        super().__init__(name=name)
        self._email = email

    @property
    def init_data(self) -> Dict:
        return {self.name: {"email": {}}}

    def update(self, email: str) -> None:
        self._email = email

    # TODO
    @property
    def data(self) -> Dict:
        pass

class Phonenumber(DataProperty):
    def __init__(self, name: str, phone_number: str = None):
        super().__init__(name=name)
        self._phone_number = phone_number

    @property
    def init_data(self) -> Dict:
        return {self.name: {"phone_number": {}}}

    def update(self, phone_number: str) -> None:
        self._phone_number = phone_number

    # TODO
    @property
    def data(self) -> Dict:
        pass

class Formula(DataProperty):
    def __init__(self, name: str, formula: str = None):
        super().__init__(name=name)
        self._formula = formula

    @property
    def init_data(self) -> Dict:
        if self._formula is None:
            return {self.name: {"formula": {}}}
        return {self.name: {"formula": {"expression": self._formula}}}

    def update(self, formula: str) -> None:
        self._formula = formula

    @property
    def data(self) -> Dict:
        return {self.name: {"formula": {"expression": self._formula}}}

class Relation(DataProperty):
    def __init__(self, name: str, related_db_id: str, relation_ids: List[str] = [], dual_prop: bool = True):
        super().__init__(name=name)
        self.related_db_id = related_db_id
        self._relation = [{"id": i} for i in relation_ids]
        self.dual_prop = dual_prop

    @property
    def init_data(self) -> Dict:
        if self.dual_prop:
            return {self.name: {"relation": {"database_id": self.related_db_id, "dual_property": {}}}}
        return {self.name: {"relation": {"database_id": self.related_db_id, "single_property": {}}}}

    def update(self, ids: List[str]) -> None:
        self._relation = [{"id": i} for i in ids]

    @property
    def data(self) -> Dict:
        return {self.name: {"relation": self._relation}}

class Rollup(DataProperty):
    def __init__(self, name: str, rollup_property_name: str, relation_property_name: str, function: str):
        super().__init__(name=name)
        self._rollup_property_name = rollup_property_name
        self._relation_property_name = relation_property_name
        self._function = function

    @property
    def init_data(self) -> Dict:
        return {self.name: {"rollup": {
            "rollup_property_name": self._rollup_property_name,
            "relation_property_name": self._relation_property_name,
            "function": self._function,
        }}}

    def update(self, rollup_property_name: str, relation_property_name: str, function: str) -> None:
        self._rollup_property_name = rollup_property_name
        self._relation_property_name = relation_property_name
        self._function = function

    @property
    def data(self):
        return

class Createdtime(DataProperty):
    def __init__(self, name: str):
        super().__init__(name=name)

    @property
    def init_data(self) -> Dict:
        return {self.name: {"created_time": {}}}

    def update(self) -> None:
        return

    @property
    def data(self) -> Dict:
        return

class LastEditedtime(DataProperty):
    def __init__(self, name: str):
        super().__init__(name=name)

    @property
    def init_data(self) -> Dict:
        return {self.name: {"last_edited_time": {}}}

    def update(self) -> None:
        return

    @property
    def data(self):
        return

class Rename(DataProperty):
    def __init__(self, name: str, new_name: str):
        super().__init__(name=name)
        self.new_name = new_name

    @property
    def data(self) -> Dict:
        return {self.name: {"name": self.new_name}}

