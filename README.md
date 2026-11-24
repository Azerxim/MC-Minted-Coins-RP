# Minted Coins Resources

Companion resource pack for the [Minted Coins](https://modrinth.com/datapack/minted-coins) data pack: struck coins get their own textures instead of looking like nuggets or prismarine crystals.

## Features

- **Gold**, **copper**, **iron** and **diamond coins** get a dedicated coin texture, stamped with a crown.
- In hand, on the ground and in item frames, coins are **3D models**: a raised rim, a milled edge and an embossed crown on both faces. The inventory keeps the flat icon.
- **Small coins** (small change) get their own holed coin, in 3D and in the inventory.
- **Purse**: a leather pouch, empty or full, instead of the bundle it is based on.
- **Counter** of the mint: a wooden counter with a coin press, scales and stacks of coins, instead of the barrel it is based on.
- **Coin piles**: the model grows with the stack, for coins and small coins: one coin up to 8, a small pile from 9, a large pile from 32 and a heap from 60, in 3D and in the inventory.
- Plain nuggets, prismarine crystals and firework stars keep their vanilla look.
- English, French, Spanish and German translations for the coin names, the menus and every chat message of the data pack.
- Coin icons in the menu titles and to the left of each slider of the *New mint* menu, and a line between the mint name and the coins.

### Adding a language

Copy `assets/minted_coins/lang/en_us.json` to your language code, translate it, then run `python3 tools/slider_icons.py <path to the 26.3 client jar>`: the slider icons are placed with spaces that depend on the width of each label, so the script measures them with the vanilla font and writes the `.icon` keys. The `tools` folder is not part of the pack.

Coins are recognised by their `custom_model_data` string (`minted_coins:gold_coin`, `minted_coins:copper_coin`, `minted_coins:iron_coin`, `minted_coins:diamond_coin`), so coins from every mint share the same texture.

## 📦 Compatibility

| | |
|---|---|
| **Minecraft versions** | 26.3 |
| **Type** | Resource Pack |
| **Requires** | [Minted Coins](https://modrinth.com/datapack/minted-coins) data pack on the world or server |
| **License** | All Rights Reserved ([details](LICENSE)) |

This pack replaces the item definitions of `gold_nugget`, `copper_nugget`, `iron_nugget`, `prismarine_crystals` and `firework_star`. Another resource pack that also changes these items will override it, or be overridden, depending on load order.

## 📥 Installation

Drop the downloaded zip into `.minecraft/resourcepacks/`, then enable it in **Options → Resource Packs**.

## 📄 License

Minted Coins Resources © 2026 Azerxim. All rights reserved: you may play with it, use it on servers, add it to modpacks that download it from its official page and show it in videos, but not re-upload it or share a modified version. See [LICENSE](LICENSE) for the details.
