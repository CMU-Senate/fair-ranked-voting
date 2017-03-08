# CMU Fair Ranked Voting
The reference implementation of the [single transferable vote][1] (STV) system used for [student government elections][2] at [Carnegie Mellon University][3].

## Usage

## Testing

I have included unit tests that can be run with
```
python -m unittest -v tests
```
## Frequently Asked Questions

### Why did you make this?

As a senator in the Carnegie Mellon [Student Senate][4], I was involved in many initiatives aimed at improving the student experience across the university and empowering change within student government. I care deeply about democracy and fairness in electoral systems, and I wanted to apply this to our campus. I developed this election software, and together with many other dedicated students, we converted our voting system to STV.

### Why did you choose STV?

The decision to investigate using [instant-runoff voting][5] (IRV) for single-seat executive positions was made by the previous student body executive branch. When I joined the Senate, I worked to move forward with these reforms and apply them to all elections. The simplest choice was to use STV, as it serves as an extension of IRV for multi-seat elections.

STV allows voters to rank their preferred candidates and have their votes transfer as candidates are eliminated or elected. This leads to approximately [proportional representation][6] and avoids the [spoiler effect][7] of splitting votes between similar candidates. However, STV has its issues, and [no voting system is perfect][8].

### Why should I care about a voting system?

Simply put, our elections allocate power and dictate policy, and our voting systems are what decide these elections. Traditional [first-past-the-post voting][9] has many flaws, and maybe we can come up with solutions that make our elections, and therefore our governments, even more representative, transparent, and inclusive.

[1]: https://en.wikipedia.org/wiki/Single_transferable_vote
[2]: https://stugov.andrew.cmu.edu/elections
[3]: https://www.cmu.edu
[4]: https://cmusenate.org
[5]: https://en.wikipedia.org/wiki/Instant-runoff_voting
[6]: https://en.wikipedia.org/wiki/Proportional_representation
[7]: https://en.wikipedia.org/wiki/Spoiler_effect
[8]: https://en.wikipedia.org/wiki/Arrow%27s_impossibility_theorem
[9]: https://en.wikipedia.org/wiki/First-past-the-post_voting
