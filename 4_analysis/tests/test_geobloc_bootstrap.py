"""The pooled interval must keep all model responses to a prompt together."""
from pathlib import Path
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from analysis_13_geobloc_no_great_powers import boot_bias
from pbanalysis.boot import ci


class PromptBootstrapTests(unittest.TestCase):
    def frame(self):
        return pd.DataFrame(dict(prompt_id=[f"p{i:03d}" for i in range(100)],
                                 mode="pg", model="A", r_pos=[0, 1] * 50, r_neg=0))

    def test_identical_models_do_not_shrink_prompt_uncertainty(self):
        one = self.frame()
        six = pd.concat([one.assign(model=str(i)) for i in range(6)], ignore_index=True)
        single, *_ = boot_bias(one)
        pooled, n, pos, neg = boot_bias(six)
        self.assertEqual(single, pooled)
        self.assertEqual((n, pos, neg), (600, 300, 0))

    def test_opposite_models_cancel_in_every_draw(self):
        one = self.frame()
        opposite = one.assign(model="B", r_pos=one.r_neg, r_neg=one.r_pos)
        result, *_ = boot_bias(pd.concat([one, opposite], ignore_index=True))
        self.assertEqual((result["est"], result["lo"], result["hi"], result["p"]), (0, 0, 0, 1))

    def test_single_model_matches_original_prompt_bootstrap(self):
        one = self.frame()
        counts = np.random.default_rng(0).multinomial(100, np.full(100, .01), size=3000)
        expected = ci(np.r_[.5, counts @ one.r_pos.to_numpy() / 100])
        actual, *_ = boot_bias(one)
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
