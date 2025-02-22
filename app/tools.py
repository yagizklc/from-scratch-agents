from pydantic import BaseModel


class Tool(BaseModel):
    @classmethod
    def tool_schema(cls) -> str:
        """Format a single tool's information for the system message."""
        return f"Tool Schema: {cls.model_json_schema()}"

    # NOTE: implement this for your tool
    def use(self):
        pass


class Calculator(Tool):
    pass


class Search(Tool):
    pass


class Weather(Tool):
    pass


# register your tools here
AvailableTools: list[type[Tool]] = [Calculator, Search, Weather]
