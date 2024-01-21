from fashion_strategy.simulation.generalization_version_factory.decision_rule.high_demand_decision_rule import HighDemandDecisionRule
class StrategySelector:
    def __init__(self, original_strategy_class, high_demand_strategy_class,decision_rule=None, **strategy_specific_args):
        self.original_strategy_class = original_strategy_class
        self.high_demand_strategy_class = high_demand_strategy_class
        self.strategy_specific_args = strategy_specific_args
        self.decision_rule = decision_rule if decision_rule else HighDemandDecisionRule()

    def select_strategy(self, sku, current_stock):
        context = {'sku': sku, 'current_stock': current_stock}
        need_high_demand_strategy = self.decision_rule.evaluate(context, **self.strategy_specific_args)
        if not need_high_demand_strategy:
            return self.original_strategy_class, self.strategy_specific_args
        if need_high_demand_strategy:
            high_demand_strategy_args = self.strategy_specific_args.copy()
            high_demand_strategy_args['need_high_demand_strategy'] = need_high_demand_strategy
            high_demand_strategy_args['skus_simulation'] = [sku]
            return self.high_demand_strategy_class, high_demand_strategy_args
