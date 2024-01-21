from fashion_strategy.simulation.generalization_version_factory.decision_rule.decision_rule import DecisionRule
class HighDemandDecisionRule(DecisionRule):
    def evaluate(self, context, **kwargs):
        """
                Evaluate if a high-demand strategy is needed.

                :param context: A dictionary containing relevant data like current_stock.
                :param kwargs: Additional parameters.
                :return: Boolean indicating whether a high-demand strategy is required.
                """
        sku = context.get('sku')
        current_stock = context.get('current_stock')
        warehouse_stock = current_stock.get("VZ01", {}).get(sku, 0)
        num_stores = sum(sku in current_stock[store] for store in current_stock)
        return warehouse_stock < num_stores / 2
