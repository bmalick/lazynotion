class IconUrl:
    def __init__(self, name: str, color: str = "gray"):
        self.name = name
        self.color = color

    @property
    def data(self) -> str:
        return f"https://www.notion.so/icons/{self.name}_{self.color}.svg"
