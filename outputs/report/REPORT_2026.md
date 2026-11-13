# Pitching Decision Report, 2026

Source: Statcast regular-season pitches, 2026. Run value (RV) is per 100 pitches from the pitcher's view (positive = good for the pitcher). Team is the pitcher's last team of the season, so traded pitchers show their final club.

## Key takeaways

- **What held up in later seasons:** platoon gaps persist only about 20% (the weak side holds 64% to 65% of the time for the biggest gaps), and heavily used pitches that cost runs kept costing runs. Command is a repeatable skill. Shape-based and contact-luck flags are modest hints, not calls.
- **Pitches whose results lag their shape (look at video):** Zack Littell (FS), George Kirby (ST), Zac Gallen (FF).
- **Pitches whose results beat their shape (expect some give-back):** Andrés Muñoz (SL), Fernando Cruz (FS), Chase Burns (SL).
- **Best command:** Patrick Corbin (SL), Andrés Muñoz (SL), Reynaldo López (SL). **Weakest:** Max Meyer (ST), Tyler Rogers (SI), Cade Smith (FS).
- **Platoon, largest gaps:** Cole Sulser (vs RHB), John Schreiber (vs LHB), Ryan Rolison (vs RHB).
- **Costliest heavy-use pitches:** Rhett Lowder (SL), Aaron Nola (SI), Grayson Rodriguez (FF).
- **Flagged in more than one section:** 51 pitchers, led by Zack Littell, Aaron Nola, Chase Burns (table below).

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

| Pitcher          | Team   | Sections   | Flags                                                                                                   |
|:-----------------|:-------|:-----------|:--------------------------------------------------------------------------------------------------------|
| Zack Littell     | AZ     | 4          | Costly pitch (FF); Platoon gap (vs LHB); Underperforms shape (FS); Weak command (FS)                    |
| Aaron Nola       | PHI    | 4          | Costly pitch (FF); Costly pitch (SI); Outperforms shape (KC); Underperforms shape (FF); Unlucky contact |
| Chase Burns      | CIN    | 3          | Outperforms shape (SL); Strong command (SL); Underperforms shape (FF)                                   |
| Mike Burrows     | HOU    | 3          | Costly pitch (FF); Underperforms shape (FF); Unlucky contact                                            |
| Joey Cantillo    | CLE    | 3          | Costly pitch (FF); Unlucky contact; Weak command (CU)                                                   |
| Michael Lorenzen | TOR    | 3          | Costly pitch (CH); Costly pitch (FF); Costly pitch (SI); Underperforms shape (FF); Unlucky contact      |
| Dustin May       | MIL    | 3          | Costly pitch (ST); Underperforms shape (ST); Weak command (ST)                                          |
| Juan Mejia       | COL    | 3          | Costly pitch (FF); Outperforms shape (ST); Platoon gap (vs LHB)                                         |
| Tyler Phillips   | MIA    | 3          | Costly pitch (SI); Strong command (CU); Underperforms shape (SI)                                        |
| Emmet Sheehan    | LAD    | 3          | Costly pitch (FF); Unlucky contact; Weak command (CH)                                                   |
| Andrew Abbott    | CIN    | 2          | Costly pitch (FF); Underperforms shape (FF)                                                             |
| Sandy Alcantara  | MIA    | 2          | Costly pitch (FF); Underperforms shape (CH)                                                             |

## 1. Underperforms shape: look closer

A pitch-level model predicts the chance of a miss on every swing from velocity, spin, movement, extension, release point, how the pitch differs from the pitcher's own fastball (speed and break separation) and batter side, fit out-of-fold by pitcher. Averaging over a pitcher's swings gives an expected whiff rate. The gap is actual minus expected. Pitches that whiff far fewer hitters than their shape predicts, with below-median run value, are candidates for a mechanical, sequencing or location fix. A very large gap can also mean the model is extrapolating, so check video before acting.

| Pitcher          | Team   | Pitch   | Pitches   | Velo   | Whiff%   | Expected whiff%   | Gap (pts)   | RV/100   |
|:-----------------|:-------|:--------|:----------|:-------|:---------|:------------------|:------------|:---------|
| Zack Littell     | AZ     | FS      | 456       | 84.1   | 17.1%    | 35.5%             | -18.4       | +0.24    |
| George Kirby     | SEA    | ST      | 780       | 87.5   | 26.3%    | 42.7%             | -16.4       | -0.05    |
| Zac Gallen       | AZ     | FF      | 626       | 93.4   | 6.0%     | 19.6%             | -13.6       | -0.40    |
| Bailey Ober      | MIN    | CH      | 696       | 82.6   | 20.7%    | 33.7%             | -13.0       | -0.57    |
| Bubba Chandler   | PIT    | SL      | 553       | 91.1   | 22.5%    | 35.3%             | -12.8       | +0.15    |
| Dustin May       | MIL    | ST      | 425       | 86.0   | 27.7%    | 40.3%             | -12.6       | -0.55    |
| Shane Baz        | BAL    | KC      | 960       | 85.3   | 28.7%    | 40.8%             | -12.2       | -0.40    |
| Michael Lorenzen | TOR    | FF      | 454       | 94.0   | 9.7%     | 21.7%             | -12.0       | -1.33    |
| Will Warren      | NYY    | ST      | 530       | 83.9   | 23.2%    | 35.0%             | -11.8       | -0.10    |
| Max Meyer        | MIA    | FF      | 430       | 95.1   | 12.5%    | 24.2%             | -11.7       | -0.35    |
| Chase Burns      | CIN    | FF      | 1422      | 97.6   | 17.1%    | 27.5%             | -10.4       | +0.28    |
| Aaron Nola       | PHI    | FF      | 706       | 92.3   | 14.1%    | 23.9%             | -9.7        | -1.22    |

## 2. Outperforms shape: discount the results

Whiff rate and run value well above what the shape predicts. This is usually command, location, tunneling or deception, which is partly real (see section 3: command explains much of the gap but does not protect against regression). In the year-ahead tests these pitches gave back 2.1 and 0.7 whiff points versus matched controls (significant in one of the two tests), so expect partial regression, not collapse. Do not pay for their shape; weigh their results with some discount.

| Pitcher            | Team   | Pitch   | Pitches   | Velo   | Whiff%   | Expected whiff%   | Gap (pts)   | RV/100   |
|:-------------------|:-------|:--------|:----------|:-------|:---------|:------------------|:------------|:---------|
| Andrés Muñoz       | SEA    | SL      | 404       | 87.2   | 49.5%    | 31.8%             | +17.7       | +0.35    |
| Fernando Cruz      | NYY    | FS      | 484       | 80.0   | 52.0%    | 36.4%             | +15.6       | +0.59    |
| Chase Burns        | CIN    | SL      | 1000      | 90.2   | 51.7%    | 36.3%             | +15.3       | +1.35    |
| Ranger Suarez      | BOS    | CU      | 401       | 75.7   | 37.6%    | 23.6%             | +13.9       | +0.56    |
| Cristopher Sánchez | PHI    | CH      | 1171      | 87.0   | 46.0%    | 32.2%             | +13.9       | +1.08    |
| Ryan Weathers      | NYY    | ST      | 458       | 81.2   | 38.8%    | 26.7%             | +12.1       | +0.37    |
| Nathan Eovaldi     | TEX    | CU      | 492       | 76.3   | 39.1%    | 27.0%             | +12.1       | +0.30    |
| Zack Wheeler       | PHI    | FS      | 431       | 87.4   | 45.5%    | 33.4%             | +12.1       | +0.92    |
| Michael Soroka     | AZ     | SV      | 595       | 80.6   | 35.5%    | 23.9%             | +11.6       | +1.00    |
| Aaron Nola         | PHI    | KC      | 980       | 78.4   | 41.1%    | 29.9%             | +11.3       | +0.80    |
| Cam Schlittler     | NYY    | FF      | 1352      | 98.0   | 34.7%    | 23.5%             | +11.2       | +1.58    |
| Jacob Webb         | CHC    | CH      | 442       | 85.6   | 41.5%    | 30.4%             | +11.1       | +0.72    |

## 3. Command: whose locations create misses

Command score is how many more misses per swing (in percentage points) a pitcher's locations create than the same pitch shape would league-wide (a location-aware model minus a shape-only model, both fit out-of-fold by pitcher). Zone% is the share of pitches in the zone; chase% is how often hitters swing at pitches out of it. It is a repeatable skill (year-to-year correlation 0.62) and tracks the shape gap closely (correlation 0.67 to 0.68 with actual-minus-expected whiff), so it explains much of why a pitch beats or lags its shape. But last year's whiff rate already contains it, so it does not improve forecasts, and high-command "outperformers" regressed about as much as low-command ones (-3.3 vs -2.8 and -2.5 vs -2.7 whiff points), so command alone does not make those results durable. Pitch types with at least 300 pitches and 150 swings are shown.

**Strongest command:**

| Pitcher        | Team   | Pitch   | Pitches   | Command (pts)   | Zone%   | Chase%   | Whiff%   | Shape-expected whiff%   |
|:---------------|:-------|:--------|:----------|:----------------|:--------|:---------|:---------|:------------------------|
| Patrick Corbin | TOR    | SL      | 383       | +15.7           | 32.9%   | 35.0%    | 36.6%    | 26.4%                   |
| Andrés Muñoz   | SEA    | SL      | 404       | +13.6           | 34.4%   | 46.0%    | 49.5%    | 31.8%                   |
| Reynaldo López | ATL    | SL      | 419       | +12.2           | 28.2%   | 30.2%    | 34.1%    | 27.7%                   |
| Ranger Suarez  | BOS    | CU      | 401       | +10.9           | 35.2%   | 43.1%    | 37.6%    | 23.6%                   |
| Chase Burns    | CIN    | SL      | 1000      | +10.3           | 34.1%   | 41.1%    | 51.7%    | 36.3%                   |
| Brady Singer   | CIN    | SL      | 770       | +8.9            | 37.3%   | 34.6%    | 30.7%    | 27.7%                   |
| Nick Lodolo    | CIN    | CU      | 463       | +8.8            | 31.5%   | 30.3%    | 40.6%    | 25.9%                   |
| Grant Anderson | MIL    | ST      | 341       | +8.8            | 36.1%   | 32.1%    | 39.9%    | 28.0%                   |
| Adrian Morejon | SD     | CH      | 304       | +8.8            | 27.6%   | 53.2%    | 56.0%    | 34.6%                   |
| Nick Martinez  | TB     | CH      | 649       | +8.8            | 36.2%   | 38.6%    | 30.7%    | 27.2%                   |

**Weakest command:**

| Pitcher        | Team   | Pitch   | Pitches   | Command (pts)   | Zone%   | Chase%   | Whiff%   | Shape-expected whiff%   |
|:---------------|:-------|:--------|:----------|:----------------|:--------|:---------|:---------|:------------------------|
| Max Meyer      | MIA    | ST      | 533       | -18.5           | 39.6%   | 36.3%    | 36.5%    | 55.4%                   |
| Tyler Rogers   | TOR    | SI      | 771       | -13.2           | 59.5%   | 27.9%    | 12.0%    | 23.5%                   |
| Cade Smith     | CLE    | FS      | 309       | -12.6           | 28.8%   | 36.8%    | 44.7%    | 52.1%                   |
| Max Meyer      | MIA    | SL      | 470       | -12.2           | 49.4%   | 37.4%    | 38.7%    | 49.3%                   |
| Dustin May     | MIL    | ST      | 425       | -11.9           | 42.8%   | 30.0%    | 27.7%    | 40.3%                   |
| Trevor Megill  | MIL    | KC      | 309       | -11.8           | 38.5%   | 44.7%    | 46.5%    | 54.4%                   |
| Eric Orze      | MIN    | FS      | 340       | -10.8           | 45.0%   | 34.2%    | 27.3%    | 41.4%                   |
| Andrew Alvarez | WSH    | SL      | 376       | -9.7            | 44.4%   | 34.0%    | 35.9%    | 43.5%                   |

## 4. Contact luck (weak evidence)

Actual wOBA on balls in play vs. the wOBA expected from exit velocity and launch angle (min 250 balls in play). Gap is actual minus expected: positive means the pitcher allowed more damage than the contact deserved. In testing, expected wOBA did not beat actual wOBA at predicting next year, and the "unlucky" and "lucky" groups moved the expected way in most comparisons but rarely significantly. Use as context, not as a call.

**Results worse than contact quality (possible rebound):**

| Pitcher          | Team   | Throws   | Balls in play   | Actual wOBA   | Expected wOBA   | Gap   |
|:-----------------|:-------|:---------|:----------------|:--------------|:----------------|:------|
| Tanner Gordon    | COL    | R        | 358             | .484          | .403            | +.081 |
| Jacob Lopez      | ATH    | L        | 371             | .397          | .317            | +.081 |
| Jack Perkins     | ATH    | R        | 335             | .443          | .374            | +.069 |
| Payton Tolle     | BOS    | L        | 382             | .379          | .316            | +.063 |
| Mike Burrows     | HOU    | R        | 307             | .432          | .370            | +.062 |
| Kyle Harrison    | MIL    | L        | 320             | .450          | .392            | +.059 |
| Michael Lorenzen | TOR    | R        | 467             | .458          | .402            | +.056 |
| Aaron Nola       | PHI    | R        | 504             | .430          | .380            | +.051 |

**Results better than contact quality (possible give-back):**

| Pitcher          | Team   | Throws   | Balls in play   | Actual wOBA   | Expected wOBA   | Gap   |
|:-----------------|:-------|:---------|:----------------|:--------------|:----------------|:------|
| Shane McClanahan | TB     | L        | 334             | .318          | .370            | -.052 |
| Randy Vásquez    | SD     | R        | 457             | .351          | .393            | -.042 |
| Michael King     | SD     | R        | 508             | .322          | .360            | -.038 |
| Michael Soroka   | AZ     | R        | 321             | .341          | .379            | -.038 |
| Clay Holmes      | CHC    | R        | 293             | .289          | .325            | -.036 |
| Merrill Kelly    | AZ     | R        | 513             | .380          | .415            | -.035 |
| Michael McGreevy | STL    | R        | 537             | .360          | .395            | -.035 |
| Grant Holmes     | ATL    | R        | 460             | .344          | .378            | -.034 |

## 5. Platoon vulnerabilities

Largest run-value gaps between left- and right-handed batters (at least 400 pitches each side). Gap is RV/100 against lefties minus RV/100 against righties: positive means the pitcher is weaker against right-handed batters. 
Only about 20% of a pitcher's gap carried into the following season in testing, so the expected next-year gap shrinks it accordingly. The weak side stayed the weak side 64% to 65% of the time for the biggest gaps. 
Use for deployment hints, not hard role limits.

| Pitcher            | Team   | Throws   | Pitches vs L   | Pitches vs R   | RV/100 vs L   | RV/100 vs R   | Gap   | Expected next-year gap   | Weak side   |
|:-------------------|:-------|:---------|:---------------|:---------------|:--------------|:--------------|:------|:-------------------------|:------------|
| Cole Sulser        | TB     | R        | 527            | 410            | +2.12         | -2.79         | +4.90 | +0.98                    | vs RHB      |
| John Schreiber     | NYY    | R        | 458            | 539            | -2.68         | +2.03         | -4.71 | -0.94                    | vs LHB      |
| Ryan Rolison       | CHC    | L        | 464            | 526            | +3.15         | -1.27         | +4.42 | +0.88                    | vs RHB      |
| Mason Fluharty     | TOR    | L        | 537            | 497            | +2.51         | -1.71         | +4.22 | +0.84                    | vs RHB      |
| Blade Tidwell      | SF     | R        | 545            | 414            | -1.59         | +2.45         | -4.04 | -0.81                    | vs LHB      |
| Cristopher Sánchez | PHI    | L        | 657            | 2501           | +3.73         | -0.12         | +3.86 | +0.77                    | vs RHB      |
| José A. Ferrer     | SEA    | L        | 473            | 606            | +1.16         | -2.20         | +3.37 | +0.67                    | vs RHB      |
| Jake Bennett       | BOS    | L        | 419            | 1199           | +3.10         | -0.03         | +3.13 | +0.63                    | vs RHB      |
| Peyton Gray        | TEX    | R        | 465            | 479            | +1.02         | -2.07         | +3.09 | +0.62                    | vs RHB      |
| Daniel Lynch IV    | KC     | L        | 457            | 843            | +2.68         | -0.38         | +3.06 | +0.61                    | vs RHB      |
| Hunter Gaddis      | CLE    | R        | 498            | 484            | -1.24         | +1.81         | -3.05 | -0.61                    | vs LHB      |
| Casey Mize         | SD     | R        | 1176           | 906            | +0.65         | -2.22         | +2.87 | +0.57                    | vs RHB      |

## 6. Heavily used pitches that cost runs

Pitch types thrown at least 15% of the time with shrunk RV below -0.5 per 100, ranked by runs lost vs. the league average for that pitch type over the season. Flagged pitches did 0.35 to 0.78 runs per 100 worse than unflagged heavy-use pitches the following year. Candidates for usage reduction, a shape or location change, or replacement.

| Pitcher           | Team   | Pitch   | Pitches   | Usage   | RV/100   | Runs lost vs avg   |
|:------------------|:-------|:--------|:----------|:--------|:---------|:-------------------|
| Rhett Lowder      | CIN    | SL      | 610       | 27%     | -1.32    | 18.6               |
| Aaron Nola        | PHI    | SI      | 535       | 18%     | -1.34    | 17.8               |
| Grayson Rodriguez | LAA    | FF      | 905       | 51%     | -1.01    | 15.7               |
| Sean Manaea       | NYM    | ST      | 752       | 30%     | -0.95    | 15.6               |
| Aaron Nola        | PHI    | FF      | 706       | 24%     | -1.21    | 15.5               |
| Zack Littell      | AZ     | FF      | 502       | 25%     | -1.46    | 14.9               |
| Andrew Painter    | PHI    | FF      | 697       | 33%     | -1.08    | 13.9               |
| Trevor Rogers     | BAL    | CH      | 550       | 20%     | -1.00    | 13.9               |
| Roki Sasaki       | LAD    | FF      | 881       | 42%     | -0.89    | 13.8               |
| Seth Lugo         | KC     | FF      | 468       | 17%     | -1.40    | 13.8               |
| Michael Lorenzen  | TOR    | SI      | 486       | 20%     | -0.94    | 13.3               |
| Kyle Bradish      | BAL    | SL      | 636       | 24%     | -0.75    | 13.2               |

## Caveats

- Run value is noisy at these sample sizes. Shrinkage mitigates but does not remove that.
- The shape model sees physical shape, separation from the pitcher's own fastball and batter side. Location is handled separately by the command score; sequencing and pitch-to-pitch tunneling are not modeled.
- Flag tests used only three seasons and small flagged samples (29 to 96 per test), so intervals are wide.
