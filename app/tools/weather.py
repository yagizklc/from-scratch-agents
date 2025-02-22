from app.lib import Tool


class Weather(Tool):
    def use(self, location: str) -> str:
        locations = {
            "london": "cloudy and rainy, 15°C",
            "paris": "partly cloudy, 18°C",
            "istanbul": "sunny and clear, 22°C",
            "new york": "scattered showers, 17°C",
            "tokyo": "clear skies, 21°C",
        }

        location = location.lower()
        if location not in locations:
            return (
                "Location not found in database. Weather information is not available."
            )

        return f"The weather in {location.title()} is {locations[location]}."
