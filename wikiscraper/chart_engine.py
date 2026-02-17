"""Draws charts"""
import matplotlib.pyplot as plt
from wikiscraper import file_manager

def draw_freq_bar_chart(combined_df, num, mode="article", lang="en", chartfilepath=None):
    """Draws a chart of frequency in a language as compared to measured frequency"""
    if mode == "article":
        title_desc = f"Top {num} Words by Article Occurrence"
    elif mode == "language":
        title_desc = f"Top {num} Words by '{lang}' Language Frequency"
    else:
        raise ValueError("Mode must be eihter 'article' or 'language'")
    combined_df.plot(
        kind="bar",
        figsize=(12, 6),
        color=["#1f77b4", "#ff7f0e"],
        width=0.8)

    plt.title(title_desc, fontsize=16, pad=20)
    plt.ylabel("Frequency Value", fontsize=12)
    plt.xlabel("Word", fontsize=12)
    if num < 40:
        plt.xticks(rotation=45, ha="right")
    else:
        plt.xticks([])
    plt.tight_layout()
    plt.legend(title="Metric")

    if chartfilepath:
        plt.savefig(chartfilepath, bbox_inches="tight", dpi=300)
    plt.show()

def draw_language_test_bar_chart(langs_df, folder):
    """Draws all charts for unit testing"""

    langs_df.set_index(["file"], inplace=True)
    # Dependence on article
    for k in [100]:
        title = f"Top {k} Words By Occurrence in Articles \
                    Compared to Languages Articles From {folder}"

        k_langs_df = langs_df[langs_df["k"] == k]
        k_langs_df.filter(like=" score").plot(kind="bar",figsize=(12,6),width=0.8)
        plt.title(title, fontsize=16, pad=20)
        plt.ylabel("Score", fontsize=12)
        plt.xlabel("File", fontsize=12)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.legend(title="Metric")
        plt.savefig(file_manager.get_target_dir("charts") /
                    (str(folder).replace("/","_") + "_language_comparison.png"),
                    bbox_inches="tight", dpi=300)

    # Dependence on K averaged over articles
    title = f"Top K Words By Average Article Occurrence Compared to \
                    Languages (Articles From {folder} Folder)"
    avg_performance = langs_df.groupby("k").mean(numeric_only=True)
    avg_performance.plot(kind="bar", figsize=(12,5), width=0.8)
    plt.title(title, fontsize=16, pad=20)
    plt.ylabel("Score", fontsize=12)
    plt.xlabel("K", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.legend(title="Metric")
    plt.savefig(file_manager.get_target_dir("charts") /
                (str(folder).replace("/","_") + "_k_comparison.png"),
                bbox_inches="tight", dpi=300)
