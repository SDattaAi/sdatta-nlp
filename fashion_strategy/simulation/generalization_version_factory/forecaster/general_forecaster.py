from abc import ABC, abstractmethod
class ForecastingStrategy(ABC):
    @abstractmethod
    def forecast(self, *args, **kwargs):
        pass