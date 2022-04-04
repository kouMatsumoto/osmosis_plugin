import json

from senkalib.chain.osmosis.osmosis_transaction import OsmosisTransaction

from osmosis_plugin.osmosis_plugin import OsmosisPlugin


class TestOsmosisPlugin:
    token_original_ids = None

    def test_can_handle_ibc_received(self):
        test_data = TestOsmosisPlugin._get_test_data("ibc_received_effect1")
        transaction = OsmosisTransaction(test_data)
        chain_type = OsmosisPlugin.can_handle(transaction)
        assert chain_type

    def test_can_handle_cosmos_transfer(self):
        test_data = TestOsmosisPlugin._get_test_data("cosmos_transfer")
        transaction = OsmosisTransaction(test_data)
        chain_type = OsmosisPlugin.can_handle(transaction)
        assert chain_type is False

    def test_get_caajs_fee_not_zero(self):
        test_data = TestOsmosisPlugin._get_test_data("ibc_transfer")
        transaction = OsmosisTransaction(test_data)
        caajs = OsmosisPlugin.get_caajs(
            "osmo14ls9rcxxd5gqwshj85dae74tcp3umypp786h3m",
            transaction,
        )
        assert caajs[1].executed_at == "2022-02-08 01:43:31"
        assert caajs[1].chain == "osmosis"
        assert caajs[1].platform == "osmosis"
        assert caajs[1].application == "osmosis"
        assert (
            caajs[1].transaction_id
            == "AD666E0F5FB2D7DEF4B09E7BC31AF4BECB49EF76E948C4445AFF77EFFB4DEC6B"
        )
        assert caajs[1].type == "lose"
        assert caajs[1].amount == "0.01"
        assert caajs[1].token_symbol == "osmo"
        assert caajs[1].token_original_id is None
        assert caajs[1].caaj_from == "osmo14ls9rcxxd5gqwshj85dae74tcp3umypp786h3m"
        assert caajs[1].caaj_to == "fee"
        assert caajs[1].comment == ""

    def test_get_caajs_fee_zero(self):
        test_data = TestOsmosisPlugin._get_test_data("swap")
        transaction = OsmosisTransaction(test_data)
        caajs = OsmosisPlugin.get_caajs(
            "osmo14ls9rcxxd5gqwshj85dae74tcp3umypp786h3m",
            transaction,
        )
        assert len(caajs) == 2

    def test_get_caajs_swap_get(self):
        test_data = TestOsmosisPlugin._get_test_data("swap")
        transaction = OsmosisTransaction(test_data)
        caajs = OsmosisPlugin.get_caajs(
            "osmo14ls9rcxxd5gqwshj85dae74tcp3umypp786h3m",
            transaction,
        )

        assert caajs[0].executed_at == "2022-01-21 02:47:05"
        assert caajs[0].chain == "osmosis"
        assert caajs[0].platform == "osmosis"
        assert caajs[0].application == "swap"
        assert (
            caajs[0].transaction_id
            == "97A5C4A33FA36397A342D34D576AC07BA3F5CB5B7274E2BAF7092470A681FDEB"
        )
        assert caajs[0].type == "lose"
        assert caajs[0].amount == "0.01"
        assert caajs[0].token_symbol == "osmo"
        assert caajs[0].token_original_id is None
        assert caajs[0].caaj_from == "osmo14ls9rcxxd5gqwshj85dae74tcp3umypp786h3m"
        assert (
            caajs[0].caaj_to
            == "osmo1h7yfu7x4qsv2urnkl4kzydgxegdfyjdry5ee4xzj98jwz0uh07rqdkmprr"
        )
        assert caajs[0].comment == ""

        assert caajs[1].executed_at == "2022-01-21 02:47:05"
        assert caajs[1].chain == "osmosis"
        assert caajs[1].platform == "osmosis"
        assert caajs[1].application == "swap"
        assert (
            caajs[1].transaction_id
            == "97A5C4A33FA36397A342D34D576AC07BA3F5CB5B7274E2BAF7092470A681FDEB"
        )
        assert caajs[1].type == "lose"
        assert caajs[1].amount == "0.005147"
        assert caajs[1].token_symbol == "juno"
        assert (
            caajs[1].token_original_id
            == "ibc/46B44899322F3CD854D2D46DEEF881958467CDD4B3B10086DA49296BBED94BED"
        )
        assert caajs[1].caaj_to == "osmo14ls9rcxxd5gqwshj85dae74tcp3umypp786h3m"
        assert (
            caajs[1].caaj_from
            == "osmo1h7yfu7x4qsv2urnkl4kzydgxegdfyjdry5ee4xzj98jwz0uh07rqdkmprr"
        )
        assert caajs[1].comment == ""

    def test_get_caaj_transfer(self):
        test_data = TestOsmosisPlugin._get_test_data("ibc_transfer")
        transaction = OsmosisTransaction(test_data)
        caajs = OsmosisPlugin.get_caajs(
            "osmo14ls9rcxxd5gqwshj85dae74tcp3umypp786h3m",
            transaction,
        )
        assert caajs[0].executed_at == "2022-02-08 01:43:31"
        assert caajs[0].chain == "osmosis"
        assert caajs[0].platform == "osmosis"
        assert caajs[0].application == "transfer"
        assert (
            caajs[0].transaction_id
            == "AD666E0F5FB2D7DEF4B09E7BC31AF4BECB49EF76E948C4445AFF77EFFB4DEC6B"
        )
        assert caajs[0].type == "lose"
        assert caajs[0].amount == "0.000049"
        assert caajs[0].token_symbol == "juno"
        assert (
            caajs[0].token_original_id
            == "ibc/46B44899322F3CD854D2D46DEEF881958467CDD4B3B10086DA49296BBED94BED"
        )
        assert caajs[0].caaj_from == "osmo14ls9rcxxd5gqwshj85dae74tcp3umypp786h3m"
        assert caajs[0].caaj_to == "juno14ls9rcxxd5gqwshj85dae74tcp3umyppqw2uq4"
        assert caajs[0].comment == ""

    def test_get_caaj_join_pool(self):
        test_data = TestOsmosisPlugin._get_test_data("join_pool")
        transaction = OsmosisTransaction(test_data)
        caajs = OsmosisPlugin.get_caajs(
            "osmo14ls9rcxxd5gqwshj85dae74tcp3umypp786h3m",
            transaction,
        )
        assert caajs[0].executed_at == "2022-01-21 02:50:09"
        assert caajs[0].chain == "osmosis"
        assert caajs[0].platform == "osmosis"
        assert caajs[0].application == "lend"
        assert (
            caajs[0].transaction_id
            == "266ADD2B17FCDD5BBEA5499EF863AC7463C45FB6F537E02FCCA8EE048255F4D2"
        )
        assert caajs[0].type == "deposit"
        assert caajs[0].amount == "0.005146"
        assert caajs[0].token_symbol == "juno"
        assert (
            caajs[0].token_original_id
            == "ibc/46B44899322F3CD854D2D46DEEF881958467CDD4B3B10086DA49296BBED94BED"
        )
        assert caajs[0].caaj_from == "osmo14ls9rcxxd5gqwshj85dae74tcp3umypp786h3m"
        assert (
            caajs[0].caaj_to
            == "osmo1h7yfu7x4qsv2urnkl4kzydgxegdfyjdry5ee4xzj98jwz0uh07rqdkmprr"
        )
        assert caajs[0].comment == ""

        assert caajs[1].executed_at == "2022-01-21 02:50:09"
        assert caajs[1].chain == "osmosis"
        assert caajs[1].platform == "osmosis"
        assert caajs[1].application == "lend"
        assert (
            caajs[1].transaction_id
            == "266ADD2B17FCDD5BBEA5499EF863AC7463C45FB6F537E02FCCA8EE048255F4D2"
        )
        assert caajs[1].type == "deposit"
        assert caajs[1].amount == "0.009969"
        assert caajs[1].token_symbol == "osmo"
        assert caajs[1].token_original_id is None
        assert caajs[1].caaj_from == "osmo14ls9rcxxd5gqwshj85dae74tcp3umypp786h3m"
        assert (
            caajs[1].caaj_to
            == "osmo1h7yfu7x4qsv2urnkl4kzydgxegdfyjdry5ee4xzj98jwz0uh07rqdkmprr"
        )
        assert caajs[1].comment == ""

        assert caajs[2].executed_at == "2022-01-21 02:50:09"
        assert caajs[2].chain == "osmosis"
        assert caajs[2].platform == "osmosis"
        assert caajs[2].application == "lend"
        assert (
            caajs[2].transaction_id
            == "266ADD2B17FCDD5BBEA5499EF863AC7463C45FB6F537E02FCCA8EE048255F4D2"
        )
        assert caajs[2].type == "get_liquidity"
        assert caajs[2].amount == "0.004323192512586978"
        assert caajs[2].token_symbol is None
        assert caajs[2].token_original_id == "gamm/pool/497"
        assert caajs[2].caaj_from == "osmo1c9y7crgg6y9pfkq0y8mqzknqz84c3etr0kpcvj"
        assert caajs[2].caaj_to == "osmo14ls9rcxxd5gqwshj85dae74tcp3umypp786h3m"
        assert caajs[2].comment == ""

    def test_get_caaj_lock_token(self):
        test_data = TestOsmosisPlugin._get_test_data("lock_tokens")
        transaction = OsmosisTransaction(test_data)
        caajs = OsmosisPlugin.get_caajs(
            "osmo14ls9rcxxd5gqwshj85dae74tcp3umypp786h3m",
            transaction,
        )
        assert caajs[0].executed_at == "2022-01-21 02:52:07"
        assert caajs[0].chain == "osmosis"
        assert caajs[0].platform == "osmosis"
        assert caajs[0].application == "lend"
        assert (
            caajs[0].transaction_id
            == "3BA4AB4FCD0DB71F9A7239B55F1DD189DD38BFEEAF6EFFDA3BD4552DE6A3DADE"
        )
        assert caajs[0].type == "deposit_liquidity"
        assert caajs[0].amount == "0.002"
        assert caajs[0].token_symbol is None
        assert caajs[0].token_original_id == "gamm/pool/497"
        assert caajs[0].caaj_from == "osmo14ls9rcxxd5gqwshj85dae74tcp3umypp786h3m"
        assert caajs[0].caaj_to == "osmo1njty28rqtpw6n59sjj4esw76enp4mg6g7cwrhc"
        assert caajs[0].comment == ""

    def test_get_caaj_exit_pool(self):
        test_data = TestOsmosisPlugin._get_test_data("exit_pool")
        transaction = OsmosisTransaction(test_data)
        caajs = OsmosisPlugin.get_caajs(
            "osmo14ls9rcxxd5gqwshj85dae74tcp3umypp786h3m",
            transaction,
        )
        assert caajs[0].executed_at == "2022-01-21 02:54:12"
        assert caajs[0].chain == "osmosis"
        assert caajs[0].platform == "osmosis"
        assert caajs[0].application == "lend"
        assert (
            caajs[0].transaction_id
            == "8AA91C46E026F135C18BC37DA813A1682F283EFF7E5AE60899F740DE58470FBB"
        )
        assert caajs[0].type == "withdraw_liquidity"
        assert caajs[0].amount == "0.001382"
        assert caajs[0].token_symbol == "juno"
        assert (
            caajs[0].token_original_id
            == "ibc/46B44899322F3CD854D2D46DEEF881958467CDD4B3B10086DA49296BBED94BED"
        )
        assert (
            caajs[0].caaj_from
            == "osmo1h7yfu7x4qsv2urnkl4kzydgxegdfyjdry5ee4xzj98jwz0uh07rqdkmprr"
        )
        assert caajs[0].caaj_to == "osmo14ls9rcxxd5gqwshj85dae74tcp3umypp786h3m"
        assert caajs[0].comment == ""

        assert caajs[1].executed_at == "2022-01-21 02:54:12"
        assert caajs[1].chain == "osmosis"
        assert caajs[1].platform == "osmosis"
        assert caajs[1].application == "lend"
        assert (
            caajs[1].transaction_id
            == "8AA91C46E026F135C18BC37DA813A1682F283EFF7E5AE60899F740DE58470FBB"
        )
        assert caajs[1].type == "withdraw_liquidity"
        assert caajs[1].amount == "0.002678"
        assert caajs[1].token_symbol == "osmo"
        assert caajs[1].token_original_id is None
        assert caajs[1].caaj_to == "osmo14ls9rcxxd5gqwshj85dae74tcp3umypp786h3m"
        assert (
            caajs[1].caaj_from
            == "osmo1h7yfu7x4qsv2urnkl4kzydgxegdfyjdry5ee4xzj98jwz0uh07rqdkmprr"
        )
        assert caajs[1].comment == ""

        assert caajs[2].executed_at == "2022-01-21 02:54:12"
        assert caajs[2].chain == "osmosis"
        assert caajs[2].platform == "osmosis"
        assert caajs[2].application == "lend"
        assert (
            caajs[2].transaction_id
            == "8AA91C46E026F135C18BC37DA813A1682F283EFF7E5AE60899F740DE58470FBB"
        )
        assert caajs[2].type == "lose_liquidity"
        assert caajs[2].amount == "0.001161596256293489"
        assert caajs[2].token_symbol is None
        assert caajs[2].token_original_id == "gamm/pool/497"
        assert caajs[2].caaj_from == "osmo14ls9rcxxd5gqwshj85dae74tcp3umypp786h3m"
        assert caajs[2].caaj_to == "osmo1c9y7crgg6y9pfkq0y8mqzknqz84c3etr0kpcvj"
        assert caajs[2].comment == ""

    def test_get_caaj_delegate(self):
        test_data = TestOsmosisPlugin._get_test_data("delegate")
        transaction = OsmosisTransaction(test_data)
        caajs = OsmosisPlugin.get_caajs(
            "osmo14ls9rcxxd5gqwshj85dae74tcp3umypp786h3m",
            transaction,
        )

        assert caajs[0].executed_at == "2022-01-31 09:15:23"
        assert caajs[0].chain == "osmosis"
        assert caajs[0].platform == "osmosis"
        assert caajs[0].application == "lend"
        assert (
            caajs[0].transaction_id
            == "04668DE27064363B86A1925F71B453C24B08862B5F5704399B6E478616874FED"
        )
        assert caajs[0].type == "deposit"
        assert caajs[0].amount == "0.1"
        assert caajs[0].token_symbol == "osmo"
        assert caajs[0].token_original_id is None
        assert caajs[0].caaj_from == "osmo14ls9rcxxd5gqwshj85dae74tcp3umypp786h3m"
        assert caajs[0].caaj_to == "osmovaloper1clpqr4nrk4khgkxj78fcwwh6dl3uw4ep88n0y4"
        assert caajs[0].comment == ""

    def test_get_caajs_ibc_received_effect0(self):
        test_data = TestOsmosisPlugin._get_test_data("ibc_received_effect0")
        transaction = OsmosisTransaction(test_data)
        caajs = OsmosisPlugin.get_caajs(
            "osmo14ls9rcxxd5gqwshj85dae74tcp3umypp786h3m",
            transaction,
        )
        assert len(caajs) == 0

    def test_get_caajs_ibc_received_effect1(self):
        test_data = TestOsmosisPlugin._get_test_data("ibc_received_effect1")
        transaction = OsmosisTransaction(test_data)
        caajs = OsmosisPlugin.get_caajs(
            "osmo14ls9rcxxd5gqwshj85dae74tcp3umypp786h3m",
            transaction,
        )

        assert caajs[0].executed_at == "2022-01-20 06:39:04"
        assert caajs[0].chain == "osmosis"
        assert caajs[0].platform == "osmosis"
        assert caajs[0].application == "lend"
        assert (
            caajs[0].transaction_id
            == "727E12088812C7458061EB5B2284A9DBBBFBED15E3B4E174055912B8FE2F69D3"
        )
        assert caajs[0].type == "deposit"
        assert caajs[0].amount == "0.25"
        assert caajs[0].token_symbol == "atom"
        assert (
            caajs[0].token_original_id
            == "ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2"
        )
        assert caajs[0].caaj_from == "osmo1yl6hdjhmkf37639730gffanpzndzdpmhxy9ep3"
        assert caajs[0].caaj_to == "osmo14ls9rcxxd5gqwshj85dae74tcp3umypp786h3m"
        assert caajs[0].comment == ""

    @classmethod
    def _get_test_data(cls, filename):
        with open(f"tests/data/{filename}.json", encoding="utf-8") as jsonfile_local:
            test_data = json.load(jsonfile_local)
        return test_data

    def test_get_token_amount(self):
        token_amount = OsmosisPlugin._get_token_amount(
            "4900ibc/46B44899322F3CD854D2D46DEEF881958467CDD4B3B10086DA49296BBED94BED"
        )
        assert token_amount == "0.0049"

    def test_get_token_original_id(self):
        token_original_id = OsmosisPlugin._get_token_original_id(
            "4900ibc/46B44899322F3CD854D2D46DEEF881958467CDD4B3B10086DA49296BBED94BED"
        )
        assert (
            token_original_id
            == "ibc/46B44899322F3CD854D2D46DEEF881958467CDD4B3B10086DA49296BBED94BED"
        )

    def test_get_token_original_id_uosmo(self):
        token_original_id = OsmosisPlugin._get_token_original_id("4900uosmo")
        assert token_original_id is None

    def test_get_token_original_id_uion(self):
        token_original_id = OsmosisPlugin._get_token_original_id("4900uion")
        assert token_original_id is None

    def test_get_attributes_list(self):
        test_data = TestOsmosisPlugin._get_test_data("join_pool")
        transaction = OsmosisTransaction(test_data)
        attributes_list = OsmosisPlugin._get_attributes_list(transaction, "transfer")
        assert attributes_list[0] == [
            {
                "key": "recipient",
                "value": "osmo1h7yfu7x4qsv2urnkl4kzydgxegdfyjdry5ee4xzj98jwz0uh07rqdkmprr",
            },
            {"key": "sender", "value": "osmo14ls9rcxxd5gqwshj85dae74tcp3umypp786h3m"},
            {
                "key": "amount",
                "value": "5146ibc/46B44899322F3CD854D2D46DEEF881958467CDD4B3B10086DA49296BBED94BED,9969uosmo",
            },
            {
                "key": "recipient",
                "value": "osmo14ls9rcxxd5gqwshj85dae74tcp3umypp786h3m",
            },
            {"key": "sender", "value": "osmo1c9y7crgg6y9pfkq0y8mqzknqz84c3etr0kpcvj"},
            {"key": "amount", "value": "4323192512586978gamm/pool/497"},
        ]

    def test_get_atoken_symbol_uosmo(self):
        token_symbol = OsmosisPlugin._get_token_symbol("osmo")
        assert token_symbol == "osmo"

    def test_get_atoken_symbol_uion(self):
        token_symbol = OsmosisPlugin._get_token_symbol("ion")
        assert token_symbol == "ion"

    def test_get_atoken_symbol_atom(self):
        token_symbol = OsmosisPlugin._get_token_symbol(
            "ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2"
        )
        assert token_symbol == "atom"

    def test_get_atoken_symbol_nothing(self):
        token_symbol = OsmosisPlugin._get_token_symbol("nothing_symbol_in_csv")
        assert token_symbol is None

    def test_get_symbol_uuid_uosmo(self):
        symbol_uuid = OsmosisPlugin._get_symbol_uuid(None, "osmosis", "osmo")
        assert symbol_uuid == "c0c8e177-53c3-c408-d8bd-067a2ef41ea7"

    def test_get_symbol_uuid_juno(self):
        symbol_uuid = OsmosisPlugin._get_symbol_uuid(
            "ibc/46B44899322F3CD854D2D46DEEF881958467CDD4B3B10086DA49296BBED94BED",
            "osmosis",
            "juno",
        )
        assert symbol_uuid == "3a2570c5-15c4-2860-52a8-bff14f27a236"


if __name__ == "__main__":
    TestOsmosisPlugin.test_get_caaj_delegate(1)
