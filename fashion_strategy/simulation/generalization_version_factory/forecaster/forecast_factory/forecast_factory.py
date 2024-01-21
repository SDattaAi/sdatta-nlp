from fashion_strategy.simulation.generalization_version_factory.forecaster.naive_bayes_forecaster import NaiveBayesForecasting
from fashion_strategy.simulation.generalization_version_factory.forecaster.high_demand_forecaster import HighDemandForecasting
from fashion_strategy.simulation.generalization_version_factory.forecaster.eoq_forecaster import EOQForecasting
from fashion_strategy.simulation.generalization_version_factory.forecaster.jit_forecaster import JITForecasting


class ForecastFactory:
    forecast_mapping = {
        'NaiveBayesForecasting': NaiveBayesForecasting,
        'HighDemandForecasting': HighDemandForecasting,
        'EOQForecasting': EOQForecasting,
        'JITForecasting': JITForecasting
    }

    @staticmethod
    def get_forecast(forecast_type, **kwargs):
        forecast_class = ForecastFactory.forecast_mapping.get(forecast_type)
        if forecast_class:
            return forecast_class(**kwargs)  # Instantiate the class before returning
        else:
            raise ValueError("Invalid forecast type")