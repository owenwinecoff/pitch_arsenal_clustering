# Pitching Decision Report, 2024

Source: Statcast regular-season pitches, 2024. Run value (RV) is per 100 pitches from the pitcher's view (positive = good for the pitcher). Team is the pitcher's last team of the season, so traded pitchers show their final club.

> **Retrospective report.** The evidence cited below comes from tests that use seasons after 2024, which were not available at the time. Read it as a back-cast, not as what could have been known then.

## Key takeaways

- **What held up in later seasons:** platoon gaps persist only about 20% (the weak side holds 64% to 65% of the time for the biggest gaps), and heavily used pitches that cost runs kept costing runs. Command is a repeatable skill. Shape-based and contact-luck flags are modest hints, not calls.
- **Pitches whose results lag their shape (look at video):** Simeon Woods Richardson (CH), Michael Tonkin (SL), Casey Mize (SL).
- **Pitches whose results beat their shape (expect some give-back):** José Alvarado (FC), Blake Snell (CU), Fernando Cruz (FS).
- **Best command:** Reynaldo López (SL), Ranger Suarez (CU), Corbin Burnes (SL). **Weakest:** Phil Maton (CU), Landen Roupp (CU), Tyler Glasnow (CU).
- **Platoon, largest gaps:** Quinn Priester (vs LHB), Ryan Yarbrough (vs RHB), John Brebbia (vs LHB).
- **Costliest heavy-use pitches:** Patrick Corbin (SI), John Brebbia (SL), Ty Blach (SI).
- **Flagged in more than one section:** 58 pitchers, led by Griffin Canning, Patrick Corbin, Zac Gallen (table below).

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

| Pitcher           | Team   | Sections   | Flags                                                                 |
|:------------------|:-------|:-----------|:----------------------------------------------------------------------|
| Griffin Canning   | LAA    | 3          | Costly pitch (FF); Underperforms shape (SL); Weak command (SL)        |
| Patrick Corbin    | WSH    | 3          | Costly pitch (SI); Platoon gap (vs RHB); Strong command (SL)          |
| Zac Gallen        | AZ     | 3          | Outperforms shape (KC); Strong command (KC); Underperforms shape (FF) |
| MacKenzie Gore    | WSH    | 3          | Underperforms shape (CU); Unlucky contact; Weak command (CU)          |
| José Leclerc      | TEX    | 3          | Outperforms shape (FF); Platoon gap (vs LHB); Strong command (SL)     |
| Reynaldo López    | ATL    | 3          | Lucky contact; Outperforms shape (SL); Strong command (SL)            |
| Jordan Montgomery | AZ     | 3          | Costly pitch (SI); Strong command (CU); Unlucky contact               |
| Reese Olson       | DET    | 3          | Outperforms shape (SL); Strong command (SL); Underperforms shape (FF) |
| Cole Ragans       | KC     | 3          | Outperforms shape (CH); Underperforms shape (SL); Weak command (SL)   |
| Matt Waldron      | SD     | 3          | Costly pitch (KN); Underperforms shape (KN); Weak command (KN)        |
| Logan Webb        | SF     | 3          | Lucky contact; Underperforms shape (CH); Weak command (ST)            |
| Ryan Yarbrough    | TOR    | 3          | Lucky contact; Outperforms shape (ST); Platoon gap (vs RHB)           |

## 1. Underperforms shape: look closer

A pitch-level model predicts the chance of a miss on every swing from velocity, spin, movement, extension, release point, how the pitch differs from the pitcher's own fastball (speed and break separation) and batter side, fit out-of-fold by pitcher. Averaging over a pitcher's swings gives an expected whiff rate. The gap is actual minus expected. Pitches that whiff far fewer hitters than their shape predicts, with below-median run value, are candidates for a mechanical, sequencing or location fix. A very large gap can also mean the model is extrapolating, so check video before acting.

| Pitcher                 | Team   | Pitch   | Pitches   | Velo   | Whiff%   | Expected whiff%   | Gap (pts)   | RV/100   |
|:------------------------|:-------|:--------|:----------|:-------|:---------|:------------------|:------------|:---------|
| Simeon Woods Richardson | MIN    | CH      | 442       | 82.8   | 20.5%    | 35.0%             | -14.5       | -1.67    |
| Michael Tonkin          | MIN    | SL      | 487       | 83.9   | 26.6%    | 39.7%             | -13.1       | +0.16    |
| Casey Mize              | DET    | SL      | 466       | 85.8   | 20.8%    | 33.6%             | -12.8       | -0.62    |
| Landen Roupp            | SF     | CU      | 400       | 77.4   | 33.0%    | 45.4%             | -12.4       | +0.14    |
| Cooper Criswell         | BOS    | ST      | 471       | 76.8   | 20.6%    | 32.9%             | -12.2       | -0.64    |
| Miles Mikolas           | STL    | SL      | 656       | 86.5   | 16.7%    | 28.5%             | -11.8       | -0.22    |
| Ryan Weathers           | MIA    | FF      | 554       | 95.9   | 14.1%    | 25.4%             | -11.3       | -0.18    |
| Griffin Canning         | LAA    | SL      | 690       | 87.7   | 32.9%    | 43.3%             | -10.5       | -0.41    |
| Cole Ragans             | KC     | SL      | 400       | 86.0   | 32.6%    | 42.8%             | -10.2       | -0.22    |
| JP Sears                | ATH    | CH      | 549       | 84.0   | 18.8%    | 28.6%             | -9.8        | -0.25    |
| Reese Olson             | DET    | FF      | 441       | 94.2   | 10.2%    | 19.9%             | -9.8        | +0.08    |
| Mitch Spence            | ATH    | FC      | 982       | 90.7   | 17.6%    | 27.4%             | -9.8        | -0.15    |

## 2. Outperforms shape: discount the results

Whiff rate and run value well above what the shape predicts. This is usually command, location, tunneling or deception, which is partly real (see section 3: command explains much of the gap but does not protect against regression). In the year-ahead tests these pitches gave back 2.1 and 0.7 whiff points versus matched controls (significant in one of the two tests), so expect partial regression, not collapse. Do not pay for their shape; weigh their results with some discount.

| Pitcher         | Team   | Pitch   | Pitches   | Velo   | Whiff%   | Expected whiff%   | Gap (pts)   | RV/100   |
|:----------------|:-------|:--------|:----------|:-------|:---------|:------------------|:------------|:---------|
| José Alvarado   | PHI    | FC      | 410       | 92.5   | 46.5%    | 23.3%             | +23.1       | +0.50    |
| Blake Snell     | SF     | CU      | 462       | 81.1   | 49.3%    | 28.6%             | +20.7       | +1.16    |
| Fernando Cruz   | CIN    | FS      | 475       | 81.5   | 59.6%    | 39.6%             | +20.0       | +1.42    |
| Andrew Chafin   | TEX    | SL      | 435       | 82.1   | 56.0%    | 38.8%             | +17.2       | +0.75    |
| Reynaldo López  | ATL    | SL      | 620       | 85.0   | 44.5%    | 28.8%             | +15.7       | +0.99    |
| Reese Olson     | DET    | SL      | 515       | 84.8   | 45.1%    | 29.7%             | +15.4       | +1.29    |
| Dylan Lee       | ATL    | SL      | 470       | 84.0   | 45.6%    | 30.6%             | +15.0       | +0.94    |
| Aaron Bummer    | ATL    | ST      | 407       | 82.3   | 43.9%    | 29.7%             | +14.2       | +0.42    |
| Génesis Cabrera | TOR    | FC      | 405       | 89.2   | 34.1%    | 20.2%             | +13.9       | +0.83    |
| Andrés Muñoz    | SEA    | SL      | 448       | 87.6   | 48.5%    | 35.2%             | +13.3       | +0.90    |
| Derek Law       | WSH    | SL      | 413       | 87.3   | 40.3%    | 27.1%             | +13.3       | +1.21    |
| Kirby Yates     | TEX    | FF      | 623       | 93.2   | 35.2%    | 22.0%             | +13.3       | +1.46    |

## 3. Command: whose locations create misses

Command score is how many more misses per swing (in percentage points) a pitcher's locations create than the same pitch shape would league-wide (a location-aware model minus a shape-only model, both fit out-of-fold by pitcher). Zone% is the share of pitches in the zone; chase% is how often hitters swing at pitches out of it. It is a repeatable skill (year-to-year correlation 0.62) and tracks the shape gap closely (correlation 0.67 to 0.68 with actual-minus-expected whiff), so it explains much of why a pitch beats or lags its shape. But last year's whiff rate already contains it, so it does not improve forecasts, and high-command "outperformers" regressed about as much as low-command ones (-3.3 vs -2.8 and -2.5 vs -2.7 whiff points), so command alone does not make those results durable. Pitch types with at least 300 pitches and 150 swings are shown.

**Strongest command:**

| Pitcher        | Team   | Pitch   | Pitches   | Command (pts)   | Zone%   | Chase%   | Whiff%   | Shape-expected whiff%   |
|:---------------|:-------|:--------|:----------|:----------------|:--------|:---------|:---------|:------------------------|
| Reynaldo López | ATL    | SL      | 620       | +14.4           | 31.6%   | 37.7%    | 44.5%    | 28.8%                   |
| Ranger Suarez  | PHI    | CU      | 454       | +12.7           | 37.2%   | 41.8%    | 33.8%    | 23.7%                   |
| Corbin Burnes  | BAL    | SL      | 383       | +12.2           | 29.0%   | 46.0%    | 46.0%    | 38.1%                   |
| Reese Olson    | DET    | SL      | 515       | +12.0           | 39.8%   | 41.3%    | 45.1%    | 29.7%                   |
| José Leclerc   | TEX    | SL      | 384       | +11.8           | 41.7%   | 30.4%    | 45.4%    | 25.6%                   |
| Patrick Corbin | WSH    | SL      | 989       | +11.7           | 36.4%   | 35.1%    | 35.4%    | 28.7%                   |
| Andrés Muñoz   | SEA    | SL      | 448       | +11.6           | 34.4%   | 42.5%    | 48.5%    | 35.2%                   |
| Kevin Ginkel   | AZ     | SL      | 455       | +11.5           | 33.8%   | 36.5%    | 42.0%    | 33.6%                   |
| Jake Cousins   | NYY    | ST      | 423       | +11.2           | 36.4%   | 38.7%    | 47.2%    | 36.3%                   |
| Blake Snell    | SF     | CU      | 462       | +10.4           | 36.1%   | 38.0%    | 49.3%    | 28.6%                   |

**Weakest command:**

| Pitcher        | Team   | Pitch   | Pitches   | Command (pts)   | Zone%   | Chase%   | Whiff%   | Shape-expected whiff%   |
|:---------------|:-------|:--------|:----------|:----------------|:--------|:---------|:---------|:------------------------|
| Phil Maton     | NYM    | CU      | 306       | -14.4           | 37.6%   | 36.6%    | 32.7%    | 42.6%                   |
| Landen Roupp   | SF     | CU      | 400       | -11.5           | 43.2%   | 35.7%    | 33.0%    | 45.4%                   |
| Tyler Glasnow  | LAD    | CU      | 374       | -11.2           | 38.2%   | 29.4%    | 47.5%    | 51.7%                   |
| Mike Baumann   | MIA    | KC      | 357       | -10.9           | 45.9%   | 28.5%    | 28.7%    | 40.7%                   |
| Tyler Rogers   | SF     | SI      | 634       | -10.3           | 66.6%   | 26.4%    | 15.1%    | 23.4%                   |
| MacKenzie Gore | WSH    | CU      | 581       | -10.1           | 44.4%   | 29.1%    | 33.9%    | 43.1%                   |
| Max Meyer      | MIA    | SL      | 393       | -9.7            | 43.8%   | 36.2%    | 34.3%    | 44.5%                   |
| José Soriano   | LAA    | KC      | 440       | -9.6            | 49.8%   | 29.9%    | 39.6%    | 47.4%                   |

## 4. Contact luck (weak evidence)

Actual wOBA on balls in play vs. the wOBA expected from exit velocity and launch angle (min 250 balls in play). Gap is actual minus expected: positive means the pitcher allowed more damage than the contact deserved. In testing, expected wOBA did not beat actual wOBA at predicting next year, and the "unlucky" and "lucky" groups moved the expected way in most comparisons but rarely significantly. Use as context, not as a call.

**Results worse than contact quality (possible rebound):**

| Pitcher          | Team   | Throws   | Balls in play   | Actual wOBA   | Expected wOBA   | Gap   |
|:-----------------|:-------|:---------|:----------------|:--------------|:----------------|:------|
| Carson Spiers    | CIN    | R        | 297             | .461          | .394            | +.067 |
| Carlos Carrasco  | CLE    | R        | 317             | .438          | .385            | +.053 |
| Kenta Maeda      | DET    | R        | 352             | .428          | .376            | +.052 |
| Justin Verlander | HOU    | R        | 289             | .387          | .336            | +.051 |
| Slade Cecconi    | AZ     | R        | 251             | .435          | .385            | +.050 |
| Taijuan Walker   | PHI    | R        | 270             | .480          | .439            | +.041 |
| Garrett Crochet  | CWS    | L        | 342             | .422          | .380            | +.041 |
| MacKenzie Gore   | WSH    | L        | 469             | .418          | .379            | +.039 |

**Results better than contact quality (possible give-back):**

| Pitcher        | Team   | Throws   | Balls in play   | Actual wOBA   | Expected wOBA   | Gap   |
|:---------------|:-------|:---------|:----------------|:--------------|:----------------|:------|
| Ryan Yarbrough | TOR    | L        | 284             | .283          | .341            | -.058 |
| Reynaldo López | ATL    | R        | 350             | .338          | .394            | -.056 |
| Bryce Miller   | SEA    | R        | 482             | .314          | .370            | -.056 |
| Tyler Holton   | DET    | L        | 254             | .259          | .308            | -.049 |
| Tanner Houck   | BOS    | R        | 521             | .323          | .366            | -.043 |
| Ronel Blanco   | HOU    | R        | 437             | .326          | .369            | -.043 |
| Bryse Wilson   | MIL    | R        | 319             | .370          | .411            | -.040 |
| Logan Webb     | SF     | R        | 615             | .350          | .387            | -.037 |

## 5. Platoon vulnerabilities

Largest run-value gaps between left- and right-handed batters (at least 400 pitches each side). Gap is RV/100 against lefties minus RV/100 against righties: positive means the pitcher is weaker against right-handed batters. 
Only about 20% of a pitcher's gap carried into the following season in testing, so the expected next-year gap shrinks it accordingly. The weak side stayed the weak side 64% to 65% of the time for the biggest gaps. 
Use for deployment hints, not hard role limits.

| Pitcher            | Team   | Throws   | Pitches vs L   | Pitches vs R   | RV/100 vs L   | RV/100 vs R   | Gap   | Expected next-year gap   | Weak side   |
|:-------------------|:-------|:---------|:---------------|:---------------|:--------------|:--------------|:------|:-------------------------|:------------|
| Quinn Priester     | BOS    | R        | 402            | 409            | -2.14         | +1.21         | -3.35 | -0.67                    | vs LHB      |
| Ryan Yarbrough     | TOR    | L        | 564            | 950            | +2.69         | -0.32         | +3.01 | +0.60                    | vs RHB      |
| John Brebbia       | ATL    | R        | 519            | 475            | -2.75         | +0.10         | -2.85 | -0.57                    | vs LHB      |
| Shawn Armstrong    | CHC    | R        | 418            | 661            | -2.49         | +0.32         | -2.82 | -0.56                    | vs LHB      |
| Edwin Díaz         | NYM    | R        | 475            | 437            | -0.59         | +2.03         | -2.62 | -0.52                    | vs LHB      |
| Matthew Liberatore | STL    | L        | 523            | 835            | +1.62         | -0.97         | +2.59 | +0.52                    | vs RHB      |
| Alex Faedo         | DET    | R        | 486            | 521            | +1.18         | -1.38         | +2.56 | +0.51                    | vs RHB      |
| Bryan Abreu        | HOU    | R        | 668            | 623            | -0.99         | +1.56         | -2.55 | -0.51                    | vs LHB      |
| Luis Castillo      | SEA    | R        | 1284           | 1473           | -1.69         | +0.85         | -2.54 | -0.51                    | vs LHB      |
| Paul Blackburn     | NYM    | R        | 627            | 562            | +0.98         | -1.50         | +2.48 | +0.50                    | vs RHB      |
| Zack Wheeler       | PHI    | R        | 1723           | 1411           | -0.08         | +2.38         | -2.46 | -0.49                    | vs LHB      |
| Max Fried          | ATL    | L        | 643            | 2118           | -1.07         | +1.35         | -2.42 | -0.48                    | vs LHB      |

## 6. Heavily used pitches that cost runs

Pitch types thrown at least 15% of the time with shrunk RV below -0.5 per 100, ranked by runs lost vs. the league average for that pitch type over the season. Flagged pitches did 0.35 to 0.78 runs per 100 worse than unflagged heavy-use pitches the following year. Candidates for usage reduction, a shape or location change, or replacement.

| Pitcher                 | Team   | Pitch   | Pitches   | Usage   | RV/100   | Runs lost vs avg   |
|:------------------------|:-------|:--------|:----------|:--------|:---------|:-------------------|
| Patrick Corbin          | WSH    | SI      | 1030      | 36%     | -1.34    | 23.4               |
| John Brebbia            | ATL    | SL      | 515       | 52%     | -1.67    | 20.0               |
| Ty Blach                | COL    | SI      | 576       | 51%     | -1.73    | 19.7               |
| Justin Lawrence         | COL    | SI      | 629       | 58%     | -1.45    | 17.9               |
| Taijuan Walker          | PHI    | FS      | 303       | 22%     | -2.03    | 17.7               |
| Simeon Woods Richardson | MIN    | CH      | 442       | 19%     | -1.62    | 16.3               |
| Triston McKenzie        | CLE    | FF      | 683       | 52%     | -1.22    | 15.9               |
| Tyler Anderson          | LAA    | FF      | 1155      | 40%     | -0.76    | 15.7               |
| Cal Quantrill           | COL    | SI      | 635       | 24%     | -1.04    | 13.8               |
| Walker Buehler          | LAD    | FF      | 386       | 29%     | -1.50    | 13.7               |
| Roddery Muñoz           | MIA    | FF      | 401       | 27%     | -1.44    | 13.5               |
| Griffin Canning         | LAA    | FF      | 1069      | 37%     | -0.66    | 13.3               |

## Caveats

- Run value is noisy at these sample sizes. Shrinkage mitigates but does not remove that.
- The shape model sees physical shape, separation from the pitcher's own fastball and batter side. Location is handled separately by the command score; sequencing and pitch-to-pitch tunneling are not modeled.
- Flag tests used only three seasons and small flagged samples (29 to 96 per test), so intervals are wide.
