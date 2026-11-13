# Pitching Decision Report, 2025

Source: Statcast regular-season pitches, 2025. Run value (RV) is per 100 pitches from the pitcher's view (positive = good for the pitcher). Team is the pitcher's last team of the season, so traded pitchers show their final club.

> **Retrospective report.** The evidence cited below comes from tests that use seasons after 2025, which were not available at the time. Read it as a back-cast, not as what could have been known then.

## Key takeaways

- **What held up in later seasons:** platoon gaps persist only about 20% (the weak side holds 64% to 65% of the time for the biggest gaps), and heavily used pitches that cost runs kept costing runs. Command is a repeatable skill. Shape-based and contact-luck flags are modest hints, not calls.
- **Pitches whose results lag their shape (look at video):** Davis Martin (CH), Orion Kerkering (ST), Zack Littell (FS).
- **Pitches whose results beat their shape (expect some give-back):** Brendon Little (KC), Kodai Senga (FO), Bennett Sousa (SL).
- **Best command:** Kodai Senga (FO), Patrick Corbin (SL), Jack Flaherty (KC). **Weakest:** Tyler Rogers (SI), Luke Jackson (SL), Phil Maton (CU).
- **Platoon, largest gaps:** Tim Hill (vs RHB), J.T. Ginn (vs LHB), Carlos Vargas (vs RHB).
- **Costliest heavy-use pitches:** Germán Márquez (FF), Bradley Blalock (FF), Ryan Helsley (FF).
- **Flagged in more than one section:** 58 pitchers, led by Tyler Anderson, Noah Cameron, J.T. Ginn (table below).

## How much to trust each section

Each measure was tested on a later season than the one it was built from (2024->2025 and 2025->2026). Treat the sections accordingly.

| Section | Evidence | Use it for |
|---|---|---|
| 1. Underperforms shape | Modest: next-year whiff rate rose 1.2 to 2.9 points more than matched controls; significant in one of the two tests | A reason to look at video, not a prediction |
| 2. Outperforms shape | Modest: whiff rate fell 0.7 to 2.1 points more than controls; significant in one of the two tests | Discounting results, not selling |
| 3. Command score | A repeatable skill (year-to-year correlation 0.62); it does not improve next-year whiff forecasts | Explaining why results differ from shape |
| 4. Contact luck | Weak: right direction in 4 of 4 comparisons, significant in 1; expected wOBA did not beat actual wOBA at predicting next year | Context only |
| 5. Platoon gaps | Validated: about 20% of the gap persists | Shrunk platoon deployment |
| 6. Costly heavy-use pitches | Validated: flagged pitches did 0.35 to 0.78 runs/100 worse next year than other heavy-use pitches | Usage and pitch-mix review |

As a *projection*, the shape model adds only about 1% to simply regressing last year's whiff rate toward the mean (RMSE gain 0.0003 to 0.0005). Its value is as a flag for pitches to look at, not as a forecasting tool.

## Pitchers flagged in more than one section

Overlap is a useful place to start, but it is descriptive: several of these measures share inputs, so overlapping flags are not independent evidence. Strong/weak command counts the 20 highest/lowest scores; platoon counts the 25 largest gaps; contact luck the 15 largest gaps each way.

| Pitcher         | Team   | Sections   | Flags                                                                                                            |
|:----------------|:-------|:-----------|:-----------------------------------------------------------------------------------------------------------------|
| Tyler Anderson  | LAA    | 3          | Costly pitch (FC); Platoon gap (vs LHB); Strong command (CH)                                                     |
| Noah Cameron    | KC     | 3          | Lucky contact; Underperforms shape (FF); Weak command (CU)                                                       |
| J.T. Ginn       | ATH    | 3          | Outperforms shape (SI); Platoon gap (vs LHB); Unlucky contact                                                    |
| Germán Márquez  | COL    | 3          | Costly pitch (FF); Underperforms shape (FF); Underperforms shape (KC); Underperforms shape (SI); Unlucky contact |
| Aaron Nola      | PHI    | 3          | Strong command (KC); Underperforms shape (FF); Unlucky contact                                                   |
| Nick Pivetta    | SD     | 3          | Lucky contact; Outperforms shape (FF); Outperforms shape (ST); Weak command (CU)                                 |
| Jose Quintana   | MIL    | 3          | Lucky contact; Strong command (CH); Underperforms shape (CH)                                                     |
| Trevor Williams | WSH    | 3          | Costly pitch (FF); Platoon gap (vs LHB); Unlucky contact                                                         |
| Sandy Alcantara | MIA    | 2          | Costly pitch (FF); Underperforms shape (FF); Underperforms shape (SL)                                            |
| Graham Ashcraft | CIN    | 2          | Costly pitch (FC); Underperforms shape (FC)                                                                      |
| Shane Baz       | TB     | 2          | Underperforms shape (KC); Unlucky contact                                                                        |
| Valente Bellozo | MIA    | 2          | Costly pitch (FF); Platoon gap (vs LHB)                                                                          |

## 1. Underperforms shape: look closer

A pitch-level model predicts the chance of a miss on every swing from velocity, spin, movement, extension, release point, how the pitch differs from the pitcher's own fastball (speed and break separation) and batter side, fit out-of-fold by pitcher. Averaging over a pitcher's swings gives an expected whiff rate. The gap is actual minus expected. Pitches that whiff far fewer hitters than their shape predicts, with below-median run value, are candidates for a mechanical, sequencing or location fix. A very large gap can also mean the model is extrapolating, so check video before acting.

| Pitcher         | Team   | Pitch   | Pitches   | Velo   | Whiff%   | Expected whiff%   | Gap (pts)   | RV/100   |
|:----------------|:-------|:--------|:----------|:-------|:---------|:------------------|:------------|:---------|
| Davis Martin    | CWS    | CH      | 563       | 90.2   | 17.9%    | 34.3%             | -16.4       | +0.19    |
| Orion Kerkering | PHI    | ST      | 515       | 86.8   | 23.6%    | 39.0%             | -15.3       | -0.01    |
| Zack Littell    | CIN    | FS      | 732       | 83.4   | 24.0%    | 36.7%             | -12.7       | -0.28    |
| Clayton Kershaw | LAD    | FF      | 587       | 89.0   | 7.3%     | 19.4%             | -12.1       | +0.14    |
| Sandy Alcantara | MIA    | SL      | 495       | 85.3   | 21.7%    | 33.5%             | -11.8       | -0.50    |
| Griffin Canning | NYM    | SL      | 410       | 87.7   | 34.1%    | 45.8%             | -11.7       | +0.05    |
| Germán Márquez  | COL    | FF      | 737       | 94.8   | 9.0%     | 20.5%             | -11.5       | -1.83    |
| Brayan Bello    | BOS    | ST      | 496       | 85.7   | 26.7%    | 37.8%             | -11.0       | +0.01    |
| Jack Leiter     | TEX    | SL      | 591       | 87.6   | 26.3%    | 36.6%             | -10.3       | +0.08    |
| Ryan Pepiot     | TB     | SL      | 468       | 89.0   | 23.9%    | 34.0%             | -10.1       | -0.33    |
| Taijuan Walker  | PHI    | FS      | 463       | 87.4   | 19.9%    | 29.9%             | -10.0       | -0.71    |
| Bradley Blalock | COL    | FF      | 479       | 94.6   | 8.8%     | 18.4%             | -9.6        | -2.02    |

## 2. Outperforms shape: discount the results

Whiff rate and run value well above what the shape predicts. This is usually command, location, tunneling or deception, which is partly real (see section 3: command explains much of the gap but does not protect against regression). In the year-ahead tests these pitches gave back 2.1 and 0.7 whiff points versus matched controls (significant in one of the two tests), so expect partial regression, not collapse. Do not pay for their shape; weigh their results with some discount.

| Pitcher          | Team   | Pitch   | Pitches   | Velo   | Whiff%   | Expected whiff%   | Gap (pts)   | RV/100   |
|:-----------------|:-------|:--------|:----------|:-------|:---------|:------------------|:------------|:---------|
| Brendon Little   | TOR    | KC      | 571       | 87.0   | 55.6%    | 33.8%             | +21.7       | +0.76    |
| Kodai Senga      | NYM    | FO      | 542       | 82.5   | 41.8%    | 21.6%             | +20.2       | +1.38    |
| Bennett Sousa    | HOU    | SL      | 418       | 85.7   | 50.0%    | 30.4%             | +19.6       | +1.13    |
| Fernando Cruz    | NYY    | FS      | 479       | 80.6   | 56.6%    | 37.4%             | +19.3       | +0.87    |
| Joey Cantillo    | CLE    | CH      | 500       | 78.3   | 49.4%    | 32.7%             | +16.7       | +0.56    |
| Andrés Muñoz     | SEA    | SL      | 516       | 86.0   | 51.2%    | 36.0%             | +15.2       | +1.62    |
| Devin Williams   | NYY    | FF      | 528       | 94.1   | 37.7%    | 22.6%             | +15.1       | +0.40    |
| Garrett Whitlock | BOS    | SI      | 555       | 95.8   | 30.8%    | 16.6%             | +14.2       | +1.20    |
| Steven Okert     | HOU    | SL      | 608       | 80.9   | 40.7%    | 27.3%             | +13.4       | +1.49    |
| Garrett Crochet  | BOS    | ST      | 504       | 82.8   | 40.5%    | 27.3%             | +13.2       | +1.84    |
| Michael Soroka   | CHC    | SV      | 531       | 80.4   | 37.8%    | 24.7%             | +13.1       | +0.87    |
| Michael Lorenzen | KC     | CH      | 401       | 83.7   | 42.4%    | 29.8%             | +12.6       | +0.40    |

## 3. Command: whose locations create misses

Command score is how many more misses per swing (in percentage points) a pitcher's locations create than the same pitch shape would league-wide (a location-aware model minus a shape-only model, both fit out-of-fold by pitcher). Zone% is the share of pitches in the zone; chase% is how often hitters swing at pitches out of it. It is a repeatable skill (year-to-year correlation 0.62) and tracks the shape gap closely (correlation 0.67 to 0.68 with actual-minus-expected whiff), so it explains much of why a pitch beats or lags its shape. But last year's whiff rate already contains it, so it does not improve forecasts, and high-command "outperformers" regressed about as much as low-command ones (-3.3 vs -2.8 and -2.5 vs -2.7 whiff points), so command alone does not make those results durable. Pitch types with at least 300 pitches and 150 swings are shown.

**Strongest command:**

| Pitcher         | Team   | Pitch   | Pitches   | Command (pts)   | Zone%   | Chase%   | Whiff%   | Shape-expected whiff%   |
|:----------------|:-------|:--------|:----------|:----------------|:--------|:---------|:---------|:------------------------|
| Kodai Senga     | NYM    | FO      | 542       | +22.1           | 27.5%   | 45.8%    | 41.8%    | 21.6%                   |
| Patrick Corbin  | TEX    | SL      | 868       | +16.8           | 33.4%   | 34.8%    | 39.1%    | 22.4%                   |
| Jack Flaherty   | DET    | KC      | 691       | +16.1           | 32.1%   | 41.6%    | 41.5%    | 25.9%                   |
| Brendon Little  | TOR    | KC      | 571       | +14.4           | 24.7%   | 35.6%    | 55.6%    | 33.8%                   |
| Spencer Strider | ATL    | SL      | 744       | +12.7           | 34.3%   | 38.9%    | 48.3%    | 33.5%                   |
| Ronny Henriquez | MIA    | ST      | 328       | +10.5           | 38.7%   | 47.3%    | 47.3%    | 34.7%                   |
| Sonny Gray      | STL    | ST      | 523       | +10.3           | 30.8%   | 48.6%    | 42.4%    | 32.4%                   |
| Zac Gallen      | AZ     | KC      | 736       | +9.7            | 37.9%   | 43.1%    | 38.9%    | 29.8%                   |
| Paul Skenes     | PIT    | CH      | 326       | +9.4            | 23.0%   | 41.4%    | 43.9%    | 32.7%                   |
| Landen Roupp    | SF     | CH      | 315       | +9.4            | 24.4%   | 41.2%    | 28.7%    | 29.0%                   |

**Weakest command:**

| Pitcher       | Team   | Pitch   | Pitches   | Command (pts)   | Zone%   | Chase%   | Whiff%   | Shape-expected whiff%   |
|:--------------|:-------|:--------|:----------|:----------------|:--------|:---------|:---------|:------------------------|
| Tyler Rogers  | NYM    | SI      | 729       | -16.9           | 65.7%   | 27.2%    | 12.4%    | 25.6%                   |
| Luke Jackson  | SEA    | SL      | 357       | -16.2           | 49.6%   | 30.6%    | 25.1%    | 46.9%                   |
| Phil Maton    | TEX    | CU      | 385       | -15.7           | 46.0%   | 44.7%    | 41.6%    | 46.6%                   |
| Eric Orze     | TB     | FS      | 312       | -15.0           | 54.2%   | 32.9%    | 30.2%    | 41.1%                   |
| Dustin May    | BOS    | ST      | 853       | -13.2           | 46.9%   | 27.8%    | 26.7%    | 41.2%                   |
| Max Meyer     | MIA    | SL      | 363       | -12.8           | 50.1%   | 40.3%    | 42.6%    | 47.1%                   |
| Louis Varland | TOR    | KC      | 400       | -12.3           | 45.2%   | 38.8%    | 38.8%    | 50.5%                   |
| Ryan Pepiot   | TB     | CH      | 655       | -10.4           | 46.4%   | 33.9%    | 29.2%    | 40.5%                   |

## 4. Contact luck (weak evidence)

Actual wOBA on balls in play vs. the wOBA expected from exit velocity and launch angle (min 250 balls in play). Gap is actual minus expected: positive means the pitcher allowed more damage than the contact deserved. In testing, expected wOBA did not beat actual wOBA at predicting next year, and the "unlucky" and "lucky" groups moved the expected way in most comparisons but rarely significantly. Use as context, not as a call.

**Results worse than contact quality (possible rebound):**

| Pitcher        | Team   | Throws   | Balls in play   | Actual wOBA   | Expected wOBA   | Gap   |
|:---------------|:-------|:---------|:----------------|:--------------|:----------------|:------|
| J.T. Ginn      | ATH    | R        | 255             | .438          | .362            | +.076 |
| Charlie Morton | ATL    | R        | 413             | .437          | .379            | +.058 |
| JP Sears       | SD     | L        | 421             | .426          | .369            | +.057 |
| Germán Márquez | COL    | R        | 451             | .450          | .394            | +.055 |
| Colton Gordon  | HOU    | L        | 283             | .446          | .392            | +.054 |
| Aaron Nola     | PHI    | R        | 274             | .436          | .382            | +.054 |
| Dylan Cease    | SD     | R        | 425             | .419          | .366            | +.053 |
| Casey Mize     | DET    | R        | 448             | .405          | .357            | +.048 |

**Results better than contact quality (possible give-back):**

| Pitcher       | Team   | Throws   | Balls in play   | Actual wOBA   | Expected wOBA   | Gap   |
|:--------------|:-------|:---------|:----------------|:--------------|:----------------|:------|
| Trevor Rogers | BAL    | L        | 287             | .269          | .347            | -.078 |
| Nick Pivetta  | SD     | R        | 474             | .324          | .391            | -.067 |
| Tyler Mahle   | TEX    | R        | 251             | .292          | .359            | -.067 |
| Kyle Leahy    | STL    | R        | 254             | .334          | .387            | -.053 |
| Lucas Giolito | BOS    | R        | 431             | .347          | .396            | -.049 |
| Jose Quintana | MIL    | L        | 411             | .333          | .378            | -.045 |
| Randy Vásquez | SD     | R        | 433             | .328          | .372            | -.044 |
| Jacob deGrom  | TEX    | R        | 441             | .333          | .369            | -.036 |

## 5. Platoon vulnerabilities

Largest run-value gaps between left- and right-handed batters (at least 400 pitches each side). Gap is RV/100 against lefties minus RV/100 against righties: positive means the pitcher is weaker against right-handed batters. 
Only about 20% of a pitcher's gap carried into the following season in testing, so the expected next-year gap shrinks it accordingly. The weak side stayed the weak side 64% to 65% of the time for the biggest gaps. 
Use for deployment hints, not hard role limits.

| Pitcher              | Team   | Throws   | Pitches vs L   | Pitches vs R   | RV/100 vs L   | RV/100 vs R   | Gap   | Expected next-year gap   | Weak side   |
|:---------------------|:-------|:---------|:---------------|:---------------|:--------------|:--------------|:------|:-------------------------|:------------|
| Tim Hill             | NYY    | L        | 455            | 444            | +2.90         | -1.59         | +4.49 | +0.90                    | vs RHB      |
| J.T. Ginn            | ATH    | R        | 705            | 870            | -2.70         | +1.53         | -4.23 | -0.85                    | vs LHB      |
| Carlos Vargas        | SEA    | R        | 453            | 622            | +1.95         | -1.81         | +3.76 | +0.75                    | vs RHB      |
| Shawn Armstrong      | TEX    | R        | 410            | 694            | -1.02         | +2.70         | -3.72 | -0.74                    | vs LHB      |
| Jackson Rutledge     | WSH    | R        | 565            | 774            | -3.34         | +0.30         | -3.64 | -0.73                    | vs LHB      |
| Trevor Williams      | WSH    | R        | 809            | 639            | -2.06         | +1.38         | -3.43 | -0.69                    | vs LHB      |
| Huascar Brazobán     | NYM    | R        | 436            | 575            | -1.31         | +2.07         | -3.39 | -0.68                    | vs LHB      |
| Valente Bellozo      | MIA    | R        | 671            | 651            | -2.22         | +0.92         | -3.14 | -0.63                    | vs LHB      |
| Tanner Banks         | PHI    | L        | 438            | 646            | +3.00         | -0.08         | +3.07 | +0.61                    | vs RHB      |
| Michael McGreevy     | STL    | R        | 731            | 734            | -1.40         | +1.62         | -3.02 | -0.60                    | vs LHB      |
| José A. Ferrer       | WSH    | L        | 408            | 800            | +2.21         | -0.64         | +2.85 | +0.57                    | vs RHB      |
| Seranthony Domínguez | TOR    | R        | 479            | 622            | -0.86         | +1.94         | -2.80 | -0.56                    | vs LHB      |

## 6. Heavily used pitches that cost runs

Pitch types thrown at least 15% of the time with shrunk RV below -0.5 per 100, ranked by runs lost vs. the league average for that pitch type over the season. Flagged pitches did 0.35 to 0.78 runs per 100 worse than unflagged heavy-use pitches the following year. Candidates for usage reduction, a shape or location change, or replacement.

| Pitcher           | Team   | Pitch   | Pitches   | Usage   | RV/100   | Runs lost vs avg   |
|:------------------|:-------|:--------|:----------|:--------|:---------|:-------------------|
| Germán Márquez    | COL    | FF      | 737       | 35%     | -1.81    | 22.6               |
| Bradley Blalock   | COL    | FF      | 479       | 46%     | -2.00    | 19.1               |
| Ryan Helsley      | NYM    | FF      | 445       | 46%     | -1.70    | 15.9               |
| Antonio Senzatela | COL    | FF      | 1299      | 57%     | -0.76    | 15.9               |
| Jake Irvin        | WSH    | FF      | 941       | 32%     | -0.99    | 15.6               |
| Andrew Heaney     | LAD    | FF      | 909       | 46%     | -0.92    | 14.3               |
| Charlie Morton    | ATL    | FF      | 702       | 28%     | -1.06    | 13.7               |
| Grant Holmes      | ATL    | FF      | 641       | 33%     | -1.12    | 13.6               |
| Yusei Kikuchi     | LAA    | FF      | 1081      | 35%     | -0.73    | 13.5               |
| Angel Chivilli    | COL    | FF      | 469       | 46%     | -1.36    | 13.4               |
| Austin Gomber     | COL    | FF      | 340       | 34%     | -1.62    | 13.3               |
| Patrick Corbin    | TEX    | SL      | 868       | 34%     | -0.50    | 13.0               |

## Caveats

- Run value is noisy at these sample sizes. Shrinkage mitigates but does not remove that.
- The shape model sees physical shape, separation from the pitcher's own fastball and batter side. Location is handled separately by the command score; sequencing and pitch-to-pitch tunneling are not modeled.
- Flag tests used only three seasons and small flagged samples (29 to 96 per test), so intervals are wide.
