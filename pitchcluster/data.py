"""Download and cache Statcast pitch-level data."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from pybaseball import cache, statcast

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Only the columns the analysis needs; keeps the cached file small.
COLUMNS = [
    "game_date", "pitcher", "player_name", "p_throws", "stand", "pitch_type",
    "release_speed", "release_spin_rate", "spin_axis", "pfx_x", "pfx_z",
    "release_pos_x", "release_pos_z", "release_extension",
    "description", "type", "delta_run_exp", "game_type",
    # location, count and batted-ball quality
    "plate_x", "plate_z", "sz_top", "sz_bot", "balls", "strikes",
    "launch_speed", "launch_angle", "estimated_woba_using_speedangle", "woba_value", "woba_denom",
    # team attribution (pitching team = home team in the top of an inning, else away team)
    "home_team", "away_team", "inning_topbot",
]


def load_season(year: int, refresh: bool = False) -> pd.DataFrame:
    """Return regular-season Statcast pitches for `year`, cached as parquet."""
    DATA_DIR.mkdir(exist_ok=True)
    path = DATA_DIR / f"statcast_{year}.parquet"
    if path.exists() and not refresh:
        return pd.read_parquet(path)

    cache.enable()
    # Statcast pulls are chunked by pybaseball; March-November covers the season.
    df = statcast(start_dt=f"{year}-03-15", end_dt=f"{year}-11-05", verbose=False)
    df = df[df["game_type"] == "R"][COLUMNS].copy()
    df.to_parquet(path, index=False)
    return df


if __name__ == "__main__":
    yr = int(sys.argv[1]) if len(sys.argv) > 1 else 2024
    out = load_season(yr, refresh="--refresh" in sys.argv)
    print(f"{len(out):,} pitches, {out['pitcher'].nunique()} pitchers")




