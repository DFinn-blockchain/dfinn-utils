import pytest
import delayed_assert
from scripts.utils.chain_model import Chain
from tests.data.setting_data import get_substrate_chains

task_ids = [
    f'Test for {task.name}'
    for task in get_substrate_chains()
]


@pytest.mark.parametrize("chain", get_substrate_chains(), ids=task_ids)
class TestAssets:
    # workaround to differences between asset names at runtime and in our configuration
    asset_mapping = {
        'AUSD': 'KUSD'
    }
    # assets that has no working cases on network
    exclusions = {
        'Bifrost Kusama': {'DOT': ''},
        'Kintsugi': {'INTR': '', 'IBTC': '', 'DOT': ''}}

    def test_has_new_assets(self, chain: Chain):

        chain_assets = {asset['symbol'].upper(): '' for asset in chain.assets}
        chain_assets.update(self.asset_mapping)

        if chain.name in self.exclusions:
            chain_assets.update({ex_asset: '' for ex_asset in self.exclusions[chain.name]})
        chain.create_connection()
        chain.init_properties()
        symbols = chain.substrate.token_symbol if isinstance(chain.substrate.token_symbol, list) else [
            chain.properties.symbol]

        for symbol in symbols:
            delayed_assert.expect(symbol.upper() in chain_assets.keys() or symbol.upper() in chain_assets.values(),
                                  "new token to add: " + symbol)

        delayed_assert.assert_expectations()
