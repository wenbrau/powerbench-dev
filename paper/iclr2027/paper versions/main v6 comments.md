# Ronda 6 de comentarios (22/09/2026, sobre el PDF compilado en 29fc224 + 4dce563)

El PDF anotado de esta ronda no se conservó: los comentarios se extrajeron de `main.pdf` y el archivo se regeneró
antes de guardarlo. Este es el volcado textual completo (54 anotaciones, en orden de página), reconstruido del registro
de la extracción. Cada entrada da el texto subrayado (ANCLA) y la nota. Todas se aplicaron en 767d4be y c5ad77d.

## Página 3

1. ANCLA: `.` (fin del último párrafo de Related work) — NOTA: add a one sentence paragraph after this saying that extended related work can be found in appendix smth
2. ANCLA: `Every request is` — NOTA: Every request we use is...
3. ANCLA: `an explicit ask. It asks for assistance` — NOTA: ends in an explicit ask for assistance with...
4. ANCLA: `party, and by no specific means:` — NOTA: End sentence at "party." then the next sentence starts "Requests do not specify means for shifting power, so..."
5. ANCLA: `has a prior` — NOTA: has some prior
6. ANCLA: `by a route that takes` — NOTA: without taking it from anyone
7. ANCLA: `and gains nothing.` — NOTA: without gaining anything
8. ANCLA: `cautious` — NOTA: not "cautious", just "an assistant"
9. ANCLA: `English dataset` (encabezado D1) — NOTA: Base dataset
10. ANCLA: `one of eight` — NOTA: no need to say one of eight
11. ANCLA: `one of eight` — NOTA: no need to say one of eight
12. ANCLA: `a target of one of three scales` — NOTA: a target scale
13. ANCLA: `each replaces it with one of` — NOTA: instead, they have eight refusal triggers
14. ANCLA: `circumvention on the user's own devices` — NOTA: unclear and long
15. ANCLA: `and a one-sided case for a contested stance)` — NOTA: unclear and long
16. ANCLA: `(576 power-shifting and 192 control)` — NOTA: don't say this

## Página 4

17. ANCLA: `Validation.` — NOTA: without this paragraph title
18. ANCLA: `DC` — NOTA: should this be lower case italics?
19. ANCLA: `English` (base English dataset, run protocol) — NOTA: base english
20. ANCLA: `refusal rates in percentage points describe levels of refusal, not contrasts` — NOTA: remove this
21. ANCLA: `direction of disagreement:` — NOTA: add the equation for it, and then as you describe it verbally, put the variables (b and c) in parentheses when you name them (e.g. the fraction that go toward refusal in the manipulated condition (b) minus...)

## Página 5

22. ANCLA: `its expectation under chance.` — NOTA: to test if per-model bias is significant regardless of direction
23. ANCLA: `Some analyses weight` — NOTA: "Additionally, some analyses...."
24. Nota al margen (mismo lugar) — NOTA: or maybe: "To estimate average bias while taking into account the difference in usage given to the models in our panel, some analyses weigh..."
25. ANCLA: `Two models whose` — NOTA: "Finally, two models whose..."
26. ANCLA: `Throughout, q denotes a Benjamini–Hochberg adjusted p-value, and asterisks in the figures mark q < 0.05. Appendix C gives the estimate behind every mark, in one table per figure, together with breakdowns by design factor, by developer country, and by usage weighting. 4.1` — NOTA: Why is this here? This goes where we mentioned BH in the statistics methods section, and we should only say that asterisks in figures mark q < 0.05. Results starts directly with 4.1
27. ANCLA: `Figure 1A shows the central pattern.` — NOTA: don't say this, just put the figure panel you refer to in parenthesis after the result
28. ANCLA: `take power from someone` — NOTA: this is unclear, is it DE or PG?
29. ANCLA: `without taking it (14.5` — NOTA: here "(Figure X, 14.5%..."
30. ANCLA: `Models differ widely in how much they refuse, from 1.3% to 35.2% on average (Figure 1C).` — NOTA: We should mention the panels in order. We shouldn't mention 1C before 1B.
31. ANCLA: `Does this spread reflect a stance toward power? The data suggest that it does not.` — NOTA: Don't ask a question, just say what we found, introducing the data with the conclusion. That's a general comment for the rest of results. Here we could say: "However, refusal rate appears to be a general feature of a model, not specific to power-shifting requests."
32. ANCLA: `Spearman correlations between the orderings of the models under any two request types range from 0.61 to 0.88),` — NOTA: can we say this more briefly? and do we have tests for those correlations? how many of them have q < 0.05?
33. ANCLA: `Developer country plays a smaller role` — NOTA: as i said before, we introduce results with interpretation, and interpretation shouldn't be vague, it should be clear: this sentence doesn't really say much. We could just start saying "Developer country does not predict refusal rate, either in power-shifting scenarios (Figure 1B, stats) nor in control scenarios (stats)"
34. ANCLA: `no overall difference between CN and US models` — NOTA: I revise it in my previous comment, but as a general rule: here you are stating a result without clearly naming what you test, which is bad: "no overall difference between CN and US models"... difference in what? I assume you mean in the refusal rate. In that case, one would say "no overall difference in the refusal rate of CN and US models" or something like that
35. ANCLA: `0.17), p =` — NOTA: we should say in methods that we report p when no correction is needed and q when we apply BH
36. ANCLA: `DC, although` — NOTA: "...DC. However, the gap..."
37. ANCLA: `requests than on the control (interaction OR 1.88 [1.09; 3.24], q = 0.023).` — NOTA: we're missing an interpretation here, after the stats, "..., suggesting that...". But i'm not sure what it suggests. In any case, it should be brief.
38. ANCLA: `Among the features of a request, the size of the target moves refusal most.` — NOTA: We call it scale, not size. And "among the features of a request" is confusing and we haven't talked about those other features yet so let's just start with scale. We say that it happens in power grabbing, and there's a tendency in DE but not in SE or CT, so models are more reticent to help with taking power from a target when that target has the scale of a society.
39. ANCLA: `OR 3.3 per level` — NOTA: per level? what does that mean?
40. ANCLA: `One could argue that requests affecting a whole society are simply more political, and would be refused whatever they asked. However, the control requests, which also concern an individual, a group, or a society, are refused equally often at every scale` — NOTA: This is not necessary - the framing is: this is specific to power grabbing requests, as i said before; the control is part of how we check that
41. ANCLA: `q < 0.001;` — NOTA: where does this q come from? what did we test?
42. ANCLA: `but perhaps expected,` — NOTA: remove this, it's not expected
43. ANCLA: `and not` — NOTA: but not
44. ANCLA: `Finally, requests` — NOTA: Power-shifting requests
45. ANCLA: `.` (fin del párrafo de contexto y dominio) — NOTA: We need to test and report whether those difference in context and domain also appear in the control or not.
46. Nota al margen — NOTA: and probably in the figure we should have sets of two bars, one purple, one gray for the control, for each context at least (can't do the same for domain)
47. Nota al margen — NOTA: so, actually, we only need to test the context thing, we can't test the domain thing.
48. Nota al margen — NOTA: in the control I mean

## Página 6

49. ANCLA: `Refusal rises from SE to PG,` — NOTA: Refusal is highest for PG requests, and increases with the size of the target
50. ANCLA: `Figure 1:` — NOTA: About the figure itself: titles are overlapping between A and B. A could be just "By request type". Also, the model names are too long in C, and that creates a large space between row 1 and 2. We need to find another solution, like abbreviating the names (here and in every figure that uses them) and refer to an appendix in the caption where we map model abbreviations to actual model names. Also, I see that "Power shift." in B creates some space as well because it's longer than the other axis tick labels. Perhaps we could abbreviate it as PS and clarify that the first time power shifting is mentioned in the text body (but don't replace it everywhere because I think it will be confusing, only in figures).
51. ANCLA: `English dataset` — NOTA: base English (this comment should be taken into account everywhere in the text)
52. ANCLA: `bars and bands show the mean over models with 95% t intervals` — NOTA: didn't we specify this already in methods? if so, let's not repeat it here
53. ANCLA: `in each` — NOTA: refusal rate by request type
54. ANCLA: `passes` — NOTA: survives BH correction
