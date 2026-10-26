# Minted Coins Resources

Companion resource pack for the [Minted Coins](https://modrinth.com/datapack/minted-coins) data pack: struck coins get their own textures instead of looking like nuggets or prismarine crystals.

## Features

- **Gold**, **copper**, **iron** and **diamond coins** get a dedicated coin texture, stamped with a crown.
- Plain nuggets and prismarine crystals keep their vanilla look.
- English and French translations for the coin names, the *Struck by* line and the default mint names.

Coins are recognised by their `custom_model_data` string (`minted_coins:gold_coin`, `minted_coins:copper_coin`, `minted_coins:iron_coin`, `minted_coins:diamond_coin`), so coins from every mint share the same texture.

## 📦 Compatibility

| | |
|---|---|
| **Minecraft versions** | 26.3 |
| **Type** | Resource Pack |
| **Requires** | [Minted Coins](https://modrinth.com/datapack/minted-coins) data pack on the world or server |
| **License** | MIT |

This pack replaces the item definitions of `gold_nugget`, `copper_nugget`, `iron_nugget` and `prismarine_crystals`. Another resource pack that also changes these items will override it, or be overridden, depending on load order.

## 📥 Installation

Drop the downloaded zip into `.minecraft/resourcepacks/`, then enable it in **Options → Resource Packs**.
