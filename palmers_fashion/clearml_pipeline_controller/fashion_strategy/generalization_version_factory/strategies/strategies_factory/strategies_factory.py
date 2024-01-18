from simulation.generalization_version_factory.strategies.naive_bayes_strategy import NaiveBayesStrategy
from simulation.generalization_version_factory.strategies.high_demand_strategy import HighDemandStrategy
from simulation.generalization_version_factory.strategies.eoq_strategy import EoqStrategy
from simulation.generalization_version_factory.strategies.jit_strategy import JitStrategy


class StrategyFactory:
    # A dictionary mapping strategy types to their compatible strategy classes
    strategy_mapping = {
        'NaiveBayesStrategy': NaiveBayesStrategy,
        'HighDemandStrategy': HighDemandStrategy,
        'EoqStrategy': EoqStrategy,
        'JitStrategy': JitStrategy
    }

    @staticmethod
    def get_strategy(strategy_key, current_stock, AshlonStock, ActiveStores, dict_sales, accumulated_stocks, date, **kwargs):
        strategy_class = StrategyFactory.strategy_mapping.get(strategy_key)
        if strategy_class:
            return strategy_class(current_stock, AshlonStock, ActiveStores, dict_sales, accumulated_stocks, date, **kwargs)  # Instantiate the class before returning
        else:
            raise ValueError("Invalid strategy type")