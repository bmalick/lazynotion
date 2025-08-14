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
        self.title = title

    @property
    def data(self) -> List[Dict]:
        return [
            {
                "type": "text",
                "text": {
                    "content": self.title,
                    "link": None,
                }
            }
        ]

class DataProperty:
    def __init__(self, name: str):
        self.name = name

    @property
    def init_data(self) -> Dict: pass

    def update(self) -> None:
        pass

    @property
    def data(self) -> Dict:
        pass

class PropertyText(DataProperty):
    def __init__(self, name: str):
        super().__init__(name=name)

    @property
    def init_data(self) -> Dict:
        return {self.name: {"rich_text": {}}}

    # TODO
    def update(self, text: str) -> None:
        pass

    @property
    def data(self) -> Dict:
        pass

class PropertyNumber(DataProperty):
    def __init__(self, name: str):
        super().__init__(name=name)
        self._number = None

    @property
    def init_data(self) -> Dict:
        return {self.name: {"number": {}}}
    
    def update(self, number: int) -> None:
        self._number = number

    @property
    def data(self) -> Dict:
        return {self.name: {"number": self._number}}

class PropertySelect(DataProperty):
    def __init__(self, name: str, options: List[Tuple[str,str]] = []):
        super().__init__(name=name)
        self.options = options
        self._option = None

    @property
    def init_data(self) -> Dict:
        return {self.name: {"select": {"options": [{"name": n, "color": c} for n,c in self.options]}}}

    # TODO
    def update(self, option: str) -> None:
        self._option = option

    @property
    def data(self) -> Dict:
        return {self.name: {"select": {"name": self._option}}}

class PropertyMultiSelect(DataProperty):
    def __init__(self, name: str, options: List[Tuple[str,str]] = []):
        super().__init__(name=name)
        self.options = options

    @property
    def init_data(self) -> Dict:
        return {self.name: {"multi_select": {"options": [{"name": n, "color": c} for n,c in self.options]}}}

    # TODO
    def update(self) -> None:
        pass

    @property
    def data(self) -> Dict:
        pass

class PropertyDate(DataProperty):
    def __init__(self, name: str):
        super().__init__(name=name)
        self._start = None
        self._end = None

    @property
    def init_data(self) -> Dict:
        return {self.name: {"date": {}}}

    def update(self, start: str, end: str = None):
        self._start = start
        self._end = end

    @property
    def data(self) -> Dict:
        return {self.name: {"date": {"start": self._start, "end": self._end}}}


class PropertyPeople(DataProperty):
    def __init__(self, name: str):
        super().__init__(name=name)

    @property
    def init_data(self) -> Dict:
        return {self.name: {"people": {}}}

    # TODO
    def update(self) -> None:
        pass

    @property
    def data(self) -> Dict:
        pass

class PropertyFile(DataProperty):
    def __init__(self, name: str):
        super().__init__(name=name)

    @property
    def init_data(self) -> Dict:
        return {self.name: {"file": {}}}

    # TODO
    def update(self) -> None:
        pass

    @property
    def data(self) -> Dict:
        pass

class PropertyCheckbox(DataProperty):
    def __init__(self, name: str):
        super().__init__(name=name)

    @property
    def init_data(self) -> Dict:
        return {self.name: {"checkbox": {}}}

    # TODO
    def update(self) -> None:
        pass

    @property
    def data(self) -> Dict:
        pass

class PropertyUrl(DataProperty):
    def __init__(self, name: str):
        super().__init__(name=name)

    @property
    def init_data(self) -> Dict:
        return {self.name: {"url": {}}}

    # TODO
    def update(self) -> None:
        pass

    @property
    def data(self) -> Dict:
        pass

class PropertyEmail(DataProperty):
    def __init__(self, name: str):
        super().__init__(name=name)

    @property
    def init_data(self) -> Dict:
        return {self.name: {"email": {}}}

    # TODO
    def update(self) -> None:
        pass

    @property
    def data(self) -> Dict:
        pass

class PropertyPhonenumber(DataProperty):
    def __init__(self, name: str):
        super().__init__(name=name)

    @property
    def init_data(self) -> Dict:
        return {self.name: {"phone_number": {}}}

    # TODO
    def update(self) -> None:
        pass

    @property
    def data(self) -> Dict:
        pass

class PropertyFormula(DataProperty):
    def __init__(self, name: str):
        super().__init__(name=name)

    @property
    def init_data(self) -> Dict:
        return {self.name: {"formula": {}}}

    # TODO
    def update(self) -> None:
        pass

    @property
    def data(self) -> Dict:
        pass

class PropertyRelation(DataProperty):
    def __init__(self, name: str, related_db_id: str, relation_ids: List[str] = []):
        super().__init__(name=name)
        self.related_db_id = related_db_id
        self._relation = [{"id": i} for i in relation_ids]

    @property
    def init_data(self) -> Dict:
        # return {self.name: {"relation": {"database_id": self.related_db_id, "single_property": {}}}}
        return {self.name: {"relation": {"database_id": self.related_db_id, "dual_property": {}}}}

    def update(self, ids: List[str]) -> None:
        self._relation = [{"id": i} for i in ids]

    @property
    def data(self) -> Dict:
        return {self.name: {"relation": self._relation}}

class PropertyRollup(DataProperty):
    def __init__(self, name: str, rollup_property_name: str, relation_property_name: str, function: str):
        super().__init__(name=name)
        self.rollup_property_name = rollup_property_name
        self.relation_property_name = relation_property_name
        self.function = function

    @property
    def init_data(self) -> Dict:
        return {self.name: {"rollup": {
            "rollup_property_name": self.rollup_property_name,
            "relation_property_name": self.relation_property_name,
            "function": self.function,
        }}}

    # TODO
    def update(self) -> None:
        pass

    @property
    def data(self) -> Dict:
        pass

class PropertyCreatedtime(DataProperty):
    def __init__(self, name: str):
        super().__init__(name=name)

    @property
    def init_data(self) -> Dict:
        return {self.name: {"created_time": {}}}

    # TODO
    def update(self) -> None:
        pass

    @property
    def data(self) -> Dict:
        pass

class PropertyLastEditedtime(DataProperty):
    def __init__(self, name: str):
        super().__init__(name=name)

    @property
    def init_data(self) -> Dict:
        return {self.name: {"last_edited_time": {}}}

    # TODO
    def update(self) -> None:
        pass

    @property
    def data(self) -> Dict:
        pass

class RenameProperty(DataProperty):
    def __init__(self, current_name: str, new_name: str):
        self.current_name = current_name
        self.new_name = new_name

    @property
    def data(self) -> Dict:
        return {self.current_name: {"name": self.new_name}}

