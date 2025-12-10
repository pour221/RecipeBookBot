# Recipe Book Telegram Bot

This Telegram bot is your personal **recipe book** — write down, search, and share recipes easily, directly in Telegram.

> **Status:** *On pause*

---

## ✨ Features

* ✅ **Create and manage personal collections**
* ✅ **Quick recipe entry:** add a recipe (title + description)
* ✅ **Detailed recipe entry** (title, description, ingredients, equipment)
* ✅ **Search recipes by name**
* ✅ **Get a random recipe**
* 🔧 **Automatic calories and macronutrients (Kcal/P/F/C) estimation** — in development

---

## Active Collection

By default, you have an **active collection**, and all operations (adding, searching, random recipe, etc.) are performed within it.

To use another collection:

* Create a new one and set it as active via:

  * **Main menu → Change collection → Choose one**, or
  * **Main menu → Manage collections → Select collection → Set as active**

The name of your active collection is displayed in the main menu.

---

## ⚙️ Running the Bot

You can **clone the repository** and run the bot locally.
Dependencies are listed in `pyproject.toml`.

### Setup Steps

1. **Rename** the folder `data_sample` → `data`
2. Inside the `data` folder, **create a subfolder** named `db`
3. **Fill out** your `config.py`:
   * Telegram Bot API token
   * Paths to images
   * Path to the database
4. **Install dependencies** (using uv or pip):
5. **Run the bot:**

   ```bash
   python -m bot.main
   ```
## Try It Out

You can also use the deployed bot directly:
👉 [@MyRecipesBookBot](https://t.me/MyRecipesBookBot)

## 🧱 Tech Stack

* Python 3.11+
* aiogram ≥ 3.21.0
* aiosqlite ≥ 0.21.0
* SQLAlchemy ≥ 2.0.43




---
