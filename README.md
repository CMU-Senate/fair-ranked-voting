# CMU Fair Ranked Voting
The reference implementation of the [single transferable vote](https://en.wikipedia.org/wiki/Single_transferable_vote) (STV) system used for [student government elections](https://stugov.andrew.cmu.edu/elections) at [Carnegie Mellon University](https://www.cmu.edu).

## Usage
The election classes and algorithm are located in [election.py](election.py). A more formal declaration of the algorithm and election rules is located in the [bylaws.md](bylaws.md). Additionally, [run.py](run.py) provides a command-line interface to run elections:
```
usage: run.py [-h] -s SEATS [-a ALPHANUMERIC] [-b BALLOTS] [-c] [-n NAME] [-r]
              [-v]

Configure and run an election. Ballots ranking candidates may be imported from
a CSV or TXT file, or manual input if no file is specified. The expected input
format for a candidate is 'uid' or optionally 'uid (name)'.

optional arguments:
  -h, --help            show this help message and exit
  -a ALPHANUMERIC, --alphanumeric ALPHANUMERIC
                        Alphanumeric string for breaking ties
  -b BALLOTS, --ballots BALLOTS
                        File containing ballots
  -c, --disallow-nc-elimination
                        No Confidence cannot be eliminated
  -n NAME, --name NAME  Name of election
  -r, --disallow-random-tiebreak
                        Halt election instead of using random tiebreak
  -v, --verbose         Verbose printing of election results

required arguments:
  -s SEATS, --seats SEATS
                        Number of seats
```

### Example: CMU Student Senate Election 2017
Twelve seat election with a randomly-sorted alphanumeric for final tiebreaks.
```
python run.py -v -n 'CMU College of Engineering' -s 12 -a 'vrb4pes1t0xnm7jdf2k8cgzqloh9wyia5u63' -b ballots.csv
```

### Example: CMU Student Body President Election 2017
One seat election with No Confidence unable to be eliminated and halts instead of random final tiebreak.
```
python run.py -v -c -r -n 'CMU Student Body President' -s 1 -b ballots.csv
```

## Testing

The included unit tests in [tests.py](tests.py) can be run with:
```
python -m unittest -v tests
```
## Frequently Asked Questions

### Why did you make this?

As a senator in the [Carnegie Mellon Student Senate](https://cmusenate.org), I was involved in many initiatives aimed at improving the student experience across the university and empowering change within student government. I care deeply about democracy and fairness in electoral systems, and I wanted to apply this to our campus. With no free and open-source STV program that was reliably-maintained and fit our needs, the best solution was to create our own. I developed this election software, and together with many other dedicated students, we converted our voting system to STV.

### Can I use this to run elections?

Yes! I have released this project as free and open-source software under the GPLv3 license. With the code and example bylaws, you can implement an STV system and bring fair ranked voting to your organization.

### Why did you choose STV?

The decision to investigate using [instant-runoff voting](https://en.wikipedia.org/wiki/Instant-runoff_voting) (IRV) for single-seat executive positions was made by the previous student body executive branch. When I joined the Senate, I worked to move forward with these reforms and apply them to all elections. The simplest choice was to use STV, as it serves as an extension of IRV for multi-seat elections.

STV allows voters to rank their preferred candidates and have their votes transfer as candidates are eliminated or elected. This leads to approximately [proportional representation](https://en.wikipedia.org/wiki/Proportional_representation) and avoids the [spoiler effect](https://en.wikipedia.org/wiki/Spoiler_effect) of splitting votes between similar candidates. However, STV has its issues, and [no voting system is perfect](https://en.wikipedia.org/wiki/Arrow%27s_impossibility_theorem).

### Why should I care about a voting system?

Simply put, our elections allocate power and dictate policy, and our voting systems are what decide these elections. Traditional [first-past-the-post voting](https://en.wikipedia.org/wiki/First-past-the-post_voting) has many flaws, and maybe we can come up with solutions that make our elections, and therefore our governments, even more representative, transparent, and inclusive.
