import json

from models.network import Network

#######################################################################
#                           Network Config                            #
#######################################################################


ethereum = Network(
    name="ethereum",
    rpc_url="https://rpc.ankr.com/eth",
    explorer="https://etherscan.io",
    eip_1559=True,
    native_token="ETH",
)

linea = Network(
    name="linea",
    rpc_url="https://rpc.linea.build",
    explorer="https://lineascan.build",
    eip_1559=True,
    native_token="ETH",
)

optimism = Network(
    name="optimism",
    rpc_url="https://rpc.ankr.com/optimism",
    explorer="https://optimistic.etherscan.io",
    eip_1559=True,
    native_token="ETH",
)

base = Network(
    name="base",
    rpc_url="https://mainnet.base.org",
    explorer="https://basescan.org",
    eip_1559=True,
    native_token="ETH",
)

soneium = Network(
    name="soneium",
    rpc_url="https://rpc.soneium.org",
    explorer="https://soneium.blockscout.com",
    eip_1559=True,
    native_token="ETH",
)


CHAIN_MAPPING = {
    "ethereum": ethereum,
    "linea": linea,
    "optimism": optimism,
    "base": base,
    "soneium": soneium,
}


#######################################################################
#                           Smart Contracts                           #
#######################################################################

SONUS_ROUTER = "0xA0133D304c54AB0ba9fBe4468018a5717f460D3a"

VELODROME_POOL_FACTORY = "0x31832f2a97Fd20664D76Cc421207669b55CE4BC0"
VELODROME_UNIVERSAL_ROUTER = "0x652e53C6a4FE39B6B30426d9c96376a105C89A95"

WETH = "0x4200000000000000000000000000000000000006"

VELODROME_TOKENS = {
    "USDC.e": "0xbA9986D2381edf1DA03B0B9c1f8b00dc4AacC369",
    "USDT": "0x3A337a6adA9d885b6Ad95ec48F9b75f197b5AE35",
}

SONUS_TOKENS = {
    "SONUS": "0x12BE6BA8Deaa28BC5C2FD9cdfceB47EB4FDB0B35",
    "USDC.e": "0xbA9986D2381edf1DA03B0B9c1f8b00dc4AacC369",
}

OWLTO = "0xBF6B575e5a2a1272AE7bAEdABc00Cf016f2f437c"

TILTPLAY = "0x821797851cf30F0d5d3DEDc0259FaEf6BB29C3D5"

OMNIHUB = "0x4AA0F75B4c26F08A6E1d26be3707485B7DC06207"

ONCHAINGM = "0x0A027CB6Fb548Ec0302860eE5A968e73F7294D19"

KYO_FINANCE = "0x3B574a321c7BFEF28e8021D210d063C9f72b17fC"

ARCAS_CHAMPIONS_SBT = "0x52d44Bea684eCd8Cad6d02205e40FC3bD59Ad877"

# Sake Finance
SAFE_FINANCE = "0x779a0A5686c2835F3DB9dB9EA4d030508E9EB096"
SAKE_L2_POOL = "0x3C3987A310ee13F7B8cBBe21D97D4436ba5E4B5f"
AWETH = "0x4DC7c9eC156188Ea46F645E8407738C32c2B5B58"


with open("abi/SonusRouter.json") as f:
    SONUS_ROUTER_ABI = json.load(f)

with open("abi/velodrome/PoolFactory.json") as f:
    VELODROME_POOL_FACTORY_ABI = json.load(f)

with open("abi/velodrome/Pool.json") as f:
    VELODROME_POOL_ABI = json.load(f)

with open("abi/velodrome/UniversalRouter.json") as f:
    VELODROME_UNIVERSAL_ROUTER_ABI = json.load(f)

with open("abi/PersonalAssetManagerFactory.json") as f:
    KYO_ASSET_MANAGER_ABI = json.load(f)

with open("abi/sake_finance/SakeFinance.json") as f:
    SAKE_FINANCE_ABI = json.load(f)

with open("abi/sake_finance/L2Pool.json") as f:
    SAKE_L2_POOL_ABI = json.load(f)

with open("abi/ERC20.json") as f:
    ERC20_ABI = json.load(f)
