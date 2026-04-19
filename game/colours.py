class Colours:
    """ANSI colour codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    # Specific colours for game elements
    HP = '\033[91m'  # Red for HP
    MANA = '\033[94m'  # Blue for Mana
    XP = '\033[92m'  # Green for XP
    DAMAGE = '\033[91m'  # Red for damage
    HEAL = '\033[92m'  # Green for healing
    BUFF = '\033[93m'  # Yellow for buffs
    DEBUFF = '\033[95m'  # Purple for debuffs
    SPECIAL = '\033[96m'  # Cyan for special events
    TITLE = '\033[95m\033[1m'  # Bold purple for titles


def colourize(text: str, color: str) -> str:
    """Wrap text with color codes."""
    return f"{color}{text}{Colours.ENDC}"


def hp_bar(current: int, maximum: int, width: int = 20) -> str:
    """Create a colored HP bar."""
    percentage = current / maximum if maximum > 0 else 0
    filled = int(width * percentage)
    empty = width - filled

    bar = "█" * filled + "░" * empty

    if percentage > 0.6:
        bar_color = Colours.GREEN
    elif percentage > 0.3:
        bar_color = Colours.WARNING
    else:
        bar_color = Colours.FAIL

    return f"{bar_color}{bar}{Colours.ENDC} [{current}/{maximum}]"


def mana_bar(current: int, maximum: int, width: int = 20) -> str:
    """Create a colored mana bar."""
    percentage = current / maximum if maximum > 0 else 0
    filled = int(width * percentage)
    empty = width - filled

    bar = "█" * filled + "░" * empty
    return f"{Colours.MANA}{bar}{Colours.ENDC} [{current}/{maximum}]"